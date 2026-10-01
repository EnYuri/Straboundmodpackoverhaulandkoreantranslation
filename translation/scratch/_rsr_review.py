# -*- coding: utf-8 -*-
import json

ROOT = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
uniq = {int(k): v for k, v in json.load(open(f"{ROOT}/data/rsr_uniq.json", encoding="utf-8")).items()}
ko = {}
for fn in ["rsr_ko_01", "rsr_ko_02", "rsr_ko_03"]:
    for l in open(f"{ROOT}/data/{fn}.tsv", encoding="utf-8"):
        if not l.strip():
            continue
        i, t = l.split("\t", 1)
        ko[int(i)] = t.rstrip("\n")

out = open(f"{ROOT}/scratch/_rsr_review.txt", "w", encoding="utf-8")
for i in sorted(uniq):
    out.write(f"===== {i} =====\nEN: {uniq[i]}\nKO: {ko[i]}\n\n")
out.close()
print("written", len(uniq))
