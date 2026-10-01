"""Merge case-duplicate LFW patch entries: keep provider-case (uppercase)
entry with merged ops (new batch ops + old ops for uncovered fields),
drop the stale lowercase twin. Rebuild pak without dropped entries."""
import sys, json, struct, csv, collections
sys.path.insert(0, r'E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\tools')
sys.path.insert(0, r'E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\..\modpack-overhaul-repo\tools')
sys.path.insert(0, r'E:\My Games\steamapps\common\Starbound\translation\modpack-overhaul-repo\tools')
from pak import Pak
from pak_writer import load_meta_blob, _vlq

TR = r'E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak'
csv.field_size_limit(10 ** 8)

mine = set()
rows = list(csv.reader(open('data/lfw_work_filled.tsv', encoding='utf-8'), delimiter='\t'))
for r in rows[1:]:
    if r and r[0]:
        mine.add(r[0] + '.patch')

p = Pak(TR)
names = set(p.index)
bylow = collections.defaultdict(list)
for n in names:
    bylow[n.lower()].append(n)

def firstseg(n):
    return n.split('/')[1] if len(n.split('/')) > 1 else ''

def lowvar(n):
    parts = n.split('/')
    parts[1] = parts[1].lower()
    return '/'.join(parts)

def flat_ops(patch_json):
    """Flatten nested op-groups into a flat op list."""
    ops = []
    for e in patch_json:
        if isinstance(e, list):
            ops.extend(x for x in e if isinstance(x, dict))
        elif isinstance(e, dict):
            ops.append(e)
    return ops

drops = set()
overrides = {}
merged_fields_report = []
for key, group in bylow.items():
    if len(group) < 2:
        continue
    ups = [x for x in group if firstseg(x).isupper() and x in mine]
    lows = [x for x in group if firstseg(x).islower()]
    if not ups or not lows:
        continue
    u = ups[0]; l = lows[0]
    new = flat_ops(json.loads(p.read(u).decode('utf-8')))
    old = json.loads(p.read(l).decode('utf-8'))
    covered = {o.get('path') for o in new if o.get('op') in ('replace', 'add')}
    kept_old = [o for o in flat_ops(old) if o.get('path') not in covered]
    merged = kept_old + new
    overrides[u] = json.dumps(merged, ensure_ascii=False, indent=2).encode('utf-8')
    drops.add(l)
    merged_fields_report.append((u, len(kept_old), len(new)))

print('merged pairs:', len(overrides))
print('dropped:', len(drops))
for u, ko, kn in merged_fields_report:
    if ko:
        print('  kept old-only ops:', ko, 'new ops:', kn, u[-70:])

# rebuild pak without dropped entries
files = {}
for n in p.index:
    if n in drops:
        continue
    files[n] = overrides.get(n) or p.read(n)
for n, b in overrides.items():
    files[n] = b
del p

meta_blob = load_meta_blob(TR)
buf = bytearray(b'SBAsset6' + b'\x00' * 8)
index_entries = []
for name in sorted(files):
    data = files[name]
    off = len(buf)
    buf += data
    index_entries.append((name.encode('utf-8'), off, len(data)))
index_off = len(buf)
buf += meta_blob
buf += _vlq(len(index_entries))
for name, off, n in index_entries:
    buf += _vlq(len(name)) + name + struct.pack('>QQ', off, n)
buf[8:16] = struct.pack('>Q', index_off)

tmp = TR + '.tmp_casefix'
with open(tmp, 'wb') as f:
    f.write(bytes(buf))
import os
os.replace(tmp, TR)
print('wrote pak; entries', len(files))
