# -*- coding: utf-8 -*-
"""Eighteenth fix batch (2026-09-28). Confirmed findings from the parallel
fork QA pass this session over STYLE_MIX group2/group3 (non-/dialog/ STYLE_MIX
backlog) and the newly-discovered flat-patch blind spot (group A/B).

- charcreation SPECIES -> 종족 (was "원형"/prototype, character-creation
  screen race-select label every player sees).
- abyssvortex glitchDescription typo 뭔든 -> 뭐든.
- gic_trait_duellist_pistolaffinity label: [DUELLIST TRAIT] and
  SHORT-SIGHTED were left untranslated, unlike every sibling trait label in
  the same family; aligned to established 결투자 특성 / 근시 (per the
  shortsighted status effect's own label).
- mwhaddon_mission_horizon General Falke register break: the whole radio
  exchange is consistently banmal, one line used -군요 (존댓) -> -군.
- lawPBImissions_M04b mistranslation: "surcis" (French "sursis", a reprieve)
  was rendered as 심사(screening/examination), reversing the meaning
  (you got a temporary reprieve, not evaluated) -> 유예.
- ffs2 SWAT Blue team senderName inconsistency: Red team kept "SWAT"
  untranslated (established convention per lawswatplasmarifle etc.), Blue
  team had it localized as 특수기동대 -> unified to SWAT.
- novakidquest Butane Cassidy: 부탄 캐시디 (killBoss) diverged from the
  file's own completionText 부테인 캐시디, and from the established spelling
  in batch_log.md -> 부테인 캐시디.
- quest4pbiMission2 Mox Fulder: turnInDescription's "목스 풀더" diverged
  from the batch12-established spelling "목스 펄더" (see docs/batch_log.md,
  9 senderName occurrences already unified) -> 목스 펄더.
"""

import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

BASE = Path(__file__).parent
SRC_PAK = BASE / "female_translation.pak.NEW21"
OUT_PAK = BASE / "female_translation.pak.NEW22"

REPLACEMENTS = [
    ("위압. 주변의 뭔든 빨아들이는 소용돌이를 만들어요.",
     "위압. 주변의 뭐든 빨아들이는 소용돌이를 만들어요."),
    ("특이한 권총 친화력 [DUELLIST TRAIT] - 한손 권총류 무기 사용 시 SHORT-SIGHTED 디버프를 무효화하고 +20% [EWS] 명중률을 얻는다.",
     "특이한 권총 친화력 [결투자 특성] - 한손 권총류 무기 사용 시 근시 디버프를 무효화하고 +20% [EWS] 명중률을 얻는다."),
    ("드릴 기계? 흥미롭군요.", "드릴 기계? 흥미롭군."),
    ("살아남으셨어요, 하지만 이건 겨우 심사일 뿐이죠.",
     "살아남으셨어요, 하지만 이건 그저 일시적인 유예일 뿐이죠."),
    ("특수기동대 블루팀", "SWAT 블루팀"),
    ("부탄 캐시디^reset; 처치", "부테인 캐시디^reset; 처치"),
    ("목스 풀더 요원", "목스 펄더 요원"),
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
