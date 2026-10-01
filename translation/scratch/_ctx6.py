import sys,io,csv,re,collections
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
pats=collections.Counter()
samples=collections.defaultdict(list)
for r in csv.DictReader(open('data/qa_mt_style_report.tsv',encoding='utf-8-sig'),delimiter='\t'):
    if r['kind']=='DOUBLE_SPACE':
        ko=r['korean']
        for m in re.finditer(r'  +',ko):
            ctx=ko[max(0,m.start()-15):m.end()+15].replace('\n','|')
            # classify: around tag? after period? between words?
            a=ko[m.start()-1] if m.start()>0 else '^'
            b=ko[m.end()] if m.end()<len(ko) else '$'
            key=f'{a!r}...{b!r}'
            pats[key]+=1
            if len(samples[key])<3:samples[key].append((r['asset'][-40:],ctx))
for k,c in pats.most_common(30):
    print(c,k)
    for a,s in samples[k][:2]:print('   ',a,repr(s))
