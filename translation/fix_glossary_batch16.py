# -*- coding: utf-8 -*-
"""Sixteenth fix batch (2026-09-28). Small confirmed follow-ups accumulated
during the dialog review passes; each item was verified against corpus
dominant forms before inclusion.

- Seeker of Dust -> 먼지 탐구자 (codex title canonical): 시커 오브 더스트,
  더스트 탐구자, 먼지의 추격자, 먼지의 탐구자 unified (11 strings).
- dunebun -> 사구빵 (dune+bun pun, hotbrodstand established): 둔벙/듄번
  variants unified (6 strings incl. Crawler Dunebun item+quest).
- Flare Catapult -> 플레어 카타펄트 (matches batch12 GDI 카타펄트 fix;
  투석기 is a siege engine, wrong for a handheld launcher).
- [CORPORATE KAPPA TRAIT] / [CORPORATE KAPPA] bracket tags translated
  -> [기업 캇파 특성] / [기업 캇파] (Kappa->캇파 dominant 66).
- Miniknog Stronghold -> 미니크녹 요새 (quest canonical name; AI-chip
  지식부 요새 aligned). Other 지식부 uses kept -- intentional localization
  of the Ministry pun, not an error.
- Glitch emotion-prefix noun rule leftovers: Observative/Observative-ish
  관찰함/관찰력 있음/관찰력 -> 관찰; Amiable 우호적 -> 우호. Mid-sentence
  adjectives (우호적인 생물 etc.) untouched.
"""

import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

BASE = Path(__file__).parent
SRC_PAK = STAR / "mods" / "female_translation.pak"
OUT_PAK = BASE / "female_translation.pak.NEW20"

REPLACEMENTS = [
    # Seeker of Dust -> 먼지 탐구자 (codex title canonical)
    ("시커 오브 더스트", "먼지 탐구자"),
    ("더스트 탐구자", "먼지 탐구자"),
    ("먼지의 추격자", "먼지 탐구자"),
    ("먼지의 탐구자", "먼지 탐구자"),
    # dunebun -> 사구빵
    ("둔벙", "사구빵"),
    ("듄번", "사구빵"),
    # Flare Catapult -> 플레어 카타펄트
    ("플레어 투석기", "플레어 카타펄트"),
    # corporate kappa bracket tags
    ("[CORPORATE KAPPA TRAIT]", "[기업 캇파 특성]"),
    ("[CORPORATE KAPPA]", "[기업 캇파]"),
    # Miniknog Stronghold -> 미니크녹 요새 (AI chips only)
    ("지식부 요새", "미니크녹 요새"),
    # glitch emotion prefix noun-rule leftovers
    ("관찰함. 이 장난감에", "관찰. 이 장난감에"),
    ("우호적. 승무원", "우호. 승무원"),
    ("관찰력 있음. 이 봉제", "관찰. 이 봉제"),
    ("관찰력. 이 인형에", "관찰. 이 인형에"),
    ("관찰력. 라벨에는", "관찰. 라벨에는"),
    ("관찰력. 이 특이한", "관찰. 이 특이한"),
    # glossary fixed-term leftovers surfaced by the batch QA report
    ("미니크노그", "미니크녹"),
    ("FTL 드라이브 연료 주입구", "FTL 드라이브 연료 해치"),
    ("타격 보호막 1 획득", "피격 방패 1 획득"),
    ("[Corpo Kappa]", "[기업 캇파]"),
    # Miniknog faction -> 미니크녹 (glossary fixed); 지식부 was an
    # intentional ministry-pun localization but violates the fixed term.
    # particle-aware needles first (미니크녹 has final consonant)
    ("지식부가 ", "미니크녹이 "),
    ("지식부만이", "미니크녹만이"),
    ("지식부들이", "미니크녹들이"),
    ("지식부라면", "미니크녹이라면"),
    ("지식부의", "미니크녹의"),
    ("지식부는", "미니크녹은"),
    ("지식부를", "미니크녹을"),
    ("지식부", "미니크녹"),
    # particle residue from the 미니크노그->미니크녹 pass
    ("미니크녹가", "미니크녹이"),
    ("미니크녹를", "미니크녹을"),
    ("미니크녹는", "미니크녹은"),
    ("미니크녹와", "미니크녹과"),
    ("미니크녹로", "미니크녹으로"),
    # Hit Shield -> 피격 방패 (glossary fixed) remaining uses
    ("타격 보호막", "피격 방패"),
]

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


def replace_in_value(v):
    if isinstance(v, str):
        out = v
        for old, new in REPLACEMENTS:
            if old in out:
                out = out.replace(old, new)
        return out, out != v
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

    needles = [json.dumps(old, ensure_ascii=False)[1:-1].encode("utf-8")
               for old, _ in REPLACEMENTS]
    for old, needle in zip([r[0] for r in REPLACEMENTS], needles):
        if not any(needle in files[n] for n in files if n.endswith(".patch")):
            print("NEEDLE-MISS (source):", old[:80])
    assets_changed = 0
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
