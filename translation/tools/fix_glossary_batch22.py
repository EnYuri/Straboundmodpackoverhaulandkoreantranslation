# -*- coding: utf-8 -*-
"""Twenty-second fix batch (2026-09-29). One content-loss bug found via a new
sbkor.tsv cross-reference QA pass against the main pak (join on byte-identical
English source text between pak_pairs.tsv and alignment/sbkor.tsv -- the same
method that found 17 real bugs in the NonEKI pass, run here against the main
pak for the first time; unlike NonEKI, the main pak is independently
translated so most of the 640 EN-matched rows are legitimate stylistic
divergence, not bugs -- filtered down to unit/placeholder-loss candidates by
regex, leaving exactly one genuine hit).

/interface/scripted/mechassembly/arcana_mechassemblygui.config.patch
/energyFormat: EN "Energy: %d MJ" -> pak Korean "에너지: %d" drops the "MJ"
unit entirely, while the sibling /drainFormat in the same asset correctly
keeps "MJ/s" ("사용량: %.02f MJ/s"). sbkor's own value for this EN string is
"에너지: %d MJ0" (a stray "0" typo, not usable verbatim), so fixed by simply
appending " MJ" to the pak's existing text rather than copying sbkor.
"""

import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

BASE = Path(__file__).parent.parent
SRC_PAK = STAR / "mods" / "zz_translation_female.pak"
OUT_PAK = BASE / "female_translation.pak.NEW26"

TARGET_ASSET = "/interface/scripted/mechassembly/arcana_mechassemblygui.config.patch"
TARGET_POINTER = "/energyFormat"
OLD_VALUE = "에너지: %d"
NEW_VALUE = "에너지: %d MJ"


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

    data = files[TARGET_ASSET]
    doc = json.loads(data)
    changed = False
    for group in doc:
        for op in group:
            if op.get("op") == "replace" and op.get("path") == TARGET_POINTER:
                assert op["value"] == OLD_VALUE, op["value"]
                op["value"] = NEW_VALUE
                changed = True
    assert changed
    files[TARGET_ASSET] = json.dumps(doc, ensure_ascii=False).encode("utf-8")

    buf = bytearray(b"SBAsset6" + b"\x00" * 8)
    index_entries = []
    for name in sorted(files):
        d = files[name]
        off = len(buf)
        buf += d
        index_entries.append((name.encode("utf-8"), off, len(d)))

    index_off = len(buf)
    buf += meta_blob
    buf += vlq(len(index_entries))
    for name, off, n in index_entries:
        buf += vlq(len(name)) + name + struct.pack(">QQ", off, n)
    buf[8:16] = struct.pack(">Q", index_off)

    OUT_PAK.write_bytes(bytes(buf))
    print("assets changed: 1")
    print("wrote", OUT_PAK, len(buf), "bytes,", len(index_entries), "entries")


if __name__ == "__main__":
    main()
