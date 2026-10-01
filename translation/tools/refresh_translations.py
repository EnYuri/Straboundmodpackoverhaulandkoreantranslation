#!/usr/bin/env python3
# Refresh overlay op values with the current batch translations (post-edit).
import csv, glob, json, re, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from pak import Pak
from align_merged_translations import parse_json, resolve_pointer
from merge_redirected_patch_ops import apply_patch, base_asset_for

CLEAN = HERE / "data/cleaned_translation_targets.tsv"
WORKLIST = HERE / "data/worklist_new.tsv"
V3 = ROOT / "translation" / "_archive" / "translation-overlays-20260921" / "source-v3"
VANILLA = ROOT / "assets" / "packed.pak"

SOURCE_PAKS = {
    "GiC": ROOT / "mods" / "Galaxy_in_Conflict_contents_2754886445.pak",
    "Extended Story": ROOT / "mods" / "Extended_Story_contents_899795176.pak",
    "Black Armory": ROOT / "mods" / "Black_Armory_4.2.5_FU_NEKI_compat.pak",
}
OVERLAY_DIRS = {
    "GiC": "localeko_gic_legacy",
    "Extended Story": "localeko_extended_story_legacy",
    "Black Armory": "localeko_black_armory_legacy",
}

def load_korean():
    ko = {}
    for f in glob.glob(str(HERE / "translations" / "batch_*.tsv")):
        with open(f, encoding="utf-8-sig", newline="") as fh:
            for row in csv.reader(fh, delimiter="\t"):
                if row and row[0].isdigit():
                    ko[int(row[0])] = row[1] if len(row) > 1 else ""
    rows = list(csv.DictReader(open(WORKLIST, encoding="utf-8-sig"), delimiter="\t"))
    en2ko = {}
    for i, r in enumerate(rows):
        if i in ko:
            en2ko[r["englishText"].replace("\r\n", "\n")] = ko[i]
    return en2ko

def main():
    en2ko = load_korean()
    vanilla = Pak(str(VANILLA))
    paks = {mod: Pak(str(p)) for mod, p in SOURCE_PAKS.items()}
    want = {}  # (overlay patch rel, path) -> value
    counts = Counter()
    doc_cache, base_cache = {}, {}
    for row in csv.DictReader(CLEAN.open(encoding="utf-8-sig", newline=""), delimiter="\t"):
        if row["category"] != "new-translation":
            continue
        kor = en2ko.get(row["englishText"].replace("\r\n", "\n"))
        if not kor:
            continue
        mod, asset, pointer = row["sourceMod"], row["assetPath"], row["jsonPointer"]
        if mod not in OVERLAY_DIRS:
            continue
        pak = paks[mod]
        if row["inPatchAsset"] == "0":
            if asset not in pak.index:
                continue
            key = (mod, asset)
            if key not in doc_cache:
                doc_cache[key] = parse_json(pak.read(asset))
            try:
                actual = resolve_pointer(doc_cache[key], pointer)
            except Exception:
                continue
            if not isinstance(actual, str) or actual.replace("\r\n", "\n") != row["englishText"].replace("\r\n", "\n"):
                continue
            rel = asset.lstrip("/") + ".patch"
            kor_n = kor.replace("\r\n", "\n")
            want[(mod, rel, pointer)] = kor_n.replace("\n", "\r\n") if "\r\n" in actual else kor_n
            counts[mod + ":regular"] += 1
        else:
            if asset not in base_cache:
                base = base_asset_for(pak, vanilla, asset)
                if base is not None:
                    apply_patch(base, parse_json(pak.read(asset)))
                base_cache[asset] = base
            base = base_cache[asset]
            if base is None:
                continue
            if (mod, asset) not in doc_cache:
                doc_cache[(mod, asset)] = parse_json(pak.read(asset))
            doc = doc_cache[(mod, asset)]
            parts = pointer.lstrip("/").split("/")
            try:
                op = doc[int(parts[0])]
                node = op
                for p in parts[1:]:
                    node = node[int(p)] if isinstance(node, list) else node[p]
                if not isinstance(node, str) or node.replace("\r\n", "\n") != row["englishText"].replace("\r\n", "\n"):
                    continue
                fp = op["path"]
                if len(parts) > 2:
                    fp += "/" + "/".join(parts[2:])
                actual = resolve_pointer(base, fp)
                if not isinstance(actual, str) or actual.replace("\r\n", "\n") != row["englishText"].replace("\r\n", "\n"):
                    continue
                rel = asset[:-len(".patch")].lstrip("/") + ".patch"
                kor_n = kor.replace("\r\n", "\n")
                want[(mod, rel, fp)] = kor_n.replace("\n", "\r\n") if "\r\n" in actual else kor_n
                counts[mod + ":patch"] += 1
            except Exception:
                continue
    # apply updates
    updated, missing = 0, 0
    by_file = {}
    for (mod, rel, path), val in want.items():
        by_file.setdefault((mod, rel), {})[path] = val
    for (mod, rel), paths in by_file.items():
        fp = V3 / OVERLAY_DIRS[mod] / rel
        if not fp.exists():
            missing += len(paths)
            continue
        ops = json.loads(fp.read_text(encoding="utf-8"))
        touched = False
        for o in ops:
            p = o.get("path")
            if p in paths and o.get("value") != paths[p]:
                o["value"] = paths[p]
                updated += 1
                touched = True
        if touched:
            fp.write_text(json.dumps(ops, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("want:", len(want), "updated:", updated, "missing-file:", missing, dict(counts))

if __name__ == "__main__":
    main()
