# Codex review fixes for lustling codex translations (QA pass).
# - Terminology unification: voe->보에, la-voe->라보에, cunt->년/보지 tone,
#   빌-C48i, 에블린 야사, 난교, 성기, 정액, Slaves-R-Us translit.
# - Mistranslations: la-voe subject, fairer sex, 'full protectorate' -> 수호자.
# - Restores leading newline/indent blocks on title pages (EN uses them for
#   vertical centering; KO dropped them so titles render top-left).
import sys, io, json, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, 'tools')
from pak import Pak
from pak_writer import write_pak

PROV = r"E:\My Games\steamapps\common\Starbound\mods\997_sxb_Lustlings_1.2.9_clean.pak"
tmp = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak.tmp_write"
TR = tmp if os.path.exists(tmp) else \
     r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
APPLY = '--apply' in sys.argv

# substring fixes per (patchfile, page): [(old,new)]
SUB = {
('/codex/lustling/lustlingadd.codex.patch', 1): [
    ('여러분(voe)이 정의를 구할 수 있는 곳', '라보에가 정의를 구할 수 있는 곳'),
    ('그들(voe)이 당신을 물건처럼', '보에가 당신을 물건처럼'),
    ('그들(voe)의 두 배 일을', '보에의 두 배 일을'),
],
('/codex/lustling/lustlingadd.codex.patch', 2): [
    ('보와 수컷 소유 사업체가', '보에와 남성이 소유한 사업체가'),
    ('이 보에들이', '이 보에들이'),
],
('/codex/lustling/lustlingadd.codex.patch', 4): [
    ('Tiuny를 찾아갑니다', '티우니를 찾아갑니다'),
    ('Tiuny의 팔은', '티우니의 팔은'),
],
('/codex/lustling/lustlingadd.codex.patch', 5): [
    ('걔들이 voe였으니까', '걔들이 보에였으니까'),
],
('/codex/lustling/lustlingadd.codex.patch', 7): [
    ('훌륭한 창녀가 될 거라고', '훌륭한 년이 될 거라고'),
    ('누구의 창녀도 되지', '누구의 년도 되지'),
    ('저 보에들보다', '저 보에들보다'),
],
('/codex/lustling/lustlingadd.codex.patch', 10): [
    ('노예 걸레-알-어스에 오면', '슬레이브즈-알-어스에 오면'),
],
('/codex/lustling/lustlingadd.codex.patch', 11): [
    ('나아이 말로는', '나이 말로는'),
    ('바보야 나 이제 글을 읽지 못해', '바보 같지, 이제 글도 못 읽어'),
],
('/codex/lustling/lustlingdiary.codex.patch', 1): [
    ('내 오르기 그룹에서', '내 난교 모임에서'),
    ('정상까지 몸으로 올라가지 않겠다는 약속을 지키려다가', '꼭대기까지 박아서 올라가지 않겠다는 약속을 했는데도'),
    ('오럴 서비스 하나 없이', '공짜 구강성교 한 번 없이'),
],
('/codex/lustling/lustlingdiary.codex.patch', 3): [
    ('정식 보호국이 돼', '정식 수호자가 돼'),
    ('프로-텍-토레이트야', '수-호-자야'),
],
('/codex/lustling/lustlinghistory1.codex.patch', 1): [
    ('타락한 방탕함의 종족으로 되살아난', '타락과 방탕에 빠진 종족으로 되살아난'),
],
('/codex/lustling/lustlinghistory1.codex.patch', 3): [
    ('내가 읽는 즐거움을 누렸던 가장 독특한 사람들', '읽는 즐거움을 준 가장 독특한 사람들'),
],
('/codex/lustling/lustlinghistory2.codex.patch', 4): [
    ('Bill-C48i라 불리는', '빌-C48i라 불리는'),
],
('/codex/lustling/lustlinghistory3.codex.patch', 2): [
    ('이블린 야사 박사', '에블린 야사 박사'),
],
('/codex/lustling/lustlinghistory3.codex.patch', 3): [
    ('Bill-C48i는', '빌-C48i는'),
    ('라보에족의 출산율', '라보에의 출산율'),
    ('모든 라보에족에게', '모든 라보에에게'),
    ('라보에족이', '라보에가'),
],
('/codex/lustling/lustlinghistory4.codex.patch', 1): [
    ('자신들의 더 나은 성(性)을 완전히 통제하게 되고', '자기들의 여성들을 완전히 장악하게 되고'),
    ('순종적인 성 노예로', '순종적인 성 노예로'),
],
('/codex/lustling/lustlingsxeno.codex.patch', 3): [
    ('생식기를 완전히 움켜쥔', '성기를 완전히 움켜쥔'),
    ('러스틀링의 생식기를 만지는', '러스틀링의 성기를 만지는'),
    ('질에 손가락 하나를 넣고', '질에 손가락 하나를 넣고'),
],
('/codex/lustling/lustlingsxeno.codex.patch', 2): [
    ('러스틀링의 성기를 애무하거나', '러스틀링의 성기를 애무하거나'),
],
('/codex/lustling/lustlingsxeno.codex.patch', 8): [
    ('기억하세요', '기억하라'),
    ('기분 나빠하지 않습니다', '기분 나빠하지 않는다'),
    ('허락해 주세요', '허락해 주라'),
],
('/codex/lustling/lustlingsxeno.codex.patch', 10): [
    ('절대 먹지 마세요', '절대 먹지 마라'),
    ('있을 것입니다', '있을 것이다'),
],
('/codex/lustling/lustlingsxeno.codex.patch', 21): [
    ('러스틀링 역사 제1권~제6권', '러스틀링 역사 I~VI'),
],
('/codex/lustling/lustlingView.codex.patch', 3): [
    ('상당한 양의 사정액을', '상당한 양의 정액을'),
],
('/codex/lustling/lustlingView.codex.patch', 6): [
    ('상당한 양의 사정액이', '상당한 양의 정액이'),
],
('/codex/lustling/lustlingView.codex.patch', 7): [
    ('자신의 사정액이었다는', '자신의 정액이었다는'),
],
('/codex/lustling/lustlingsorigins.codex.patch', 1): [
    ('은하에서 주로 성적 용도로 활용되는 기존 종족 중 하나인', '은하에서 정평이 나 있으며 주로 성적 용도로 쓰이는 종족 중 하나인'),
],
# inspect-line wording fixes (applied earlier via _lustling_inspect.py)
('/objects/novakid/saloonpiano/saloonpiano.object.patch', -1): [
    ('좋은 피아니는 정말 좋아', '좋은 피아노는 정말 좋아'),
],
('/objects/hylotl/quillandink/quillandink.object.patch', -1): [
    ('내 섹스 일지에 써야지', '내 섹스 기록에 써야지'),
],
}

# full-page overrides (restore EN leading whitespace block + corrected KO text)
PAGE = {
('/codex/lustling/lustlinghistory5.codex.patch', 0): '러스틀링 재정착',
('/codex/lustling/lustlingdiary.codex.patch', 0): '섹스 없이 지낸 지 3일째',
('/codex/lustling/lustlingdiary.codex.patch', 2):
    '섹스 없이 지낸 지 1820일째\n(자위는 예외임, 난 신이 아니니까)',
('/codex/lustling/lustlinghistory1.codex.patch', 0): '라타시아의 황금 정원',
('/codex/lustling/lustlinghistory2.codex.patch', 0): '라타시아의 몰락.',
('/codex/lustling/lustlinghistory3.codex.patch', 0): '악마와의 거래',
('/codex/lustling/lustlinghistory4.codex.patch', 0): '러스틀링의 여명',
('/codex/lustling/lustlinghistory6.codex.patch', 0): '오늘날의 러스틀링',
('/codex/lustling/lustlingsorigins.codex.patch', 0): '러스틀링 입문',
('/codex/lustling/lustlingsxeno.codex.patch', 0):
    '러스틀링 예절 \n                      제1장\n            인사와 작별',
('/codex/lustling/lustlingsxeno.codex.patch', 6):
    '러스틀링 예절 \n                     제2장\n                 체액과 당신',
('/codex/lustling/lustlingsxeno.codex.patch', 11):
    '러스틀링 예절 \n                     제3장\n                 캐주얼 섹스',
('/codex/lustling/lustlingsxeno.codex.patch', 15):
    '러스틀링 예절 \n                     제4장\n                 여왕님을 공경하라',
}

def opsof(x, out):
    if isinstance(x, dict):
        if 'op' in x: out.append(x)
        else:
            for v in x.values(): opsof(v, out)
    elif isinstance(x, list):
        for v in x: opsof(v, out)

prov = Pak(PROV)
pk = Pak(TR)
def jx(b):
    s = b.decode('utf-8')
    try: return json.loads(s)
    except Exception:
        return json.loads(re.sub(r'[\x00-\x1f]', ' ', s))

overrides = {}
files = {k for k, _ in SUB} | {k for k, _ in PAGE}
for fn in sorted(files):
    if fn not in pk.index:
        print('MISSING PATCH', fn); continue
    doc = json.loads(pk.read(fn).decode('utf-8'))
    ops = []; opsof(doc, ops)
    en_src = None
    src = fn[:-6]  # provider asset path
    if src in prov.index:
        en_src = jx(prov.read(src))
    dirty = False
    for o in ops:
        if o.get('op') != 'replace': continue
        m = re.match(r'^/contentPages/(\d+)$', str(o.get('path', '')))
        pg = int(m.group(1)) if m else -1
        v = o.get('value')
        if not isinstance(v, str): continue
        nv = v
        for key2 in ((fn, pg), (fn, -1)):
            report = key2[1] != -1  # report misses only for page-targeted fixes
            for old, new in SUB.get(key2, []):
                if old in nv:
                    nv = nv.replace(old, new)
                elif report and new not in nv:
                    print('SUB MISS', fn, pg, old[:40])
        key = (fn, pg)
        if key in PAGE:
            lead = ''
            if en_src is not None:
                en = en_src.get('contentPages', en_src.get('content', []))
                if isinstance(en, list) and pg < len(en):
                    env = en[pg]
                    lead = env[:len(env) - len(env.lstrip())].replace('\r\n', '\n')
            nv = lead + PAGE[key]
        if nv != v:
            o['value'] = nv
            dirty = True
            print('fix', fn.split('/')[-1], pg)
    if dirty:
        overrides[fn] = json.dumps(doc, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

print('overrides:', len(overrides))
if APPLY and overrides:
    write_pak(TR, TR, overrides)
    print('applied')
