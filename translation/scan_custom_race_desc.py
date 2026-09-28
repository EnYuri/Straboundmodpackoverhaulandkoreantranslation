import sys, json, re, csv
from pathlib import Path
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak
from align_merged_translations import parse_json

ROOT = Path(r"E:\My Games\steamapps\common\Starbound")
MODS = ROOT / "mods"

VANILLA_RACES = {"apex","avian","floran","glitch","human","hylotl","novakid"}
DESC_KEY = re.compile(r"^([a-z]+)description$")

covered = set()
with open("pak_pairs.tsv", encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        covered.add((row["asset"].lower(), row["pointer"]))
print("covered pairs loaded:", len(covered), file=sys.stderr)

def walk(doc, path=""):
    if isinstance(doc, dict):
        for k, v in doc.items():
            yield from walk(v, path + "/" + str(k))
    elif isinstance(doc, list):
        for i, v in enumerate(doc):
            yield from walk(v, path + "/" + str(i))
    else:
        yield path, doc

found = {}
missing_rows = []
scanned = 0
pak_list = sorted(MODS.glob("*.pak"))
print("pak files:", len(pak_list), file=sys.stderr)
for pak_path in pak_list:
    try:
        p = Pak(str(pak_path))
    except Exception as e:
        print("pak open fail", pak_path, e, file=sys.stderr)
        continue
    for name in p.index:
        low = name.lower()
        if not (low.endswith(".object") or low.endswith(".item") or low.endswith(".liquid")
                or low.endswith(".matitem") or low.endswith(".consumable") or low.endswith(".activeitem")):
            continue
        try:
            raw = p.read(name)
            doc = parse_json(raw)
        except Exception:
            continue
        scanned += 1
        for ptr, val in walk(doc):
            if not isinstance(val, str):
                continue
            leaf = ptr.rstrip("/").split("/")[-1].lower()
            m = DESC_KEY.match(leaf)
            if not m:
                continue
            race = m.group(1)
            if race in VANILLA_RACES or race in ("short","long"):
                continue
            if not re.search(r"[A-Za-z]{3,}", val):
                continue
            key = (name.lower(), ptr)
            is_covered = key in covered
            found.setdefault(race, [0,0])
            found[race][0] += 1
            if not is_covered:
                found[race][1] += 1
                missing_rows.append((race, pak_path.name, name, ptr, val[:80]))

print("assets scanned:", scanned)
print("race : total_found, missing_from_translation_pak")
for race, (tot, miss) in sorted(found.items(), key=lambda kv: -kv[1][1]):
    print(f"  {race}: {tot} total, {miss} missing")
print()
print("TOTAL missing rows:", len(missing_rows))
with open("custom_race_desc_missing.tsv", "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(("race","pak","asset","pointer","english_sample"))
    w.writerows(missing_rows)
