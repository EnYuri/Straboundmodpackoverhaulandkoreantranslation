import csv, sys, io, re
from collections import Counter
csv.field_size_limit(sys.maxsize)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# race-specific description keys (exclude generic /description, /longdescription,
# /shortdescription, and non-race misc keys)
GENERIC = {'description', 'longdescription', 'shortdescription'}
RACE_RX = re.compile(r'/(\w+)[Dd]escription$')

# word ending in polite ending, sentence-final-ish position
END_RX = re.compile(
    r'([가-힣]+?(?:습니다|습니까|세요|십시오|시오|합시다|해요|예요|이에요|이예요|'
    r'예죠|이죠|네요|군요|랍니다|에요))(?=[.!?…\n, ]|$)')

words = Counter()
fields = set()
for row in csv.DictReader(open('data/pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
    m = RACE_RX.search(row['pointer'])
    if not m or m.group(1).lower() in GENERIC:
        continue
    ko = row['korean']
    for mm in END_RX.finditer(ko):
        words[mm.group(1)] += 1
    fields.add((row['asset'], row['pointer']))

print('fields:', len(fields), 'tokens:', sum(words.values()))
for w, c in words.most_common(300):
    print(c, w)
