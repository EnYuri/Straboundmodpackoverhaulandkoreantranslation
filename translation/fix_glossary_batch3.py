"""Third glossary-consistency batch fix (2026-09-28 item-name/description
priority QA pass). Each entry was verified against pak_pairs.tsv /
qa_pak_glossary_report.tsv occurrence counts and surrounding context before
being added here. See fix_glossary_batch2.py for the shared rebuild approach
and batchim-safety rationale; the same rules apply here.

Notable non-mechanical decisions folded into this batch:
- Kappa: only the "카파 수리 키트" (Corporate Kappa race trait) label text is a
  real glossary violation (Kappa -> 캇파, "카파로 쓰지 않는다"). The
  "K'Rakoth Codex Kappa" instance is the Greek-letter chapter-naming
  convention (Alpha..Omega) used for that codex series, not the youkai race,
  so it is intentionally left as "카파" and NOT touched.
- Two-Handed: "강력한 즉석 무기." for EN "A powerful two-handed sword." is an
  outright mistranslation (copy/paste of an unrelated "improvised weapon"
  string), not a terminology issue. Fixed to "강력한 양손검." per the
  Two-Handed -> 양손 (attributive) glossary rule + established plain "검"
  usage for unqualified "sword" elsewhere in the pak (see crossedge: "강력한
  검").
- Aeginian Federal Union / Aeginian: the pak has three competing stems for
  "Aeginian" - "아에기니안" (39 uses, most common, but built on the EXPLICITLY
  BANNED "아에기" form per the Aegi glossary row: "아에기/에기/에이기(구형,
  사용 금지)"), "에지니안" (19 uses, correct stem, adjectival), and "에지족"
  (18 uses, correct stem, demonym-noun). Majority usage does not override an
  explicit glossary ban, so all "아에기니안"/"아이기니안" (typo) instances
  are unified onto the already-correct "에지니안" stem. The specific compound
  "Aeginian Federal Union" is further unified to the exact fixed phrase
  "에지족 연방 연합" per its dedicated glossary row, regardless of which
  stem/suffix variant it originally appeared with.

Order matters: longer/more specific phrases are replaced before their
shorter/bare prefixes so a bare-form replace never clobbers an already-fixed
phrase.
"""
import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

SRC_PAK = STAR / "mods" / "female_translation.pak"
OUT_PAK = STAR / "translation" / "translation-baseline-20260921" / "female_translation.pak.NEW7"

REPLACEMENTS = [
    # Two-Handed sword description bug fix (mistranslation, not terminology)
    ("강력한 즉석 무기.", "강력한 양손검."),
    # Kappa -> 캇파 (Corporate Kappa race trait only; codex "카파" left alone)
    ("카파 수리 키트", "캇파 수리 키트"),
    # Assault Rifle -> 돌격소총 (no space)
    ("어설트 라이플", "돌격소총"),
    ("어썰트 라이플", "돌격소총"),
    ("어설트 소총", "돌격소총"),
    ("돌격 소총", "돌격소총"),
    # Grenade Launcher -> 유탄 발사기 (with space)
    ("유탄발사기", "유탄 발사기"),
    # Erchius -> 에르키우스
    ("에르치우스", "에르키우스"),
    ("얼치어스", "에르키우스"),
    # Novakid -> 노바키드 (longer form first)
    ("노바킨드", "노바키드"),
    ("노바킨", "노바키드"),
    # Saturnian -> 새터니안
    ("새터니언", "새터니안"),
    # Telebrium -> 텔레브리엄
    ("텔레브리움", "텔레브리엄"),
    # Hymid -> 하이미드
    ("히미드", "하이미드"),
    # Enerth Engineering -> 에너스 엔지니어링 (transliteration + word choice)
    ("에네르스 엔지니어링", "에너스 엔지니어링"),
    ("에네르스", "에너스"),
    ("에너스 공학", "에너스 엔지니어링"),
    # Parry (bare) -> 패링 (Parry Window "패링 창" is untouched, no overlap)
    ("카타나 패리", "카타나 패링"),
    ("독성 패리", "독성 패링"),
    # Aeginian Federal Union -> 에지족 연방 연합 (exact fixed compound,
    # regardless of which stem/suffix variant it appeared with)
    ("아에기니안 연방 유니온", "에지족 연방 연합"),
    ("아에기니안 연방 유니언", "에지족 연방 연합"),
    ("아에기니안 연방 연합", "에지족 연방 연합"),
    ("에지니안 연방 연합", "에지족 연방 연합"),
    ("아이기니안 연방", "에지족 연방 연합"),
    ("아에기니안 연방", "에지족 연방 연합"),
    ("에지니안 연방", "에지족 연방 연합"),
    # Aeginian (bare stem) -> 에지니안; Aegi (bare race noun) -> 에지
    ("아이기니안", "에지니안"),
    ("아에기니안", "에지니안"),
    ("아에기", "에지"),
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
