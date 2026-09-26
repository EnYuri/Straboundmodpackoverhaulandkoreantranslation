# -*- coding: utf-8 -*-
import csv, re
src = open('gen_0745.py', encoding='utf-8-sig').read()
fix = {}
for i in ['48478', '48824', '48939']:
    m = re.search("'" + i + "':\\s*'((?:[^'\\\\]|\\\\.)*)'", src)
    raw = m.group(1)
    fix[i] = raw.replace('\\n', '\n').replace("\\'", "'").replace('\\\\', '\\')
    print(i, repr(fix[i]))
rows = [r for r in csv.reader(open('translations/rest_priority_0745.tsv', encoding='utf-8-sig', newline=''), delimiter='\t') if r]
for r in rows:
    if r[0] in fix: r[1] = fix[r[0]]
def dc(t):
    return '"' + t.replace('"', '""') + '"' if ('\n' in t or '"' in t or '\t' in t or t != t.strip() or not t) else t
with open('translations/rest_priority_0745.tsv', 'w', encoding='utf-8-sig', newline='') as f:
    for r in rows: f.write('\t'.join(dc(c) for c in r) + '\n')
