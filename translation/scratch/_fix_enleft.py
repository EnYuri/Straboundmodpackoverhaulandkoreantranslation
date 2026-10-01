import sys,io,os,json,time
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
sys.path.insert(0,r'E:/My Games/steamapps/common/Starbound');sys.path.insert(0,'tools')
import pak,sbjson,pak_writer
TR=r'E:/My Games/steamapps/common/Starbound/mods/zz_translation_female.pak'
pk=pak.Pak(TR)
FIX=[
 ('fu_craftinfo',"'A bug! Report it!'".strip("'"),'버그입니다! 신고해주세요!'),
 ('fu_craftinfo','Oops. Buggy recipe for this item in this crafting station...','이 제작대의 이 아이템 제작법에 버그가 있습니다...'),
 ('akkimariscavenging','insert item','아이템을 넣으세요'),
 ('SkillMenu','DisplayMessage|Reloaded Music','DisplayMessage|음악 다시 불러옴'),
 ('craftingmedical','^#b9b5b2;Health and well-being','^#b9b5b2;건강과 안녕'),
 ('craftingmedical','^orange;Health Center^reset;','^orange;보건 센터^reset;'),
 ('woodencookingtable','^#b9b5b2;Delicious food.','^#b9b5b2;맛있는 음식.'),
 ('woodencookingtable','^orange;Kitchen Counter^reset;','^orange;주방 조리대^reset;'),
 ('woodencookingtable','^#b9b5b2;A much nicer kitchen.','^#b9b5b2;훨씬 좋은 주방.'),
 ('woodencookingtable',"^orange;Chef's Kitchen^reset;",'^orange;셰프의 주방^reset;'),
]
def walk(o,fn,hits):
    if isinstance(o,list):
        for x in o:walk(x,fn,hits)
    elif isinstance(o,dict):
        if o.get('op') in ('replace','add') and isinstance(o.get('value'),str):
            for pat,old,new in FIX:
                if pat in fn and o['value']==old:
                    o['value']=new;hits.append((fn,o.get('path','')))
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
        for h in hits:print('FIX',h[0][-52:],h[1][-50:])
print('files:',len(ov))
if ov and '--apply' in sys.argv:
    pak_writer.write_pak(TR+'.staged',TR,ov);del pk
    for i in range(60):
        try:os.replace(TR+'.staged',TR);print('replaced');break
        except PermissionError:time.sleep(5)
