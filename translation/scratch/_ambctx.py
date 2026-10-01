import csv, sys, io, re
csv.field_size_limit(sys.maxsize)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
RACE_RX = re.compile(r'/(\w+)[Dd]escription$')
GEN = {'longdescription','shortdescription','turnindescription','defaultdescription','genericdescription','passivedescription','defaultrecruitdescription','inspectiondescription','recruitdescription','completiondescription','nonehintdescription','selecttechdescription','scandescription','sktestdescription','itemdescription'}
TARGETS = ['겁니다', '기립니다', '도가니다', '바구니다', '주머니다', '적습니다',
           '납니다', '냅니다', '듭니다', '띕니다', '느립니다', '다릅니다',
           '예쁩니다', '큽니다', '깁니다', '빠릅니다', '아닙니다', '감사드립니다',
           '꿉니다', '나옵니다', '싶어합니다', '합니다.', '혀납니다']
for row in csv.DictReader(open('data/pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
    m = RACE_RX.search(row['pointer'])
    if not m or (m.group(1) + 'description').lower() in GEN:
        continue
    ko = row['korean']
    for t in TARGETS:
        if t in ko:
            i = ko.find(t)
            print(t, '|', row['asset'].split('/')[-1], '|',
                  ko[max(0, i - 55):i + 55].replace('\n', ' / '))
