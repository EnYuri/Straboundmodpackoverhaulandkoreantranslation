# -*- coding: utf-8 -*-
"""Twentieth fix batch (2026-09-29). Fresh qa_pak_glossary.py rescan against
the current installed pak (after batches 20-34 from other sessions plus this
session's batch17-19) surfaced 37 fixed-glossary violations, concentrated in
the `<raceid>Description` custom-race examine text written during the 23rd
campaign (which apparently didn't have the glossary loaded for every pass).

Method: exact-value (not blind substring) replacement per (asset, pointer),
built from the qa_pak_glossary_report.tsv + full korean text from
pak_pairs.tsv, so ambiguous common words (e.g. Cultivator's 경작자, which is
a legitimate generic word elsewhere; Shortsword's 단검, reserved for Dagger)
only get corrected in the exact flagged strings, not globally.

- Hylotl: 하일로틀 -> 하이로틀 (9 rows)
- Crafting Station: 작업대/제작 스테이션 -> 제작대 (5 rows)
- United Systems: 유나이티드 시스템즈 -> 연합 시스템 (5 rows)
- Grand Protector: 그랜드 프로텍터 -> 고위 수호자 (4 rows)
- Poptop: 팝탑 -> 팝톱 (3 rows)
- Miniknog: 미니노그 -> 미니크녹 (2 rows)
- Protectorate: 프로텍토레이트 -> 보호국 (2 rows)
- Cultivator: 경작자 -> 컬티베이터 (2 rows)
- Jorgasian: 조르가시안 -> 조가시안 (2 rows)
- Matter Manipulator: 매터 매니퓰레이터 -> 물질 조작기 (1 row)
- Shortsword: 단검 -> 소검 (1 row, scoped -- Dagger keeps 단검 elsewhere)
- Terrene Protectorate: 테렌 보호국 -> 행성 보호국 (1 row)
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
OUT_PAK = BASE / "backup_paks/female_translation.pak.NEW24"

TERM_FIX = {
    "하일로틀": "하이로틀",
    "메크 제작 스테이션": "메크 제작대",
    "유나이티드 시스템즈": "연합 시스템",
    "그랜드 프로텍터": "고위 수호자",
    "팝탑": "팝톱",
    "미니노그": "미니크녹",
    "프로텍토레이트": "보호국",
    "조르가시안": "조가시안",
    "매터 매니퓰레이터": "물질 조작기",
    "테렌 보호국": "행성 보호국",
}

# rows needing a scoped fix distinct from the generic TERM_FIX table above
SPECIAL = {
    ("/items/buildscripts/ct_mimics/tool.activeitem.patch", "/presets/railgun/altaDescription"):
        ("작업대 설계도", "제작대 설계도"),
    ("/objects/alta/crafting/constructor/ct_alta_constructor.object.patch", "/altaDescription"):
        ("이 작업대엔", "이 제작대엔"),
    ("/objects/biome/alterash_prime/phospholion/ct_phospholion_formation/ct_phospholion_formation.object.patch", "/altaDescription"):
        ("작업대에서", "제작대에서"),
    ("/objects/angel/angelhanginglightweapon2/angelhanginglightweapon2.object.patch", "/angelDescription"):
        ("엔젤 솔라리움 단검이야", "엔젤 솔라리움 소검이야"),
    ("/objects/atprk_ancient/atprk_ancientstatueprop/atprk_ancientcultivatorprop.object.patch", "/noolithDescription"):
        ("우리의 경작자여", "우리의 컬티베이터여"),
    ("/objects/atprk_breakable/atprk_ancientshardsstatue/atprk_ancientshardsstatue2.object.patch", "/noolithDescription"):
        ("우리의 경작자여", "우리의 컬티베이터여"),
}

data = json.loads((BASE / "_glossary_violation_full.json").read_text(encoding="utf-8"))

REPLACEMENTS = []  # (old_full_value, new_full_value)
for row in data:
    key = (row["asset"], row["pointer"])
    old = row["korean"]
    new = old
    if key in SPECIAL:
        frag_old, frag_new = SPECIAL[key]
        new = new.replace(frag_old, frag_new)
    else:
        for term_old, term_new in TERM_FIX.items():
            if term_old in new:
                new = new.replace(term_old, term_new)
    if new != old:
        REPLACEMENTS.append((old, new))
    else:
        print("NO CHANGE (check manually):", key, old[:80])

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
    matched = 0
    for old, needle in zip([r[0] for r in REPLACEMENTS], needles):
        if any(needle in files[n] for n in files if n.endswith(".patch")):
            matched += 1
        else:
            print("NEEDLE-MISS (source):", old[:80])
    print("needles matched:", matched, "/", len(REPLACEMENTS))

    assets_changed = 0
    for name in sorted(files):
        if not name.endswith(".patch"):
            continue
        data_b = files[name]
        if not any(n in data_b for n in needles):
            continue
        try:
            doc = json.loads(data_b)
        except Exception:
            continue
        new_doc, changed = replace_in_value(doc)
        if changed:
            files[name] = json.dumps(new_doc, ensure_ascii=False).encode("utf-8")
            assets_changed += 1

    buf = bytearray(b"SBAsset6" + b"\x00" * 8)
    index_entries = []
    for name in sorted(files):
        data_b = files[name]
        off = len(buf)
        buf += data_b
        index_entries.append((name.encode("utf-8"), off, len(data_b)))

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
