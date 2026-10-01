#!/usr/bin/env python3
"""Apply a JSON {id: korean} rewrite map, mark those ids reviewed in
style_worklist.tsv, and re-run the structural check.

usage: python style_apply.py rewrites.json [ids-to-mark-ok-without-change ...]
Ids present in the JSON are marked DONE; extra ids on the command line are
marked OK (reviewed, no change needed).
"""
import csv, glob, io, json, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
NEW = json.load(open(sys.argv[1], encoding='utf-8'))
OK = set(sys.argv[2:])

def dump_cell(t):
    return '"' + t.replace('"', '""') + '"' if ('\n' in t or '"' in t or '\t' in t or t != t.strip()) else t

seen = set()
for bf in sorted(glob.glob('translations/rest_*.tsv')):
    rows = [r for r in csv.reader(open(bf, encoding='utf-8-sig', newline=''), delimiter='\t') if r]
    ch = False
    for r in rows:
        if r[0] in NEW:
            seen.add(r[0])
            if r[1] != NEW[r[0]]:
                r[1] = NEW[r[0]]; ch = True
    if ch:
        open(bf, 'w', encoding='utf-8-sig', newline='').write(''.join(r[0] + '\t' + dump_cell(r[1]) + '\n' for r in rows))
missing = [k for k in NEW if k not in seen]
if missing:
    print('!! ids not found in any batch file:', missing)

rows = list(csv.reader(open('data/style_worklist.tsv', encoding='utf-8-sig', newline=''), delimiter='\t'))
head, body = rows[0], rows[1:]
for r in body:
    if r[0] in NEW: r[-1] = 'DONE'
    elif r[0] in OK: r[-1] = 'OK'
out = io.StringIO(); w = csv.writer(out, delimiter='\t', lineterminator='\n')
w.writerow(head); w.writerows(body)
open('data/style_worklist.tsv', 'w', encoding='utf-8-sig', newline='').write(out.getvalue())
left = sum(1 for r in body if r[-1] == 'TODO')
print(f'rewritten {len(seen)}, marked OK {len(OK & {r[0] for r in body})}, TODO left {left}')
print(subprocess.run([sys.executable, 'qa_structure.py'], capture_output=True, text=True, encoding='utf-8').stdout.strip())
