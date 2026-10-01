"""Fill ko column in elithian_work.tsv from elithian_ko.tsv (uniq index -> ko)."""
import csv, re, sys

csv.field_size_limit(10**8)

# uniq EN in index order
uniq = {}
cur = None
for l in open('scratch/_el_uniq.txt', encoding='utf-8'):
    m = re.match(r'^### (\d+) x\d+', l)
    if m:
        cur = int(m.group(1))
        uniq[cur] = ''
    elif cur is not None:
        uniq[cur] += l.rstrip('\n')

rows = {}
for l in open('data/elithian_ko.tsv', encoding='utf-8'):
    if l.startswith('idx') or not l.strip():
        continue
    i, k = l.rstrip('\n').split('\t', 1)
    rows[int(i)] = k

en2ko = {uniq[i]: rows[i] for i in uniq}
assert len(en2ko) == len(rows) == 964, (len(en2ko), len(rows))

wr = list(csv.reader(open('data/elithian_work.tsv', encoding='utf-8'), delimiter='\t'))
todo = filled = 0
for r in wr[1:]:
    if len(r) >= 4 and not r[3]:
        todo += 1
        ko = en2ko.get(r[2])
        if ko:
            r[3] = ko
            filled += 1
print('todo:', todo, 'filled:', filled, 'still empty:', todo - filled)

with open('data/elithian_work.tsv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerows(wr)
