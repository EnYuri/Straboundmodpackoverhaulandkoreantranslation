import sys,io,csv,re,collections
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
n_int=0;examples=[]
for r in csv.DictReader(open('data/qa_mt_style_report.tsv',encoding='utf-8-sig'),delimiter='\t'):
    if r['kind']!='DOUBLE_SPACE':continue
    ko,en=r['korean'],r['english']
    for m in re.finditer(r'  +',ko):
        if m.start()==0 or m.end()==len(ko):continue
        # interior double space
        n_int+=1
        # does EN contain a double space anywhere?
        end2=bool(re.search(r'  +',en))
        ctx=ko[max(0,m.start()-25):m.end()+25].replace('\n','|')
        examples.append((r['asset'][-45:],r['pointer'][-25:],end2,ctx))
print('interior double-space count:',n_int)
print('with EN double-space:',sum(1 for e in examples if e[2]))
for e in examples[:30]:print(('ENds' if e[2] else '----'),e[0],e[1],repr(e[3]))
