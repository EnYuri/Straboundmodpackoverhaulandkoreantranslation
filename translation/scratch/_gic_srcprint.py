# Print full EN for mismatched indices + correct newline comparison.
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

ko = {}
for l in open(os.path.join(BASE, "data", "gic_ko_02.tsv"), encoding="utf-8"):
    i, t = l.rstrip("\n").split("\t", 1)
    ko[int(i)] = t

# correct newline check: EN real newlines vs KO literal \n
nl_bad = [i for i in range(244, 526)
          if en.get(i, "").count("\n") != ko[i].count("\\n")]
print("newline mismatches:", nl_bad)

for i in [421, 425, 445, 457, 459, 463, 465, 469, 471, 473,
          477, 479, 481, 483, 485, 487, 493, 497, 503, 507,
          509, 513, 515, 517, 523, 525]:
    print(f"\n=== {i} ===")
    print("EN:", repr(en.get(i, "<none>"))[:700])
    print("KO:", repr(ko[i])[:400])
