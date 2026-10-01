import csv, sys, io, re
csv.field_size_limit(sys.maxsize)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RACES = ('apex|avian|floran|glitch|human|hylotl|novakid|avali|avikan|fenerox|felin|'
         'neko|kazdra|saturn|saturn2|lastree|viera|alta|moogle|woggle|lamia|pygs|'
         'orcana|nightar|elduukhar|skelekin|shadow|kemono|callistan|droden|trink|'
         'webber|wasphive|knightmare|argonian|remorian|phant|radien|sergin|stalker|'
         'gyrusen|pingkin|merrkin|odiar|xian|thelusian|poptop|akkimari|blattra|'
         'echidna|peglaci|vulpes|familiar|ninguen|lyrd|prototoke|bunnykin|succubus|'
         'incubus|felin')
rx = re.compile(r'/(' + RACES + r')([Dd]escription)$', re.I)
n = {'race': 0, 'other': 0}
others = {}
races = {}
for row in csv.DictReader(open('data/qa_mt_style_report.tsv', encoding='utf-8'), delimiter='\t'):
    if row['kind'] != 'EXAMINE_POLITE':
        continue
    ptr = row['pointer']
    m = rx.search(ptr)
    if m:
        n['race'] += 1
        races[m.group(1).lower()] = races.get(m.group(1).lower(), 0) + 1
    else:
        n['other'] += 1
        others[ptr] = others.get(ptr, 0) + 1
print(n)
print('--- non-race pointers ---')
for k, v in sorted(others.items(), key=lambda x: -x[1])[:50]:
    print(v, k)
print('--- race keys ---')
for k, v in sorted(races.items(), key=lambda x: -x[1]):
    print(v, k)
