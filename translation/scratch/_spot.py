import csv, sys, io, re, random
csv.field_size_limit(sys.maxsize)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
random.seed(7)
rows = []
for row in csv.DictReader(open('data/pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
    if re.search(r'(\w+)[Dd]escription$', row['pointer']) and row['korean']:
        rows.append(row)
random.shuffle(rows)
for r in rows[:40]:
    print(r['asset'].split('/')[-1], r['pointer'])
    print('  ', r['korean'].replace('\n', ' / ')[:160])
