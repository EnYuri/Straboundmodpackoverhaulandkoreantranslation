# Rebuild gic_ko_02.tsv: A(244-335) + B(336-443) + C2(444-525), fix 421 reset tag.
import os

BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
D = os.path.join(BASE, "data")

rows = {}
for part in ["gic_ko_02a.tsv", "gic_ko_02b.tsv", "gic_ko_02c2.tsv"]:
    for l in open(os.path.join(D, part), encoding="utf-8"):
        i, t = l.rstrip("\n").split("\t", 1)
        rows[int(i)] = t

assert sorted(rows) == list(range(244, 526)), "index coverage broken"

# fix 421: trailing ^reset without semicolon
if rows[421].endswith("^reset"):
    rows[421] += ";"
    print("fixed 421")

with open(os.path.join(D, "gic_ko_02.tsv"), "w", encoding="utf-8") as f:
    for i in sorted(rows):
        f.write(f"{i}\t{rows[i]}\n")
print("rebuilt:", len(rows), "rows")
