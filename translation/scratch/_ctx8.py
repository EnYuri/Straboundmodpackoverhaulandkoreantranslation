import sys,io,csv,re,collections
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
POL=re.compile(r'(습니다|습니다\.|해요|세요|이에요|예요|네요|까요|어요|아요)\s*$')
PLAIN=re.compile(r'(다|이다|한다|된다|있다|없다|같다|이다|는다|라|까|냐|구나)\.?\s*$')
pol=pla=0
for r in csv.DictReader(open('data/pak_pairs.tsv',encoding='utf-8-sig'),delimiter='\t'):
    if not r['pointer'].endswith('description'):continue
    ko=r['korean'].strip()
    if not ko:continue
    tail=ko.rsplit('\n',1)[-1].strip()
    if POL.search(tail):pol+=1
    elif PLAIN.search(tail):pla+=1
print('description endings: polite',pol,'plain',pla)
