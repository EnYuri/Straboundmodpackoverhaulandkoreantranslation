# -*- coding: utf-8 -*-
# Restore orange DEPLOYMENT ORDER emphasis lost in KO rows.
import json, re

ROOT = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
uniq = {int(k): v for k, v in json.load(open(ROOT + "/data/rsr_uniq.json", encoding="utf-8")).items()}

files = ["rsr_ko_01", "rsr_ko_02", "rsr_ko_03"]
data = {}
for fn in files:
    rows = {}
    for l in open(f"{ROOT}/data/{fn}.tsv", encoding="utf-8"):
        if not l.strip():
            continue
        i, t = l.split("\t", 1)
        rows[int(i)] = t.rstrip("\n")
    data[fn] = rows

# For every EN row containing 'DEPLOYMENT ORDER' inside a colored line,
# ensure KO keeps the ^reset;^orange;...^reset; <color>; sequence.
pat_en = re.compile(r"(\^#[0-9A-Fa-f]{6};)[^\n]*?when using a \^reset;\^orange;DEPLOYMENT ORDER\^reset;")
fixed = []
for i, en in uniq.items():
    if "DEPLOYMENT ORDER" not in en:
        continue
    for fn in files:
        if i not in data[fn]:
            continue
        ko = data[fn][i]
        if "^orange;" in ko:
            continue  # already preserved
        m = pat_en.search(en)
        color = m.group(1) if m else None
        # KO pattern: '<배치 명령> 사용 시 ' appears mid-line; wrap term in orange.
        if color:
            new = ko.replace("배치 명령 사용 시", f"^reset;^orange;배치 명령^reset; {color}사용 시", 1)
        else:
            new = ko
        if new != ko:
            data[fn][i] = new
            fixed.append((i, color))

for fn in files:
    with open(f"{ROOT}/data/{fn}.tsv", "w", encoding="utf-8", newline="\n") as f:
        for i in sorted(data[fn]):
            f.write(f"{i}\t{data[fn][i]}\n")

print("fixed:", fixed)
