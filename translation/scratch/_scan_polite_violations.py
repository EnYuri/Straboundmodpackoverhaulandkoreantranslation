import csv
import re

rows = []
with open("archive/glitch_novakid_all.tsv", encoding="utf-8-sig") as f:
    r = csv.DictReader(f, delimiter="\t")
    for row in r:
        rows.append(row)
print("total", len(rows))


def tail(s, n=12):
    s2 = re.sub(r"\^[a-zA-Z#0-9]*;", "", s)
    return s2.strip()[-n:]


polite_pat = re.compile(r"(요|죠|니다|시죠|세요|나요|가요|던가요|군요)[.!?]?\s*$")

glitch_viol = []
novakid_viol = []
for row in rows:
    ko = row["korean"]
    t = tail(ko, 12)
    if not t:
        continue
    is_glitch = "glitchdescription" in row["pointer"].lower()
    if polite_pat.search(t):
        if is_glitch:
            glitch_viol.append(row)
        else:
            novakid_viol.append(row)

print("glitch violations (heuristic):", len(glitch_viol))
print("novakid violations (heuristic):", len(novakid_viol))

with open("archive/glitch_polite_violations.tsv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["asset", "pointer", "korean"])
    for r in glitch_viol:
        w.writerow([r["asset"], r["pointer"], r["korean"]])

with open("archive/novakid_polite_violations.tsv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["asset", "pointer", "korean"])
    for r in novakid_viol:
        w.writerow([r["asset"], r["pointer"], r["korean"]])
