"""Ninth fix batch (2026-09-28). Origin: fork-based STYLE_MIX dialogue
comprehension review (group0 + group1), launched after the user flagged that
narrow automated heuristics + manual spot-checking don't scale to a
182,157-row corpus ("이 거 번역한 문자열이 수십만개다"). Two of four planned
fork groups (group0, group1, ~2,720 rows across 39 assets) completed and
reported 14 confirmed real issues, applied here per "수정만 하고 마무리ㅣ".
group2/group3 (~2,716 more rows) remain un-run/deferred.

14 confirmed issues (verified against pak_pairs.tsv before fixing, not just
trusting the fork's quoted snippets):

1. Leda Portia name: senderName is consistently "레다 포르샤" (5x); the lone
   /ttppmission2d1/text body instance said "레다 포르티아" -> unified to 포르샤.
2. Qingque Tea Brewer item name: the object's own /shortdescription (the
   authoritative in-game name) and a quest completionText both say
   "칭췌 차 우림기"; two radiomessages/interface strings used other variants
   ("칭추에 찻주전자" x2, "칭퀘 차 양조기" x1) -> unified to 칭췌 차 우림기.
   ("칭취" elsewhere refers to the tea flavor, not the machine - untouched.)
3. Officer -> 경관 (26x) vs 장교 (3x stray instances in
   lawenforcementconverse.config.patch) -> unified to 경관.
4. Beacon (atprk_fuelderguardian) -> 비컨 (8x) vs 비콘 (1x) / 신호기 (1x)
   -> unified to 비컨.
5. Bridge (ship's bridge, ffs_whitecrow.radiomessages.patch, referenced by
   ffs2_lastboss_1_10/1_11/1_15/1_16 and ffs_whitecrow_1_4) mistranslated as
   "교두보/교두부" (military "bridgehead") -> corrected to "함교" (ship's
   bridge), matching context (FTL drive, hotline, engineering team contact).
6. Mox Fulder / Agent Fulder: senderName consistently "목스 펄더" (9x); six
   "Agent Fulder" occurrences in lawPBImissions_M04a/M04b radiomessages body
   text said "폴더 요원" -> unified to 펄더 요원. (The unrelated object
   "Mox Folder's Missions", whose EN source literally says "Folder", is a
   different in-game name and left untouched.)
7. "갈갈이" typo (2x, pf_samuraimerc.config.patch) -> "갈가리".
8. Bare "님" honorific for "Sir" (ffs2_radiomessages, 3 instances) is
   inconsistent with the same file's dominant "대장님" (10x) -> unified.
9. Relic Seekers -> 유물 탐색단 (30+x) vs 유물 탐구자 (6x stray instances)
   -> unified to 탐색단, keeping each sentence's own phrasing/template intact.
10. /converse/novakid/avali/2: grammatically fragmented telegraphic Korean
    -> rewritten as a natural sentence.
11. Arcane catalyst -> 아케인 촉매 (2x) vs 비전 촉매 (1x, shpd_catalyst2)
    -> unified to 아케인; plus a damaged "^oange;" tag (2x, shpd_dart) fixed
    to "^orange;".
12. /converse/saturn/default/29 (SaturnGuardMage): telegraphic/particle-
    dropped sentence -> rewritten naturally.
13. "partner" -> 파트너 (9x, mwhaddon_mission_sideStory) vs the lone
    horizon_4_1 instance saying "친구" -> unified to 파트너.
14. "target" -> ffs_alice_combat.config.patch has 목표 (1x) vs 과녁 (1x)
    for the same enemy-tracking concept -> unified to 목표.
"""
import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

SRC_PAK = STAR / "mods" / "female_translation.pak"
OUT_PAK = STAR / "translation" / "translation-baseline-20260921" / "female_translation.pak.NEW13"

REPLACEMENTS = [
    # 1. Leda Portia
    ("현재 고위 수호자이신 레다 포르티아 님의 초상화가 사라졌어요.",
     "현재 고위 수호자이신 레다 포르샤 님의 초상화가 사라졌어요."),

    # 2. Qingque Tea Brewer
    ("칭추에 찻주전자 - 여기서 사랑스러운 찻잔을 꾸미세요!",
     "칭췌 차 우림기 - 여기서 사랑스러운 찻잔을 꾸미세요!"),
    ("^green;칭퀘 차 양조기^reset;의 ^orange;찻잔^reset;에 넣을 수 있다.",
     "^green;칭췌 차 우림기^reset;의 ^orange;찻잔^reset;에 넣을 수 있다."),
    ("^green;칭추에 찻주전자^reset;에서 추가 효과를 적용할 수 있다.",
     "^green;칭췌 차 우림기^reset;에서 추가 효과를 적용할 수 있다."),

    # 3. Officer -> 경관
    ("물질 조작기가 없으면, 현장 작업이 한계가 있어. <entityname> 장교인 너와는 다르게!",
     "물질 조작기가 없으면, 현장 작업이 한계가 있어. <entityname> 경관인 너와는 다르게!"),
    ("장교 <entityname>, 당신을 위해 새 사건을 몇 건 조사하고 있었어요.",
     "<entityname> 경관, 당신을 위해 새 사건을 몇 건 조사하고 있었어요."),
    ("역 소문에 네가 진짜 명사수라던데, <entityname> 장교!",
     "역 소문에 네가 진짜 명사수라던데, <entityname> 경관!"),

    # 4. Beacon
    ("오직 한 명만이 비콘을 지킬 수 있다... 더도 덜도 말고.",
     "오직 한 명만이 비컨을 지킬 수 있다... 더도 덜도 말고."),
    ("신호기를 지켜라!", "비컨을 지켜라!"),

    # 5. Bridge -> 함교
    ("교두보 핫라인을 다시 온라인으로 만들어야 해!", "함교 핫라인을 다시 온라인으로 만들어야 해!"),
    ("그럼 ^green;교두부에 연락해야 한다^white;, 최대한 빨리!",
     "그럼 ^green;함교에 연락해야 한다^white;, 최대한 빨리!"),
    ("^white;교두보까지 거의 다 왔어. 서둘러!", "^white;함교까지 거의 다 왔어. 서둘러!"),
    ("^white;여기는 교두보. 말해.", "^white;여기는 함교. 말해."),
    ("^white;요원, 이 구역엔 ^green;교두부^white;와 ^green;화물실^white;이 있다. ",
     "^white;요원, 이 구역엔 ^green;함교^white;와 ^green;화물실^white;이 있다. "),

    # 6. Fulder
    ("폴더 요원이 말했던 오염된 보호국 함선 중 하나다.", "펄더 요원이 말했던 오염된 보호국 함선 중 하나다."),
    ("폴더 요원에게 좌표를 보낼 수 있겠어, 그리고 오오...", "펄더 요원에게 좌표를 보낼 수 있겠어, 그리고 오오..."),
    ("폴더 요원, 여러 시신을 바닥에서 봤습니다.", "펄더 요원, 여러 시신을 바닥에서 봤습니다."),
    ("폴더 요원, 보안실에 있습니다.", "펄더 요원, 보안실에 있습니다."),
    ("폴더 요원, 서버실에 있습니다.", "펄더 요원, 서버실에 있습니다."),
    ("폴더 요원, 들리십니까?", "펄더 요원, 들리십니까?"),

    # 7. 갈갈이 -> 갈가리
    ("내 검 널 갈갈이 자를 거야!", "내 검 널 갈가리 자를 거야!"),

    # 8. bare 님 -> 대장님 (Sir, ffs2)
    ("..예.. 알겠습니다, 님. 앨리스 중위가 저와 함께 있었지만 지금은 아닙니다.",
     "..예.. 알겠습니다, 대장님. 앨리스 중위가 저와 함께 있었지만 지금은 아닙니다."),
    ("그리고 나머지는 ..어.. 민간인들뿐입니다. 여기서 군사 훈련을 받은 건 저뿐입니다, 님.",
     "그리고 나머지는 ..어.. 민간인들뿐입니다. 여기서 군사 훈련을 받은 건 저뿐입니다, 대장님."),
    ("님, 진짜요?", "대장님, 진짜요?"),
    ("님, 하늘에 저 ^green;주황빛^white; 보입니까?", "대장님, 하늘에 저 ^green;주황빛^white; 보입니까?"),

    # 9. Relic Seekers 탐구자 -> 탐색단
    ("유물 탐구자에 들어오지 않을래?", "유물 탐색단에 들어오지 않을래?"),
    ("동료 중 우리 유물 탐구자에 들어갈 생각 없어?", "동료 중 우리 유물 탐색단에 들어갈 생각 없어?"),

    # 10. novakid/avali/2 grammar fix
    ("하우디 깃털 친구! 아발리 만나면 항상 기뻐! 특히 외인혐오 아닌!",
     "하우디, 깃털 친구! 아발리를 만나는 건 언제나 반가운 일이지! 특히 종족차별 안 하는 아발리라면 더더욱!"),

    # 11. Arcane catalyst + ^oange; typo
    ("저건 주문 크리스탈을 만드는 데 쓰이는 ^green;비전 촉매^reset;예요. 제 데이터뱅크에 따르면 연금술 반응 중 비전 촉매가 형성될 확률은 ^green;33%^reset;예요.",
     "저건 주문 크리스탈을 만드는 데 쓰이는 ^green;아케인 촉매^reset;예요. 제 데이터뱅크에 따르면 연금술 반응 중 아케인 촉매가 형성될 확률은 ^green;33%^reset;예요."),
    ("^green;다트^reset;를 발견했다. ^oange;연금술 씨앗을 바르거나^reset; ^green;연금술 가마^reset;에서 정화할 수 있어 유용한 도구다.",
     "^green;다트^reset;를 발견했다. ^orange;연금술 씨앗을 바르거나^reset; ^green;연금술 가마^reset;에서 정화할 수 있어 유용한 도구다."),

    # 12. SaturnGuardMage grammar fix
    ("여행자들 새터니안 음료 달다 불평. 설탕 여덟 스푼뿐인데!",
     "여행자들은 새터니안 음료가 달다고 투덜댄다. 나는 설탕을 여덟 스푼밖에 안 쓰는데!"),

    # 13. partner
    ("조심해, 친구. 전장 한가운데 떨궈줘야 해. 내 말을 듣기 전에 안전한 위치인지 확인해.",
     "조심해, 파트너. 전장 한가운데 떨궈줘야 해. 내 말을 듣기 전에 안전한 위치인지 확인해."),

    # 14. target -> 목표
    ("너무 멀다! 과녁을 맞힐 수가 없어!", "너무 멀다! 목표를 맞힐 수가 없어!"),
]


def _vlqr(d, p):
    r = 0
    while True:
        b = d[p]; p += 1
        r = (r << 7) | (b & 0x7F)
        if not b & 0x80:
            return r, p


def _key(d, p):
    l, p = _vlqr(d, p)
    return p + l


def _val(d, p):
    t = d[p]; p += 1
    if t == 0x05:
        l, p = _vlqr(d, p); return p + l
    if t == 0x04:
        _, p = _vlqr(d, p); return p
    if t == 0x06:
        c, p = _vlqr(d, p)
        for _ in range(c):
            p = _val(d, p)
        return p
    if t == 0x01:
        c, p = _vlqr(d, p)
        for _ in range(c):
            p = _key(d, p); p = _val(d, p)
        return p
    if t == 0x00:
        return p
    if t == 0x02:
        return p + 1
    if t == 0x03:
        return p + 8
    raise ValueError(f"dynval type {t:#x} at {p - 1}")


def vlq(n):
    parts = []
    while True:
        parts.append(n & 0x7F)
        n >>= 7
        if not n:
            break
    out = bytearray()
    for i, b in enumerate(reversed(parts)):
        out.append(b | (0x80 if i < len(parts) - 1 else 0))
    return bytes(out)


def replace_in_value(v):
    if isinstance(v, str):
        changed = False
        for old, new in REPLACEMENTS:
            if old in v:
                v = v.replace(old, new)
                changed = True
        return v, changed
    if isinstance(v, list):
        changed = False
        out = []
        for item in v:
            nv, c = replace_in_value(item)
            out.append(nv)
            changed = changed or c
        return out, changed
    if isinstance(v, dict):
        changed = False
        out = {}
        for k, item in v.items():
            nv, c = replace_in_value(item)
            out[k] = nv
            changed = changed or c
        return out, changed
    return v, False


def main():
    d0 = SRC_PAK.read_bytes()
    off0 = struct.unpack(">Q", d0[8:16])[0]
    assert d0[off0:off0 + 5] == b"INDEX"
    p = off0 + 5
    pairs, p = _vlqr(d0, p)
    for _ in range(pairs):
        p = _key(d0, p)
        p = _val(d0, p)
    meta_blob = d0[off0:p]

    src = Pak(str(SRC_PAK))
    files = {name: src.read(name) for name in src.index}
    print("base pak entries:", len(files))

    needles = [old.encode("utf-8") for old, _ in REPLACEMENTS]
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
