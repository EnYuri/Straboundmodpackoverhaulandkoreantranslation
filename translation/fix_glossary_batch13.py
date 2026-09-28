"""Thirteenth fix batch (2026-09-28). Origin: manual review of the
/dialog/tentacles/ asset group (37 config files, 1,539 pairs; shared strings
also update /npcs/furniture/naked.npctype.patch automatically).

All pairs verified against pak_pairs.tsv before fixing. Highlights:

- Glitch emotion-prefix noun-form normalization (batch10 rule): residual
  verb/adjective forms 물들었다/피곤하다/더럽혀졌다/절박하다/지쳤다/궁금하네/
  이상하다/유혹적/아파 -> 물듦/피곤/더럽혀짐/절박/지침/호기심/이상함/유혹적임/아픔.
  Context needles used so legit mid-sentence uses elsewhere stay untouched.
  Note: the FFS stagehand "Desperate." prefix gets the same fix.
- Kinky -> 음란 (glitch-pregnant convention; 킹키 transliteration removed).
- Floran fuck-meat unified to 떡감 (corpus dominant 20 uses incl. sexbound
  dialogs) over 떡고기/박을-고기/박음-고기/씹갯살/씹당하는 variants.
- Tentacle-context hive -> 둥지 where rendered as 벌집 (beehive image is wrong;
  literal hive-biome/material 벌집 uses kept). 둥지/하이브 synonym mix kept.
- Fenerox telegraphic cleanup: 부드러운 꽉 -> 부드러운 죔, 그립 transliteration
  -> 붙잡음, drained mistranslations (다 마심 / 빠짐) -> 탈진, fur heavy -> 털
  무거움.
- Register slips fixed inside 반말/telegraphic voices: avian-exhausted 존댓말
  x2, novakid-exhausted -네요, fenerox 그르렁대요.
- Mistranslations: hump->혹 (actually 박기), Not...Like...This -> 이렇게는 안 돼,
  dish->접시 (corrupted 'this'), gestate->수정 (should be 잉태), virility->
  생식력 (should be 정력), seedbed->종자상 (unified to 씨받이 convention),
  untranslated AAH, Ook Ook Ah! monkey sound restored, Oook 우움->우욱,
  squawk 꼬끼오->꽥꽥, 촉수기는->촉수긴 typo, 제발알->제바알, 하이브서->하이브에서.
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
OUT_PAK = BASE / "female_translation.pak.NEW17"

REPLACEMENTS = [
    # ---- glitch emotion-prefix noun-form normalization (context needles) ----
    ("물들었다. 그들의 흔적이", "물듦. 그들의 흔적이"),
    ("피곤하다. 어디나 촉수뿐", "피곤. 어디나 촉수뿐"),
    ("피곤하다. 촉수 분비물로 가득한데도", "피곤. 촉수 분비물로 가득한데도"),
    ("피곤하다. 끝없는 쾌락은", "피곤. 끝없는 쾌락은"),
    ("더럽혀졌다. 그들이 나의 신성함을", "더럽혀짐. 그들이 나의 신성함을"),
    ("절박하다. 날 채워줘", "절박. 날 채워줘"),
    ("절박하다. 또 다른 쇳덩이는", "절박. 또 다른 쇳덩이는"),
    ("지쳤다. 촉수가 날 채워주는데도", "지침. 촉수가 날 채워주는데도"),
    ("궁금하네... 촉수들이", "호기심. 촉수들이"),
    ("궁금하네... 시간이", "호기심. 시간이"),
    ("궁금하네... 내 안의", "호기심. 내 안의"),
    ("궁금하네... 부풀어", "호기심. 부풀어"),
    ("이상하다. 내 금속", "이상함. 내 금속"),
    ("유혹적. 나는", "유혹적임. 나는"),
    ("킹키. 볼래?", "음란. 볼래?"),
    ("아파. 이 자라나는", "아픔. 이 자라나는"),

    # ---- mistranslations / lost meaning ----
    ("엉덩이 혹 하나하나가 날 지치게 해", "엉덩이를 박힐 때마다 날 지치게 해"),
    ("이렇게... 끝날... 순...", "이렇게는... 안 돼..."),
    ("AAH! 세상이 빙글빙글", "아악! 세상이 빙글빙글"),
    ("그냥 종자상이야", "그냥 씨받이야"),
    ("접시 몰랐어어", "이런 건 몰랐어어"),
    ("내 뇌에에에 수정해애애", "내 뇌에에에 잉태해애애"),
    ("그들의 생식력은", "그들의 정력은"),

    # ---- floran fuck-meat -> 떡감 (dominant form) ----
    ("박을-고기 얻어", "떡감 얻어"),
    ("박을-고기야", "떡감이야"),
    ("박음-고기", "떡감"),
    ("질긴 씹갯살", "질긴 떡감"),
    ("씹당하는 부화장", "떡감 부화장"),
    ("떡고기", "떡감"),

    # ---- register slips inside 반말/telegraphic voices ----
    ("신경 쓰지 마세요, 그냥 여행을 즐기는 중이에요.", "신경 쓰지 마, 그냥 즐기는 중이야."),
    ("손질해서 빼낼 수는 있을까요", "손질해 뺄 수 있을까"),
    ("안장에 쓸린 상처가 치료가 절실하다고 할 수 있겠네요",
     "안장에 쓸린 상처가 치료가 절실하다고 할 수 있겠네"),
    ("부드럽게 그르렁대요", "부드러운 가르랑거림"),

    # ---- fenerox telegraphic cleanup ----
    ("부드러운 꽉 쥠", "부드러운 죔"),
    ("부드러운 꽉.", "부드러운 죔."),
    ("단단 그립", "단단 붙잡음"),
    ("끈적 그립", "끈적 붙잡음"),
    ("강한 그립", "강한 붙잡음"),
    ("페네록스 다 마심", "페네록스 탈진"),
    ("페네록스 빠짐. 촉수 빠짐.", "페네록스 탈진. 촉수 탈진."),
    ("정액 부카케. 털이 잔뜩.", "정액 부카케. 털 무거움."),
    ("꽉 끼네.", "꽉 죔."),

    # ---- misc consistency / typos ----
    ("촉수 사실 최-최고!", "촉수가 사실 최-최고야!"),
    ("우으, 아아!", "우끼 우끼 아!"),
    ("*우움!", "*우욱!"),
    ("*꼬끼오 꼬끼오*", "*꽥꽥*"),
    ("촉수기는 하지", "촉수긴 하지"),
    ("제발알?", "제바알?"),
    ("이 하이브서", "이 하이브에서"),

    # ---- tentacle-context hive 벌집 -> 둥지 ----
    ("벌집은 자라날 것이다!", "둥지는 자라날 것이다!"),
    ("이 벌집은 집 냄새가 나아", "이 둥지는 집 냄새가 나아"),
    ("벌집에서 배가 부풀어", "둥지에서 배가 부풀어"),
    ("벌집에선 그냥 평범한 하루지", "둥지에선 그냥 평범한 하루지"),
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
