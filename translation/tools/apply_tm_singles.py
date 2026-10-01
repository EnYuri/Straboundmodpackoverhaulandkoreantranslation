"""Merge tm-single translation-memory hits into the v3 overlay sources.

For every cleaned candidate with category=tm-single on a regular (non-.patch)
asset, verify the current source pak still has the expected English text at the
JSON pointer, then append a replace op to the overlay's <asset>.patch file.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from pak import Pak
from align_merged_translations import parse_json, resolve_pointer

CLEAN = HERE / "data/cleaned_translation_targets.tsv"
OVERLAY_ROOT = ROOT / "translation" / "_archive" / "translation-overlays-20260921" / "source-v3"
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


def main():
    rows = []
    with CLEAN.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["category"] == "tm-single" and row["inPatchAsset"] == "0":
                rows.append(row)

    paks = {mod: Pak(str(path)) for mod, path in SOURCE_PAKS.items()}
    grouped = defaultdict(lambda: defaultdict(list))  # mod -> assetPath -> ops
    counts = Counter()
    doc_cache = {}

    for row in rows:
        mod = row["sourceMod"]
        asset, pointer = row["assetPath"], row["jsonPointer"]
        pak = paks[mod]
        if asset not in pak.index:
            counts[f"{mod}:asset-missing"] += 1
            continue
        key = (mod, asset)
        if key not in doc_cache:
            doc_cache[key] = parse_json(pak.read(asset))
        try:
            actual = resolve_pointer(doc_cache[key], pointer)
        except Exception:
            counts[f"{mod}:pointer-missing"] += 1
            continue
        if actual != row["englishText"]:
            counts[f"{mod}:text-changed"] += 1
            continue
        grouped[mod][asset].append(
            {"op": "replace", "path": pointer, "value": row["suggestedKorean"]})
        counts[f"{mod}:merged"] += 1

    for mod, assets in grouped.items():
        out_dir = OVERLAY_ROOT / OVERLAY_DIRS[mod]
        for asset, ops in assets.items():
            patch_rel = (asset + ".patch").lstrip("/")
            patch_path = out_dir / patch_rel
            existing = []
            if patch_path.exists():
                existing = json.loads(patch_path.read_text(encoding="utf-8"))
                existing_paths = {op.get("path") for op in existing}
                ops = [op for op in ops if op["path"] not in existing_paths]
            if not ops:
                continue
            patch_path.parent.mkdir(parents=True, exist_ok=True)
            patch_path.write_text(
                json.dumps(existing + ops, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8")

    print(json.dumps(dict(counts), ensure_ascii=False))


if __name__ == "__main__":
    main()
