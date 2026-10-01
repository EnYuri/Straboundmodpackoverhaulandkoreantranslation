# Compare tag counts EN vs KO for flagged indices.
import re, os

BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"

# parse uniq dump: lines like "=== NNN ===" then the text
en = {}
cur = None
for l in open(os.path.join(BASE, "scratch", "_gic_uniq.txt"), encoding="utf-8"):
    m = re.match(r"^=== (\d+) ===$", l.strip())
    if m:
        cur = int(m.group(1)); en[cur] = []
    elif cur is not None:
        en[cur].append(l.rstrip("\n"))
en = {k: "\n".join(v).strip("\n") for k, v in en.items()}
print("uniq entries:", len(en))

ko = {}
for l in open(os.path.join(BASE, "data", "gic_ko_02.tsv"), encoding="utf-8"):
    i, t = l.rstrip("\n").split("\t", 1)
    ko[int(i)] = t

tag = re.compile(r"\^[A-Za-z#][^;\s]*;")
FLAG = [363, 371, 377, 389, 399, 401, 417, 421, 425, 431]
for i in FLAG:
    e, k = en.get(i, "<MISSING>"), ko[i]
    et, kt = tag.findall(e.replace("\\n", " ")), tag.findall(k.replace("\\n", " "))
    print(f"--- {i} ---")
    print("EN tags:", et)
    print("KO tags:", kt)
    print("EN:", e[:200].replace("\\n", " | "))
