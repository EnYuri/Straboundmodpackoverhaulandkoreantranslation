#!/usr/bin/env python3
# Span-edit repack of Craftable_Seeds_FU_1.1_compat.pak: its /player.config.patch
# adds sapling blueprints via "/defaultBlueprints/tier1/-" (array append), so a
# positional overlay patch can't safely target them (same class of problem
# documented for NonEKI in HANDOFF.md). Replace the shortdescription strings
# in-place in the raw JSON text instead, byte-for-byte, leaving everything
# else (including array order/position) untouched.
import sys
sys.path.insert(0, "../../")
from pak import Pak
from write_pak import write_pak

SRC = "../../mods/Craftable_Seeds_FU_1.1_compat.pak"

REPLACEMENTS = [
    ('"shortdescription":"Bamboo Shoot Sapling"', '"shortdescription":"죽순 묘목"'),
    ('"shortdescription":"Banana Sapling"', '"shortdescription":"바나나 묘목"'),
    ('"shortdescription":"Bio Spore Sapling"', '"shortdescription":"바이오 홀씨 묘목"'),
    ('"shortdescription":"Coconut Sapling"', '"shortdescription":"코코넛 묘목"'),
    ('"shortdescription":"Flower Petal Sapling"', '"shortdescription":"꽃잎 묘목"'),
    ('"shortdescription":"Bio Sample Sapling"', '"shortdescription":"바이오 샘플 묘목"'),
    ('"shortdescription":"Nyani String Sapling"', '"shortdescription":"니아니 실 묘목"'),
    ('"shortdescription":"Peach Sapling"', '"shortdescription":"복숭아 묘목"'),
    ('"shortdescription":"Pearlfruit Sapling"', '"shortdescription":"진주과일 묘목"'),
    ('"shortdescription":"Pear Sapling"', '"shortdescription":"배 묘목"'),
    ('"shortdescription":"Putrid Slime Sapling"', '"shortdescription":"부패한 슬라임 묘목"'),
    ('"shortdescription":"Red Apple Sapling"', '"shortdescription":"빨간 사과 묘목"'),
    ('"shortdescription":"Shiny Crystal Sapling"', '"shortdescription":"반짝이는 크리스탈 묘목"'),
]

p = Pak(SRC)
text = p.read("/player.config.patch").decode("utf-8")
counts = {}
for en, ko in REPLACEMENTS:
    n = text.count(en)
    counts[en] = n
    text = text.replace(en, ko)

files = {}
for name in p.index:
    if name == "/player.config.patch":
        files[name] = text.encode("utf-8")
    else:
        files[name] = p.read(name)

meta = dict(p.meta)
meta["version"] = str(meta.get("version", "")) + "+ko20260927"

size, n = write_pak(SRC, files, meta)
print("wrote", size, "bytes,", n, "assets")
for en, c in counts.items():
    print(f"  {c:2d}x  {en}")
