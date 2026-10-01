#!/usr/bin/env python3
"""Repair remaining structural defects in zz_translation_female.pak:

A) Fields where EN ends with a `^color;Type: X^reset;` suffix that KO
   dropped entirely -> re-append the translated type line.
B) Fields whose KO is a translation of a *different* string (rest-file
   id-drift residue): wrong item names, quest titles, set-bonus blocks.
   -> replace with correct translations keyed on the EN test value.
"""
import csv, io, json, os, re, sys, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:/My Games/steamapps/common/Starbound")
sys.path.insert(0, "tools")
import pak, sbjson, pak_writer

MODS = r"E:/My Games/steamapps/common/Starbound/mods"
TR = os.path.join(MODS, "zz_translation_female.pak")
csv.field_size_limit(10 ** 8)

TYPE_MAP = {
    "Fruit": "과일",
    "Vegetable": "야채",
    "Vegetables": "야채",
    "Vegetables + Dairy": "야채 + 유제품",
    "Robot Food": "로봇 음식",
    "Cooked Meat": "익힌 고기",
    "Cooked Seafood": "익힌 해산물",
    "Cooked Meat + Vegetables": "익힌 고기 + 야채",
    "Cooked Seafood + Vegetables": "익힌 해산물 + 야채",
    "Meaty Plant": "고기 식물",
    "Meaty Plant + Dairy": "고기 식물 + 유제품",
    "Dairy": "유제품",
}

# (asset suffix, pointer) -> full new KO value
FULL_FIX = {
    # --- Set Bonuses blocks (compat-injected description) ---
    ("r-prismatic.chest.patch", "/description"):
        "^orange;세트 보너스^reset;: \r\n^yellow;\ue024^reset; +^green;30^reset;% 방패 스태미나, 막기, 방패 재생\r\n^yellow;\ue024^reset; ^cyan;면역^reset;: 모든 냉기, 산소",
    ("r-prismatic.legs.patch", "/description"):
        "^orange;세트 보너스^reset;: \r\n^yellow;\ue024^reset; +^green;30^reset;% 방패 스태미나, 막기, 방패 재생\r\n^yellow;\ue024^reset; ^cyan;면역^reset;: 모든 냉기, 산소",
    ("r_impervious.chest.patch", "/description"):
        "^orange;세트 보너스^reset;: \r\n^yellow;\ue024^reset; +^green;35^reset;% 방패 스태미나, 막기, 방패 재생\r\n^yellow;\ue024^reset; ^cyan;면역^reset;: 치명적인 열기, 산, 화상, 산소, 가스, 압력",
    ("r_impervious.legs.patch", "/description"):
        "^orange;세트 보너스^reset;: \r\n^yellow;\ue024^reset; +^green;35^reset;% 방패 스태미나, 막기, 방패 재생\r\n^yellow;\ue024^reset; ^cyan;면역^reset;: 치명적인 열기, 산, 화상, 산소, 가스, 압력",
    # --- arcana crafting stations (wrong tier/name in KO) ---
    ("arcana_crafting_anvil_1.object.patch", "/shortdescription"): "^#9e6b55;기본 모루^reset;",
    ("arcana_crafting_cookingStation_2.object.patch", "/shortdescription"): "^#3ec7dd;기본 조리대^reset;",
    ("arcana_crafting_essenceExtractor_1.object.patch", "/shortdescription"): "^#9e6b55;목제 정수 추출기^reset;",
    ("arcana_crafting_furnace_2.object.patch", "/shortdescription"): "^#3ec7dd;아르카니움 용광로^reset;",
    ("arcana_crafting_main_1.object.patch", "/shortdescription"): "^#9e6b55;마법사의 작업대^reset;",
    ("arcana_crafting_techStation_3.object.patch", "/shortdescription"): "^#9e6b55;기본 테크 스테이션^reset;",
    ("arcana_crafting_workbench_2.object.patch", "/shortdescription"): "^#3ec7dd;아르카니움 작업대^reset;",
    ("mwhaddon_crafting_alchemist.object.patch", "/shortdescription"): "^#9e6b55;약제사의 작업대^reset;",
    # --- GiC Esther chapter titles ---
    ("gic_esther_chapter_4c_grandlibrarian.questtemplate.patch", "/title"): "^yellow;[GiC]: 그랜드 라이브러리언",
    ("gic_esther_chapter_4d_noblevampire.questtemplate.patch", "/title"): "^yellow;[GiC]: 귀족 뱀파이어",
    ("gic_esther_chapter_0_2_armsofgazring.questtemplate.patch", "/title"): "^yellow;[GiC]: 제0장 - 가즈링의 무장",
    ("gic_esther_chapter_1_1_fng.questtemplate.patch", "/title"): "^yellow;[GiC]: 제1장 - F.N.G",
    ("gic_esther_chapter_2_0_thekinless.questtemplate.patch", "/title"): "^yellow;[GiC]: 제2장 - 혈연 없는 자들",
    ("gic_esther_chapter_2_wud_birdhunting.questtemplate.patch", "/title"): "^yellow;[GiC]: 가즈리 - 태양의 눈",
    ("gic_esther_chapter_3_0_theotherworld.questtemplate.patch", "/title"): "^yellow;[GiC]: 제3장 - 저세상",
    ("gic_esther_chapter_4_0_eldestabode.questtemplate.patch", "/title"): "^yellow;[GiC]: 제4장 - 최연장자의 거처",
    ("gic_esther_chapter_5_0_division16.questtemplate.patch", "/title"): "^yellow;[GiC]: 제5장 - 16사단",
    ("gic_esther_chapter_6_0_luna.questtemplate.patch", "/title"): "^yellow;[GiC]: 제6장 - 루나",
    ("vierabootship.questtemplate.patch", "/title"): "^orange;숲을 깨우며...^reset;",
    ("vierawakeup.questtemplate.patch", "/title"): "^orange;어느 하루의 일상...^reset;",
}

rows = list(csv.DictReader(open("data/pak_pairs.tsv", encoding="utf-8-sig"), delimiter="\t"))
type_tail = re.compile(r"(\^[^;^\s]{1,20};)Type: ([^\^|]+?)\^reset;\s*$")

byfile = {}
for r in rows:
    e, k = r["english"], r["korean"]
    key = None
    for suf, ptr in FULL_FIX:
        if r["asset"].endswith(suf) and r["pointer"] == ptr:
            key = (suf, ptr)
            break
    if key:
        if k != FULL_FIX[key]:
            byfile.setdefault(r["asset"], []).append((r["pointer"], k, FULL_FIX[key]))
        continue
    m = type_tail.search(e)
    if m and "유형:" not in k:
        ko_type = TYPE_MAP.get(m.group(2).strip())
        if ko_type:
            nk = k.rstrip() + " " + m.group(1) + "유형: " + ko_type + "^reset;"
            byfile.setdefault(r["asset"], []).append((r["pointer"], k, nk))
        else:
            print("UNMAPPED TYPE:", m.group(2), r["asset"])

print("files:", len(byfile), "fields:", sum(len(v) for v in byfile.values()))
pk = pak.Pak(TR)
ov = {}
unmatched = []
for fn, lst in byfile.items():
    try:
        d = sbjson.parse_sb(pk.read(fn).decode("utf-8"))
    except Exception as ex:
        print("parse fail", fn, ex)
        continue
    want = {p: (old, new) for p, old, new in lst}
    n = 0
    def rec(o):
        global n
        if isinstance(o, list):
            for x in o:
                rec(x)
        elif isinstance(o, dict):
            if o.get("op") == "replace":
                p = o.get("path"); v = o.get("value")
                if p in want and isinstance(v, str) and v == want[p][0]:
                    o["value"] = want[p][1]; n += 1
            for x in o.values():
                if isinstance(x, (list, dict)):
                    rec(x)
    rec(d)
    if n:
        ov[fn] = json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if n < len(lst):
        unmatched.append((fn, n, len(lst)))
print("patched files:", len(ov), "| unmatched:", unmatched[:8])
del pk
if "--apply" in sys.argv and ov:
    staged = TR + ".staged"
    pak_writer.write_pak(staged, TR, ov)
    for i in range(60):
        try:
            os.replace(staged, TR)
            print("replaced")
            break
        except PermissionError:
            time.sleep(5)
else:
    print("dry-run")
