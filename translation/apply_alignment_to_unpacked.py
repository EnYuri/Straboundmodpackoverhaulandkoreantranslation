import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from align_merged_translations import parse_json, resolve_pointer
from generate_legacy_overlays import set_pointer

MATCHED = {"pointer-string", "patch-key-string", "patch-index-string"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("unpacked_root", type=Path)
    parser.add_argument("alignment", type=Path)
    args = parser.parse_args()

    changes = defaultdict(list)
    with args.alignment.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["status"] in MATCHED:
                changes[row["assetPath"]].append(row)

    counts = Counter()
    for asset_path, rows in changes.items():
        disk_path = args.unpacked_root / asset_path.lstrip("/")
        if not disk_path.is_file():
            raise FileNotFoundError(disk_path)
        document = parse_json(disk_path.read_bytes())
        for row in rows:
            pointer = row["currentPointer"]
            actual = resolve_pointer(document, pointer)
            if actual != row["currentOriginal"]:
                raise ValueError(
                    f"source changed at {asset_path}#{pointer}: "
                    f"{actual!r} != {row['currentOriginal']!r}"
                )
            set_pointer(document, pointer, row["legacyKorean"])
            counts["strings"] += 1
            counts["patch-strings" if asset_path.endswith(".patch") else "regular-strings"] += 1
        disk_path.write_text(
            json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        counts["assets"] += 1

    metadata_path = args.unpacked_root / "_metadata"
    metadata = parse_json(metadata_path.read_bytes())
    metadata["version"] = f"{metadata.get('version', '')}+ko.20260921"
    metadata["friendlyName"] = f"{metadata.get('friendlyName', metadata.get('name', ''))} + 한국어 복구"
    metadata["description"] = (
        f"{metadata.get('description', '')}\n\n"
        "Local maintenance: restored legacy Korean strings aligned to the current asset structure."
    ).strip()
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(dict(sorted(counts.items())), ensure_ascii=False))


if __name__ == "__main__":
    main()
