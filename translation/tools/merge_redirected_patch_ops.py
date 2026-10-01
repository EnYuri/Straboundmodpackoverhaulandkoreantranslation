"""Merge v2 redirected patch-source translations into the v3 overlay sources.

For each redirected op (a translation that lived inside a source .patch
document), verify the final asset pointer exists after applying the source
mod's own patch document to the base asset, then append a replace op to the
overlay patch file of the same name.
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


def set_pointer(document, pointer, value):
    parts = pointer.lstrip("/").split("/")
    current = document
    for raw in parts[:-1]:
        part = raw.replace("~1", "/").replace("~0", "~")
        current = current[int(part)] if isinstance(current, list) else current[part]
    final = parts[-1].replace("~1", "/").replace("~0", "~")
    if isinstance(current, list):
        if final == "-":
            current.append(value)
        else:
            current[int(final)] = value
    else:
        current[final] = value

V2 = ROOT / "translation" / "_archive" / "translation-overlays-20260921" / "source-v2"
V3 = ROOT / "translation" / "_archive" / "translation-overlays-20260921" / "source-v3"
VANILLA = ROOT / "assets" / "packed.pak"
SOURCE_PAKS = {
    "gic": ROOT / "mods" / "Galaxy_in_Conflict_contents_2754886445.pak",
    "extended_story": ROOT / "mods" / "Extended_Story_contents_899795176.pak",
}
OVERLAY_DIRS = {
    "gic": "localeko_gic_legacy",
    "extended_story": "localeko_extended_story_legacy",
}


def apply_patch(document, ops):
    for op in ops:
        if not isinstance(op, dict):
            continue
        path = op.get("path", "")
        kind = op.get("op")
        if kind in ("add", "replace"):
            try:
                set_pointer(document, path, op.get("value"))
            except Exception:
                pass
        elif kind == "remove":
            parts = path.lstrip("/").split("/")
            try:
                parent = document
                for raw in parts[:-1]:
                    part = raw.replace("~1", "/").replace("~0", "~")
                    parent = parent[int(part)] if isinstance(parent, list) else parent[part]
                last = parts[-1].replace("~1", "/").replace("~0", "~")
                if isinstance(parent, list):
                    parent.pop(int(last))
                else:
                    del parent[last]
            except Exception:
                pass


def base_asset_for(pak, vanilla, asset_path):
    # The base asset the source .patch applies to is the same path minus .patch
    target = asset_path[:-len(".patch")] if asset_path.endswith(".patch") else asset_path
    if target in pak.index:
        return parse_json(pak.read(target))
    if target in vanilla.index:
        return parse_json(vanilla.read(target))
    return None


def main():
    vanilla = Pak(str(VANILLA))
    counts = Counter()
    merged = defaultdict(list)

    for mod, pak_path in SOURCE_PAKS.items():
        pak = Pak(str(pak_path))
        tsv = V2 / f"{OVERLAY_DIRS[mod]}.redirected_patch_operations.tsv"
        with tsv.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                merged[(mod, row["outputPatch"])].append(row)

    for (mod, out_patch), rows in sorted(merged.items()):
        pak = Pak(str(SOURCE_PAKS[mod]))
        # source patch doc lives at outputPatch path inside source pak
        src_asset = rows[0]["sourcePatch"]
        if src_asset not in pak.index:
            counts[f"{mod}:source-patch-missing:{src_asset}"] += len(rows)
            continue
        base = base_asset_for(pak, vanilla, src_asset)
        if base is None:
            counts[f"{mod}:base-asset-missing:{src_asset}"] += len(rows)
            continue
        src_ops = parse_json(pak.read(src_asset))
        apply_patch(base, src_ops)

        ops_to_add = []
        for row in rows:
            pointer = row["finalAssetPointer"]
            try:
                actual = resolve_pointer(base, pointer)
            except Exception:
                counts[f"{mod}:final-pointer-missing"] += 1
                continue
            if actual != row["currentOriginal"]:
                counts[f"{mod}:final-text-mismatch"] += 1
                continue
            ops_to_add.append({"op": "replace", "path": pointer,
                               "value": row["legacyKorean"]})
            counts[f"{mod}:merged"] += 1

        if not ops_to_add:
            continue
        patch_rel = out_patch.lstrip("/")
        patch_path = V3 / OVERLAY_DIRS[mod] / patch_rel
        existing = []
        if patch_path.exists():
            existing = json.loads(patch_path.read_text(encoding="utf-8"))
            existing_paths = {op.get("path") for op in existing}
            ops_to_add = [op for op in ops_to_add if op["path"] not in existing_paths]
        if ops_to_add:
            patch_path.parent.mkdir(parents=True, exist_ok=True)
            patch_path.write_text(
                json.dumps(existing + ops_to_add, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8")

    print(json.dumps(dict(counts), ensure_ascii=False))


if __name__ == "__main__":
    main()
