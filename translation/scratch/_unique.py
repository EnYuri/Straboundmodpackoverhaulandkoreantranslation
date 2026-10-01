import csv, sys, io, re
from collections import Counter
csv.field_size_limit(sys.maxsize)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RACE_RX = re.compile(r'/(\w+)[Dd]escription$')
GENERIC = {'longdescription', 'shortdescription', 'turnindescription', 'defaultdescription',
           'genericdescription', 'passivedescription', 'defaultrecruitdescription',
           'inspectiondescription', 'recruitdescription', 'completiondescription',
           'nonehintdescription', 'selecttechdescription', 'scandescription',
           'sktestdescription', 'itemdescription'}
END = re.compile(r"[가-힣]+(?:으?세요|십시오|시오|습니다|습니까|십니까|랍니다|답니다|합시다|봅시다|니까요|까요|나요|이에요|이예요|네요|군요|죠|여요|해요|어요|아요|예요|요)(?=[\s.!?…,;'\"()~\^]|$)")
c = Counter()
for row in csv.DictReader(open('data/pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
    m = RACE_RX.search(row['pointer'])
    if not m:
        continue
    key = (m.group(1) + 'description').lower()
    if key in GENERIC:
        continue
    for mt in END.finditer(row['korean']):
        c[mt.group(0)] += 1
for w, n in c.most_common():
    print(n, w)
