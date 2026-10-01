import csv

rows = []
with open("archive/polite_violations_with_en.tsv", encoding="utf-8-sig") as f:
    r = csv.DictReader(f, delimiter="\t")
    for row in r:
        rows.append(row)

glitch = [r for r in rows if r["kind"] == "glitch"]
novakid = [r for r in rows if r["kind"] == "novakid"]
print("glitch", len(glitch), "novakid", len(novakid))


def chunk(lst, n):
    size = (len(lst) + n - 1) // n
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def write(fname, rows):
    with open(fname, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["kind", "asset", "pointer", "english", "korean"])
        for row in rows:
            w.writerow([row["kind"], row["asset"], row["pointer"], row["english"], row["korean"]])


for i, part in enumerate(chunk(glitch, 3), 1):
    write(f"glitch_rewrite_{i}.tsv", part)
    print(f"glitch_rewrite_{i}.tsv", len(part))

for i, part in enumerate(chunk(novakid, 2), 1):
    write(f"novakid_rewrite_{i}.tsv", part)
    print(f"novakid_rewrite_{i}.tsv", len(part))
