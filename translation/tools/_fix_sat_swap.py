# Repair name/description swap corruption in Saturnians patches.
# Root cause: *_ko_* row order vs uniq id order flipped on (desc,name) pairs,
# so name text landed in /description and description text in /shortdescription.
# Also restores the ^yellow;<antennae>^white; glyph prefix lost by the
# sat_names apply (U+0482 is outside the PUA range the prefix regex matched).
import sys, io, json, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
APPLY = '--apply' in sys.argv
pk = Pak(TR)

GLITCH = '많은 새터니안들이 글리치 양식 대장법을 받아들이기 시작했다. 마을 경비대가 글리치 갑옷을 아주 좋아한다.'
DECO = '새터니안들도 글리치 양식 대장법을 받아들이기 시작했지만, 그들의 갑옷은 장식용에 가장 적합하다.'
VOID = '이 투구에는 공허 마법이 걸려 있다. 착용자의 눈이 위협적으로 빛난다.'
FACE = '이 투구는 얼굴을 가리고 눈을 글리치처럼 빛나게 한다. 사실상 그게 전부다.'
WIZ = '글리치 마법사 투구를 바탕으로 한 철 투구. 글리치 마법사한테 투구가 왜 필요한데?'
REC = '멋진 투구의 새터니안 재현품이지만, 장식용일 뿐이다.'
CONTACT = '글리치와의 최근 접촉으로 일부 새터니안들이 그들의 패션을 받아들이게 됐다.'
WOVEN = '비단과 은도금 실로 짠 로브. '

# patch filename -> {field: correct value}
FIX = {
 'satglitchtier1.head.patch': {'description': GLITCH, 'shortdescription': '새터니안 하급 기사의 투구'},
 'satglitchtier2.head.patch': {'description': GLITCH, 'shortdescription': '새터니안 병사의 투구'},
 'satglitchtier3.head.patch': {'description': GLITCH, 'shortdescription': '새터니안 기사의 투구'},
 'satglitchtier3B.head.patch': {'description': VOID, 'shortdescription': '새터니안 기사의 투구 B'},
 'satglitchtier4.head.patch': {'description': DECO, 'shortdescription': '새터니안 흑기사의 투구'},
 'satglitchtier4B.head.patch': {'description': FACE, 'shortdescription': '새터니안 흑기사의 투구 B'},
 'satglitchtier5accelerator.head.patch': {'description': DECO, 'shortdescription': '새터니안 성전사의 투구'},
 'satglitchtier5manipulator.head.patch': {'description': WIZ, 'shortdescription': '새터니안 창기사의 투구'},
 'satglitchtier5manipulatorB.head.patch': {'description': REC, 'shortdescription': '새터니안 창기사의 투구'},
 'satglitchtier5separator.head.patch': {'description': REC, 'shortdescription': '새터니안 성기사의 투구'},
 'satglitchtier6accelerator.head.patch': {'description': REC, 'shortdescription': '새터니안 군단병의 투구'},
 'satglitchtier6acceleratorB.head.patch': {'description': REC, 'shortdescription': '새터니안 군단병의 투구 B'},
 'satglitchtier6manipulator.head.patch': {'description': REC, 'shortdescription': '새터니안 기사단원의 투구'},
 'satglitchtier6separator.head.patch': {'description': REC, 'shortdescription': '새터니안 파멸 군주의 투구'},
 'saturnhylotltier6separator.head.patch': {'shortdescription': '^cyan;^white;약광층 투구'},
 'saturnlunairobes2.head.patch': {'description': '착용자의 얼굴을 흰색으로 강조하는 단순한 후드.', 'shortdescription': '느슨한 후드'},
 'saturnlunairobes2.legs.patch': {'description': '악티아스의 정령 마법사들은 달빛으로 마법에 힘을 불어넣는다.', 'shortdescription': '액티안 치마'},
 'saturnmerchant.chest.patch': {'description': CONTACT, 'shortdescription': '새터니안 글리치 셔츠'},
 'saturnmerchant.legs.patch': {'description': CONTACT, 'shortdescription': '새터니안 글리치 바지'},
 'saturnnoble.legs.patch': {'description': CONTACT, 'shortdescription': '새터니안 글리치 치마'},
 'ornaterobes.chest.patch': {'description': WOVEN, 'shortdescription': '정교한 로브'},
 'ornaterobes.legs.patch': {'description': WOVEN, 'shortdescription': '정교한 치마'},
 'saturnDemon.head.patch': {'description': '사나워 보이는 뿔 달린 후드.', 'shortdescription': '악마 뿔 후드'},
}

GLYPH_ASSETS = [
 'saturnNovMA.head','saturnStarhatAnt.head','saturnAntSorcererRobes.head',
 'saturnAntAlchemistset.head','saturnAntBuckledHat.head','saturnAntShadowhat.head',
 'saturnAntStarHat2.head','saturnAntTopHat.head','saturnAntTopHat2.head',
 'saturnAntTopHat3.head','saturnAntSunHat.head','saturnAntWideHat.head',
 'saturnAntWideShadyHat.head','saturnAntWidestHat.head','saturnAntchef.head',
 'saturnAntHeavyFluffhood.head','saturnAntHeavyhood.head','saturnAntHeavyScarfedHood.head',
 'saturnAntArtWizard.head','saturnAnttier4notevil.head','saturnAntornaterobes.head',
 'saturnGlaDStarhatAnt.head','saturnGlaStarhatAnt.head',
]
GLYPH = '҂'

def walk_ops(x, out):
    if isinstance(x, dict):
        if 'op' in x: out.append(x)
        else:
            for v in x.values(): walk_ops(v, out)
    elif isinstance(x, list):
        for v in x: walk_ops(v, out)

overrides = {}
changed = 0
fix_base = {k: v for k, v in FIX.items()}
glyph_names = set(GLYPH_ASSETS)
for fn in pk.index:
    if not fn.endswith('.patch'): continue
    base = fn.rsplit('/', 1)[-1]
    stem = base[:-len('.patch')]
    doc = None
    if base in fix_base:
        doc = json.loads(pk.read(fn).decode('utf-8'))
        ops = []
        walk_ops(doc, ops)
        for o in ops:
            if o.get('op') != 'replace': continue
            leaf = str(o.get('path', '')).rsplit('/', 1)[-1]
            if leaf in fix_base[base] and o.get('value') != fix_base[base][leaf]:
                print('FIX %s %s: %s -> %s' % (base, leaf, str(o.get('value'))[:50], fix_base[base][leaf][:50]))
                o['value'] = fix_base[base][leaf]
                changed += 1
    if stem in glyph_names:
        if doc is None:
            doc = json.loads(pk.read(fn).decode('utf-8'))
            ops = []
            walk_ops(doc, ops)
        for o in ops:
            if o.get('op') != 'replace': continue
            v = o.get('value')
            if isinstance(v, str) and v.startswith('^yellow;') and GLYPH not in v:
                nv = v.replace('^yellow;', '^yellow;' + GLYPH + '^white;', 1)
                print('GLYPH %s: %s -> %s' % (base, v[:45], nv[:45]))
                o['value'] = nv
                changed += 1
    if doc is not None:
        overrides[fn] = json.dumps(doc, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

print('ops changed:', changed, '| patch files:', len(overrides))
if APPLY and overrides:
    sys.path.insert(0, 'tools')
    from pak_writer import write_pak
    write_pak(TR, TR, overrides)
    print('applied')
