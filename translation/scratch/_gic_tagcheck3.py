# Compare tag counts EN vs KO for all indices 244-525 using the full dump.
import re, os

BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"

en = {}
cur = None
for l in open(os.path.join(BASE, "scratch", "_gic_244_525.txt"), encoding="utf-8"):
    m = re.match(r"^=== (\d+) ===$", l.strip())
    if m:
        cur = int(m.group(1)); en[cur] = []
    elif cur is not None:
        en[cur].append(l.rstrip("\n"))
en = {k: "\n".join(v).strip("\n") for k, v in en.items()}
print("dump entries:", len(en))

ko = {}
for l in open(os.path.join(BASE, "data", "gic_ko_02.tsv"), encoding="utf-8"):
    i, t = l.rstrip("\n").split("\t", 1)
    ko[int(i)] = t

tag = re.compile(r"\^[A-Za-z#][^;\s]*;")
nl = re.compile(r"\\n")
mismatch = 0
for i in range(244, 526):
    e, k = en.get(i, ""), ko[i]
    et, kt = tag.findall(e), tag.findall(k)
    en_nl, ko_nl = len(nl.findall(e)), len(nl.findall(k))
    if et != kt or en_nl != ko_nl:
        mismatch += 1
        print(f"--- {i} ---")
        if et != kt:
            print("  EN tags:", et)
            print("  KO tags:", kt)
        if en_nl != ko_nl:
            print(f"  newlines EN={en_nl} KO={ko_nl}")
print("total mismatches:", mismatch)
