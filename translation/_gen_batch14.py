"""Generator for fix_glossary_batch14.py — embeds all replacement pairs."""
import json

scoped = json.load(open('_batch14_scoped.json', encoding='utf-8'))

manual = [
    # ---- global grammar/typo/substring fixes ----
    ('미니크녹가 ', '미니크녹이 '),
    ('건만증', '건망증'),
    ('날 무겁다 마, 그냥 사색 중.', '날 무겁다 여기지 마, 그냥 사색 중.'),
    ('궁금한가?', '궁금해?'),
    ('우...움직이지 마', '움...움직이지 마'),
    ('맙소사 수익이라니...', '달콤한 수익이여...'),
    ('자유야. 다음은?', '자유. 다음은?'),
    ('무장 해제! 도와줘!', '난 비무장이야! 도와줘!'),
    ('여객기 조종은', '여객선 조종은'),
    ('이상 곳. 무서웠어. 아직도.', '이상한 곳. 무서웠어. 아직도.'),
    # ---- aegi register (allianceoutpost, casual villager dominant) ----
    ('대사관 접수대의 여성은 사실 내게 꽤 도움이 되었다.', '대사관 접수대의 여성은 사실 내게 꽤 도움이 됐어.'),
    ('이곳 정원은 정말 아름답다.', '이곳 정원은 정말 아름다워.'),
    ('오늘 대사관에는 무슨 일이시죠?', '오늘 대사관에는 무슨 일이야?'),
    ('여기 자주 오세요?', '여기 자주 와?'),
    ('크레온은 매력적인 도시입니다.', '크레온은 매력적인 도시야.'),
    ('멀리 떠다니는 호버카들을 보고 있으면 마음이 편안해져요.', '멀리 떠다니는 호버카들을 보고 있으면 마음이 편안해져.'),
    ('이곳 공원들은 믿기 어려울 만큼 평화롭다.', '이곳 공원들은 믿기 어려울 만큼 평화로워.'),
    # ---- USCMdisbanded 해라체 -> 해체 (ex-marine casual voice) ----
    ('보호국은 USCM을 인류 역사의 일탈적 각주로 여겼다. 이제는 그들도 역사가 되었다.', '보호국은 USCM을 인류 역사의 일탈적 각주로 여겼어. 이제는 그들도 역사가 됐어.'),
    ('USCM에서는 반란이 큰 문제였다. 그 모든 감옥들이 다 어디서 왔다고 생각해?', 'USCM에서는 반란이 큰 문제였어. 그 모든 감옥들이 다 어디서 왔다고 생각해?'),
    ('불복종은 USCM 내에서 용납되지 않았다. 그러면 형벌 식민지행 편도 티켓을 받게 되었다.', '불복종은 USCM 내에서 용납되지 않았어. 그러면 형벌 식민지행 편도 티켓을 받게 됐어.'),
    # ---- moogle register (kupo-casual dominant) ----
    ('제가 도와드릴 일이 있을까요, 쿠포?', '도와줄 일 있어, 쿠포?'),
    ('좋은 소식 가져오셨나요, 쿠포?', '좋은 소식 가져왔어, 쿠포?'),
    ('물건을 부수지 말아주세요, 쿠포!', '물건을 부수지 마, 쿠포!'),
    ('제 물건 소중히 다뤄주세요, 쿠포!', '내 물건 소중히 다뤄, 쿠포!'),
    ('제 물건을 가져가지 말아주세요, 쿠포.', '내 물건 가져가지 마, 쿠포.'),
    ('다른 사람 물건을 소중히 다뤄주세요, 쿠포!', '다른 사람 물건 소중히 다뤄, 쿠포!'),
    ('떠돌이 비에라를 본 지 정말 오래됐네요, 쿠포!', '떠돌이 비에라를 본 지 정말 오래됐네, 쿠포!'),
    # ---- ayylien register ----
    ('두려워하지 마세요, 저는 평화롭게 왔습니다.', '두려워하지 마, 난 평화롭게 왔어.'),
    ('살아있는 무시 표본 하나 얻을 수 있을까요? 아주 중요한 연구에 쓸 거예요.', '살아있는 무시 표본 하나 얻을 수 있을까? 아주 중요한 연구에 쓸 거야.'),
    ('이 정착지에는 접시 모양 물체가 더 필요하다. 더 안전해지게 말이다.', '이 정착지에는 접시 모양 물체가 더 필요해. 더 안전해지게 말이야.'),
    # ---- SaturnGuardMage register ----
    ('최대한 예의 바르게 행동해주세요.', '최대한 예의 바르게 행동해.'),
    ('당신은 우호적인가요?', '너 우호적이야?'),
    ('감당하기 벅차 보이는군요. 제가 당신을 보살펴 드릴까요?', '감당하기 벅차 보이네. 내가 보살펴 줄까?'),
    # ---- unboundvillagesecurity register (반말-guard dominant) ----
    ('그만 이동해주세요, 여기 볼일 없으시잖아요.', '그만 이동해, 여기 볼일 없잖아.'),
    ('지나가 주세요, 낯선 사람이 이미 충분히 돌아다니고 있어서요.', '지나가 줘, 낯선 사람이 이미 충분히 돌아다니고 있어서.'),
    ('우리는 외부인을 믿지 않으니, 가던 길 가세요.', '우리는 외부인을 믿지 않으니, 가던 길 가.'),
    # ---- saturnWaspmim register ----
    ('이 근처 풍경이 아름답네요!', '이 근처 풍경이 아름답네!'),
    ('아피아리안은 아직도 꽃의 행성을 찾고 있나요?', '아피아리안은 아직도 꽃의 행성을 찾고 있어?'),
    ('스트레스 많이 받았어요...', '스트레스 많이 받았어...'),
    ('그들이 도망쳤나요?', '그들이 도망쳤어?'),
    ('도망가고 있어요!', '도망가고 있어!'),
    # ---- devouttenant broken sentence ----
    ('자랑. 우리 주인 수백 년 전 떠났지만 왕국 서있어.', '자랑. 우리 주인들은 수백 년 전에 떠났지만 왕국은 아직 서 있어.'),
    # ---- samuraimerc ----
    ('명예 위해!', '명예를 위해!'),
    ('내 검 널 갈가리 자를 거야!', '내 검이 널 갈기갈기 자를 거야!'),
    ('무엇보다 충성을, 그게 죽어야 한다는 뜻이라도 두렵겠지!', '무엇보다 충성을, 유감이지만 그건 네가 죽어야 한다는 뜻이야!'),
    ('우리 주인님께서 침입자는 안 된다고 하셨습니다, 유감이지만요, 이해해주시리라 믿습니다.', '우리 주인님께서 침입자는 안 된다고 하셨어. 유감이지만 이해해주리라 믿어.'),
    # ---- lustia arcade hint ----
    ('한동안 문 닫았어요. 정말 아쉽네요.', '한동안 문 닫았어. 정말 아쉽네.'),
    ('사람들은 트레이딩 카드 중독을 사랑했다.', '사람들은 트레이딩 카드 중독에 빠져 있었어.'),
]

asset_scoped = {
    '/dialog/eldermerchant.config.patch': [
        ('이리 와!', "크' 프응글루이 크' 므게프나 우'이글!"),
        ('음, 아니당...', '을을 노그 야...'),
    ],
    '/dialog/sgD03MU/flee.config.patch': [
        ('이제 안전한가요?', '이제 안전해?'),
    ],
}

allp = manual + sorted(scoped.items())

header = '''"""Fourteenth fix batch (2026-09-28). Origin: manual review of the remaining
small /dialog/ assets (_review_dialog_small.txt, 2,659 pairs) plus corpus-wide
emotion-prefix consistency pass.

All pairs verified against pak_pairs.tsv before fixing. Highlights:

- 미니크녹가 -> 미니크녹이: consonant-final proper noun + wrong subject
  particle, 45 corpus-wide occurrences (dialog, npc, object, codex assets).
- Glitch emotion-prefix noun-form normalization (batch10 rule), EN-scoped:
  Cautious 조심/조심함/경계 -> 주의 (Careful/Wary 조심 kept),
  Alert 경계/경보 -> 경고 (Alarmed/Alerted/Wary 경계 kept),
  Observant 관찰적/관찰함/관측력 있음/관찰력 -> 관찰,
  Neutral 중립적/무덤덤함 -> 중립, Tired 피곤하다 -> 피곤,
  Traumatized 트라우마가 생겼다 -> 트라우마, Invigorated -> 활기 넘침,
  Doubtful 글쎄 -> 의심, Amicable 우호적 -> 우호, Threatening 위협적 -> 위협,
  Skeptical 회의적 -> 회의적임, Speculative 추측이지만 -> 추측,
  Envious 질투함 -> 질투, Content 내용 -> 만족 (viera FTL objects).
- Register slips normalized to each voice's dominant register:
  aegi villagers 7, USCM ex-marines 해라체 3, moogle kupo-casual 7,
  ayylien 3, SaturnGuardMage 3, unbound village guards 3,
  saturn wasp-mimics 5, lustia arcade 2, samuraimerc hylotl/hylotl 1.
- Mistranslations: sgD03 flee 무장 해제 -> 비무장 (unarmed != disarmed),
  gicexp 맙소사 수익이라니 -> 달콤한 수익이여 (Sweet profits exclamation,
  matching esc_intromission rendering), samuraimerc afraid->유감 (not 두렵),
  devouttenant converse/7 missing particles restored,
  eldermerchant R'lyeh utterances 이리 와!/음, 아니당... -> transliterations
  matching the asset's other gibberish lines (asset-scoped; identical
  strings elsewhere untouched).
- Typos: nakedvillager 건만증 -> 건망증, P1078_M03hostile stutter
  우...움직이지 마 -> 움...움직이지 마, prisoner fenerox 이상 곳 -> 이상한 곳,
  rainbowent 날 무겁다 마 -> 날 무겁다 여기지 마.
- Terms: shuttlepilot 여객기 -> 여객선 (Passenger Liner, matches
  여객선 프레임 item name), prisoner fenerox 자유야 -> 자유 (telegraphic).
- Deferred: saturnKytaguard /hail/saturn/saturn/2 EN 'I\\'m here to' is
  truncated in the source mod itself; KO 여긴 is faithful, left as-is.
  Neutral->자랑 prefix on 4 glitch-anvil objects kept (body is a deliberate
  lore rewrite, prefix fits it).
"""

import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\\My Games\\steamapps\\common\\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

BASE = Path(__file__).parent
SRC_PAK = STAR / "mods" / "female_translation.pak"
OUT_PAK = BASE / "female_translation.pak.NEW18"

REPLACEMENTS = [
'''

engine = ''']

# asset-scoped replacements: needles safe only inside these assets
ASSET_SCOPED = {
'''

with open('fix_glossary_batch14.py', 'w', encoding='utf-8') as out:
    out.write(header)
    for old, new in allp:
        out.write('    (%r,\n     %r),\n' % (old, new))
    out.write(engine)
    for a, prs in asset_scoped.items():
        out.write('    %r: [\n' % a)
        for old, new in prs:
            out.write('        (%r, %r),\n' % (old, new))
        out.write('    ],\n')
    out.write('''}

print("total replacement pairs:", len(REPLACEMENTS))


def _vlqr(buf, p):
    # MSB-first base-128 varint, matching pak.py rvu()
    v = 0
    while True:
        b = buf[p]
        p += 1
        v = (v << 7) | (b & 0x7F)
        if not (b & 0x80):
            return v, p


def vlq(v):
    # MSB-first base-128 varint, matching pak.py rvu() (no zigzag)
    stack = []
    while True:
        stack.append(v & 0x7F)
        v >>= 7
        if not v:
            break
    out = bytearray()
    for i, b in enumerate(reversed(stack)):
        out.append(b | 0x80 if i < len(stack) - 1 else b)
    return bytes(out)


def _key(buf, p):
    n, p = _vlqr(buf, p)
    return p + n


def _rjson_skip(buf, p):
    t = buf[p]
    p += 1
    if t == 1:
        return p
    if t == 2:
        return p + 8
    if t == 3:
        return p + 1
    if t == 4:
        _, p = _vlqr(buf, p)
        return p
    if t == 5:
        n, p = _vlqr(buf, p)
        return p + n
    if t == 6:
        n, p = _vlqr(buf, p)
        for _ in range(n):
            p = _rjson_skip(buf, p)
        return p
    if t == 7:
        n, p = _vlqr(buf, p)
        for _ in range(n):
            p = _key(buf, p)
            p = _rjson_skip(buf, p)
        return p
    raise ValueError("bad json type %d at %d" % (t, p))


def replace_in_value(v, pairs):
    if isinstance(v, str):
        changed = False
        for old, new in pairs:
            if old in v:
                v = v.replace(old, new)
                changed = True
        return v, changed
    if isinstance(v, list):
        out = []
        changed = False
        for x in v:
            x, c = replace_in_value(x, pairs)
            out.append(x)
            changed = changed or c
        return out, changed
    if isinstance(v, dict):
        out = {}
        changed = False
        for k, x in v.items():
            x, c = replace_in_value(x, pairs)
            out[k] = x
            changed = changed or c
        return out, changed
    return v, False


def main():
    d0 = SRC_PAK.read_bytes()
    off0 = struct.unpack(">Q", d0[8:16])[0]
    assert d0[off0:off0 + 5] == b"INDEX"
    p = off0 + 5
    nmeta, p = _vlqr(d0, p)
    for _ in range(nmeta):
        p = _key(d0, p)
        p = _rjson_skip(d0, p)
    meta_blob = d0[off0:p]

    src = Pak(str(SRC_PAK))
    files = {name: src.read(name) for name in src.index}
    print("base pak entries:", len(files))

    # needles must match the raw (JSON-escaped) bytes inside .patch files
    needles = [json.dumps(old, ensure_ascii=False)[1:-1].encode("utf-8")
               for old, _ in REPLACEMENTS]
    scoped_needles = {
        a: [json.dumps(o, ensure_ascii=False)[1:-1].encode("utf-8")
            for o, _ in prs]
        for a, prs in ASSET_SCOPED.items()
    }
    # verify each needle exists in the source before rewriting
    for old, needle in zip([r[0] for r in REPLACEMENTS], needles):
        if not any(needle in files[n] for n in files if n.endswith(".patch")):
            print("NEEDLE-MISS (source):", old[:80])
    for a, prs in ASSET_SCOPED.items():
        for i, (old, _) in enumerate(prs):
            if a in files and scoped_needles[a][i] not in files[a]:
                print("NEEDLE-MISS (scoped %s):" % a, old[:80])
    assets_changed = 0
    for name in sorted(files):
        if not name.endswith(".patch"):
            continue
        data = files[name]
        extra = ASSET_SCOPED.get(name, [])
        if not any(n in data for n in needles) and \\
                not any(n in data for n in scoped_needles.get(name, [])):
            continue
        try:
            doc = json.loads(data)
        except Exception:
            continue
        new_doc, changed = replace_in_value(doc, REPLACEMENTS)
        if extra:
            new_doc, changed2 = replace_in_value(new_doc, extra)
            changed = changed or changed2
        if changed:
            files[name] = json.dumps(new_doc, ensure_ascii=False).encode("utf-8")
            assets_changed += 1
            print("fixed", name)

    buf = bytearray(b"SBAsset6" + b"\\x00" * 8)
    index_entries = []
    for name in sorted(files):
        data = files[name]
        off = len(buf)
        buf += data
        index_entries.append((name.encode("utf-8"), off, len(data)))

    index_off = len(buf)
    buf += meta_blob
    buf += vlq(len(index_entries))
    for name, off, n in index_entries:
        buf += vlq(len(name)) + name + struct.pack(">QQ", off, n)
    buf[8:16] = struct.pack(">Q", index_off)

    OUT_PAK.write_bytes(bytes(buf))
    print("assets changed:", assets_changed)
    print("wrote", OUT_PAK, len(buf), "bytes,", len(index_entries), "entries")


if __name__ == "__main__":
    main()
''')

print('written, pairs:', len(allp))
