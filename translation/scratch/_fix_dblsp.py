import sys,io,os,json,time
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
sys.path.insert(0,r'E:/My Games/steamapps/common/Starbound');sys.path.insert(0,'tools')
import pak,sbjson,pak_writer
TR=r'E:/My Games/steamapps/common/Starbound/mods/zz_translation_female.pak'
pk=pak.Pak(TR)
ov={}
for fn in pk.index:
    if 'horizonLiberator' not in fn or not fn.endswith('.patch'):continue
    d=sbjson.parse_sb(pk.read(fn).decode('utf-8-sig'))
    hit=[0]
    def w(o):
        if isinstance(o,list):
            for x in o:w(x)
        elif isinstance(o,dict):
            v=o.get('value')
            if isinstance(v,str) and '중갑.  ' in v:
                o['value']=v.replace('중갑.  ','중갑. ');hit[0]+=1
            for vv in o.values():
                if isinstance(vv,(list,dict)):w(vv)
    w(d)
    if hit[0]:ov[fn]=json.dumps(d,ensure_ascii=False,separators=(',',':')).encode('utf-8');print('FIX',fn[-55:],hit[0])
if ov and '--apply' in sys.argv:
    pak_writer.write_pak(TR+'.staged',TR,ov);del pk
    for i in range(60):
        try:os.replace(TR+'.staged',TR);print('replaced');break
        except PermissionError:time.sleep(5)
else:print('files:',len(ov))
