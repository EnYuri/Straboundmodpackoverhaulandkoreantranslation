import sys,io,os,json,time,csv,collections,pickle,copy
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
sys.path.insert(0,r'E:/My Games/steamapps/common/Starbound')
sys.path.insert(0,'tools')
import pak,sbjson,pak_writer
csv.field_size_limit(10**8)
MD=r'E:/My Games/steamapps/common/Starbound/mods'
TR=os.path.join(MD,'zz_translation_female.pak')
st=pickle.load(open('data/_upstream_state.pkl','rb'))
final,seen=st['final'],st['seen']
bad=list(csv.DictReader(open('data/_test_audit.tsv',encoding='utf-8-sig'),delimiter='\t'))
perfile=collections.defaultdict(list)
for r in bad:perfile[r['asset']].append(r)
pk=pak.Pak(TR);ov={};fixed={'test':0,'nw_add':0,'nw_drop':0}
def segs(p):return [x.replace('~1','/').replace('~0','~') for x in p.strip('/').split('/')]
def join(s):return '/'+'/'.join(x.replace('~','~0').replace('/','~1') for x in s)
def exists_container(asset,pref):
    f=final.get(asset,{})
    if pref=='' or pref=='/':return True
    return pref in f or any(k.startswith(pref+'/') for k in f)
for fn,rows in perfile.items():
    try:d=sbjson.parse_sb(pk.read(fn).decode('utf-8-sig'))
    except:continue
    changed=False
    # index test ops by (path,value-str) for matching
    def walk_groups(d):
        gs=[]
        def rec(o):
            if isinstance(o,list):
                if any(isinstance(x,dict) and x.get('op') for x in o):gs.append(o)
                else:
                    for x in o:rec(x)
            elif isinstance(o,dict):
                for v in o.values():rec(v)
        rec(d)
        return gs
    groups=walk_groups(d)
    for g in groups:
        tops=[o for o in g if isinstance(o,dict) and o.get('op')=='test']
        rops=[o for o in g if isinstance(o,dict) and o.get('op') in ('replace','add','remove')]
        for t in tops:
            p=t.get('path');tv=t.get('value')
            row=next((r for r in rows if r['pointer']==p and str(r['our_test'])==str(tv)),None)
            if row is None:row=next((r for r in rows if r['pointer']==p),None)
            if row is None:continue
            if row['upstream'].startswith('STATE:'):
                nv=final.get(fn,{}).get(p)
                t['value']=copy.deepcopy(nv);changed=True;fixed['test']+=1
            else:
                # NEVER_WRITTEN: remove test, convert replace->add at FIRST missing segment
                idx=g.index(t);g.pop(idx);changed=True
                ss=segs(p)
                fmiss=len(ss)
                for i in range(1,len(ss)+1):
                    cand=join(ss[:i])
                    f=final.get(fn,{})
                    if not (cand in f or any(k.startswith(cand+'/') for k in f)):
                        fmiss=i-1;break
                anc=ss[:fmiss];tail=ss[fmiss:]
                if not tail:
                    nv=final.get(fn,{}).get(p)
                    g.insert(idx,{"op":"test","path":p,"value":copy.deepcopy(nv)})
                    fixed['test']+=1;continue
                for rop in rops:
                    rv=rop.get('value')
                    if any(sg.isdigit() for sg in tail[1:]):
                        fixed['nw_drop']+=1;continue  # numeric in nested tail -> skip
                    if len(tail)==1:
                        rop['op']='add';rop['path']=p
                    else:
                        nv=rv
                        for s2 in reversed(tail[1:]):nv={s2:nv}
                        rop['op']='add';rop['path']=join(anc+[tail[0]]);rop['value']=nv
                    fixed['nw_add']+=1
    if changed:ov[fn]=json.dumps(d,ensure_ascii=False,separators=(',',':')).encode('utf-8')
del pk
print('files:',len(ov),'fixes:',fixed)
if '--apply' in sys.argv and ov:
    pak_writer.write_pak(TR+'.staged',TR,ov)
    for i in range(60):
        try:os.replace(TR+'.staged',TR);print('replaced');break
        except PermissionError:time.sleep(5)
