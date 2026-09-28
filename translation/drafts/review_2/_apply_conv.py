import json,re,csv,collections
d=json.load(open('docs/_review_map.json',encoding='utf-8'))
meta,tr=d['meta'],d['tr']

def jamo(s):
    c=ord(s)-0xAC00
    return (c//588,(c%588)//28,c%28)
MARK={'애','앙','엥','엉','응','잉','앵','옹','융','양','영','음','엄','엣','앗','엇','읏','흠','흥','흣','욯','읔','엌','웅'}
def deelong_word(w):
    while len(w)>=3:
        last,prev=w[-1],w[-2]
        L,P=jamo(last),jamo(prev)
        if L[0]!=11: break
        if last in MARK and P[2]==0:
            w=w[:-1]; continue
        if L[2]==0 and P[2]==0:
            if last in {'어','아','오','우','으','이','유','야','여','요','예','에','애'} and L[1]==P[1]:
                w=w[:-1]; continue
            if last=='어' and P[1] in {5,6,7,13,14,18,20}:
                w=w[:-1]; continue
            if last=='아' and P[1] in {0,1,2,3}:
                w=w[:-1]; continue
            if last=='우' and P[1] in {12,16}:
                w=w[:-1]; continue
            if last=='오' and P[1] in {8,9,10,11}:
                w=w[:-1]; continue
        break
    return w

import importlib.util
spec=importlib.util.spec_from_file_location('_conv','docs/_conv.py')
# reuse D/SUF/NODA/conv_last by exec'ing the dict part is complex; simpler: import module but it runs full pass.
# Instead re-declare by executing the file up to 'changes=[]' marker? Simpler: exec whole file is a dry-run, no writes — safe.
_conv=importlib.util.module_from_spec(spec)
spec.loader.exec_module(_conv)  # runs preview generation again (harmless)
D,SUF,NODA=_conv.D,_conv.SUF,_conv.NODA
conv_last=_conv.conv_last

byfile=collections.defaultdict(dict)
for fid,(t,f) in tr.items():
    m=meta.get(fid)
    if m not in NODA: continue
    tt=t
    if m=='florandescription':
        tt=re.sub(r'[가-힣]{3,}',lambda mm:deelong_word(mm.group(0)),tt)
    def repl(mm):
        w,p=mm.group(1),mm.group(2)
        if '?' in p: return mm.group(0)
        nw=conv_last(w)
        return (nw if nw else w)+p
    nt=re.sub(r"([가-힣']{2,})([.!…]+|$)",repl,tt)
    if nt!=t: byfile[f][fid]=nt

total=0
for f,upd in byfile.items():
    rows=list(csv.reader(open('translations/'+f,encoding='utf-8-sig',newline=''),delimiter='\t',quoting=csv.QUOTE_MINIMAL))
    n=0
    for r in rows:
        if len(r)>=2 and r[0] in upd:
            r[1]=upd[r[0]]; n+=1
    with open('translations/'+f,'w',encoding='utf-8',newline='') as fo:
        csv.writer(fo,delimiter='\t',quoting=csv.QUOTE_MINIMAL,lineterminator='\n').writerows(rows)
    total+=n
    print(f.split('/')[-1],n)
print('TOTAL',total)
