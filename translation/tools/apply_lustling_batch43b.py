# Batch43b: apply manual translations (data/lustling_batch43_ko.tsv) to the
# remaining uncovered Lustlings modifyed items. Test values are re-read from
# the live item files so multiline strings can't mismatch.
import sys, io, json, re, csv
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\tools")
from pak import Pak
from pak_writer import write_pak

TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
LK = r"E:\My Games\steamapps\common\Starbound\mods\997_sxb_Lustlings_1.2.9_clean.pak"
KO_TSV = r"data\lustling_batch43_ko.tsv"
SRC_TSV = r"data\lustling_untranslated.tsv"


def parse_sb(raw):
    s = raw.decode('utf-8', errors='replace')
    s = re.sub(r'//[^\n]*', '', s)
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    out = []
    ins = False
    for i, c in enumerate(s):
        if c == '"' and (i == 0 or s[i - 1] != chr(92)):
            ins = not ins
        out.append('\\r' if ins and c == '\r' else '\\n' if ins and c == '\n' else c)
    return json.loads(re.sub(r',(\s*[}\]])', r'\1', ''.join(out)))


csv.field_size_limit(10 ** 8)
ko = {}
with open(KO_TSV, encoding='utf-8') as f:
    for r in csv.reader(f, delimiter='\t'):
        if len(r) >= 3 and r[0] != 'basename':
            ko[(r[0], r[1])] = r[2]

src = []
with open(SRC_TSV, encoding='utf-8') as f:
    for r in csv.reader(f, delimiter='\t'):
        if len(r) >= 3 and r[0] != 'asset':
            src.append((r[0], r[1]))

missing = [(a, f) for a, f in src if (a.rsplit('/', 1)[-1], f) not in ko]
print('src rows:', len(src), 'ko rows:', len(ko), 'missing:', len(missing))
for a, f in missing[:20]:
    print('  MISS', a, f)

# ambiguity check: same basename+field on different assets with different EN
from collections import defaultdict
en_by = defaultdict(set)
for a, f in src:
    en_by[(a.rsplit('/', 1)[-1], f)].add(a)
amb = {k: v for k, v in en_by.items() if len(v) > 1}
print('basename+field shared by multiple assets:', len(amb))
for k, v in list(amb.items())[:10]:
    print('  AMB', k, v)

lk = Pak(LK)
overrides = {}
per_asset = {}
for a, f in src:
    bn = a.rsplit('/', 1)[-1]
    k = ko.get((bn, f))
    if k is None:
        continue
    per_asset.setdefault(a, {})[f] = k

made = 0
for a, fmap in per_asset.items():
    try:
        doc = parse_sb(lk.read(a))
    except Exception:
        print('  unreadable', a)
        continue
    ops = []
    for f, k in fmap.items():
        cur = doc.get(f)
        if not isinstance(cur, str):
            print('  no field', a, f)
            continue
        ops.append([{"op": "test", "path": "/" + f, "value": cur},
                    {"op": "replace", "path": "/" + f, "value": k}])
    if ops:
        overrides[a + '.patch'] = json.dumps(ops, ensure_ascii=False, indent=2).encode('utf-8')
        made += 1
print('patches built:', made)
if '--apply' in sys.argv and overrides:
    print('wrote pak; entries', write_pak(TR, TR, overrides))
else:
    print('dry run — pass --apply to write')
