import csv, sys, io, re
from collections import Counter
csv.field_size_limit(sys.maxsize)
RACE_RX = re.compile(r'/(\w+)[Dd]escription$')
GEN = {'longdescription','shortdescription','turnindescription','defaultdescription','genericdescription','passivedescription','defaultrecruitdescription','inspectiondescription','recruitdescription','completiondescription','nonehintdescription','selecttechdescription','scandescription','sktestdescription','itemdescription'}
END = re.compile(r"[가-힣]+니다(?=[\s.!?…,;'\"()~^]|$)")
c = Counter()
for row in csv.DictReader(open('data/pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
    m = RACE_RX.search(row['pointer'])
    if not m or (m.group(1) + 'description').lower() in GEN:
        continue
    for mt in END.finditer(row['korean']):
        c[mt.group(0)] += 1
out = io.open('_nida3.txt', 'w', encoding='utf-8')
for w, n in sorted(c.items()):
    if w.endswith('습니다'): tag = 'SEUP'
    elif w.endswith('입니다'): tag = 'IP'
    elif w.endswith('합니다'): tag = 'HAP'
    elif w.endswith('랍니다') or w.endswith('답니다'): tag = 'RAP'
    else: tag = 'BNIDA'
    out.write('%s\t%d\t%s\n' % (tag, n, w))
out.close()
print('done', len(c))
