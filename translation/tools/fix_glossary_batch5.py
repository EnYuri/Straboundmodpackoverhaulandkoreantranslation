"""Fifth glossary-consistency batch fix (2026-09-28 item-name/description
priority QA pass, continued after batch2/3/4). Sourced from a re-run of
qa_pak_glossary.py against pak_pairs.tsv extracted post-batch4 (violations
dropped 374 -> 313; this batch addresses the newly-surfaced long-tail
singleton terms that were previously crowded out of the top-30 by bigger
offenders).

Terms surveyed but intentionally left unchanged:
- Hit Shield (glossary: 피격 방패, GiC 확정 용어) vs the pak's actual
  established usage, "타격 보호막", used *consistently* across all 5
  occurrences (Miko Hit-Shield x2, Enduring Mind x2, Orange Potion x1) with
  zero existing uses of "피격 방패" anywhere in the pak. This is a real
  majority-usage-vs-glossary conflict (unlike the Aeginian/아에기 case, there
  is no explicit "banned form" note here, just an apparently unapplied
  preference) -- left for the user to confirm before overwriting 5
  consistent, already-shipped instances with a term that has never actually
  been used.
- Union flag (글로서리: 유니언 깃발, "연합 깃발 금지"): the report hit is
  `flagaegipride`'s "Aeginian Federal Union flag" description, which
  literally contains the substring "Union flag" only because of English
  word adjacency ("Federal Union" + generic "flag"), not the distinct
  "Union" faction the glossary row is about. Already correctly reads
  "에지족 연방 연합 깃발" per the Aeginian Federal Union fix in batch3;
  false-positive collision, not touched.
- The Ruined ("폐허가 된" in a Floran codex poem describing a ruined city):
  glossary note explicitly excludes the generic adjective "ruined" from
  this Angel-race-faction term; textbook documented exception.
- Boneworking Station / Leatherworking Station (avikan/* crafting objects):
  the glossary rows are specifically for the Elithian Alliance's tiered
  crafting stations ("Elithian Alliance 제작대... 혼용하지 않음"); these hits
  are Avikan-faction crafting objects, a different race's stations that
  coincidentally share the English name. Left alone.
- dunebuns / "Crawler Dunebun" quest reward: the glossary row is for the
  generic Elithian food item "dunebuns" (사구빵); "Crawler Dunebun" here
  reads as a distinct creature/pet proper noun, not the food item.
"""
import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

SRC_PAK = STAR / "mods" / "zz_translation_female.pak"
OUT_PAK = STAR / "translation" / "translation-baseline-20260921" / "female_translation.pak.NEW9"

REPLACEMENTS = [
    # Ruin-Killer -> 루인킬러 (no space)
    ("루인 킬러", "루인킬러"),
    # Thrust Damage -> 찌르기 피해 (targeted; bare "관통 피해" also legitimately
    # appears once elsewhere for unrelated content)
    ("단검 투척: 가장 가까운 적에게 전투용 단검을 던져 관통 피해 100.",
     "단검 투척: 가장 가까운 적에게 전투용 단검을 던져 찌르기 피해 100."),
    # Broadsword -> 브로드소드 (glossary explicitly forbids 대검/장검 here)
    ("강철 주괴 정확히 6개 (대검)", "강철 주괴 정확히 6개 (브로드소드)"),
    # Zerchesium -> 제르세슘
    ("제르케시움", "제르세슘"),
    # United Systems -> 연합 시스템 (glossary explicitly forbids 연합 체계)
    ("연합 체계 무기", "연합 시스템 무기"),
    # Droden -> 드로덴 (majority form is already 드로덴, 212 vs this typo)
    ("드로든", "드로덴"),
    # Knockback -> 넉백
    ("강한 날려보내기", "강한 넉백"),
    # Fusion Chamber -> 핵융합로 (Elithian Alliance namespace confirmed:
    # /objects/alliance/crafting/alliancefurnace/)
    ("융합실", "핵융합로"),
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
