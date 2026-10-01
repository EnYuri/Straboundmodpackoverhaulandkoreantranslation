import csv, sys, io, re
from collections import Counter
csv.field_size_limit(sys.maxsize)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GENERIC = {'description', 'longdescription', 'shortdescription'}
RACE_RX = re.compile(r'/(\w+)[Dd]escription$')

# every word ending in a polite form at sentence/clause-final position
END_RX = re.compile(r'([가-힣]+?(?:습니다|습니까|입니다|세요|십시오|시오|합시다|'
                    r'어요|아요|여요|해요|예요|이에요|이예요|예죠|이죠|에죠|'
                    r'네요|군요|는군요|랍니다|답니다|죠|지요|요))(?=[.!?…\n,; ]|$)')

words = Counter()
for row in csv.DictReader(open('data/pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
    m = RACE_RX.search(row['pointer'])
    if not m or m.group(1).lower() in GENERIC:
        continue
    for mm in END_RX.finditer(row['korean']):
        w = mm.group(1)
        if len(w) >= 2:
            words[w] += 1

print('tokens:', sum(words.values()), 'unique:', len(words))
for w, c in words.most_common(500):
    print(c, w)
