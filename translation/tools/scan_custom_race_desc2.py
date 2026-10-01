import sys, json, re, csv, collections
from pathlib import Path
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak
from align_merged_translations import parse_json

ROOT = Path(r"E:\My Games\steamapps\common\Starbound")
MODS = ROOT / "mods"

VANILLA_RACES = {"apex","avian","floran","glitch","human","hylotl","novakid"}
DESC_KEY = re.compile(r"^([a-z]+)description$")
NOISE_RACES = {"inspection","generic","default","defaultrecruit","defaultplayer","defaultnpc",
               "defaultpassivemonster","defaultaggressivemonster","tokenrace","passive","perks",
               "scan","cultist","xi"}

# asset(lower) -> {english: korean} from ALREADY covered vanilla-race description pairs
asset_vanilla_ko = collections.defaultdict(dict)
with open("data/pak_pairs.tsv", encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        ptr = row["pointer"]
        leaf = ptr.rstrip("/").split("/")[-1].lower()
        m = DESC_KEY.match(leaf)
        if m and m.group(1) in VANILLA_RACES:
            asset_vanilla_ko[row["asset"].lower()][row["english"]] = row["korean"]

def walk(doc, path=""):
    if isinstance(doc, dict):
        for k, v in doc.items():
            yield from walk(v, path + "/" + str(k))
    elif isinstance(doc, list):
        for i, v in enumerate(doc):
            yield from walk(v, path + "/" + str(i))
    else:
        yield path, doc

covered = set()
with open("data/pak_pairs.tsv", encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        covered.add((row["asset"].lower(), row["pointer"]))

auto_rows = []
need_rows = []
pak_list = sorted(MODS.glob("*.pak"))
for pak_path in pak_list:
    try:
        p = Pak(str(pak_path))
    except Exception:
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
        for ptr, val in walk(doc):
            if not isinstance(val, str):
                continue
            leaf = ptr.rstrip("/").split("/")[-1].lower()
            m = DESC_KEY.match(leaf)
            if not m:
                continue
            race = m.group(1)
            if race in VANILLA_RACES or race in ("short","long") or race in NOISE_RACES:
                continue
            if not re.search(r"[A-Za-z]{3,}", val):
                continue
            key = (name.lower(), ptr)
            if key in covered:
                continue
            ko = asset_vanilla_ko.get(name.lower(), {}).get(val)
            if ko is not None:
                auto_rows.append((race, pak_path.name, name, ptr, val, ko))
            else:
                need_rows.append((race, pak_path.name, name, ptr, val))

print("auto-fillable (exact match to already-translated vanilla desc on same asset):", len(auto_rows))
print("still need manual translation:", len(need_rows))

with open("data/custom_race_desc_autofill.tsv", "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(("race","pak","asset","pointer","english","korean"))
    w.writerows(auto_rows)

with open("data/custom_race_desc_need.tsv", "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(("race","pak","asset","pointer","english"))
    w.writerows(need_rows)

byrace = collections.Counter(r[0] for r in need_rows)
print()
print("remaining-need race breakdown (top 30):")
for race, cnt in byrace.most_common(30):
    print(f"  {race}: {cnt}")

# unique english text count among need_rows
uniq = collections.Counter(r[4] for r in need_rows)
print()
print("unique english strings needing translation:", len(uniq))
