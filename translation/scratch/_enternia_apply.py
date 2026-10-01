import sys, os, csv, json
csv.field_size_limit(10**8)
sys.path.insert(0, 'tools')
code = open('tools/untrans_batch.py', encoding='utf-8').read()
ns = {}
exec(compile(code.split("if sys.argv[1] == 'extract'")[0], 'ub', 'exec'), ns)
parse_sb, write_pak, TR, SURV = ns['parse_sb'], ns['write_pak'], ns['TR'], ns['SURV']
sys.path.insert(0, '../modpack-overhaul-repo/tools')
from pak import Pak

pk = Pak(os.path.join(ns['MODS'], 'Enternia_contents_2006558650.pak'))

surv = {}
for r in csv.reader(open(SURV, encoding='utf-8'), delimiter='\t'):
    if len(r) >= 2:
        surv[r[1]] = r[0]

def find_paths(o, field, target, pfx=''):
    hits = []
    if isinstance(o, dict):
        for k, v in o.items():
            p = pfx + '/' + k
            if k == field and v == target:
                hits.append(p)
            elif isinstance(v, (dict, list)):
                hits += find_paths(v, field, target, p)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            hits += find_paths(x, field, target, pfx + f'/{i}')
    return hits

rows = [r for r in csv.reader(open('data/enternia_filled.tsv', encoding='utf-8'), delimiter='\t')][1:]
by_asset = {}
for r in rows:
    if len(r) >= 4 and r[3].strip():
        by_asset.setdefault(r[0], []).append((r[1], r[2], r[3]))

overrides = {}
miss = []
for path, fmap in by_asset.items():
    if 'Enternia' not in (surv.get(path) or ''):
        continue
    try:
        doc = parse_sb(pk.read(path))
    except Exception:
        print('unreadable', path); continue
    ops = []
    for fld, en, ko in fmap:
        hits = find_paths(doc, fld, en)
        if not hits:
            miss.append((path, fld))
            continue
        for p in hits:
            ops.append([{"op": "test", "path": p, "value": en},
                        {"op": "replace", "path": p, "value": ko}])
    if ops:
        overrides[path + '.patch'] = json.dumps(ops, ensure_ascii=False, indent=2).encode('utf-8')

print('patches:', len(overrides), 'fields missed:', len(miss))
for m in miss[:20]:
    print(' ', m)
if '--apply' in sys.argv and overrides:
    print('wrote pak; entries', write_pak(TR, TR, overrides))
else:
    print('dry run')
