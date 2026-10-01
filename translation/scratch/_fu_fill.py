# Fill data/fu_work.tsv ko column from fu_ko*.tsv index maps (uniq first-seen
# order over todo rows, same as the extraction dump).
import csv
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
csv.field_size_limit(10 ** 8)

ko = {}
for f in ["data/fu_ko.tsv", "data/fu_ko2.tsv", "data/fu_ko3.tsv"]:
    for line in open(f, encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if len(p) == 2:
            ko[int(p[0])] = p[1]

rows = list(csv.reader(open("data/fu_work.tsv", encoding="utf-8"), delimiter="\t"))
todo = [r for r in rows[1:] if len(r) >= 4 and not r[3]]
uniq = []
seen = set()
for r in todo:
    if r[2] not in seen:
        seen.add(r[2])
        uniq.append(r[2])
print("todo:", len(todo), "uniq:", len(uniq), "ko:", len(ko))

idx = {en: i for i, en in enumerate(uniq)}
miss = []
for r in todo:
    k = ko.get(idx[r[2]])
    if k is None:
        miss.append(r[2][:50])
        continue
    r[3] = k.replace("\\n", "\n")
print("missing:", miss[:10])

with open("data/fu_work.tsv", "w", encoding="utf-8", newline="") as f:
    csv.writer(f, delimiter="\t").writerows(rows)
print("unfilled:", sum(1 for r in rows[1:] if len(r) >= 4 and not r[3]))
