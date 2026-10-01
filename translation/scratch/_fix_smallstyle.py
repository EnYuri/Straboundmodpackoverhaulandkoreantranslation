import sys,io,os,json,time
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
sys.path.insert(0,r'E:/My Games/steamapps/common/Starbound');sys.path.insert(0,'tools')
import pak,sbjson,pak_writer
TR=r'E:/My Games/steamapps/common/Starbound/mods/zz_translation_female.pak'
pk=pak.Pak(TR)
# (asset-substring, path-substring, old-substr, new-substr)
FIX=[
 ('ffguide3','/longContentPages/0','수도 있습니다!.','수도 있습니다.'),
 ('networkguide','/contentPages/7','묶음를','묶음을'),
 ('vierahistory2','/contentPages/0','숲를 안내자로','숲을 안내자로'),
 ('vieralore23','/contentPages/0','숲가 태어났다','숲이 태어났다'),
 ('vieralore33','/contentPages/0','숲와 가장','숲과 가장'),
 ('pf_poisonprotection','/description','쓰자.^reset;.','쓰자.^reset;'),
 ('bo_multi_caliber','/description','^white;^white;.\n\n','^white;^white;\n\n'),
 ('_FUversioning','/welcome','경우 !업데이트 버튼','경우 "!업데이트" 버튼'),
 ('outfitfitter_saturn','/description','\\ue012\ue012','\ue012'),
 ('fu_woodensifter','/description','^cyan;^orange;2W^cyan; 전력 필요.^reset;','^cyan;전력 ^orange;2W^cyan; 필요.^reset;'),
]
def walk(o,fn,hits):
    if isinstance(o,list):
        for x in o:walk(x,fn,hits)
    elif isinstance(o,dict):
        v=o.get('value')
        if isinstance(v,str) and o.get('op') in('replace','add','test'):
            for pat,ptr,old,new in FIX:
                if pat in fn and ptr in o.get('path','') and old in v:
                    o['value']=v.replace(old,new);hits.append((fn,o['path']))
        for vv in o.values():
            if isinstance(vv,(list,dict)):walk(vv,fn,hits)
ov={}
for fn in pk.index:
    if not fn.endswith('.patch'):continue
    if not any(f[0] in fn for f in FIX):continue
    try:d=sbjson.parse_sb(pk.read(fn).decode('utf-8-sig'))
    except:continue
    hits=[];walk(d,fn,hits)
    if hits:
        ov[fn]=json.dumps(d,ensure_ascii=False,separators=(',',':')).encode('utf-8')
        for h in hits:print('FIX',h[0][-50:],h[1][-40:])
print('files:',len(ov))
if ov and '--apply' in sys.argv:
    pak_writer.write_pak(TR+'.staged',TR,ov);del pk
    for i in range(60):
        try:os.replace(TR+'.staged',TR);print('replaced');break
        except PermissionError:time.sleep(5)
