# -*- coding: utf-8 -*-
"""Twenty-third fix batch (2026-09-29). Follow-up to batch22: the unit-mismatch
scan (EN/KO %-unit token comparison across all 186,213 non-blank pak_pairs.tsv
rows, `_struct_unit_mismatch.tsv`) surfaced the SAME "MJ" unit-loss bug in
three more mech-assembly GUI config patches that batch22 didn't touch (batch22
fixed only arcana_mechassemblygui.config.patch). All four assets share the
identical EN source "Energy: %d MJ" but were each authored as separate patch
files, so the same translation slip was repeated independently in each.
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
OUT_PAK = BASE / "female_translation.pak.NEW27"

TARGETS = [
    "/interface/scripted/sgspidermechstation/sgspidermechstation.config.patch",
    "/interface/scripted/xscm_config/_mechassemblygui.config.patch",
    "/interface/scripted/xscm_config/xscm_config_gui.config.patch",
]
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

    assets_changed = 0
    for name in TARGETS:
        data = files[name]
        doc = json.loads(data)
        changed = False
        for group in doc:
            for op in group:
                if op.get("op") == "replace" and op.get("path") == TARGET_POINTER:
                    assert op["value"] == OLD_VALUE, (name, op["value"])
                    op["value"] = NEW_VALUE
                    changed = True
        assert changed, name
        files[name] = json.dumps(doc, ensure_ascii=False).encode("utf-8")
        assets_changed += 1
        print("fixed", name)

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
    print("assets changed:", assets_changed)
    print("wrote", OUT_PAK, len(buf), "bytes,", len(index_entries), "entries")


if __name__ == "__main__":
    main()
