"""Identify skipped (non-top-level) fields in elithian_work.tsv."""
import csv, sys, io, os
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\tools")
sys.stdout.reconfigure(encoding='utf-8')
csv.field_size_limit(10**8)
from pak import Pak
import re, json

MODS = r"E:\My Games\steamapps\common\Starbound\mods"
SURV = r"data\coverage_survey.tsv"

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

rows = [r for r in csv.reader(open('data/elithian_work.tsv', encoding='utf-8'), delimiter='\t')]
surv = {}
for r in csv.reader(open(SURV, encoding='utf-8'), delimiter='\t'):
    if len(r) >= 2:
        surv[r[1]] = r[0]
paks = {}
skipped = []
for r in rows[1:]:
    if len(r) < 4 or not r[3]:
        continue
    path, fld = r[0], r[1]
    prov = surv.get(path)
    if prov not in paks:
        paks[prov] = Pak(os.path.join(MODS, prov.split('/')[-1]))
    try:
        doc = parse_sb(paks[prov].read(path))
    except Exception:
        print('unreadable', path)
        continue
    if not isinstance(doc.get(fld), str):
        skipped.append((path, fld, r[2][:80], r[3][:60]))
        # locate nested pointer
        def find(o, trail):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == fld and isinstance(v, str):
                        print('   pointer:', trail + '/' + k, '->', repr(v[:80]))
                    elif isinstance(v, (dict, list)):
                        find(v, trail + '/' + k)
            elif isinstance(o, list):
                for i, x in enumerate(o):
                    find(x, trail + '/' + str(i))
        find(doc, '')
for s in skipped:
    print('SKIPPED:', s[0], s[1], s[2], '->', s[3])
