import sys,io,csv,re,collections
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
# which english words remain; group by word
words=collections.Counter();ex=collections.defaultdict(list)
TAG=re.compile(r'\^[^^\s]{1,20};')
for r in csv.DictReader(open('data/qa_mt_style_report.tsv',encoding='utf-8-sig'),delimiter='\t'):
    if r['kind']!='ENG_LEFT':continue
    ko=TAG.sub('',r['korean'])
    for w in re.findall(r"[A-Za-z][A-Za-z'\-]*",ko):
        if w.lower() in {'url','http','https','www'}:continue
        words[w]+=1
        if len(ex[w])<2:ex[w].append((r['asset'][-40:],ko[max(0,ko.find(w)-30):ko.find(w)+len(w)+30].replace('\n','|')))
for w,c in words.most_common(80):
    print(c,w)
    for a,s in ex[w][:1]:print('   ',a,repr(s))
