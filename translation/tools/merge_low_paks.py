"""Merge the 4 zz_localeko_*_low_20260927.pak overlays into mods/zz_translation_female.pak,
per README's "new translations must be unified into female_translation.pak" convention.

Verified beforehand: for every path shared between female_translation.pak and the 4 low
paks, the two sides' .patch documents touch disjoint JSON pointers (different race-specific
description fields on the same object/item file) -- zero pointer-level overlap across 1558
shared paths. So merging is safe as list-concatenation of patch-groups (each .patch is a
list of independent [{test,...},{replace,...}] groups); no group is ever replaced or dropped.

Safety: writes to a new file first; caller must verify then swap in place.
"""
import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

SRC_PAK = STAR / "mods" / "zz_translation_female.pak"
OUT_PAK = STAR / "translation" / "translation-baseline-20260921" / "female_translation.pak.NEW2"

LOW_PAKS = [
    "zz_localeko_elithian_low_20260927",
    "zz_localeko_krakoth_low_20260927",
    "zz_localeko_nuggubs_low_20260927",
    "zz_localeko_plushbound_low_20260927",
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


def merge_patch(base_bytes, add_bytes):
    a = json.loads(base_bytes)
    b = json.loads(add_bytes)
    assert isinstance(a, list) and all(isinstance(g, list) for g in a)
    assert isinstance(b, list) and all(isinstance(g, list) for g in b)
    merged = a + b
    return json.dumps(merged, ensure_ascii=False).encode("utf-8")


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

    merged, added = 0, 0
    for name in LOW_PAKS:
        p = Pak(str(STAR / "mods" / f"{name}.pak"))
        for key in p.index:
            data = p.read(key)
            if key in files:
                files[key] = merge_patch(files[key], data)
                merged += 1
            else:
                files[key] = data
                added += 1
    print("merged (pointer-disjoint concat):", merged, "newly added:", added)

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
    print("wrote", OUT_PAK, len(buf), "bytes,", len(index_entries), "entries")


if __name__ == "__main__":
    main()
