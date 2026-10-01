import re, json, sys
LIT = chr(92) + 'n'
lo, hi = int(sys.argv[1]), int(sys.argv[2])
fns = sys.argv[3:]
ko = {}
for fn in fns:
    for line in open(fn, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip(): continue
        i, v = line.split('\t', 1)
        ko[int(i)] = v
assert sorted(ko) == list(range(lo, hi+1)), [i for i in range(lo,hi+1) if i not in ko]
uniq = json.load(open('data/gic_uniq.json',encoding='utf-8'))
td, nd = [], []
for i in range(lo, hi+1):
    en = uniq[str(i)]
    if sorted(re.findall(r'\^[#A-Za-z0-9]+;', ko[i])) != sorted(re.findall(r'\^[#A-Za-z0-9]+;', en)):
        td.append(i)
    if en.count('\n') != ko[i].count(LIT):
        nd.append((i, en.count('\n'), ko[i].count(LIT)))
print('rows:', len(ko), '| tag diffs:', td, '| nl diffs:', nd)
