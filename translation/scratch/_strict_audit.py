import sys,io,pickle,json,collections
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
sys.path.insert(0,r'E:/My Games/steamapps/common/Starbound');sys.path.insert(0,'tools')
import pak,sbjson
st=pickle.load(open('data/_upstream_state.pkl','rb'));final=st['final']
pk=pak.Pak(r'E:/My Games/steamapps/common/Starbound/mods/zz_translation_female.pak')
bad=collections.Counter();detail=[]
for fn in pk.index:
    if not fn.endswith('.patch'):continue
    try:d=sbjson.parse_sb(pk.read(fn).decode('utf-8-sig'))
    except:continue
    base=fn[:-6]  # strip .patch
    fstate=final.get(base,final.get(fn,{}))
    def rec(o):
        if isinstance(o,list):
            for x in o:rec(x)
        elif isinstance(o,dict):
            if o.get('op')=='test' and 'path' in o:
                tv=o.get('value')
                uv=fstate.get(o['path'],'<ABSENT>')
                if isinstance(uv,str) and '\\n' not in uv: pass
                norm=lambda s:s.replace('\r\n','\n') if isinstance(s,str) else s
                if norm(uv)!=norm(tv) and uv!='<ABSENT>':
                    bad['MISMATCH']+=1;detail.append(('MISM',fn,o['path'],str(tv)[:50],str(uv)[:50]))
                elif uv=='<ABSENT>':
                    bad['ABSENT']+=1;detail.append(('ABSNT',fn,o['path'],str(tv)[:50],''))
            for v in o.values():
                if isinstance(v,(list,dict)):rec(v)
    rec(d)
print('bad:',dict(bad))
for d in detail[:30]:print(d[0],d[1][-45:],'|',d[2][-35:],'|',d[3][:45],'|',d[4][:45])
