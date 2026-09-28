import csv
import re
from collections import Counter

prefixes = Counter()
with open("glitch_polite_violations.tsv", encoding="utf-8-sig") as f:
    r = csv.DictReader(f, delimiter="\t")
    for row in r:
        ko = row["korean"]
        ko2 = re.sub(r"\^[a-zA-Z#0-9]*;", "", ko).strip()
        m = re.match(r"^([^.!?]{1,20}[.!?])\s*", ko2)
        if m:
            prefixes[m.group(1)] += 1
        else:
            prefixes["<NO-MATCH>: " + ko2[:20]] += 1

with open("_glitch_prefixes_out.txt", "w", encoding="utf-8") as f:
    for p, c in prefixes.most_common(150):
        f.write(f"{c}\t{p}\n")
print("wrote _glitch_prefixes_out.txt, unique prefixes:", len(prefixes))
