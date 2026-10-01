import sys,io,os,json,time,pickle,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
sys.path.insert(0,r'E:/My Games/steamapps/common/Starbound')
sys.path.insert(0,'tools')
import pak,sbjson,pak_writer
TR=r'E:/My Games/steamapps/common/Starbound/mods/zz_translation_female.pak'
pk=pak.Pak(TR)

# target replace values per (asset, path); special handling for kevin/maxhealthboost
QUIETUS='성간법 위반을 피하는 독특한 풍미의 생체 무기.\n^cyan;대상의 치유 30% 감소^reset;. (10초)'
PROT={
'/items/armors/protectorate/protectoratearmor/protectoratearmor.chest.patch':
'모두의 안전을 보장하기 위한 실험적인 파워 아머다.\n^orange;세트 보너스^reset;:\n^yellow;^reset; 파워 대시 기술. 넉백 부분 저항;\n^yellow;^reset; 프로텍토레이트 병기: 피해량 x^green;1.3^reset;\n^yellow;^reset; ^cyan;면역^reset;: 치명적 방사능, 치명적 열기/냉기, 독, 산소, 가스',
'/items/armors/protectorate/protectoratearmor/protectoratearmor.head.patch':
'고귀한 대의의 얼굴이다.\n^cyan;헤드램프^reset;\n^orange;세트 보너스^reset;:\n^yellow;^reset; 프로텍터 스피어 기술;\n^yellow;^reset; 프로텍토레이트 병기: 피해량 x^green;1.3^reset;\n^yellow;^reset; ^cyan;면역^reset;: 치명적 방사능, 치명적 열기/냉기, 독, 산소, 가스',
'/items/armors/protectorate/protectoratearmor/protectoratearmor.legs.patch':
'이 부츠는 더 밝은 미래를 향해 나아간다.\n^orange;세트 보너스^reset;:\n^yellow;^reset; 로켓 추진기. 낙하 피해 면역;\n^yellow;^reset; 프로텍토레이트 병기: 피해량 x^green;1.3^reset;\n^yellow;^reset; ^cyan;면역^reset;: 치명적 방사능, 치명적 열기/냉기, 독, 산소, 가스'}
MM={
'/upgrades/power1/description':'물질 분해율 200%로 증가',
'/upgrades/power2/description':'물질 분해율 300%로 증가',
'/upgrades/power3/description':'물질 분해율 400%로 증가',
'/upgrades/size1/description':'채광 범위를 3x3 타일로 증가',
'/upgrades/size2/description':'채광 범위를 4x4 타일로 증가',
'/upgrades/size3/description':'채광 범위를 5x5 타일로 증가'}
ELDER='/items/active/weapons/melee/spear/elderspear.activeitem.patch'
QUIET=[a for a in ['/items/active/weapons/ranged/unique/quietusassaultrifle.activeitem.patch',
'/items/active/weapons/ranged/unique/quietusrocketlauncher.activeitem.patch',
'/items/active/weapons/ranged/unique/quietusshotgun.activeitem.patch']]
BOOST=['/stats/effects/maxhealthboost/maxhealthboost%d.statuseffect.patch'%n for n in (3,4,6,70,80,90)]
KEVIN='/codex/documents/scienceoutpost_kevin.codex.patch'

def ops_at(d,path,op):
    out=[]
    def rec(o):
        if isinstance(o,list):
            for x in o:rec(x)
        elif isinstance(o,dict):
            if o.get('op')==op and o.get('path')==path:out.append(o)
            else:
                for v in o.values():
                    if isinstance(v,(list,dict)):rec(v)
    rec(d);return out

ov={}
def load(fn):
    return sbjson.parse_sb(pk.read(fn).decode('utf-8-sig'))

# 1) kevin dates
d=load(KEVIN)
for path,first_only in [('/contentPages/70',True),('/longContentPages/9',True)]:
    for r in ops_at(d,path,'replace'):
        v=r.get('value','')
        if isinstance(v,str) and '5월 15일' in v:
            r['value']=v.replace('5월 15일','5월 2일',1)
ov[KEVIN]=d

# 2) mmupgrade
fn='/interface/scripted/mmupgrade/mmupgradegui.original.config.patch'
d=load(fn)
for p,nv in MM.items():
    for r in ops_at(d,p,'replace'):r['value']=nv
ov[fn]=d

# 3) elderspear
d=load(ELDER)
for r in ops_at(d,'/description','replace'):
    v=r['value']
    if not v.startswith('^#a5ff00;'):r['value']='^#a5ff00;'+v
ov[ELDER]=d

# 4) quietus
for fn in QUIET:
    d=load(fn)
    for r in ops_at(d,'/description','replace'):r['value']=QUIETUS
    ov[fn]=d

# 5) protectoratearmor
for fn,nv in PROT.items():
    d=load(fn)
    for r in ops_at(d,'/description','replace'):r['value']=nv
    ov[fn]=d

# 6) maxhealthboost: drop stray #ERROR! replace groups
for fn in BOOST:
    d=load(fn)
    def clean(o):
        if isinstance(o,list):
            o[:]=[x for x in o if not (isinstance(x,dict) and x.get('op')=='replace' and x.get('value')=='#ERROR!')]
            for x in o:clean(x)
            # drop emptied groups
            o[:]=[x for x in o if x!=[]]
    if isinstance(d,list):
        d[:]=[g for g in d if not (isinstance(g,list) and all(isinstance(x,dict) and x.get('op')=='replace' and x.get('value')=='#ERROR!' for x in g))]
        for g in d:clean(g)
    ov[fn]=d

for fn,d in ov.items():
    ov[fn]=json.dumps(d,ensure_ascii=False,separators=(',',':')).encode('utf-8')
print('files:',len(ov))
pak_writer.write_pak(TR+'.staged',TR,ov)
del pk
for i in range(60):
    try:os.replace(TR+'.staged',TR);print('replaced');break
    except PermissionError:time.sleep(5)
