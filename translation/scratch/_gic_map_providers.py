# Map each gic_work asset to the provider pak/dir that contains it.
import csv, os, sys, glob
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\tools")
from pak import Pak

BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
MODS = r"E:\My Games\steamapps\common\Starbound\mods"

assets = set()
for r in csv.reader(open(os.path.join(BASE, "data", "gic_work.tsv"), encoding="utf-8"), delimiter="\t"):
    if r and r[0] != "asset":
        assets.add(r[0])
print("work assets:", len(assets))

providers = [os.path.join(MODS, f) for f in os.listdir(MODS)
             if "gic" in f.lower() or "galaxy_in_conflict" in f.lower()
             or "conflict" in f.lower()]
# also include the big workshop pak found in the survey
providers.append(os.path.join(MODS, "contents_2983581962.pak"))
# unpacked dirs
providers += [os.path.join(MODS, d) for d in os.listdir(MODS)
              if os.path.isdir(os.path.join(MODS, d))]

paks = {}
dir_prov = []
for p in providers:
    if p.endswith(".pak") and os.path.exists(p):
        try:
            paks[p] = set(Pak(p).index)
        except Exception as e:
            print("  unreadable pak:", p, e)
    elif os.path.isdir(p):
        dir_prov.append(p)

def in_dir(d, asset):
    return os.path.exists(os.path.join(d, asset.lstrip("/").replace("/", os.sep)))

mapping = {}
missing = []
for a in sorted(assets):
    hits = [p for p, idx in paks.items() if a in idx]
    hits += [d for d in dir_prov if in_dir(d, a)]
    if hits:
        mapping[a] = hits
    else:
        missing.append(a)

print("mapped:", len(mapping), "missing:", len(missing))
for m in missing[:15]:
    print("  MISSING", m)
from collections import Counter
c = Counter()
for a, hs in mapping.items():
    c[tuple(os.path.basename(h) for h in hs)] += 1
for k, v in c.most_common(12):
    print(v, k)
