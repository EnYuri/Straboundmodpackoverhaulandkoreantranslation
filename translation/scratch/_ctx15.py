import sys,io,csv,re,collections
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
DUP=re.compile(r'\b([가-힣A-Za-z]+(?:[의를은이가을도에과와로서로써]|요|다)?) \1\b')
n=0
for r in csv.DictReader(open('data/qa_mt_style_report.tsv',encoding='utf-8-sig'),delimiter='\t'):
    if r['kind']!='DUP_WORD':continue
    ko=r['korean']
    for m in DUP.finditer(ko):
        ctx=ko[max(0,m.start()-35):m.end()+35].replace('\n','|')
        print(r['asset'][-42:],'|',r['pointer'][-20:],'|',repr(ctx))
        n+=1;break
print('total rows w/ vis-dup:',n)
