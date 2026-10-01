"""Second glossary-consistency batch fix, found via qa_pak_glossary.py during
the 2026-09-28 item-name/description priority QA pass. Each entry below was
individually verified against pak_pairs.tsv (occurrence counts + surrounding
context) to confirm it is a real fixed-glossary violation, not a false
positive, and that the replacement's batchim class matches the surrounding
particle (so no 은/는, 이/가, 을/를, 으로/로 mismatch is introduced). Where a
term's batchim class changes, the specific particled forms are listed
explicitly instead of relying on a bare substring replace.

Order matters: longer/particled forms are replaced before their bare/shorter
prefix so a bare-form replace never clobbers an already-fixed particled form.
"""
import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

SRC_PAK = STAR / "mods" / "zz_translation_female.pak"
OUT_PAK = STAR / "translation" / "translation-baseline-20260921" / "female_translation.pak.NEW6"

# (old, new) pairs, applied in order, longest/most-specific first per term.
REPLACEMENTS = [
    # Poptop -> 팝톱 (batchim ㅂ both sides, direct substring safe)
    ("팝탑", "팝톱"),
    # Drahl -> 드랄 (batchim ㄹ both sides)
    ("드라흘", "드랄"),
    # Vaash -> 바쉬 (vowel-final both sides)
    ("바시", "바쉬"),
    # Thelean -> 텔레안 (batchim ㄴ both sides)
    ("텔리안", "텔레안"),
    ("델레안", "텔레안"),
    # Centens -> 센텐스 (particle-aware; consonant-final 센텐 -> vowel-final 센텐스)
    ("센텐이", "센텐스가"),
    ("센텐은", "센텐스는"),
    ("센텐을", "센텐스를"),
    ("센텐즈다", "센텐스다"),
    ("센텐즈가", "센텐스가"),
    ("센텐즈도", "센텐스도"),
    ("센텐들", "센텐스들"),
    ("센텐 ", "센텐스 "),  # bare attributive use before another noun
    # Centensian consistency (163 vs 3 majority; same family, not a separate
    # glossary row but an obvious typo against the dominant spelling)
    ("센텐시아 ", "센텐시안 "),
    ("센텐시아", "센텐시안"),
    # Peacekeeper -> 피스키퍼 (particle-aware; consonant-final 평화유지군 -> vowel-final 피스키퍼)
    ("평화유지군으로", "피스키퍼로"),
    ("평화유지군", "피스키퍼"),
    # Protectorate -> 보호국 (particle-aware; vowel-final 프로텍토레이트 -> consonant-final 보호국)
    ("프로텍토레이트를", "보호국을"),
    ("프로텍토레이트의", "보호국의"),
    ("프로텍토레이트처럼", "보호국처럼"),
    ("프로텍토레이트는", "보호국은"),
    ("프로텍토레이트", "보호국"),
    ("보호령의", "보호국의"),
    ("수호령의", "보호국의"),
    # Elithian Alliance -> 엘리시안 얼라이언스 (unambiguous compound phrase;
    # verified all 17 occurrences are genuinely "Elithian Alliance" context)
    ("엘리시아 동맹", "엘리시안 얼라이언스"),
    ("엘리시안 연합", "엘리시안 얼라이언스"),
    ("엘리시안 동맹", "엘리시안 얼라이언스"),
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
