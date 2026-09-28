# -*- coding: utf-8 -*-
"""Seventeenth fix batch (2026-09-28). 선원(sailor) -> 승무원(crew member)
global-scope judgment call, resolved this session per user request.

Investigation: grep'd every "선원" occurrence in the deployed pak (54 rows,
see pak_pairs.tsv), then cross-checked how vanilla sbkor.tsv already
localizes Starbound's core ship-crew hiring mechanic (Expand Your Crew /
crew uniform / crew member count UI) -- it consistently uses 승무원, never
선원. 선원 literally means "sailor/mariner" (a sea-vessel term); Starbound's
"crew" is the starship-crew hiring feature, so 승무원 is the correct baseline
term and 선원 was the error, not a legitimate stylistic choice.

Scope of this fix -- ONLY rows about the ship's-crew game mechanic:
- npcs/crew/* crewmember dialogue offering to join "your crew"
- items/active/arcana_crew crew contracts
- interface confirmation dialogs for hiring crew
- ship's-bridge object descriptions ("Captain and crew navigate the ship")
- azure weapon descriptions ("Arcanian ship crew")
- summonball_crewmateF/M Pokeball items (also fixes a second bug found in
  the same strings: 암/수 are animal-gender suffixes, wrong for a humanoid
  crewmate -- should be 여/남)

Explicitly EXCLUDED (kept as 선원 -- genuinely about sea sailors, not the
ship's-crew mechanic):
- om_starrycultistsailor.npctype dialogue (ocean biome NPC literally about
  fishing/sailing, EN says "sailor")
- CCGthankyou codex "Sailor Set" (real-world fashion item name)
- esc_yamawaro_machete "Privateer's Machete" -> 사략선원 (privateer is a
  historical sea-vessel sailor, correct as-is)
- essential_gc_captainrumbarrels dialogue (a rum-pirate captain talking
  about his own crew with maritime flavor, not the player's ship-crew
  system; left as a judgment call, low priority either way)
- nmm_mvg sandcrewmatebucket "모래선원" (ambiguous novelty item name, not
  clearly part of the crew mechanic)

Also fixes an unrelated mistranslation found in the same grep pass: the
config_scannersignals "rowdy ... crew" flightcontrol analysis lines used
선원단 (sailor band) for informal work crews (construction/medical/
electrician/armsdealer/cooks) that have nothing to do with sailors OR the
player's ship crew -- replaced with 무리 (group/gang).
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
OUT_PAK = BASE / "female_translation.pak.NEW21"

REPLACEMENTS = [
    # scannersignals: 선원단(sailor band) is wrong for generic work crews --
    # fix before the crew->승무원 pass so it doesn't get caught by it.
    ("난폭한 건설 선원단입니다.", "난폭한 건설 인부 무리입니다."),
    ("난폭한 의료진 선원단입니다.", "난폭한 의료진 무리입니다."),
    ("난폭한 전기 기술자 선원단입니다.", "난폭한 전기 기술자 무리입니다."),
    ("난폭한 무기상 선원단입니다.", "난폭한 무기상 무리입니다."),
    ("난폭한 요리사 선원단입니다.", "난폭한 요리사 무리입니다."),

    # ship's-crew mechanic: 선원 -> 승무원
    ("네 선원단에 입대하고 싶어할 만한 사람들을 좀 알지도 몰라.",
     "네 승무원단에 입대하고 싶어할 만한 사람들을 좀 알지도 몰라."),
    ("을(를) 선원으로 고용할까요?", "을(를) 승무원으로 고용할까요?"),

    ("블러드 어쌔신 선원 계약서", "블러드 어쌔신 승무원 계약서"),
    ("마크스맨 선원 계약서", "마크스맨 승무원 계약서"),
    ("메이지 선원 계약서", "메이지 승무원 계약서"),
    ("버서커 선원 계약서", "버서커 승무원 계약서"),
    ("정비사 선원 계약서", "정비사 승무원 계약서"),
    ("켐로드 선원 계약서", "켐로드 승무원 계약서"),

    ("아르카니안 선원들이 사용하는 시제품 권총.", "아르카니안 승무원들이 사용하는 시제품 권총."),
    ("아르카니안 선원들이 사용하는 녹슨 저격소총.", "아르카니안 승무원들이 사용하는 녹슨 저격소총."),

    ("네 선원으로 합류해서 기계도 가치 있는 존재라는 걸 세상에 보여 주고 싶어. 날 받아 줄래?",
     "네 승무원으로 합류해서 기계도 가치 있는 존재라는 걸 세상에 보여 주고 싶어. 날 받아 줄래?"),
    ("대신 네 선원단에 합류하면 안 될까?", "대신 네 승무원단에 합류하면 안 될까?"),

    ("선원들 유니폼 좀 바꾸고 싶으면, 인사하러 와!", "승무원들 유니폼 좀 바꾸고 싶으면, 인사하러 와!"),
    ("선원들 복장을 바꾸고 싶다면, 내가 딱이야!", "승무원들 복장을 바꾸고 싶다면, 내가 딱이야!"),

    ("함께 일할 선원을 찾고 있습니다. 관심 있으신가요?", "함께 일할 승무원을 찾고 있습니다. 관심 있으신가요?"),
    ("저 이미 당신 선원인데, 바보같이!", "저 이미 당신 승무원인데, 바보같이!"),

    ("선원으로서, 저는 멋진 별들을 많이 방문할 수 있어요!", "승무원으로서, 저는 멋진 별들을 많이 방문할 수 있어요!"),
    ("그래도 내 선원들과 여기 있을 수 있어서 여전히 감사해.", "그래도 내 승무원들과 여기 있을 수 있어서 여전히 감사해."),

    ("함장과 선원이 여기서 함선을 조종한다.", "함장과 승무원이 여기서 함선을 조종한다."),
    ("이거면 선원을 모집해야 할 이유로 충분해!", "이거면 승무원을 모집해야 할 이유로 충분해!"),

    ("오렌지는 우주 항해 선원으로 일부 글리치를 고용했다.", "오렌지는 우주 항해 승무원으로 일부 글리치를 고용했다."),

    ("선원 (암) 포켓볼", "승무원 (여) 포켓볼"),
    ("선원 (수) 포켓볼", "승무원 (남) 포켓볼"),

    # newly-discovered mistranslation, unrelated to the crew/sailor question
    ("^#8d8d8d;원형", "^#8d8d8d;종족"),
]

print("total replacement pairs:", len(REPLACEMENTS))


def _vlqr(buf, p):
    v = 0
    while True:
        b = buf[p]
        p += 1
        v = (v << 7) | (b & 0x7F)
        if not (b & 0x80):
            return v, p


def vlq(v):
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
    return buf[p:p + n].decode("utf-8"), p + n


def _rjson_skip(buf, p):
    t = buf[p]
    p += 1
    if t == 0x01:
        return p
    if t == 0x02:
        return p + 8
    if t == 0x03:
        return p + 1
    if t == 0x04:
        _, p = _vlqr(buf, p)
        return p
    if t == 0x05:
        n, p = _vlqr(buf, p)
        return p + n
    if t == 0x06:
        n, p = _vlqr(buf, p)
        for _ in range(n):
            p = _rjson_skip(buf, p)
        return p
    if t == 0x07:
        n, p = _vlqr(buf, p)
        for _ in range(n):
            _, p = _key(buf, p)
            p = _rjson_skip(buf, p)
        return p
    raise ValueError("unknown json type %r at %d" % (t, p))


def replace_in_value(v):
    if isinstance(v, str):
        out = v
        for old, new in REPLACEMENTS:
            if old in out:
                out = out.replace(old, new)
        return out, out != v
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
        _, p = _key(d0, p)
        p = _rjson_skip(d0, p)
    meta_blob = d0[off0:p]

    src = Pak(str(SRC_PAK))
    files = {name: src.read(name) for name in src.index}
    print("base pak entries:", len(files))

    needles = [json.dumps(old, ensure_ascii=False)[1:-1].encode("utf-8")
               for old, _ in REPLACEMENTS]
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
