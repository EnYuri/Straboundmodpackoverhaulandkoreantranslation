import csv, sys, io, re
csv.field_size_limit(sys.maxsize)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RACE_RX = re.compile(r'/(\w+)[Dd]escription$')
GENERIC = {'description', 'longdescription', 'shortdescription', 'turnin',
           'default', 'generic', 'passive', 'defaultrecruit', 'inspection',
           'recruit', 'completion', 'nonehint', 'selecttech', 'scan', 'sktest'}
TARGETS = ['드세요', '여보세요', '힘내세요', '끄세요', '잠드세요', '두세요',
           '내쉬세요', '묶으십시오', '따르십시오', '마십시오', '쉬시오',
           '떠나시오', '있습니까', '랍니다', '답니다', '합시다', '담요',
           '마세요', '누구일까요', '나요']
for row in csv.DictReader(open('data/pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
    m = RACE_RX.search(row['pointer'])
    if not m or m.group(1).lower() in GENERIC:
        continue
    ko = row['korean']
    for t in TARGETS:
        if t in ko:
            i = ko.find(t)
            print(t, '|', row['asset'].split('/')[-1] + row['pointer'])
            print('   ', ko[max(0, i - 60):i + 60].replace('\n', ' / '))
            break
