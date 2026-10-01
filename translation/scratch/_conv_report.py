import csv, sys, io, re
from collections import Counter
csv.field_size_limit(sys.maxsize)
sys.path.insert(0, '.')
import importlib.util
spec = importlib.util.spec_from_file_location('frp', 'tools/fix_race_polite.py')
frp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frp)

pairs = {}
for row in csv.DictReader(open('data/pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
    seg = row['pointer'].rsplit('/', 1)[-1]
    if not frp.race_key_ok(seg):
        continue
    for m in frp.END_RX.finditer(row['korean']):
        w = m.group(0)
        nw = frp.conv_word(m)
        if nw != w:
            pairs.setdefault(w, nw)

with open('_conv_words.txt', 'w', encoding='utf-8') as f:
    for w, nw in sorted(pairs.items()):
        f.write('%s\t%s\n' % (w, nw))
print('unique converted words:', len(pairs))
