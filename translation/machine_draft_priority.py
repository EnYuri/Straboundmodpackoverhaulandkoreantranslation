#!/usr/bin/env python3
"""Create a masked machine-translation draft for a priority batch.

This is a drafting aid only: run the project QA afterwards and review the
result before treating the batch as complete. Markup, placeholders, input
tokens, and line layout are preserved verbatim.
"""
import csv, json, re, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

BATCH = sys.argv[1]
OUT = sys.argv[2]
ids = []
for line in open(BATCH, encoding='utf-8-sig'):
    m = re.match(r'^(\d+)\t', line)
    if m: ids.append(m.group(1))
work = {r['id']: r['englishText'] for r in csv.DictReader(open('rest_worklist.tsv', encoding='utf-8-sig', newline=''), delimiter='\t') if r['id'] in set(ids)}
token_rx = re.compile(r'\^[^;\s]+;|\[[^\]\n]+\]|<[^>\n]+>|\$\{[^}\n]+\}|%\d*\$?[a-zA-Z]|[\ue000-\uf8ff]')

def mask(s):
    values=[]
    def sub(m):
        values.append(m.group(0)); return f'ZZXMARK{len(values)-1}QZZ'
    return token_rx.sub(sub, s), values

def unmask(s, values):
    for i, v in enumerate(values):
        s = s.replace(f'ZZXMARK{i}QZZ', v)
        s = s.replace(f'ZZXMARK {i} QZZ', v)
    return s

def translate_line(line):
    if not line.strip(): return line
    lead = line[:len(line)-len(line.lstrip())]
    tail = line[len(line.rstrip()):]
    text, vals = mask(line.strip())
    if len(text) > 4200:
        # Long prose is split on sentence whitespace; preserve the exact original layout.
        parts = re.split(r'(?<=[.!?])\s+', text)
        return lead + ' '.join(translate_line(p) for p in parts) + tail
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ko&dt=t&q=' + urllib.parse.quote(text)
    for attempt in range(4):
        try:
            data = json.loads(urllib.request.urlopen(url, timeout=30).read().decode('utf-8'))
            return lead + unmask(''.join(x[0] for x in data[0]), vals) + tail
        except Exception:
            if attempt == 3: raise
            time.sleep(1 + attempt)

def translate_item(item):
    i, text = item
    return i, '\n'.join(translate_line(line) for line in text.split('\n'))

out={}
with ThreadPoolExecutor(max_workers=6) as pool:
    futures = [pool.submit(translate_item, item) for item in work.items()]
    for n, f in enumerate(as_completed(futures), 1):
        i, text = f.result(); out[i]=text
        if n % 25 == 0: print(f'drafted {n}/{len(work)}', flush=True)
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'wrote {len(out)} rows to {OUT}')
