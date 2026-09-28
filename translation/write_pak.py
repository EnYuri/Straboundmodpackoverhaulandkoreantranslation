#!/usr/bin/env python3
# Minimal SBAsset6 writer for a standalone translation overlay pak.
# Format reverse-engineered from pak.py's reader + build_pak.py's reuse of an
# existing metadata blob; this instead writes a fresh, self-contained one.
import struct, json


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


def _zigzag(n):
    return (n << 1) if n >= 0 else (((-n) - 1) << 1) | 1


def _wstr(s):
    b = s.encode("utf-8")
    return _vlq(len(b)) + b


def _wval(v):
    # type tags per pak.py's rjson: 1=null 2=double 3=bool 4=int 5=string 6=list 7=map
    if v is None:
        return bytes([1])
    if isinstance(v, bool):
        return bytes([3, 1 if v else 0])
    if isinstance(v, int):
        return bytes([4]) + _vlq(_zigzag(v))
    if isinstance(v, float):
        return bytes([2]) + struct.pack(">d", v)
    if isinstance(v, str):
        return bytes([5]) + _wstr(v)
    if isinstance(v, list):
        return bytes([6]) + _vlq(len(v)) + b"".join(_wval(x) for x in v)
    if isinstance(v, dict):
        return bytes([7]) + _vlq(len(v)) + b"".join(_wstr(k) + _wval(x) for k, x in v.items())
    raise TypeError(type(v))


def write_pak(out_path, files, meta):
    """files: {asset_path (leading '/'): bytes}. meta: dict, must include
    'name' and 'priority' at minimum."""
    buf = bytearray(b"SBAsset6" + b"\x00" * 8)
    index_entries = []
    for name in sorted(files):
        data = files[name]
        off = len(buf)
        buf += data
        index_entries.append((name.encode("utf-8"), off, len(data)))
    index_off = len(buf)
    buf += b"INDEX"
    buf += _vlq(len(meta))
    for k, v in meta.items():
        buf += _wstr(k) + _wval(v)
    buf += _vlq(len(index_entries))
    for name, off, n in index_entries:
        buf += _vlq(len(name)) + name + struct.pack(">QQ", off, n)
    buf[8:16] = struct.pack(">Q", index_off)
    with open(out_path, "wb") as fh:
        fh.write(bytes(buf))
    return len(buf), len(index_entries)


def patch_bytes(op_groups):
    """op_groups: list of lists-of-ops (each inner list = one atomic
    test+replace group), matching the [[..],[..]] convention used elsewhere
    in this project's overlay paks."""
    return json.dumps(op_groups, ensure_ascii=False, indent=2).encode("utf-8")
