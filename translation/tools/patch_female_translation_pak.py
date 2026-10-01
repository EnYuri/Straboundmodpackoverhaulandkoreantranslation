"""Surgically refresh mods/zz_translation_female.pak with the current, de-corrupted
content of translation/_archive/translation-overlays-20260921/source-v3/{localeko_gic_legacy,
localeko_black_armory_legacy,localeko_extended_story_legacy}, WITHOUT needing
the missing E:/pakx staging tree. Every other entry in the pak (sbkor, fuko,
postload, etc.) is carried over byte-for-byte unchanged.

Safety: writes to a new file first; caller must verify then swap in place.
"""
import os
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak, rvu, rstr  # noqa: E402

SRC_PAK = STAR / "mods" / "zz_translation_female.pak"
OUT_PAK = STAR / "translation" / "translation-baseline-20260921" / "female_translation.pak.NEW"

V3 = STAR / "translation" / "_archive" / "translation-overlays-20260921" / "source-v3"
OVERLAY_DIRS = [
    "localeko_gic_legacy",
    "localeko_black_armory_legacy",
    "localeko_extended_story_legacy",
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


def main():
    d0 = SRC_PAK.read_bytes()
    off0 = struct.unpack(">Q", d0[8:16])[0]
    assert d0[off0:off0 + 5] == b"INDEX"
    p = off0 + 5
    pairs, p = _vlqr(d0, p)
    for _ in range(pairs):
        p = _key(d0, p)
        p = _val(d0, p)
    meta_blob = d0[off0:p]  # 'INDEX' + complete metadata dynval, byte-identical

    src = Pak(str(SRC_PAK))
    files = {name: src.read(name) for name in src.index}
    print("base pak entries:", len(files))

    overridden, added = 0, 0
    for d in OVERLAY_DIRS:
        base = V3 / d
        for root, _, fs in os.walk(base):
            for f in fs:
                full = Path(root) / f
                rel = full.relative_to(base).as_posix()
                key = "/" + rel
                data = full.read_bytes()
                if key in files:
                    if files[key] != data:
                        overridden += 1
                else:
                    added += 1
                files[key] = data
    print("overridden:", overridden, "newly added:", added)

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
