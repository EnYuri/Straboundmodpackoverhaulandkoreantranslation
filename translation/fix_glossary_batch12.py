"""Twelfth fix batch (2026-09-28). Origin: manual review of the radiomessages
asset group (alliancestory 6, arcana_bags 2, arcana_mission_desertstart 11,
arcana_mission_seekerIntro 18, arcana_radiomessage_* 26, atprk_planetpincomments
68, ffs_radiomessages 110, ffs_radiomessages_hc 19, gicexp_missions 174,
gico_messages 21, hellishdemon 32, lawHQmissions_M03 10, mwhaddon_mission_
mainStory 132, om_harpyIntro 18, pf_newtutorial 7, sb_tutorial 13,
thea-instances 20, viera 15, voideddungeon/exploration/tutorial 35).

All pairs verified against pak_pairs.tsv before fixing. Highlights:

- Aurea Seekers faction members -> 탐구자 (glossary fixed: Aurea Seekers =
  아우레아 탐구자). Branded item names (시커 권총/아틀라스) left matching their
  item defs; corpus-wide Seeker item-name decision deferred.
- Aurea Collective: 컬렉티브 -> 콜렉티브 (dominant 25:9). Lodestar Temple:
  로드스타 사원 -> 신전 (dominant 10:4).
- Glitch-style emotion tag normalization in atprk_planetpincomments and
  elsewhere, to corpus-dominant noun forms: 정통.->정보., 짜증남->짜증,
  곰곰이.->사색., 생각에 잠김.->사색., 향수에 잠김.->향수., 분개함.->분개.,
  당황함.->당혹., 수상하다.(prefix)->의심., 별 감흥 없음.->무관심.,
  불안하다.(prefix)->불안., 불길하네.->불길함., 어안이 벙벙하다.->어안벙벙.,
  통찰력 있긴.->통찰력., 혼란스럽다.(Confused tag)->혼란.
- ffs internal consistency: Wallace 월레스->월리스 (64:1), Chicha 치시아->치차,
  armored troops -> 중무장 병력, sector NN -> NN구역, armory 병기고->무기고,
  drop pod 드롭 포드->탈출 포드 (narrative form; gicexp item name kept).
- gicexp: Perimeter III 페리미터->경계선 (same site as 경계선 I), safe house
  아지트/안전가옥->안전 가옥, datavault spacing 데이터볼트, Resistance faction
  ->저항군 (file-internal), ship bridge 다리->함교, interceptor joke unified to
  요격기, security crew ->보안 요원, truncated "n-" stray latin removed.
- mwhaddon: Sally's Senpai -> 선배 (in-file dominant 27:10), Emerald's Glimpse
  ->에메랄드 글림프스 (42:1), Omniversal Arcane Covenant ->옴니버설 아케인
  코버넌트 (3:1), High Magus ->대마법사 (16:5), Supreinter ->슈프레인터,
  Breach Sphere 브리치 구체->브리치 스피어, catapult 투석기->캐터펄트,
  Seeker of Dust ->먼지 탐구자 (codex title form).
- Item-name anchors: Hazard Lab Table 위험 실험 탁자, Inventor's Table
  발명가의 작업대, Stone Hearth 돌 벽난로, Wooden Tool Table 나무 도구대,
  regulator 조절기, Woven Fabric 섬유 천, Violated Elite Drahl 유린당한 정예
  드랄, magicite refs in viera chain ->마기사이트 (matches Magicite Crystal
  Ore def). Global magicite unification (매지사이트/마기석/마법석) deferred -
  needs item-name decision.
- Tech -> 테크 for game-system usage (glossary context rule).
- Register unifications: alliancestory intro2 -> 존댓말 (speaker's other two
  messages), hellishdemon stragglers -> 반말, om_harpyIntro stragglers -> 반말.
"""

import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

BASE = Path(__file__).parent
SRC_PAK = STAR / "mods" / "female_translation.pak"
OUT_PAK = BASE / "female_translation.pak.NEW16"

REPLACEMENTS = [
    # ---- global naming / spelling unification ----
    ("컬렉티브", "콜렉티브"),
    ("로드스타 사원", "로드스타 신전"),
    ("선배님", "선배"),
    ("짜증남", "짜증"),
    ("곰곰이.", "사색."),
    ("정통.", "정보."),
    ("생각에 잠김.", "사색."),
    ("향수에 잠김.", "향수."),
    ("분개함.", "분개."),
    ("당황함.", "당혹."),

    # ---- atprk_planetpincomments ----
    ("분석적. X 구역에서", "분석적. 섹터 X에서"),
    ("혼란스럽다. 또 불모지라고?", "혼란. 또 불모지라고?"),
    ("불길하네. 이제 좀 알겠어.", "불길함. 이제 좀 알겠어."),
    ("불안하다. 영원한", "불안. 영원한"),
    ("불안하다. ^#949493;루나", "불안. ^#949493;루나"),
    ("어안이 벙벙하다. 잠깐", "어안벙벙. 잠깐"),
    ("수상하다. 이럴 리가 없어.", "의심. 이럴 리가 없어."),
    ("수상하다. 여기서 수상한 짓은", "의심. 여기서 수상한 짓은"),
    ("수상하다. 널 카페 텔레포터", "의심. 널 카페 텔레포터"),
    ("별 감흥 없음. 뭐 그래", "무관심. 뭐 그래"),
    ("별 감흥 없음. 글쎄", "무관심. 글쎄"),
    ("통찰력 있긴. 반면", "통찰력. 반면"),
    ("낚시는커녕 말이다", "낚시는 말할 것도 없다"),

    # ---- ffs_radiomessages ----
    ("월레스의 신분증", "월리스의 신분증"),
    ("치시아가 그것을 유족에게", "치차가 그것을 유족에게"),
    ("무장 부대를 투입하라", "중무장 병력을 투입하라"),
    ("장갑 부대가 도착했습니다", "중무장 병력이 도착했습니다"),
    ("무장 병력이 도착했다", "중무장 병력이 도착했다"),
    ("섹터 03 접근이 개방되었습니다", "03구역 접근이 개방되었습니다"),
    ("병기고 급습", "무기고 급습"),
    ("드롭 포드의 생존 시스템", "탈출 포드의 생존 시스템"),
    ("머리 앞쪽에 대형 미지의 유기체 신호를 감지했다",
     "전방에 대형 미지의 유기체 신호를 감지했다"),

    # ---- gicexp_missions ----
    ("즉시 페리미터 III에 보고해", "즉시 경계선 III에 보고해"),
    ("곧장 아지트를 쓸어라", "곧장 안전 가옥을 쓸어라"),
    ("안전가옥에 도달해야", "안전 가옥에 도달해야"),
    ("데이터 볼트", "데이터볼트"),
    ("레지스탕스가 '장치'를 안전하게 회수해", "저항군이 '장치'를 안전하게 회수해"),
    ("탈출선을 발진시켜 n-", "탈출선을 발진시켜-"),
    ("저들이 다리 근처에 있다", "저들이 함교 근처에 있다"),
    ("'''신호국'''", "''신호국''"),
    ("인터셉터라고?!", "요격기라고?!"),
    ("왜 인터셉터라고 부르는 거야", "왜 요격기라고 부르는 거야"),
    ("보안 승무원, 소탕 프로토콜을 실행하라", "보안 요원, 소탕 프로토콜을 실행하라"),
    ("보안팀, 수익을 지켜라", "보안 요원, 수익을 지켜라"),
    ("맙소사 수익이라니, 저게 뭐야?", "달콤한 수익이여, 저게 뭐야?"),

    # ---- alliancestory (register unified to the admiral's 존댓말) ----
    ("곧 얼라이언스의 다른 지도자들과 만나서, 이 비극에 대해 충분히 논의할게. "
     "네 다음 임무가 뭐가 될지도 논의할 거야.",
     "곧 얼라이언스의 다른 지도자들과 만나 이 비극에 대해 충분히 논의할 겁니다. "
     "다음 임무가 무엇이 될지도 논의하겠습니다."),

    # ---- hellishdemon (register unified to dominant 반말 + typo) ----
    ("너 같은 약골은 여길 자격이 없어", "너 같은 약골이 있을 곳이 아니야"),
    ("더 고통받아..더, 더엇!!", "더 고통받아.. 더, 더!!"),
    ("이곳의 대기가 당신을 미치게 만들고 있습니다.. 그런데도 계속 머무르시겠습니까?",
     "이곳의 대기가 널 미치게 만들고 있지.. 그런데도 계속 머무를 셈이야?"),
    ("당신이 여기 올 이유는 없습니다.", "네가 여기 올 이유는 없어."),
    ("이 불타는 지옥들이 네 가죽을 찢고 갈라댄다",
     "이 불타는 지옥들이 네 가죽을 찢어발기고 갈라낸다"),

    # ---- lawHQmissions_M03 ----
    ("어떤 잘난 척쟁이가 손대지 못하도록", "어떤 잘난 척하는 놈이 손대지 못하도록"),

    # ---- mwhaddon_mission_mainStory ----
    ("에메랄드의 섬광과 동일함", "에메랄드 글림프스와 동일함"),
    ("옴니버설 비전 서약", "옴니버설 아케인 코버넌트"),
    ("대마법사를 올려주었지", "대마법사 자리를 내려주었지"),
    ("하이 마구스 중 한 명이야", "대마법사 중 한 명이야"),
    ("수프린터 제국대학교", "슈프레인터 제국대학교"),
    ("브리치 구체^reset; 형태로", "브리치 스피어^reset; 형태로"),
    ("투석기를 발사", "캐터펄트를 발사"),
    ("투석기는 ^orange;커서가", "캐터펄트는 ^orange;커서가"),
    ("투석을 취소할 수", "캐터펄트 발사를 취소할 수"),
    ("우리는 방금 폭력을 관-", "방금 폭력적인 반응을 관측했-"),
    ("자리에서 참을성 있게 기다려라", "제자리에서 차분히 기다려라"),
    ("그냥 ^yellow;어쩌다 부활했나^reset;?", "그냥 ^yellow;어떻게 부활한 거지^reset;?"),
    ("'먼지의 탐구자'에 대해서요", "'먼지 탐구자'에 대해서요"),
    ("찡! 그분은", "짹! 그분은"),
    ("돌아와, 시커.", "돌아와, 탐구자."),
    ("괜찮아, 시커?", "괜찮아, 탐구자?"),

    # ---- arcana (Seeker faction -> 탐구자; Tech -> 테크; course name) ----
    ("조심하세요, 시커.", "조심하세요, 탐구자."),
    ("기본 시커 훈련", "기본 탐구자 훈련"),
    ("아우레아 콜렉티브의 시커가 될 거다", "아우레아 콜렉티브의 탐구자가 될 거다"),
    ("기술이 마음에 드나요?", "테크가 마음에 드나요?"),
    ("새 기술을 획득했다", "새 테크를 획득했다"),
    ("이동 훈련 과정을 완료하게 됩니다", "기동 코스를 완료하게 됩니다"),
    ("기동성 코스는 끝입니다", "기동 코스는 끝입니다"),
    ("시간 없는 행성", "타임리스 행성"),

    # ---- om_harpyIntro (register unified to dominant 반말) ----
    ("제가 당신 감방 문을 열면, 여기 있는 다른 포로들을 구할 시간이 충분하지 않을 거예요. "
     "제 지시를 신중히 따라주셔야 해요.",
     "네 감방 문을 열고 나면, 여기 있는 다른 포로들을 구할 시간이 부족할 거야. "
     "내 지시를 잘 따라야 해."),
    ("무기 상자가 있어요. 점프 타이밍을 맞춰 각 발판에 조심스럽게 착지해야 합니다.",
     "무기 상자가 있어. 점프 타이밍을 맞춰 각 발판에 조심해서 착지해야 해."),
    ("정박한 우주선을 감지하고 있습니다", "정박한 우주선을 감지하고 있어"),
    ("탈출할 수 있습니다^reset;", "탈출할 수 있어^reset;"),

    # ---- pf_newtutorial (item-name anchors) ----
    ("개량형 위험 연구소 탁자", "개량형 위험 실험 탁자"),
    ("발명가 테이블", "발명가의 작업대"),
    ("심지어 레귤레이터까지", "심지어 조절기까지"),

    # ---- sb_tutorial ----
    ("나무 도구 작업대", "나무 도구대"),
    ("여행 중 발견한 주목할 장소, 친구에게 보낼 메시지, 내 조언을 적어둘 만하다.",
     "메모나 친구에게 보낼 메시지, 내 조언, 여행 중 발견한 주목할 만한 장소를 적어 둘 만하다."),
    ("기술 사본을 얻으려면, ^orange;기술 개발 콘솔^green;에서 "
     "^orange;기술 장착 메뉴^green;의 기술을 선택하고",
     "테크 사본을 얻으려면, ^orange;테크 개발 콘솔^green;에서 "
     "^orange;테크 장착 메뉴^green;의 테크를 선택하고"),
    ("기술 사본이 남으면", "테크 사본이 남으면"),

    # ---- thea-instances (monster name anchor) ----
    ("침해된 엘리트 드랄", "유린당한 정예 드랄"),

    # ---- viera + magicitediscovery01 quest (item-name anchors) ----
    # the 모아와라 needle uses the pre-replacement 매지사이트 spelling and must
    # run before the generic 매지사이트 pair
    ("^green;모아와라^reset; - ^orange;제련한 매지사이트^reset;에 더해",
     "^green;모아오라^reset;: ^orange;제련한 마기사이트^reset;에 더해"),
    ("마기석 정제 과정", "마기사이트 정제 과정"),
    ("제련한 매지사이트", "제련한 마기사이트"),
    ("매지사이트 광석", "마기사이트 광석"),
    ("스톤 헤스", "돌 벽난로"),
    ("아무 ^orange;돌 화로^reset;에서든", "아무 ^orange;돌 벽난로^reset;에서든"),
    ("^orange;돌 화로^reset;에서 제련하라", "^orange;돌 벽난로^reset;에서 제련하라"),
    ("직물 6개", "섬유 천 6개"),
    ("선하 대장에게", "선하 선장에게"),

    # ---- voided ----
    ("시야에 들어가지 마시오", "시야에 들어가지 마라"),
    ("파상 공격 생성 장치는", "웨이브 생성기는"),
    ("책갈피 등록", "즐겨찾기"),
    ("미확인 균류 독소", "미확인 마이코톡신"),
    ("곰팡이독소", "마이코톡신"),
]

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


def replace_in_value(v):
    if isinstance(v, str):
        changed = False
        for old, new in REPLACEMENTS:
            if old in v:
                v = v.replace(old, new)
                changed = True
        return v, changed
    if isinstance(v, list):
        out = []
        changed = False
        for x in v:
            x, c = replace_in_value(x)
            out.append(x)
            changed = changed or c
        return out, changed
    if isinstance(v, dict):
        out = {}
        changed = False
        for k, x in v.items():
            x, c = replace_in_value(x)
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
    # verify each needle exists in the source before rewriting
    for old, needle in zip([r[0] for r in REPLACEMENTS], needles):
        if not any(needle in files[n] for n in files if n.endswith(".patch")):
            print("NEEDLE-MISS (source):", old[:80])
    assets_changed = 0
    for name in sorted(files):
        if not name.endswith(".patch"):
            continue
        data = files[name]
        if not any(n in data for n in needles):
            continue
        try:
            doc = json.loads(data)
        except Exception:
            continue
        new_doc, changed = replace_in_value(doc)
        if changed:
            files[name] = json.dumps(new_doc, ensure_ascii=False).encode("utf-8")
            assets_changed += 1
            print("fixed", name)

    buf = bytearray(b"SBAsset6" + b"\x00" * 8)
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
