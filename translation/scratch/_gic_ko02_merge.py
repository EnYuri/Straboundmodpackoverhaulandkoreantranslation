# Merge gic_ko_02a/b/c into gic_ko_02.tsv, substitute __EESTR__, verify coverage.
import re, os

BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
DATA = os.path.join(BASE, "data")
OUT = os.path.join(DATA, "gic_ko_02.tsv")

lines = []
for part in ("gic_ko_02a.tsv", "gic_ko_02b.tsv", "gic_ko_02c.tsv"):
    with open(os.path.join(DATA, part), encoding="utf-8") as f:
        lines.extend(f.read().splitlines())

# Substitute the ear-plug E-string placeholder (original EN is a very long
# "Eeeeee..." joke line; reproduce ~1000 chars of '이').
lines = [l.replace("__EESTR__", "이" * 1000) for l in lines]

with open(OUT, "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(lines) + "\n")

# ---- verification ----
idxs = []
for i, l in enumerate(lines, 1):
    parts = l.split("\t")
    assert len(parts) == 2, f"line {i}: {len(parts)} cols: {l[:80]!r}"
    idxs.append(int(parts[0]))

missing = [i for i in range(244, 526) if i not in idxs]
extra = [i for i in idxs if i < 244 or i > 525]
dups = sorted({i for i in idxs if idxs.count(i) > 1})
print(f"rows={len(idxs)} missing={missing} extra={extra} dups={dups}")
assert idxs == list(range(244, 526)), "index sequence mismatch"

# tag balance check on the KO column
tagpat = re.compile(r"\^[A-Za-z#][A-Za-z0-9#]*;")
for l in lines:
    i, ko = l.split("\t", 1)
    opens = len(re.findall(r"\^[^;]*;", ko))
    resets = ko.count("^reset;") + ko.count("^Reset;")
    print(f"{i}: opens={opens} resets={resets} " + ("MISMATCH" if opens != resets * 2 and opens != resets else ""))
print("done")
