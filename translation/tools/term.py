import csv, glob, re, sys
# Look up how terms were translated before (installed TM + manual batches).
# usage: python term.py "Arcane Star" Tripolar ...   (case-insensitive substring; shortest 3 hits each)
sys.stdout.reconfigure(encoding='utf-8')
pairs = []
rd = csv.reader(open('data/translation_memory.tsv', encoding='utf-8-sig', newline=''), delimiter='\t')
next(rd)
for r in rd:
    if len(r) >= 4:
        pairs.append((r[2], r[3], 'TM'))
en = {r['id']: r['englishText'] for r in csv.DictReader(open('data/rest_worklist.tsv', encoding='utf-8-sig', newline=''), delimiter='\t')}
for bf in sorted(glob.glob('translations/rest_*.tsv')):
    for r in csv.reader(open(bf, encoding='utf-8-sig', newline=''), delimiter='\t'):
        if r and r[0] in en:
            pairs.append((en[r[0]], r[1], r[0]))
for t in sys.argv[1:]:
    p = re.compile(re.escape(t), re.I)
    hits = sorted((x for x in pairs if p.search(x[0])), key=lambda x: len(x[0]))[:3]
    if not hits:
        print('--', t, ': none')
    for e, k, src in hits:
        print('==', t, f'[{src}]', e[:110].replace('\n', ' / '), '=>', k[:110].replace('\n', ' / '))
