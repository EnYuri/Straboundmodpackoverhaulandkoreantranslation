# -*- coding: utf-8 -*-
# Dump matched context for risky batch42 rules before applying.
import sys, json, re, csv
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak
from fix_codex_review_batch42 import RULES, TARGET, PAIRS

csv.field_size_limit(10**8)
en_map = {}
for r in csv.reader(open(PAIRS, encoding='utf-8-sig'), delimiter='\t'):
    if len(r) >= 4:
        en_map[(r[0], r[1])] = r[2]

WATCH = {w.split('=')[0] for w in sys.argv[1].split(',')}
pk = Pak(TARGET)
for asset in sorted(pk.index):
    if not asset.endswith('.patch'):
        continue
    try:
        doc = json.loads(pk.read(asset))
    except Exception:
        continue
    if not isinstance(doc, list):
        continue
    stack = list(doc)
    while stack:
        it = stack.pop()
        if isinstance(it, list):
            stack.extend(it)
            continue
        if not (isinstance(it, dict) and it.get('op') in ('replace', 'add') and isinstance(it.get('value'), str)):
            continue
        v = it['value']
        path = it.get('path', '')
        for lbl, pat, rep, eg, ag, pg, isre in RULES:
            if lbl not in WATCH:
                continue
            if ag and not re.search(ag, asset):
                continue
            if pg and not re.search(pg, path):
                continue
            en = en_map.get((asset, path), '')
            if eg:
                pos, neg = eg if isinstance(eg, tuple) else (eg, None)
                if not re.search(pos, en) or (neg and re.search(neg, en)):
                    continue
            for m in re.finditer(pat if isre else re.escape(pat), v):
                s = max(0, m.start()-30); e = min(len(v), m.end()+30)
                print(f'[{lbl}] {asset} {path}')
                print(f'    ...{v[s:e]}...')
                print(f'    EN: {en[:120]}')
