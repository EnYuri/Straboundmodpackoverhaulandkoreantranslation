#!/usr/bin/env python3
"""Repack mods_src/female_overhaul -> <Starbound>/mods/zz_female_overhaul.pak.

Case-preserving SBAsset6 writer (the stock asset_packer folds case on
Windows). The pak's INDEX metadata is built from the source tree's
`_metadata` JSON file; that file itself is not packed.

Usage: python tools/repack_overhaul.py [source_dir] [out_pak]
"""
import os, json, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STAR = "E:/My Games/steamapps/common/Starbound"
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "mods_src", "female_overhaul")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(STAR, "mods", "zz_female_overhaul.pak")


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


def wstr(s):
    b = s.encode("utf-8")
    return vlq(len(b)) + b


def wval(v):
    if v is None:
        return b"\x01"
    if isinstance(v, bool):
        return b"\x03" + (b"\x01" if v else b"\x00")
    if isinstance(v, float):
        return b"\x02" + struct.pack(">d", v)
    if isinstance(v, int):
        z = (v << 1) if v >= 0 else ((-v - 1) << 1) | 1
        return b"\x04" + vlq(z)
    if isinstance(v, str):
        return b"\x05" + wstr(v)
    if isinstance(v, list):
        return b"\x06" + vlq(len(v)) + b"".join(wval(x) for x in v)
    if isinstance(v, dict):
        return b"\x07" + vlq(len(v)) + b"".join(wstr(k) + wval(x) for k, x in v.items())
    raise TypeError(f"unsupported metadata value: {v!r}")


meta = json.load(open(os.path.join(SRC, "_metadata"), encoding="utf-8-sig"))
meta_blob = b"INDEX" + vlq(len(meta)) + b"".join(
    wstr(k) + wval(v) for k, v in meta.items())

files = {}
for root, _, fns in os.walk(SRC):
    for fn in fns:
        src = os.path.join(root, fn)
        rel = "/" + os.path.relpath(src, SRC).replace(os.sep, "/")
        if rel in ("/_metadata", "/_previewimage", "/preview.png"):
            continue
        files[rel] = open(src, "rb").read()

buf = bytearray(b"SBAsset6" + b"\x00" * 8)
entries = []
for name in sorted(files):
    data = files[name]
    entries.append((name.encode("utf-8"), len(buf), len(data)))
    buf += data

index_off = len(buf)
buf += meta_blob
buf += vlq(len(entries))
for name, off, n in entries:
    buf += vlq(len(name)) + name + struct.pack(">QQ", off, n)
buf[8:16] = struct.pack(">Q", index_off)

open(OUT, "wb").write(bytes(buf))
print(f"wrote {OUT}: {len(buf)} bytes, {len(entries)} entries")
