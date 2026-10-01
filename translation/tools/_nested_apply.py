#!/usr/bin/env python3
# Re-apply a filled work TSV, resolving nested leaf-key paths that the flat
# applier skips. Usage: python _nested_apply.py <filled_tsv>
import csv, json, sys, io, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
csv.field_size_limit(10**8)
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\tools")
from pak import Pak
from pak_writer import write_pak
from align_merged_translations import parse_json

SB = r"E:\My Games\steamapps\common\Starbound"
MODS = SB + r"\mods"
TR = MODS + r"\zz_translation_female.pak"
SURV = r"data\coverage_survey.tsv"

def parse_sb(raw):
    s = raw.decode('utf-8', errors='replace')
    s = re.sub(r'//[^\n]*', '', s)
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    out, ins = [], False
    for i, c in enumerate(s):
        if c == '"' and (i == 0 or s[i - 1] != chr(92)):
            ins = not ins
        out.append('\r' if ins and c == '\r' else '\n' if ins and c == '\n' else c)
    return json.loads(re.sub(r',(\s*[}\]])', r'\1', ''.join(out)))

def find_paths(node, key, cur_path=''):
    hits = []
    if isinstance(node, dict):
        for k, v in node.items():
            np = cur_path + '/' + k
            if k == key and isinstance(v, str):
                hits.append((np, v))
            else:
                hits += find_paths(v, key, np)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            hits += find_paths(v, key, f'{cur_path}/{i}')
    return hits

tsv = sys.argv[1]
rows = [r for r in csv.reader(open(tsv, encoding='utf-8'), delimiter='\t')]
prov_map = {}
for r in rows[1:]:
    if len(r) >= 4 and r[3].strip():
        prov_map.setdefault(r[0], {})[r[1]] = r[3]
surv = {}
for r in csv.reader(open(SURV, encoding='utf-8'), delimiter='\t'):
    if len(r) >= 2:
        surv[r[1]] = r[0]
paks, overrides, bad = {}, {}, 0
for path, fmap in prov_map.items():
    prov = surv.get(path)
    if not prov:
        print('no provider', path); continue
    if prov not in paks:
        paks[prov] = Pak(os.path.join(MODS, prov.split('/')[-1]))
    try:
        doc = parse_sb(paks[prov].read(path))
    except Exception:
        print('unreadable', path); continue
    ops = []
    for fld, ko in fmap.items():
        cur = doc.get(fld) if isinstance(doc, dict) else None
        if isinstance(cur, str):
            ops.append([{"op": "test", "path": "/" + fld, "value": cur},
                        {"op": "replace", "path": "/" + fld, "value": ko}])
        else:
            hits = find_paths(doc, fld)
            if not hits:
                print('  NO MATCH', path, fld); bad += 1
            for hp, hv in hits:
                ops.append([{"op": "test", "path": hp, "value": hv},
                            {"op": "replace", "path": hp, "value": ko}])
    if ops:
        overrides[path + '.patch'] = json.dumps(ops, ensure_ascii=False, indent=2).encode('utf-8')
print('patches:', len(overrides), 'unmatched:', bad)
if '--apply' in sys.argv and overrides:
    print('entries:', write_pak(TR, TR, overrides))
