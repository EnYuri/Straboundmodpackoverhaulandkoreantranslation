import csv, sys, io, re
from collections import Counter
csv.field_size_limit(sys.maxsize)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RACE_RX = re.compile(r'/(\w+)[Dd]escription$')
c = Counter()
for row in csv.DictReader(open('data/pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
    m = RACE_RX.search(row['pointer'])
    if m:
        c[m.group(1).lower()] += 1
for k, v in c.most_common(200):
    print(v, k)
