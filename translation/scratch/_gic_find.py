# Find where the misplaced chunk-C translations actually belong in the uniq list.
import re, os

BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
en = {}
cur = None
for l in open(os.path.join(BASE, "scratch", "_gic_uniq.txt"), encoding="utf-8"):
    m = re.match(r"^### (\d+)", l.strip())
    if m:
        cur = int(m.group(1)); en[cur] = []
    elif cur is not None:
        en[cur].append(l.rstrip("\n"))
en = {k: "\n".join(v).strip("\n") for k, v in en.items()}
print("uniq:", len(en))

pats = ["Kettlebell", "Riverward", "Scrounger", "Support", "Marine", "Auxiliary",
        "Tag", "Executioner", "Carnage", "Frenzy", "Evasion", "Muscle", "Cocoon",
        "Brawler", "Star", "Damping", "Pyro", "Gladiator", "Smoke", "Disposable",
        "Final", "Iron", "Omamori", "Occult", "Investigator", "Heart", "Stigma",
        "Sphere", "Override", "Paraffin", "Feather", "Operators", "Manager"]
out = open(os.path.join(BASE, "scratch", "_gic_find.txt"), "w", encoding="utf-8")
for i in sorted(en):
    t = en[i]
    first = t.split("\n")[0][:110]
    if any(p.lower() in first.lower() for p in pats):
        out.write(f"{i}\t{first}\n")
out.close()
print("done")
