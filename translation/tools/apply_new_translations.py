"""Apply new-translation batches (worklist_new korean) to overlay sources
and emit the NonEKI repack target list.

- inPatchAsset=0 rows -> verify English at pointer, append replace op to the
  mod's v3 overlay patch file.
- inPatchAsset=1 rows (GiC/Extended Story) -> resolve the op inside the source
  .patch doc, apply the source patch to the base asset, verify the final
  pointer holds the English text, then append a replace op at the final path.
- NonEKI rows -> written to noneki_new_targets.tsv for the span repacker.
"""
import csv
import glob
import json
import re
import sys
from collections import Counter, defaultdict
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
NONEKI_OUT = HERE / "data/noneki_new_targets.tsv"

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
            en2ko[r["englishText"]] = ko[i]
    return en2ko


def main():
    en2ko = load_korean()
    vanilla = Pak(str(VANILLA))
    paks = {mod: Pak(str(p)) for mod, p in SOURCE_PAKS.items()}

    rows = []
    noneki = []
    with CLEAN.open(encoding="utf-8-sig", newline="") as h:
        for row in csv.DictReader(h, delimiter="\t"):
            if row["category"] != "new-translation":
                continue
            kor = en2ko.get(row["englishText"]) or \
                en2ko.get(row["englishText"].replace("\r\n", "\n"))
            if not kor:
                continue
            if row["sourceMod"] == "NonEKI":
                noneki.append((row["assetPath"], row["jsonPointer"],
                               row["englishText"], kor))
            else:
                row["_korean"] = kor
                rows.append(row)

    counts = Counter()
    grouped = defaultdict(lambda: defaultdict(list))
    doc_cache = {}
    patch_base_cache = {}

    for row in rows:
        mod, asset, pointer = row["sourceMod"], row["assetPath"], row["jsonPointer"]
        kor = row["_korean"]
        pak = paks[mod]
        if asset not in pak.index:
            counts[f"{mod}:asset-missing"] += 1
            continue

        if row["inPatchAsset"] == "0":
            key = (mod, asset)
            if key not in doc_cache:
                doc_cache[key] = parse_json(pak.read(asset))
            try:
                actual = resolve_pointer(doc_cache[key], pointer)
            except Exception:
                counts[f"{mod}:pointer-missing"] += 1
                continue
            if actual.replace("\r\n", "\n") != row["englishText"].replace("\r\n", "\n"):
                counts[f"{mod}:text-changed"] += 1
                continue
            kor_n = kor.replace("\r\n", "\n")
            value = kor_n.replace("\n", "\r\n") if "\r\n" in actual else kor_n
            grouped[mod][asset].append(
                {"op": "replace", "path": pointer, "value": value})
            counts[f"{mod}:merged"] += 1
            continue

        # inPatchAsset=1: pointer indexes into the .patch document
        if asset not in patch_base_cache:
            base = base_asset_for(pak, vanilla, asset)
            if base is not None:
                apply_patch(base, parse_json(pak.read(asset)))
            patch_base_cache[asset] = base
        base = patch_base_cache[asset]
        if base is None:
            counts[f"{mod}:base-missing"] += 1
            continue
        if (mod, asset) not in doc_cache:
            doc_cache[(mod, asset)] = parse_json(pak.read(asset))
        doc = doc_cache[(mod, asset)]
        parts = pointer.lstrip("/").split("/")
        try:
            op_idx = int(parts[0])
            op = doc[op_idx]
            # literal may be nested inside the op's value
            node = op
            for p in parts[1:]:
                node = node[int(p)] if isinstance(node, list) else node[p]
            if not isinstance(node, str) or \
                    node.replace("\r\n", "\n") != row["englishText"].replace("\r\n", "\n"):
                counts[f"{mod}:patch-text-mismatch"] += 1
                continue
            final_pointer = op["path"]
            # descend into op["value"] if the pointer went deeper
            if len(parts) > 2:
                final_pointer = final_pointer + "/" + "/".join(parts[2:])
            actual = resolve_pointer(base, final_pointer)
            if not isinstance(actual, str) or \
                    actual.replace("\r\n", "\n") != row["englishText"].replace("\r\n", "\n"):
                counts[f"{mod}:final-text-mismatch"] += 1
                continue
            kor_n = kor.replace("\r\n", "\n")
            value = kor_n.replace("\n", "\r\n") if "\r\n" in actual else kor_n
            grouped[mod][asset].append(
                {"op": "replace", "path": final_pointer, "value": value})
            counts[f"{mod}:merged-patch"] += 1
        except Exception:
            counts[f"{mod}:patch-resolve-failed"] += 1
            continue

    for mod, assets in grouped.items():
        out_dir = V3 / OVERLAY_DIRS[mod]
        for asset, ops in assets.items():
            patch_rel = (asset + ".patch").lstrip("/") \
                if not asset.endswith(".patch") else asset.lstrip("/")
            # patch-sourced rows target the base asset's overlay file
            if asset.endswith(".patch"):
                patch_rel = asset[:-len(".patch")].lstrip("/") + ".patch"
            patch_path = out_dir / patch_rel
            existing = []
            if patch_path.exists():
                existing = json.loads(patch_path.read_text(encoding="utf-8"))
                seen = {op.get("path") for op in existing}
                ops = [op for op in ops if op["path"] not in seen]
            seen_ops = set()
            dedup = []
            for op in ops:
                if op["path"] not in seen_ops:
                    seen_ops.add(op["path"]); dedup.append(op)
            if not dedup:
                continue
            patch_path.parent.mkdir(parents=True, exist_ok=True)
            patch_path.write_text(
                json.dumps(existing + dedup, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8")

    with NONEKI_OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["assetPath", "jsonPointer", "englishText", "korean"])
        w.writerows(noneki)

    print(json.dumps(dict(counts), ensure_ascii=False))
    print("noneki targets:", len(noneki))


if __name__ == "__main__":
    main()
