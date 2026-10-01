import sys,io,os,json,time
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
sys.path.insert(0,r'E:/My Games/steamapps/common/Starbound');sys.path.insert(0,'tools')
import pak,sbjson,pak_writer
TR=r'E:/My Games/steamapps/common/Starbound/mods/zz_translation_female.pak'
pk=pak.Pak(TR)
FIX=[
 # bare colorname -> add caret
 ('precursorcodex1',' red;<알 수 없음>',' ^red;<알 수 없음>'),
 ('gic_altcharge_demo','green;[ALT-FIRE]','^green;[ALT-FIRE]'),
 ('plebiancap',' orange;플레비안 모자^reset;을',' ^orange;플레비안 모자^reset;를'),
 ('shoggoth_wagner',' orange;델타 프레야',' ^orange;델타 프레야'),
 ('10industrialcentrifuge',' orange;산업용 원심분리기^reset; 를',' ^orange;산업용 원심분리기^reset;를'),
 ('10industrialcentrifuge','모래^reset; 를','모래^reset;를'),
 ('1beestation',' orange;양봉장 제작소^reset; 를',' ^orange;양봉장 제작소^reset;를'),
 ('2apiary','orange;양봉장^reset; 은','^orange;양봉장^reset;은'),
 ('9alveary',' orange;대형 양봉장^reset; 을',' ^orange;대형 양봉장^reset;을'),
 ('neb-damagetypekills','orange;안녕, 난 밥이야.','^orange;안녕, 난 밥이야.'),
 # ^reset without semicolon inside text
 ('1boozekit','^reset; 를','^reset;를'),('1boozekit','^reset에','^reset;에'),
 ('create_protocite','range;프로토사이트 주괴^reset; 를','^orange;프로토사이트 주괴^reset;를'),
 ('create_protocite','^reset에','^reset;에'),
 ('fu_t10_','^reset의','^reset;의'),
 # ^#hex without semicolon
 ('esc_armor_coalition_vdv','^#CCD8B6+무기','^#CCD8B6;+무기'),
 ('esc_armor_comm_commando','^#CCD8B6+무기','^#CCD8B6;+무기'),
 ('esc_armor_commonwealth_alt1','^#CCD8B6+무기','^#CCD8B6;+무기'),
 ('esc_armor_commonwealth','^#CCD8B6+무기','^#CCD8B6;+무기'),
 ('esc_armor_uiu','^#CCD8B6+','^#CCD8B6;+'),
 ('gicexp_armor_ntsec','^#CCD8B6+무기','^#CCD8B6;+무기'),
 # trailing ^reset / untranslated
 ('gic_plantfibresalad','유형: 식물^reset','유형: 식물^reset;'),
 ('gic_sawdustbread','유형: Grain^reset','유형: 곡물^reset;'),
 # garbled mfgstation tail
 ('mfgstation','^orange;140J^cyan이 필요합니다. 공예 당 힘의.^reset;','제작당 ^orange;140J^cyan;의 전력이 필요합니다.^reset;'),
]
def walk(o,fn,hits):
    if isinstance(o,list):
        for x in o:walk(x,fn,hits)
    elif isinstance(o,dict):
        v=o.get('value')
        if isinstance(v,str):
            for pat,old,new in FIX:
                if pat in fn and old in v:
                    o['value']=v.replace(old,new);hits.append((fn,o.get('path','')))
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
        for h in hits:print('FIX',h[0][-55:],h[1][-45:])
print('files:',len(ov))
if ov and '--apply' in sys.argv:
    pak_writer.write_pak(TR+'.staged',TR,ov);del pk
    for i in range(60):
        try:os.replace(TR+'.staged',TR);print('replaced');break
        except PermissionError:time.sleep(5)
