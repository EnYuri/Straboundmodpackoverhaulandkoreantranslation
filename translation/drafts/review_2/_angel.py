import json,re,collections,importlib.util
d=json.load(open('docs/_review_map.json',encoding='utf-8'))
meta,tr=d['meta'],d['tr']
spec=importlib.util.spec_from_file_location('_conv','docs/_conv.py')
c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
D,SUF=c.D,c.SUF

def strip_batchim_ㄴ(ch):
    code=ord(ch)-0xAC00
    if code<0 or code%28!=4: return None  # ㄴ 종성 index 4
    return chr(code-4+0xAC00)

def da_to_gunyo(w):
    # ends with 다
    if w.endswith('습니다'): return w[:-3]+'군요'
    if w.endswith('입니다'): return w[:-3]+'이군요'
    if w.endswith('니다') and len(w)>=3 and ord(w[-3])>=0xAC00 and (ord(w[-3])-0xAC00)%28==17:
        # -ㅂ니다 verbs: drop ㅂ batchim + 는군요
        p=ord(w[-3])-0xAC00
        return w[:-3]+chr(0xAC00+p-17)+'는군요'
    if len(w)>=2 and w[-1]=='다':
        stem=w[:-1]
        # verb -ㄴ다 : previous syllable has ㄴ batchim (but not '는다') -> remove ㄴ + 는군요
        if stem and stem[-1]!='는' and ord(stem[-1])>=0xAC00 and (ord(stem[-1])-0xAC00)%28==4:
            return stem[:-1]+strip_batchim_ㄴ(stem[-1])+'는군요'
        return stem+'군요'
    return None

def hae_to_da(w):
    if w in D: return D[w]
    for a,b in SUF:
        if w.endswith(a) and len(w)>len(a): return w[:-len(a)]+b
    if w.endswith('이야') and len(w)>3: return w[:-2]+'이다'
    return None

def convert_word(w):
    # questions handled separately
    orig=w
    if w.endswith('요'):
        w=w[:-1]
        if w.endswith('예'):  # X예요 -> X이군요
            return w[:-1]+'이군요'
        if w.endswith('이에'):
            return w[:-2]+'이군요'
        w2=hae_to_da(w)
        if w2:
            g=da_to_gunyo(w2)
            return g if g else w2+'요'
        return orig
    g=da_to_gunyo(w)
    if g: return g
    w2=hae_to_da(w)
    if w2:
        g=da_to_gunyo(w2)
        return g if g else w2
    return orig

changes=[]
for fid,(t,f) in tr.items():
    if meta.get(fid)!='angeldescription': continue
    def repl(mm):
        w,p=mm.group(1),mm.group(2)
        if '?' in p: return mm.group(0)
        nw=convert_word(w)
        return nw+p
    nt=re.sub(r"([가-힣']{2,})([.!…]+|$)",repl,t)
    if nt!=t: changes.append((fid,t,nt,f))
print('angel changes:',len(changes))
o=open('docs/_angel_preview.txt','w',encoding='utf-8')
for fid,o_,n,f in changes:
    o.write(f'{fid}\t{f}\n- {o_}\n+ {n}\n\n')
o.close()
