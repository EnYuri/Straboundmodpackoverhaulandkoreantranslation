# -*- coding: utf-8 -*-
"""Twenty-first fix batch (2026-09-29). One content-mismatch bug found via a
new structural QA pass (^color; tag multiset comparison between EN and KO
across all 279,703 extracted pairs -- a bug class distinct from
qa_pak_context.py's natural-language heuristics).

/species/esc_realisticapex.species.patch /charCreationTooltip/description:
this custom race (a cosmetic "realistic" reskin of vanilla Apex) has its own
unique English lore text ("A race of highly intelligent primates. For
millennia, the Apex were close to human in appearance until a scientific
breakthrough allowed them to trade physical devolution for intellectual
evolution."), but the Korean value was a verbatim copy of vanilla
/species/apex.species.patch's value -- which itself has a BLANK English test
(the stat-block text there is this project's own added flavor for the base
Apex entry, not a translation of anything). Confirmed by finding the exact
Korean intro sentence duplicated only in these two assets. Fixed by
translating the real intro text (kept in the same 습니다체 register as the
reused Apex template) and leaving the stat block itself intact, since
"realistic Apex" is a pure visual reskin sharing Apex's actual game stats.
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
OUT_PAK = BASE / "backup_paks/female_translation.pak.NEW25"

OLD_VALUE = (BASE / "_realisticapex_full.txt").read_text(encoding="utf-8")
NEW_VALUE = (BASE / "_realisticapex_fixed.txt").read_text(encoding="utf-8")
assert OLD_VALUE != NEW_VALUE

REPLACEMENTS = [(OLD_VALUE, NEW_VALUE)]

print("total replacement pairs:", len(REPLACEMENTS))


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


REPL_MAP = dict(REPLACEMENTS)


def replace_in_value(v):
    if isinstance(v, str):
        if v in REPL_MAP:
            return REPL_MAP[v], True
        return v, False
    if isinstance(v, list):
        out = []
        changed = False
        for x in v:
            x, c = replace_in_value(x)
            out.append(x)
            changed = changed or c
        return out, changed
    if isinstance(v, dict):
        out = {}
        changed = False
        for k, x in v.items():
            x, c = replace_in_value(x)
            out[k] = x
            changed = changed or c
        return out, changed
    return v, False


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

    needles = [json.dumps(old, ensure_ascii=False)[1:-1].encode("utf-8") for old, _ in REPLACEMENTS]
    for old, needle in zip([r[0] for r in REPLACEMENTS], needles):
        if not any(needle in files[n] for n in files if n.endswith(".patch")):
            print("NEEDLE-MISS (source):", old[:80])
    assets_changed = 0
    TARGET_ASSET = "/species/esc_realisticapex.species.patch"
    for name in sorted(files):
        if name != TARGET_ASSET:
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
