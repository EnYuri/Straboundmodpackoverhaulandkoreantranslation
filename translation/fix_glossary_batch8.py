"""Eighth glossary-consistency batch fix (2026-09-28). User directive:
unify "Protector" to "수호자" as well (following the Grand Protector ->
"고위 수호자" change in batch7): "'프로텍터'도 '수호자'로 통일하죠."

Scope decisions:
- Bare "프로텍터" (57 hits) is overwhelmingly the vanilla Starbound player
  title ("Protector") used throughout Protectorate dialogue/quests/codex/
  item names -> unified to "수호자" via a blanket substring replace.
- Three families are protected from the blanket replace and left as-is
  because they are brand/product-style compounds, not the literal role
  title, and (for the Auto- family) need to stay consistent with sibling
  terms that are already transliterated:
  - "오토프로텍터" (Autoprotector) - sibling of 오토리펠러/오토애널라이저,
    both already transliterated; translating only this one would break
    that internal consistency.
  - "EDS 프로텍터" (EDS Protector, a defensive droid designation).
  - "테레네 프로텍터레이트" (Terrene Protectorate's own accepted glossary
    alternative, decided to keep as-is in batch4/7 investigation).
- Two "esc_componentcase" strings use "프로텍터레이트" (Protectorate, not
  Protector) with no "Protectorate" in the English source at all (translator
  flavor addition) - fixed directly to "보호국" per the existing Protectorate
  rule, since this isn't part of today's Protector-specific change.
- Bare "보호자" (rule=context 이전 선호형) needed individual, context-aware
  fixes rather than a blanket replace, because "보호자" is also the ordinary
  Korean word for "guardian/caretaker" used completely unrelated to the
  Protectorate storyline (alta NPC dialogue about a "caretaker", a plush
  "robotic caretaker" etc. - EN text confirms these say "caretaker", not
  "Protector", and must NOT be touched). Only instances whose English source
  says "Protector" are converted.
"""
import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

SRC_PAK = STAR / "mods" / "female_translation.pak"
OUT_PAK = STAR / "translation" / "translation-baseline-20260921" / "female_translation.pak.NEW12"

REPLACEMENTS = [
    # --- protect exceptions before the blanket "프로텍터" -> "수호자" pass ---
    ("테레네 프로텍터레이트", "@@KEEP_TERRENE_PROTECTORATE@@"),
    ("오토프로텍터", "@@KEEP_AUTOPROTECTOR@@"),
    ("EDS 프로텍터", "@@KEEP_EDS_PROTECTOR@@"),

    # --- two rogue "Protectorate" mistranslations unrelated to today's
    # Protector change (EN has no "Protectorate" at all; translator-added
    # flavor text using the wrong pre-existing term) ---
    ("프로텍터레이트에서 사용하는 작은 상자.", "보호국에서 사용하는 작은 상자."),
    ("프로텍터레이트 부품 상자", "보호국 부품 상자"),

    # --- bare "보호자" (context-checked against EN == "Protector", not
    # "caretaker") -> "수호자" ---
    ("어느 보호자의 기록", "어느 수호자의 기록"),
    ("보호자여", "수호자여"),
    ("데이터 보호자 인형", "데이터 수호자 인형"),
    ("보호자의 기록 - U5C3", "수호자의 기록 - U5C3"),
    ("보호자의 일지: 기록 ", "수호자의 일지: 기록 "),
    ("보호자? 다행이다!", "수호자? 다행이다!"),
    ("보호자? 적어도 한 명은", "수호자? 적어도 한 명은"),
    ("보호자^reset;구나", "수호자^reset;구나"),
    ("보호자가 되는 걸 꿈꿔왔어", "수호자가 되는 걸 꿈꿔왔어"),
    ("보호자들을 위한 설명이 가득한", "수호자들을 위한 설명이 가득한"),
    ("보호자가 되기 위한 독창적이고", "수호자가 되기 위한 독창적이고"),
    ("보호자를 위한 설명을 담고", "수호자를 위한 설명을 담고"),
    ("보호자를 위한 최초의 설명문", "수호자를 위한 최초의 설명문"),
    ("찢어진 보호자 초상화", "찢어진 수호자 초상화"),
    ("이 죽은 보호자는 아마", "이 죽은 수호자는 아마"),
    ("보호자의 가장 중요한 도구의 포스터", "수호자의 가장 중요한 도구의 포스터"),
    ("보호자라니... 요즘 보기 드문", "수호자라니... 요즘 보기 드문"),
    ("나의 가장 친한 보호자 친구", "나의 가장 친한 수호자 친구"),

    # --- blanket Protector -> 수호자 (safe now that exceptions are protected) ---
    ("프로텍터", "수호자"),

    # --- restore protected exceptions ---
    ("@@KEEP_TERRENE_PROTECTORATE@@", "테레네 프로텍터레이트"),
    ("@@KEEP_AUTOPROTECTOR@@", "오토프로텍터"),
    ("@@KEEP_EDS_PROTECTOR@@", "EDS 프로텍터"),
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


def replace_in_value(v):
    if isinstance(v, str):
        changed = False
        for old, new in REPLACEMENTS:
            if old in v:
                v = v.replace(old, new)
                changed = True
        return v, changed
    if isinstance(v, list):
        changed = False
        out = []
        for item in v:
            nv, c = replace_in_value(item)
            out.append(nv)
            changed = changed or c
        return out, changed
    if isinstance(v, dict):
        changed = False
        out = {}
        for k, item in v.items():
            nv, c = replace_in_value(item)
            out[k] = nv
            changed = changed or c
        return out, changed
    return v, False


def main():
    d0 = SRC_PAK.read_bytes()
    off0 = struct.unpack(">Q", d0[8:16])[0]
    assert d0[off0:off0 + 5] == b"INDEX"
    p = off0 + 5
    pairs, p = _vlqr(d0, p)
    for _ in range(pairs):
        p = _key(d0, p)
        p = _val(d0, p)
    meta_blob = d0[off0:p]

    src = Pak(str(SRC_PAK))
    files = {name: src.read(name) for name in src.index}
    print("base pak entries:", len(files))

    needles = [old.encode("utf-8") for old, _ in REPLACEMENTS]
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
