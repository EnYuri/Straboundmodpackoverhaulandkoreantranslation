#!/usr/bin/env python3
"""Dump the next TODO rows from style_worklist.tsv for natural-Korean rewriting.

usage: python style_next.py [count] [id|worst|long|inspect]
  id      - worklist order (default)
  worst   - lowest Hangul-per-word density first
  long    - non-inspection text first, then longest source text
  inspect - deferred object-inspection dialogue, longest first
"""
import csv, glob, re, sys
sys.stdout.reconfigure(encoding='utf-8')
n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
mode = sys.argv[2] if len(sys.argv) > 2 else 'id'
TAGRE = re.compile(r'\^[^;^\s]{1,20};')
wl = {r['id']: r for r in csv.DictReader(open('rest_worklist.tsv', encoding='utf-8-sig', newline=''), delimiter='\t')}
ko = {}
for bf in glob.glob('translations/rest_*.tsv'):
    for r in csv.reader(open(bf, encoding='utf-8-sig', newline=''), delimiter='\t'):
        if r:
            ko[r[0]] = r[1]
def ewords(k):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", TAGRE.sub('', wl[k]['englishText'])))
def is_inspection(k):
    hints = [x.strip().lower() for x in wl[k]['keyHints'].split('|') if x.strip()]
    generic = {'description', 'longdescription', 'shortdescription'}
    return bool(hints) and all(x.endswith('description') and x not in generic for x in hints)
todo = [r for r in csv.DictReader(open('style_worklist.tsv', encoding='utf-8-sig', newline=''), delimiter='\t') if r['status'] == 'TODO']
if mode == 'worst':
    todo.sort(key=lambda r: float(r['density']))
elif mode == 'long':
    todo.sort(key=lambda r: (is_inspection(r['id']), -ewords(r['id'])))
elif mode == 'inspect':
    todo = [r for r in todo if is_inspection(r['id'])]
    todo.sort(key=lambda r: -ewords(r['id']))
elif mode != 'id':
    raise SystemExit(f'unknown order: {mode}')
print(f'# TODO remaining: {len(todo)}  (order: {mode})')
for r in todo[:n]:
    k = r['id']
    print(f"===== {k} [{wl[k]['keyHints'][:40]}] {wl[k]['mods'][:40]} ({r['flags']})")
    print('--EN--'); print(wl[k]['englishText'])
    print('--KO--'); print(ko[k])
