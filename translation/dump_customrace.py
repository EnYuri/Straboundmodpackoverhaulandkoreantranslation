import csv, glob, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
UNIQ = HERE / "translations" / "customrace_unique.tsv"

done = set()
for f in glob.glob(str(HERE / "translations" / "customrace_batch_*.tsv")):
    with open(f, encoding="utf-8-sig", newline="") as fh:
        for row in csv.reader(fh, delimiter="\t"):
            if row and row[0].isdigit():
                done.add(int(row[0]))

rows = list(csv.DictReader(open(UNIQ, encoding="utf-8-sig", newline=""), delimiter="\t"))
remaining = [r for r in rows if int(r["id"]) not in done]
remaining.sort(key=lambda r: -int(r["count"]))
print(f"# total unique: {len(rows)}, done: {len(done)}, remaining: {len(remaining)}", file=sys.stderr)

count = int(sys.argv[1]) if len(sys.argv) > 1 else 80
for r in remaining[:count]:
    print(f"{r['id']}\t{r['race']}\t{r['count']}\t{r['asset']}\t{r['english']}")
