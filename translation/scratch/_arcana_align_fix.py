# Fix index-misaligned arcana KO entries: correct data/arcana_ko.tsv, refresh
# data/arcana_work.tsv ko cells, and rewrite the applied patch replace values.
import csv
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, "tools")
csv.field_size_limit(10 ** 8)

from pak import Pak  # noqa: E402
from pak_writer import write_pak  # noqa: E402

DEPLOY = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
NL = chr(10)

FIX = {
    458: "제자 리더 바지",
    459: "해방자 슈트",
    460: "호라이즌 해방자용 전체 중갑. " + "\\n\\n" + "^orange;세트 보너스:^reset; " + "\\n" + "^green;+3% 전기 저항·+3% 독 저항 부여.^reset;",
    166: "아주르 팔",
    167: "장식용 아주르 가지.",
    168: "아주르 팔",
}
for i, v in FIX.items():
    FIX[i] = v.replace("\\n", NL)

# rebuild uniq EN order from the dump
import re
uniq = {}
cur = None
buf = []
for line in open("scratch/_arcana_uniq.txt", encoding="utf-8"):
    m = re.match(r"### (\d+) x(\d+)", line)
    if m:
        if cur is not None:
            uniq[cur] = NL.join(buf).rstrip(NL)
        cur = int(m.group(1))
        buf = []
    else:
        buf.append(line.rstrip(NL))
uniq[cur] = NL.join(buf).rstrip(NL)

en_by_idx = {i: uniq[i] for i in FIX}
old_ko = {}
ko_lines = open("data/arcana_ko.tsv", encoding="utf-8").read().splitlines()
for n, l in enumerate(ko_lines):
    p = l.split("\t")
    if len(p) == 2 and int(p[0]) in FIX:
        old_ko[int(p[0])] = p[1]
        ko_lines[n] = p[0] + "\t" + FIX[int(p[0])].replace(NL, "\\n")
open("data/arcana_ko.tsv", "w", encoding="utf-8").write(NL.join(ko_lines) + NL)
print("ko fixed:", {i: old_ko[i] for i in FIX})

# update work TSV + collect per-patch new values (work TSV and pak both hold
# real newlines now; old_ko from the map file holds literal backslash-n)
old_nl = {i: old_ko[i].replace("\\n", NL) for i in FIX}
rows = list(csv.reader(open("data/arcana_work.tsv", encoding="utf-8"), delimiter="\t"))
targets = {}  # patch name -> [(old, new)]
for r in rows[1:]:
    if len(r) < 4 or not r[3]:
        continue
    for i, en in en_by_idx.items():
        if r[2] == en and r[3] == old_nl[i]:
            r[3] = FIX[i]
            targets.setdefault(r[0] + ".patch", []).append((old_nl[i], FIX[i]))
with open("data/arcana_work.tsv", "w", encoding="utf-8", newline="") as f:
    csv.writer(f, delimiter="\t").writerows(rows)
print("patch files to fix:", len(targets))

p = Pak(DEPLOY)
overrides = {}
for pn, pairs in targets.items():
    doc = json.loads(p.read(pn))

    def walk(node):
        if isinstance(node, dict):
            for old, new in pairs:
                if node.get("op") == "replace" and node.get("value") == old:
                    node["value"] = new
        elif isinstance(node, list):
            for x in node:
                walk(x)
    walk(doc)
    overrides[pn] = json.dumps(doc, ensure_ascii=False).encode("utf-8")
    print("fixed", pn[-60:])

try:
    print("entries:", write_pak(DEPLOY, DEPLOY, overrides))
except PermissionError:
    print("locked; tmp entries:", len(Pak(DEPLOY + ".tmp_write").index))
    sys.exit(3)
