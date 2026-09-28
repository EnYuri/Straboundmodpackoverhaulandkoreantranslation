"""Minimal SBAsset6 writer that clones an existing pak's file table, applying
overrides/additions, and reuses its INDEX metadata blob verbatim.
Mirrors the binary-format logic in build_pak.py (VLQ + dynval parsing).
"""
import os
import struct
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pak import Pak


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
    raise ValueError(f"dynval type {t:#x} at {p-1}")


def _vlq(n):
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


def load_meta_blob(pak_path):
    d0 = open(pak_path, "rb").read()
    off0 = struct.unpack(">Q", d0[8:16])[0]
    assert d0[off0:off0 + 5] == b"INDEX"
    p = off0 + 5
    pairs, p = _vlqr(d0, p)
    for _ in range(pairs):
        p = _key(d0, p)
        p = _val(d0, p)
    return d0[off0:p]


def write_pak(out_path, base_pak_path, overrides):
    """overrides: dict of '/rel/path' -> bytes, replacing or adding entries.
    All other entries are cloned verbatim from base_pak_path."""
    meta_blob = load_meta_blob(base_pak_path)
    p = Pak(base_pak_path)
    files = {}
    for name in p.index:
        files[name] = p.read(name)
    files.update(overrides)
    del p  # release the read handle before we may overwrite base_pak_path

    buf = bytearray(b"SBAsset6" + b"\x00" * 8)
    index_entries = []
    for name in sorted(files):
        data = files[name]
        off = len(buf)
        buf += data
        index_entries.append((name.encode("utf-8"), off, len(data)))

    index_off = len(buf)
    buf += meta_blob
    buf += _vlq(len(index_entries))
    for name, off, n in index_entries:
        buf += _vlq(len(name)) + name + struct.pack(">QQ", off, n)
    buf[8:16] = struct.pack(">Q", index_off)

    tmp_path = str(out_path) + ".tmp_write"
    with open(tmp_path, "wb") as f:
        f.write(bytes(buf))
    os.replace(tmp_path, out_path)
    return len(files)
