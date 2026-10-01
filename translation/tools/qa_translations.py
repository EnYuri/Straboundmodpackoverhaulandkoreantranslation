"""QA pass over translation batches vs worklist_new.tsv.

Checks per entry:
  1. color tag preservation  (^name; / ^#hex; multiset must match source)
  2. bracket token preservation ([LMB], [SHIFT], {var}, <var>, %d ...)
  3. number preservation (every numeric token in source appears in target)
  4. newline count match
  5. untranslated (target identical to source)
  6. english remnants (latin words >=4 chars not in whitelist)

Writes qa_report.tsv and prints a summary.
"""
import csv, re, glob, io, sys

BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"

rows = list(csv.DictReader(open(f"{BASE}/data/worklist_new.tsv", encoding="utf-8-sig"), delimiter="\t"))
en = {i: rows[i]["englishText"] for i in range(len(rows))}

# load translations (multi-line values: an entry starts with "idx\t")
ko = {}
for f in glob.glob(f"{BASE}/translations/batch_*.tsv"):
    cur = None
    for line in open(f, encoding="utf-8"):
        line = line.rstrip("\n")
        m = re.match(r"^(\d+)\t(.*)$", line)
        if m:
            cur = int(m.group(1))
            ko[cur] = m.group(2)
        elif cur is not None:
            ko[cur] += "\n" + line

TAG = re.compile(r"\^([A-Za-z]+|#[0-9A-Fa-f]{2,8});")
BRACKET = re.compile(r"\[[A-Za-z0-9+_\-]+\]|\{[^}]{0,40}\}|%[ds]|&[a-z]+;")
NUM = re.compile(r"\d+(?:\.\d+)?%?")
# words allowed to stay latin in translations
WHITELIST = {w.lower() for w in """
HP DMG AP DPS NPC GiC GIC ES BA AYA BADA TAT WYM MV NR CA KH NF KO ML HC SHIP CRYPT BBR
MEMORY RAZED P S L X F W SHIFT ALT FIRE LMB RMB SOS IED USCM RPG XMG M1 AK Mk Mk1 Mk2 Mk3
Mk.1 Mk.2 Mk.3 UFO Kojiro Nazrin Nitori Tenshi Satori Julian Bowerbird Machinarius Wrexor
Nar Titansteel Akeman Fosse Sheruto Gazrian Dullahan Letheia Erchius Pericarpyx Protocite
Quietus Telebrium Zerchesium Lunari Prisilite Pristal Tritanium Gensidium Gen1 Gen2
Browning Bazooka Panzerfaust Slug AMMO MAG SNK SMG LMG DMR AR SR shotgun pistol rifle
Occasus Protectorate Miniknog Apex Avian Floran Glitch Hylotl Novakid Human Penguin
Esther Asra Nox Kluex SAIL FTL AI Mysterious Institute Vault Key Forge Encounter Telos
""".split()}

issues = []
def add(i, kind, detail):
    issues.append((i, kind, detail))

for i in range(6700):
    src, dst = en[i], ko.get(i)
    if dst is None:
        add(i, "MISSING", "")
        continue
    if dst.strip() == src.strip():
        add(i, "UNTRANSLATED", dst[:60])
        continue
    # 1. color tags
    st, dt = TAG.findall(src), TAG.findall(dst)
    if sorted(t.lower() for t in st) != sorted(t.lower() for t in dt):
        add(i, "TAG", f"src={st} dst={dt}")
    # 2. brackets/vars
    sb, db = BRACKET.findall(src), BRACKET.findall(dst)
    miss = [b for b in sb if b not in db]
    if miss:
        add(i, "BRACKET", f"missing={miss}")
    # 3. numbers
    sn = NUM.findall(src)
    dn = NUM.findall(dst)
    missn = [n for n in sn if n not in dn]
    if missn:
        add(i, "NUM", f"src missing={missn}")
    # 4. newlines
    if src.count("\n") != dst.count("\n"):
        add(i, "NEWLINE", f"src={src.count(chr(10))} dst={dst.count(chr(10))}")
    # 6. latin remnants
    words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'\-]{3,}", dst))
    left = {w for w in words if w not in WHITELIST}
    if left:
        add(i, "LATIN", ",".join(sorted(left)[:8]))

with open(f"{BASE}/data/qa_report.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["idx", "kind", "detail", "english", "korean"])
    for i, k, d in issues:
        w.writerow([i, k, d, en[i].replace("\n", "\\n")[:120], (ko.get(i) or "").replace("\n", "\\n")[:120]])

from collections import Counter
c = Counter(k for _, k, _ in issues)
print("total issues:", len(issues), dict(c))
print("report:", f"{BASE}/data/qa_report.tsv")
