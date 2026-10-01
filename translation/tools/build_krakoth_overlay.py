#!/usr/bin/env python3
# Apply translated batches of krakoth_low_worklist.tsv into the K'Rakoth
# overlay pak (creates it on first run, updates it on later runs by merging
# with whatever is already inside).
import csv, glob, sys
sys.path.insert(0, "../../")
from pak import Pak
from align_merged_translations import parse_json
from write_pak import write_pak, patch_bytes

WORKLIST = "data/krakoth_low_worklist.tsv"
OUT_PAK = "../../mods/zz_localeko_krakoth_low_20260927.pak"

worklist = {}
with open(WORKLIST, encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        worklist[int(r["id"])] = r

translated = {}
for bf in sorted(glob.glob("translations/krakoth_*.tsv")):
    with open(bf, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            translated[int(r["id"])] = r["korean"]

overlays = {}
for i, ko in translated.items():
    r = worklist[i]
    asset, pointer, en = r["assetPath"], r["jsonPointer"], r["englishText"]
    overlays.setdefault(asset, []).append([
        {"op": "test", "path": pointer, "value": en},
        {"op": "replace", "path": pointer, "value": ko},
    ])

# merge with whatever is already packed (so re-running with a bigger
# translations/ set doesn't require redoing earlier batches)
try:
    old = Pak(OUT_PAK)
    for name in old.index:
        if not name.endswith(".patch"):
            continue
        base = name[:-len(".patch")]
        if base in overlays:
            continue  # this run's data supersedes
        try:
            ops = parse_json(old.read(name))
        except Exception:
            continue
        for el in ops if isinstance(ops, list) else []:
            group = el if isinstance(el, list) else [el]
            overlays.setdefault(base, []).append(group)
except FileNotFoundError:
    pass

files = {asset + ".patch": patch_bytes(groups) for asset, groups in overlays.items()}
meta = {
    "name": "zz_localeko_krakoth_low_20260927",
    "friendlyName": "Korean Overhaul - K'Rakoth Species-Flavor Text",
    "author": "local maintenance",
    "description": "Per-race item/object flavor text for the K'Rakoth Mod (florandescription, glitchdescription, anneliskdescription, fenrondescription, noolithdescription, etc.), translated in batches.",
    "version": "2026-09-27.1",
    "priority": 999999862,
}
size, n = write_pak(OUT_PAK, files, meta)
print("wrote", size, "bytes,", n, "assets,", len(overlays), "target files,", len(translated), "translated rows total")
