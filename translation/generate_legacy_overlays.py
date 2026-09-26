import argparse
import csv
import json
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pak import Pak

from align_merged_translations import parse_json, resolve_pointer

MATCHED = {"pointer-string", "patch-key-string", "patch-index-string"}


def set_pointer(document, pointer, value):
    parts = pointer.lstrip("/").split("/")
    current = document
    for raw_part in parts[:-1]:
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            current = current[part]
        else:
            current = current[int(part)]
    final = parts[-1].replace("~1", "/").replace("~0", "~")
    if isinstance(current, dict):
        current[final] = value
    else:
        current[int(final)] = value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_root", type=Path)
    parser.add_argument("inputs", nargs="+", help="label|overlay name|source pak|alignment TSV")
    parser.add_argument("--regular-only", action="store_true",
                        help="skip translations sourced from .patch assets entirely")
    args = parser.parse_args()

    if args.output_root.exists():
        shutil.rmtree(args.output_root)
    args.output_root.mkdir(parents=True)
    complete_summary = {}

    for specification in args.inputs:
        label, overlay_name, raw_pak, raw_alignment = specification.split("|", 3)
        pak_path = Path(raw_pak)
        alignment_path = Path(raw_alignment)
        source = Pak(str(pak_path))
        output = args.output_root / overlay_name
        output.mkdir()
        grouped = defaultdict(list)
        expected = {}
        regular_verification = defaultdict(list)
        redirected_rows = []
        counts = Counter()

        with alignment_path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                if row["status"] not in MATCHED:
                    continue
                asset_path = row["assetPath"]
                pointer = row["currentPointer"]
                location = (asset_path, pointer)
                if location in expected and expected[location][1] != row["legacyKorean"]:
                    raise ValueError(f"conflicting translation at {label}:{asset_path}#{pointer}")
                expected[location] = (row["currentOriginal"], row["legacyKorean"])

        for (asset_path, pointer), (original, korean) in expected.items():
            if asset_path not in source.index:
                raise KeyError(f"missing source asset: {label}:{asset_path}")
            document = parse_json(source.read(asset_path))
            actual = resolve_pointer(document, pointer)
            if actual != original:
                raise ValueError(
                    f"source changed at {label}:{asset_path}#{pointer}: {actual!r} != {original!r}"
                )
            if asset_path.endswith(".patch"):
                if args.regular_only:
                    counts["skipped-patch-operations"] += 1
                    continue
                parts = pointer.lstrip("/").split("/")
                if len(parts) < 2 or not parts[0].isdigit() or parts[1] != "value":
                    counts["unmappable-patch-operations"] += 1
                    continue
                operation = document[int(parts[0])]
                base_pointer = operation.get("path") if isinstance(operation, dict) else None
                if not isinstance(base_pointer, str) or operation.get("op") not in {"add", "replace"}:
                    counts["unmappable-patch-operations"] += 1
                    continue
                relative = "/" + "/".join(parts[2:]) if len(parts) > 2 else ""
                target_pointer = base_pointer.rstrip("/") + relative
                target_parts = target_pointer.lstrip("/").split("/")
                if "-" in target_parts or not target_pointer:
                    counts["unmappable-patch-operations"] += 1
                    continue
                # A .patch.patch is not supported by Starbound: the extra suffix is
                # still applied to the final asset. Redirect the translation to the
                # path that the source patch creates or replaces instead.
                output_asset = asset_path
                grouped[output_asset].append(
                    {"op": "replace", "path": target_pointer, "value": korean}
                )
                redirected_rows.append((asset_path, pointer, output_asset,
                                        target_pointer, operation.get("op"), original, korean))
                counts["redirected-patch-operations"] += 1
            else:
                output_asset = asset_path + ".patch"
                grouped[output_asset].append({"op": "replace", "path": pointer, "value": korean})
                regular_verification[asset_path].append((pointer, korean))
                counts["regular-operations"] += 1

        for output_asset, operations in grouped.items():
            destination = output / output_asset.lstrip("/")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                json.dumps(operations, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )

        metadata = {
            "name": overlay_name,
            "friendlyName": f"{label} 한국어 오버레이 (구 번역 복구)",
            "version": "2026-09-21.1",
            "author": "local maintenance",
            "description": "최신 자산 위치와 일치하는 기존 한국어 번역을 복구하는 로컬 오버레이.",
            "includes": [source.meta.get("name")],
        }
        (output / "_metadata").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        # Verify regular generated operations against a fresh copy of their target.
        # Redirected patch operations are validated by the real asset loader below.
        for target_asset, operations in regular_verification.items():
            document = parse_json(source.read(target_asset))
            for pointer, korean in operations:
                set_pointer(document, pointer, korean)
                if resolve_pointer(document, pointer) != korean:
                    raise ValueError(f"verification failed: {label}:{target_asset}#{pointer}")

        with (args.output_root / f"{overlay_name}.redirected_patch_operations.tsv").open(
                "w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
            writer.writerow(("sourcePatch", "sourceDocumentPointer", "outputPatch",
                             "finalAssetPointer", "sourceOperation", "currentOriginal",
                             "legacyKorean"))
            writer.writerows(redirected_rows)

        counts["patch-assets"] = len(grouped)
        counts["redirected-patch-assets"] = len({row[2] for row in redirected_rows})
        counts["regular-patch-assets"] = len(grouped) - counts["redirected-patch-assets"]
        complete_summary[label] = {
            "overlayName": overlay_name,
            "sourcePak": str(pak_path),
            **dict(sorted(counts.items())),
        }

    with (args.output_root / "overlay_generation_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(complete_summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps(complete_summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
