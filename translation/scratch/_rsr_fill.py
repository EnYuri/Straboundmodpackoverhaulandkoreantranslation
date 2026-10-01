# -*- coding: utf-8 -*-
# Fill rsr_work.tsv ko column from rsr_ko_*.tsv (uniq EN -> KO, literal \n -> real NL).
import csv, json

ROOT = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
uniq = {int(k): v for k, v in json.load(open(f"{ROOT}/data/rsr_uniq.json", encoding="utf-8")).items()}
ko_by_en = {uniq[i]: None for i in uniq}
ko_by_idx = {}
for fn in ["rsr_ko_01", "rsr_ko_02", "rsr_ko_03"]:
    for l in open(f"{ROOT}/data/{fn}.tsv", encoding="utf-8"):
        if not l.strip():
            continue
        i, t = l.split("\t", 1)
        ko_by_idx[int(i)] = t.rstrip("\n").replace("\\n", "\n")
ko_by_en = {uniq[i]: ko_by_idx[i] for i in uniq}

inp, outp = f"{ROOT}/data/rsr_work.tsv", f"{ROOT}/data/rsr_work_filled.tsv"
rows = list(csv.reader(open(inp, encoding="utf-8"), delimiter="\t"))
hit = miss = 0
for r in rows[1:]:
    if len(r) < 5:
        continue
    if r[3].strip():
        hit += 1  # reused
        continue
    v = ko_by_en.get(r[2])
    if v:
        r[3] = v
        hit += 1
    else:
        miss += 1
with open(outp, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerows(rows)
print("rows:", len(rows) - 1, "filled-or-reused:", hit, "still empty:", miss)
