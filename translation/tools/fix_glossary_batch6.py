"""Sixth glossary-consistency batch fix (2026-09-28), continued after
batch2-5. Sourced from a re-run of qa_pak_glossary.py against pak_pairs.tsv
extracted post-batch5 (violations dropped 313 -> 305; these are newly
surfaced long-tail singletons from the Elithian Alliance banner family)."""
import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

SRC_PAK = STAR / "mods" / "zz_translation_female.pak"
OUT_PAK = STAR / "translation" / "translation-baseline-20260921" / "female_translation.pak.NEW10"

REPLACEMENTS = [
    # Aventor -> 아벤토르
    ("아벤터", "아벤토르"),
    # Hymidian Republic of Hyzolia -> 하이졸리아 하이미드 공화국
    ("하이졸리아 하이미디안 공화국", "하이졸리아 하이미드 공화국"),
    # Triple Monarchy -> 삼중 군주국
    ("삼중 군주 배너", "삼중 군주국 배너"),
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
