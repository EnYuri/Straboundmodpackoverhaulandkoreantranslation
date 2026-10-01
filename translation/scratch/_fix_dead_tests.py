import sys,io,os,json,time,pickle,re,collections,copy,csv
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
sys.path.insert(0,r'E:/My Games/steamapps/common/Starbound')
sys.path.insert(0,'tools')
import pak,sbjson,pak_writer
st=pickle.load(open('data/_upstream_state.pkl','rb'))
final,seen=st['final'],st['seen']
MD=r'E:/My Games/steamapps/common/Starbound/mods'
TR=os.path.join(MD,'zz_translation_female.pak')
pk=pak.Pak(TR)
def fl(o,pre,out):
    if isinstance(o,dict):
        for kk,vv in o.items():fl(vv,pre+'/'+kk,out)
    elif isinstance(o,list):
        for i,vv in enumerate(o):fl(vv,pre+'/'+str(i),out)
    else:out[pre]=o
hangul=lambda s:isinstance(s,str) and bool(re.search(r'[가-힣]',s))
num=re.compile(r'\d+')
ov={};report=[]
for fn in pk.index:
    if not fn.endswith('.patch'):continue
    try:d=sbjson.parse_sb(pk.read(fn).decode('utf-8-sig'))
    except:continue
    tests=[];reps=collections.defaultdict(list)
    def walk(o):
        if isinstance(o,list):
            for x in o:walk(x)
        elif isinstance(o,dict):
            if o.get('op')=='test':tests.append(o)
            elif o.get('op')=='replace':reps[o.get('path')].append(o)
            for v in o.values():
                if isinstance(v,(list,dict)):walk(v)
    walk(d)
    byp=collections.defaultdict(list)
    for t in tests:byp[t.get('path')].append(t)
    f=final.get(fn,{})
    ch=False
    for p,ts in byp.items():
        fv=f.get(p)
        if any(t.get('value')==fv for t in ts):continue
        subf={k:v2 for k,v2 in f.items() if k==p or k.startswith(p+'/')}
        ok=False
        for t in ts:
            sv={};fl(t.get('value'),p,sv)
            if sv and all(k in subf and str(subf[k])==str(x) for k,x in sv.items()):ok=True;break
        if ok:continue
        # dead path: set all tests to final value (prefer whole-value from patch writes; else reconstruct from leaves? if fv missing and subf exists -> skip leaf paths)
        if p in f:
            nv=copy.deepcopy(f[p])
            for t in ts:
                t['value']=copy.deepcopy(nv)
            ch=True
            # check replace vs final for content mismatch signals
            for r in reps.get(p,[]):
                rv=r.get('value')
                if isinstance(rv,str) and isinstance(nv,str):
                    nF=set(num.findall(nv));nR=set(num.findall(rv))
                    if nF-nR:
                        report.append((fn,p,'num',nv,rv))
                elif isinstance(nv,list) and isinstance(rv,list):
                    if len(nv)!=len(rv):report.append((fn,p,'len',str(len(nv)),str(len(rv))))
        elif subf:
            # final exists only as flattened leaves: our test path is a container; build dict/list
            # reconstruct value
            node={}
            for k in subf:
                pass
            # fallback: set test to the leaf-final map assembled object? simpler: compare our test leaves to final leaves -> if mismatch, rewrite per-leaf? skip and log
            report.append((fn,p,'leafmismatch',str(ts[0].get('value'))[:60],str(subf)[:120]))
            for t in ts:
                # try leaf-level fix: if test value is scalar and single leaf exists
                if len(subf)==1:
                    k,v2=next(iter(subf.items()))
                    if k==p:t['value']=v2;ch=True
    if ch:ov[fn]=json.dumps(d,ensure_ascii=False,separators=(',',':')).encode('utf-8')
print('files changed:',len(ov))
w=csv.writer(open('data/_dead_fix_report.tsv','w',encoding='utf-8',newline=''),delimiter='\t')
w.writerow(['asset','pointer','kind','final','replace'])
for r in report:w.writerow(list(r))
print('flagged:',len(report))
if '--apply' in sys.argv and ov:
    pak_writer.write_pak(TR+'.staged',TR,ov)
    del pk
    for i in range(60):
        try:os.replace(TR+'.staged',TR);print('replaced');break
        except PermissionError:time.sleep(5)
