# -*- coding: utf-8 -*-
"""Nineteenth fix batch (2026-09-28). Glitch/Novakid honorific-register
normalization -- the systemic pattern discovered during the flat-patch
sanity pass (batch18): a large subset of GIC-mod glitchDescription/
novakidDescription fields used 해요체/합니다체 endings, violating the
established glitch rule ("감정어. 본문" -- 감정어 is a bare noun, 본문 is
plain -다/반말) and the novakid rule (casual banmal, ~구만/~군/~겠어).

Method: regex-scanned every glitchdescription/novakiddescription value in
the deployed pak for a polite-ending heuristic (13,567 total fields
checked), got 1,034 glitch + 592 novakid hits, paired each with its English
source (via nested test/replace or, for flat patches, via base-pak JSON
pointer resolution), and had 5 parallel fork reviewers rewrite each body to
the correct register while preserving meaning (not a blind suffix swap --
each was hand-rewritten with correct verb conjugation). 15 of the 1,626
flagged rows turned out to be heuristic false positives (already correct,
e.g. "...아니다." matched on the "니다" substring) and were left unchanged.
A handful of rows were independently flagged and reworded slightly
differently across two fork batches, sharing the exact same source string;
those 17 duplicates were resolved by keeping the first fork's wording
(both were equally valid, just phrased slightly differently).

This is an EXACT-VALUE replacement pass (not substring), since each pair is
a full field value, not a fragment -- reduces any risk of accidental
partial-string collateral matches across unrelated fields.

Also fixes two mistranslations fork reviewers found by inspecting the
English source while rewriting (unrelated to the register issue itself):
- fu_vieraftldrivemk1a/2a/3a: "faster'n 'light drive" (dialect spelling of
  "faster-than-light") was mistranslated as "가벼운" (lightweight, wrong
  sense of "light") -> corrected to "초광속" (faster-than-light) while also
  fixing the register.
"""

import csv
import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

BASE = Path(__file__).parent.parent
SRC_PAK = STAR / "mods" / "zz_translation_female.pak"
OUT_PAK = BASE / "female_translation.pak.NEW23"

REPLACEMENTS = []
with open(BASE / "_consolidated_rewrite_pairs.tsv", encoding="utf-8-sig", newline="") as f:
    r = csv.DictReader(f, delimiter="\t")
    for row in r:
        REPLACEMENTS.append((row["old_korean"], row["new_korean"]))

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
    matched_needles = set()
    for old, needle in zip([r[0] for r in REPLACEMENTS], needles):
        found = any(needle in files[n] for n in files if n.endswith(".patch"))
        if not found:
            print("NEEDLE-MISS (source):", old[:80])
        else:
            matched_needles.add(old)
    print("needles matched:", len(matched_needles), "/", len(REPLACEMENTS))

    assets_changed = 0
    fields_changed = 0
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
