"""Surgical fix for two genuine content-loss bugs found during the 2026-09-28
(5차) full-pak systematic context/tone QA pass (see docs/batch_log.md):

1. `/items/aichips/nonEKIaichip.item.patch` shipStatus 0-3: the translation
   pipeline kept only the "$ status" prompt-prefix line and silently dropped
   the entire following AI dialogue line(s) -- up to 5 real sentences lost
   per entry.
2. 8 object descriptions (7 `sb_techstation` species variants + 1
   `letheia_extra_21`) dropped the trailing "^red;Destroyed when broken."
   safety-warning sentence entirely.

Both are targeted find-and-replace against the exact known-bad `replace`
values (verified unique per asset via a prior read), so there is no risk of
touching unrelated content.
"""
import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

SRC_PAK = STAR / "mods" / "zz_translation_female.pak"
OUT_PAK = STAR / "translation" / "translation-baseline-20260921" / "female_translation.pak.NEW3"

AICHIP_ASSET = "/items/aichips/nonEKIaichip.item.patch"
AICHIP_FIXES = {
    "/aiData/shipStatus/0/text": (
        "^#6f6f6f;$ status ",
        "^#6f6f6f;$ 상태 \n^cyan;>음.. 저기, 배 좀 재부팅해줄 수 있어?",
    ),
    "/aiData/shipStatus/1/text": (
        "^#6f6f6f;$ 상태 ",
        "^#6f6f6f;$ 상태 \n^cyan;>그게, 지금 우리 배 상태가 영 안 좋아. "
        "^green;일단 궤도 도는 행성에 내려가서 좀 둘러보는 게 좋을 거야. "
        "^cyan;이 난장판을 고칠 만한 걸 찾을 수 있길 빌어보자.",
    ),
    "/aiData/shipStatus/2/text": (
        "^#6f6f6f;$ 상태 ",
        "^#6f6f6f;$ 상태 \n^cyan;>좋은 소식이야, 배는 최소한 날 수는 있어! \n"
        ">추진기는 문제없어. \n>배의 텔레포터도 작동해. \n"
        ">^green;이 성계 안에서는 어디든 갈 수 있지만, "
        "^cyan;FTL 드라이브를 고치기 전엔 성간 이동은 안 돼.",
    ),
    "/aiData/shipStatus/3/text": (
        "^#6f6f6f;$ 상태 ",
        "^#6f6f6f;$ 상태 \n^cyan;>또 왔네! 배는 평소처럼 상태 좋아. \n"
        ">추진기는 문제없어. \n>FTL 드라이브도 문제없어. \n"
        ">배의 텔레포터도 작동해. \n>이제 거의 ^green;우주 어디든 갈 수 있어!",
    ),
}

DESTROYED_ASSETS = [
    "/objects/letheiaobjectsexpanded/letheia_extra_21/letheia_extra_21.object.patch",
    "/objects/upgrade/sb_techstation/apex.object.patch",
    "/objects/upgrade/sb_techstation/avian.object.patch",
    "/objects/upgrade/sb_techstation/floran.object.patch",
    "/objects/upgrade/sb_techstation/glitch.object.patch",
    "/objects/upgrade/sb_techstation/human.object.patch",
    "/objects/upgrade/sb_techstation/hylotl.object.patch",
    "/objects/upgrade/sb_techstation/novakid.object.patch",
]
OLD_TECHSTATION_KO = "이 스테이션에서 기술을 장착하고 강화하세요."
NEW_TECHSTATION_KO = "이 스테이션에서 기술을 장착하고 강화하세요. ^red;파괴하면 부서집니다."


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


def fix_aichip(doc):
    changed = 0
    for group in doc:
        for op in group:
            if op.get("op") == "replace" and op.get("path") in AICHIP_FIXES:
                expected_old, new = AICHIP_FIXES[op["path"]]
                assert op["value"] == expected_old, (op["path"], op["value"])
                op["value"] = new
                changed += 1
    assert changed == len(AICHIP_FIXES), changed
    return doc


def fix_destroyed(doc):
    changed = 0
    for group in doc:
        for op in group:
            if op.get("op") == "replace" and op.get("path") == "/description":
                assert op["value"] == OLD_TECHSTATION_KO, op["value"]
                op["value"] = NEW_TECHSTATION_KO
                changed += 1
    assert changed == 1, changed
    return doc


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

    doc = json.loads(files[AICHIP_ASSET])
    doc = fix_aichip(doc)
    files[AICHIP_ASSET] = json.dumps(doc, ensure_ascii=False).encode("utf-8")
    print("fixed", AICHIP_ASSET)

    for asset in DESTROYED_ASSETS:
        doc = json.loads(files[asset])
        doc = fix_destroyed(doc)
        files[asset] = json.dumps(doc, ensure_ascii=False).encode("utf-8")
        print("fixed", asset)

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
    print("wrote", OUT_PAK, len(buf), "bytes,", len(index_entries), "entries")


if __name__ == "__main__":
    main()
