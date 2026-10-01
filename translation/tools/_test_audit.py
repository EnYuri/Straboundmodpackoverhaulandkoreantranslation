import sys,io,os,json,re,collections
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
sys.path.insert(0,r'E:/My Games/steamapps/common/Starbound')
sys.path.insert(0,'tools')
import pak,sbjson
MD=r'E:/My Games/steamapps/common/Starbound/mods'
paks=[('__vanilla__',r'E:/My Games/steamapps/common/Starbound/assets/packed.pak'),('__opensb__',r'E:/My Games/steamapps/common/Starbound/assets/opensb.pak')]
ent=[]
for f in os.listdir(MD):
    if 'zz_translation' in f:continue
    full=os.path.join(MD,f)
    if f.endswith('.pak') or os.path.isdir(full):ent.append((f,full))
paks+=sorted(ent)
tpk=pak.Pak(os.path.join(MD,'zz_translation_female.pak'))
def parse(b):
    return sbjson.parse_sb(b.decode('utf-8-sig'))
our_tests=collections.defaultdict(list)
for fn in tpk.index:
    if not fn.endswith('.patch'):continue
    try:d=parse(tpk.read(fn))
    except:continue
    def walk(o):
        if isinstance(o,list):
            for x in o:walk(x)
        elif isinstance(o,dict):
            if o.get('op')=='test':our_tests[fn].append((o.get('path',''),o.get('value')))
            else:
                for v in o.values():
                    if isinstance(v,(list,dict)):walk(v)
    walk(d)
targets=set(our_tests)
seen=collections.defaultdict(lambda:collections.defaultdict(set))   # our_patch_fn -> ptr -> set(values ever seen upstream)
final={}                            # our_patch_fn -> ptr -> last value
def dirlist(root):
    for dp,dn,fs in os.walk(root):
        for x in fs:
            yield '/'+os.path.relpath(os.path.join(dp,x),root).replace(os.sep,'/')
for f,path in paks:
    if os.path.isdir(path):
        for fn in dirlist(path):
            fh=open(os.path.join(path,fn.lstrip('/').replace('/',os.sep)),'rb').read()
            if fn.endswith('.patch'):
                if fn not in targets:continue
                try:d=parse(fh)
                except:continue
                def walk2(o,fn=fn):
                    if isinstance(o,list):
                        for x in o:walk2(x,fn)
                    elif isinstance(o,dict):
                        if o.get('op') in ('replace','add','test'):
                            p=o.get('path','')
                            v=o.get('value')
                            seen[fn][p].add(str(v))
                            if o['op'] in ('replace','add'):
                                final.setdefault(fn,{})[p]=v
                                if isinstance(v,(dict,list)):flat2(v,p,fn)
                        for vv in o.values():
                            if isinstance(vv,(list,dict)):walk2(vv,fn)
                walk2(d)
            else:
                key=fn+'.patch'
                if key in targets:
                    stt={}
                    try:j=parse(fh)
                    except:continue
                    def flat3(o,pre):
                        if isinstance(o,dict):
                            for k,v in o.items():flat3(v,pre+'/'+k)
                        elif isinstance(o,list):
                            for i,v in enumerate(o):flat3(v,pre+'/'+str(i))
                        else:stt[pre]=o
                    flat3(j,'')
                    for p,v in stt.items():seen[key][p].add(str(v))
                    final[key]=stt
        continue
    pp=pak.Pak(path)
    for fn in pp.index:
        if fn.endswith('.patch'):
            if fn not in targets:continue
            try:d=parse(pp.read(fn))
            except:continue
            def flat2(o,pre,fn=fn):
                if isinstance(o,dict):
                    for k,v in o.items():flat2(v,pre+'/'+k,fn)
                elif isinstance(o,list):
                    for i,v in enumerate(o):flat2(v,pre+'/'+str(i),fn)
                else:
                    seen[fn][pre].add(str(o))
                    final.setdefault(fn,{})[pre]=o
            def walk(o,fn=fn):
                if isinstance(o,list):
                    for x in o:walk(x,fn)
                elif isinstance(o,dict):
                    if o.get('op') in ('replace','add','test'):
                        p=o.get('path','')
                        v=o.get('value')
                        seen[fn][p].add(str(v))
                        if o['op'] in ('replace','add'):
                            final.setdefault(fn,{})[p]=v
                            if isinstance(v,(dict,list)):flat2(v,p,fn)
                    for vv in o.values():
                        if isinstance(vv,(list,dict)):walk(vv,fn)
            walk(d)
        else:
            key=fn+'.patch'
            if key in targets:
                st={}
                try:
                    j=parse(pp.read(fn))
                except:continue
                def flat(o,pre):
                    if isinstance(o,dict):
                        for k,v in o.items():flat(v,pre+'/'+k)
                    elif isinstance(o,list):
                        for i,v in enumerate(o):flat(v,pre+'/'+str(i))
                    else:st[pre]=o
                flat(j,'')
                for p,v in st.items():seen[key][p].add(str(v))
                final[key]=st
    del pp
bad=[]
for fn,tests in our_tests.items():
    for ptr,val in tests:
        hist=seen.get(fn,{}).get(ptr,set())
        if str(val) in hist:continue
        # container test: compare flattened subpaths
        if isinstance(val,(list,dict)):
            sub={}
            def fl(o,pre):
                if isinstance(o,dict):
                    for kk,vv in o.items():fl(vv,pre+'/'+kk)
                elif isinstance(o,list):
                    for i,vv in enumerate(o):fl(vv,pre+'/'+str(i))
                else:sub[pre]=str(o)
            fl(val,ptr)
            if all(str(final.get(fn,{}).get(p))==v for p,v in sub.items()) and sub:continue
            # also accept if all test leaves appear in seen history for those ptrs
            if all(v in seen.get(fn,{}).get(p,set()) for p,v in sub.items()) and sub:continue
        if ptr in final.get(fn,{}):
            bad.append((fn,ptr,val,'STATE:'+str(final[fn][ptr])[:100]))
        else:
            bad.append((fn,ptr,val,'NEVER_WRITTEN'))
print('tests:',sum(len(v) for v in our_tests.values()),'bad:',len(bad),'files:',len(set(b[0] for b in bad)))
import csv
with open('data/_test_audit.tsv','w',encoding='utf-8',newline='') as fo:
    w=csv.writer(fo,delimiter='\t');w.writerow(['asset','pointer','our_test','upstream'])
    for b in bad:w.writerow([b[0],b[1],str(b[2]),b[3]])
print(collections.Counter(b[3].split(':')[0] for b in bad))
import pickle
pickle.dump({'final':{k:v for k,v in final.items()},'seen':{k:dict(v) for k,v in seen.items()}},open('data/_upstream_state.pkl','wb'))
print('state saved')
for b in bad[:35]:
    print(b[0][-55:],b[1][-38:],'|',repr(str(b[2]))[:52],'|',b[3][:80])
