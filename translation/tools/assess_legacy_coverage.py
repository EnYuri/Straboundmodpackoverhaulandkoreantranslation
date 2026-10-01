import argparse
import csv
import json
from collections import Counter
from pathlib import Path

MATCHED = {"pointer-string", "patch-key-string", "patch-index-string"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("inventory", type=Path)
    parser.add_argument("inputs", nargs="+", help="label=pak filename=alignment TSV")
    args = parser.parse_args()

    targets = {}
    aligned = {}
    for specification in args.inputs:
        label, pak_name, raw_path = specification.split("=", 2)
        targets[pak_name] = label
        keys = set()
        with Path(raw_path).open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                if row["status"] in MATCHED:
                    keys.add((row["assetPath"], row["currentPointer"]))
        aligned[label] = keys

    counts = {label: Counter() for label in targets.values()}
    remaining = []
    with args.inventory.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            label = targets.get(row["pak"])
            if label is None:
                continue
            counts[label]["inventoryCandidates"] += 1
            key = (row["assetPath"], row["jsonPointer"])
            if key in aligned[label]:
                counts[label]["coveredAtExactLocation"] += 1
            else:
                counts[label]["remainingCandidates"] += 1
                remaining.append((label, row["pak"], row["assetPath"],
                                  row["jsonPointer"], row["englishText"]))

    output_path = args.output_dir / "data/legacy_remaining_candidates.tsv"
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("sourceMod", "pak", "assetPath", "jsonPointer", "englishText"))
        writer.writerows(remaining)

    summary = {}
    for label, item in counts.items():
        total = item["inventoryCandidates"]
        covered = item["coveredAtExactLocation"]
        summary[label] = {
            "inventoryCandidates": total,
            "coveredAtExactLocation": covered,
            "remainingCandidates": item["remainingCandidates"],
            "heuristicCoveragePercent": round(covered * 100 / total, 1) if total else 0,
            "allAlignedLocations": len(aligned[label]),
        }
    with (args.output_dir / "legacy_coverage_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
