import csv

files = [
    "glitch_rewrite_1_output.tsv",
    "glitch_rewrite_2_output.tsv",
    "glitch_rewrite_3_output.tsv",
    "novakid_rewrite_1_output.tsv",
    "novakid_rewrite_2_output.tsv",
]

mapping = {}
conflicts = []
rows_total = 0
noop = 0
for fn in files:
    with open(fn, encoding="utf-8-sig") as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            rows_total += 1
            old = row["old_korean"]
            new = row["new_korean"]
            if old == new:
                noop += 1
                continue
            if old in mapping and mapping[old] != new:
                conflicts.append((old, mapping[old], new, fn))
            else:
                mapping[old] = new

print("rows total:", rows_total)
print("noop (old==new):", noop)
print("unique old->new pairs:", len(mapping))
print("conflicts:", len(conflicts))
for c in conflicts[:20]:
    print("CONFLICT:", repr(c[0][:40]), "->", repr(c[1][:40]), "vs", repr(c[2][:40]), "in", c[3])

with open("_consolidated_rewrite_pairs.tsv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["old_korean", "new_korean"])
    for old, new in mapping.items():
        w.writerow([old, new])
print("wrote _consolidated_rewrite_pairs.tsv")
