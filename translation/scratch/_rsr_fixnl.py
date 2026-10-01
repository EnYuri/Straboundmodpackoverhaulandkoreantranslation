# -*- coding: utf-8 -*-
# Collapse rsr_ko_*.tsv multi-line rows into single lines with literal \n.
import re

ROOT = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
BS = chr(92)

for fn in ["rsr_ko_01", "rsr_ko_02", "rsr_ko_03"]:
    path = f"{ROOT}/data/{fn}.tsv"
    src = open(path, encoding="utf-8").read().split("\n")
    rows = []
    cur = None
    for l in src:
        m = re.match(r"^(\d+)\t(.*)", l)
        if m:
            if cur is not None:
                rows.append(cur)
            cur = [m.group(1), m.group(2).rstrip("\r")]
        else:
            if cur is not None:
                cur[1] += "\n" + l.rstrip("\r")
            elif l.strip():
                print("ORPHAN", fn, l[:60])
    if cur is not None:
        rows.append(cur)
    out = []
    for k, (idx, val) in enumerate(rows):
        if k == len(rows) - 1:
            val = val.rstrip("\n")
        out.append(idx + "\t" + val.replace("\n", BS + "n"))
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print(fn, len(rows), "rows")
