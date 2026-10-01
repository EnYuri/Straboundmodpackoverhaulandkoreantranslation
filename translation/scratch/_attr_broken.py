# -*- coding: utf-8 -*-
# Per-patch attribution for 'broken' assets: simulate patch chains and record
# which provider's patch produces failing test ops.
import sys, io, os, re, json, csv, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

SB = r"E:\My Games\steamapps\common\Starbound"
MODS = SB + r"\mods"

TRANSLATION_PAKS = {
    'zz_translation_female.pak',
    'zz_localeko_highpriority_20260927.pak',
    '-9998_trans_sbkor_0.98_structfix.pak',
}
SKIP_PROVIDERS = TRANSLATION_PAKS | {'zz_female_overhaul.pak', 'zzz_diag_objdump'}


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


def ptr_parts(p):
    return [s.replace('~1', '/').replace('~0', '~') for s in p.strip('/').split('/')]


def ptr_get(doc, p):
    cur = doc
    for part in ptr_parts(p):
        cur = cur[part] if isinstance(cur, dict) else cur[int(part)]
    return cur


def ptr_set(doc, p, val, insert=False):
    parts = ptr_parts(p)
    cur = doc
    for part in parts[:-1]:
        cur = cur[part] if isinstance(cur, dict) else cur[int(part)]
    last = parts[-1]
    if isinstance(cur, list):
        if last == '-':
            cur.append(val)
        else:
            i = int(last)
            cur.insert(i, val) if insert else cur.__setitem__(i, val)
    else:
        cur[last] = val


def ptr_del(doc, p):
    parts = ptr_parts(p)
    cur = doc
    for part in parts[:-1]:
        cur = cur[part] if isinstance(cur, dict) else cur[int(part)]
    last = parts[-1]
    cur.pop(int(last)) if isinstance(cur, list) else cur.pop(last, None)


def flat_ops(ops, out):
    for o in ops:
        if isinstance(o, list):
            flat_ops(o, out)
        elif isinstance(o, dict):
            out.append(o)


def apply_patch(doc, ops):
    fails = []
    flat = []
    flat_ops(ops, flat)
    for i, op in enumerate(flat):
        kind, path = op.get('op'), op.get('path', '')
        try:
            if kind == 'test':
                if ptr_get(doc, path) != op.get('value'):
                    fails.append(i)
            elif kind in ('replace', 'add'):
                ptr_set(doc, path, op.get('value'), insert=(kind == 'add'))
            elif kind == 'remove':
                ptr_del(doc, path)
        except Exception:
            fails.append(i)
    return fails


providers = [('packed.pak', 'pak', Pak(SB + r"\assets\packed.pak"))]
for fn in sorted(os.listdir(MODS), key=str.lower):
    fp = os.path.join(MODS, fn)
    if fn.endswith('.pak'):
        try:
            providers.append(('mods/' + fn, 'pak', Pak(fp)))
        except Exception:
            pass
    elif os.path.isdir(fp):
        providers.append(('mods/' + fn + '/', 'dir', fp))

readers = {n: r for n, k, r in providers}
order = {n: i for i, (n, k, r) in enumerate(providers)}

# pass1: for each asset with patches, last non-patch provider (base doc owner)
base_of = {}
patches_of = {}
for name, kind, reader in providers:
    if kind == 'pak':
        idx = reader.index
        read = reader.read
    else:
        idx = []
        for root, _, files in os.walk(reader):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), reader).replace('\\', '/')
                idx.append('/' + rel)

        def make_read(base):
            return lambda p: open(os.path.join(base, p.lstrip('/')), 'rb').read()
        read = make_read(reader)
    skip_prov = name.split('/')[-1] in SKIP_PROVIDERS or name.endswith('/')
    for path in idx:
        if path.endswith('.metadata'):
            continue
        if path.endswith('.patch'):
            real = path[:-6]
            if not skip_prov or name.split('/')[-1] in TRANSLATION_PAKS:
                patches_of.setdefault(real, []).append((name, read(path)))
            continue
        if skip_prov:
            continue
        base_of[path] = name  # last provider wins

print('assets with patches:', len(patches_of))

attr = collections.Counter()          # translation pak -> assets where it first fails
zz_fail_assets = []                    # assets where zz_translation_female fails
per_pak_assets = collections.defaultdict(set)
for path, plist in patches_of.items():
    base = base_of.get(path)
    if base is None:
        continue
    try:
        doc = parse_sb(readers[base].read(path))
    except Exception:
        continue
    plist = sorted(plist, key=lambda t: order[t[0]])
    failed = False
    for n, b in plist:
        try:
            ops = json.loads(b.decode('utf-8'))
        except Exception:
            continue
        fails = apply_patch(doc, ops)
        if fails and n.split('/')[-1] in TRANSLATION_PAKS:
            per_pak_assets[n.split('/')[-1]].add(path)
            if n.split('/')[-1] == 'zz_translation_female.pak':
                zz_fail_assets.append((path, len(fails)))
            attr[n.split('/')[-1]] += 1
            failed = True
    # keep applying rest anyway (doc mutated)

for p, c in attr.most_common():
    print('pak with failing test ops: %-55s assets=%d' % (p, c))
print('zz_translation_female failing assets:', len(zz_fail_assets))
w = csv.writer(open('data/attr_zz_fails.tsv', 'w', encoding='utf-8', newline=''), delimiter='\t')
w.writerow(['asset', 'failing_ops'])
for a, n in zz_fail_assets:
    w.writerow([a, n])
print('wrote data/attr_zz_fails.tsv')
