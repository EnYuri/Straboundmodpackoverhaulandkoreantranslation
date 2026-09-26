"""QA pass over missed_*.tsv translation batches vs missed_worklist.tsv.

Same checks as qa_translations.py:
  1. color tag preservation (^name; / ^#hex;)
  2. bracket token preservation ([LMB], {var}, <var>, %d ...)
  3. number preservation
  4. newline count match
  5. untranslated (identical to source)
  6. latin remnants >=4 chars not in whitelist
"""
import csv, re, glob, io
from collections import Counter

BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"

en = {}
with open(f"{BASE}/missed_worklist.tsv", encoding="utf-8-sig", newline="") as f:
    r = csv.reader(f, delimiter="\t")
    next(r)
    for row in r:
        if len(row) >= 3:
            en[row[0]] = row[2]

ko = {}
for f in glob.glob(f"{BASE}/translations/missed_*.tsv"):
    txt = open(f, encoding="utf-8", newline="").read()
    r = csv.reader(io.StringIO(txt), delimiter="\t", quoting=csv.QUOTE_MINIMAL)
    for row in r:
        if len(row) >= 2 and row[0].strip():
            ko[row[0].strip()] = row[1]

TAG = re.compile(r"\^([A-Za-z]+|#[0-9A-Fa-f]{2,8});")
BRACKET = re.compile(r"\[[A-Za-z0-9+_\-]+\]|\{[^}]{0,40}\}|<[^>]{0,40}>|%[ds]|&[a-z]+;")
NUM = re.compile(r"\d+(?:\.\d+)?%?")
WHITELIST = {w.lower() for w in """
HP DMG AP DPS NPC GiC GIC ES BA AYA BADA TAT WYM MV NR CA KH NF KO ML HC SHIP CRYPT BBR
MEMORY RAZED P S L X F W SHIFT ALT FIRE LMB RMB SOS IED USCM RPG XMG M1 AK Mk Mk1 Mk2 Mk3
Mk.1 Mk.2 Mk.3 UFO Kojiro Nazrin Nitori Tenshi Satori Julian Bowerbird Machinarius Wrexor
Nar Titansteel Akeman Fosse Sheruto Gazrian Dullahan Letheia Erchius Pericarpyx Protocite
Quietus Telebrium Zerchesium Lunari Prisilite Pristal Tritanium Gensidium Gen1 Gen2
Browning Bazooka Panzerfaust Slug AMMO MAG SNK SMG LMG DMR AR SR shotgun pistol rifle
Occasus Protectorate Miniknog Apex Avian Floran Glitch Hylotl Novakid Human Penguin
Esther Asra Nox Kluex SAIL FTL AI Mysterious Institute Vault Key Forge Encounter Telos
OK WWW URL HP MP EXP LV XP DNA RNA ID NPCs WiFi GPS UFO RAM CPU GPU VR 3D 2D
""".split()}

issues = []
def add(i, kind, detail):
    issues.append((i, kind, detail))

for sid, src in en.items():
    dst = ko.get(sid)
    if dst is None:
        continue  # covered by translation memory, not manual batches
    if dst.strip() == src.strip() and re.search(r"[A-Za-z]{4,}", src):
        add(sid, "UNTRANSLATED", dst[:60])
        continue
    a, b = Counter(TAG.findall(src)), Counter(TAG.findall(dst))
    if a != b:
        add(sid, "TAG", f"{dict(a)} -> {dict(b)}")
    a, b = Counter(BRACKET.findall(src)), Counter(BRACKET.findall(dst))
    if a != b:
        add(sid, "BRACKET", f"{dict(a)} -> {dict(b)}")
    a, b = Counter(NUM.findall(src)), Counter(NUM.findall(dst))
    if a - b:
        add(sid, "NUM", f"missing {dict(a - b)} src={src[:60]}")
    if src.count("\n") != dst.count("\n"):
        add(sid, "NEWLINE", f"{src.count(chr(10))} -> {dst.count(chr(10))}")
    # latin remnants (strip tags/brackets first)
    clean = TAG.sub(" ", BRACKET.sub(" ", dst))
    words = {w for w in re.findall(r"[A-Za-z]{4,}", clean) if w.lower() not in WHITELIST}
    if words:
        add(sid, "LATIN", f"{sorted(words)[:6]} | {dst[:60]}")

with open(f"{BASE}/qa_missed_report.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["id", "kind", "detail", "src", "dst"])
    for i, k, d in issues:
        w.writerow([i, k, d, en.get(i, "")[:120], ko.get(i, "")[:120]])

print("total issues:", len(issues), Counter(k for _, k, _ in issues))
print("report: qa_missed_report.tsv")
