# -*- coding: utf-8 -*-
# Remove the extra ^reset; before ' |^reset;' (EN keeps reset only after the pipe).
ROOT = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
files = ["rsr_ko_01", "rsr_ko_02", "rsr_ko_03"]
for fn in files:
    path = f"{ROOT}/data/{fn}.tsv"
    rows = []
    for l in open(path, encoding="utf-8"):
        if not l.strip():
            continue
        i, t = l.split("\t", 1)
        rows.append((i, t.rstrip("\n")))
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for i, t in rows:
            t = t.replace("60초.^reset; |^reset;", "60초. |^reset;")
            f.write(f"{i}\t{t}\n")
print("done")
