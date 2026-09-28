import csv
from collections import OrderedDict

groups = OrderedDict()
with open("glitch_rewrite_2.tsv", encoding="utf-8-sig") as f:
    r = csv.DictReader(f, delimiter="\t")
    for row in r:
        key = (row["english"], row["korean"])
        groups.setdefault(key, []).append(row)

print("total rows:", sum(len(v) for v in groups.values()))
print("unique EN/KO pairs:", len(groups))

with open("_glitch2_unique.tsv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["count", "english", "korean"])
    for (en, ko), v in sorted(groups.items(), key=lambda x: -len(x[1])):
        w.writerow([len(v), en, ko])
