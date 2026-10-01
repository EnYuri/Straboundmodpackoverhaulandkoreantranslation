import re, json
LIT = chr(92) + 'n'
ko = {}
for fn in ['data/gic_ko_06a.tsv','data/gic_ko_06b.tsv']:
    for line in open(fn, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip(): continue
        i, v = line.split('\t', 1)
        ko[int(i)] = v
assert sorted(ko) == list(range(1401,1701))
uniq = json.load(open('data/gic_uniq.json',encoding='utf-8'))
td, nd = [], []
for i in range(1401,1701):
    en = uniq[str(i)]
    if sorted(re.findall(r'\^[#A-Za-z0-9]+;', ko[i])) != sorted(re.findall(r'\^[#A-Za-z0-9]+;', en)):
        td.append(i)
    if en.count('\n') != ko[i].count(LIT):
        nd.append((i, en.count('\n'), ko[i].count(LIT)))
print('rows:', len(ko), '| tag diffs:', td, '| nl diffs:', nd)
