import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

MATCHED = {"pointer-string", "patch-key-string", "patch-index-string"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("inputs", nargs="+", help="label=path")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    memory = defaultdict(lambda: {"count": 0, "mods": set(), "statuses": set(), "example": ""})
    unresolved = []
    locations = defaultdict(set)
    per_mod = {}

    for specification in args.inputs:
        label, raw_path = specification.split("=", 1)
        path = Path(raw_path)
        counts = Counter()
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                status = row["status"]
                counts[status] += 1
                if status in MATCHED:
                    pair = (row["currentOriginal"], row["legacyKorean"])
                    item = memory[pair]
                    item["count"] += 1
                    item["mods"].add(label)
                    item["statuses"].add(status)
                    if not item["example"]:
                        item["example"] = f'{label}:{row["assetPath"]}#{row["currentPointer"]}'
                    location = (label, row["assetPath"], row["currentPointer"])
                    locations[location].add(row["legacyKorean"])
                else:
                    unresolved.append((label, row["assetPath"], row["legacyPointer"],
                                       status, row["legacyKorean"]))
        per_mod[label] = dict(sorted(counts.items()))

    conflicts = {location: translations for location, translations in locations.items()
                 if len(translations) > 1}

    memory_path = args.output_dir / "data/legacy_translation_memory.tsv"
    with memory_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("occurrences", "sourceMods", "statuses", "currentOriginal",
                         "legacyKorean", "exampleLocation"))
        for (original, korean), item in sorted(
                memory.items(), key=lambda entry: (-entry[1]["count"], entry[0][0], entry[0][1])):
            writer.writerow((item["count"], ",".join(sorted(item["mods"])),
                             ",".join(sorted(item["statuses"])), original, korean,
                             item["example"]))

    unresolved_path = args.output_dir / "data/legacy_unresolved.tsv"
    with unresolved_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("sourceMod", "assetPath", "legacyPointer", "status", "legacyKorean"))
        writer.writerows(unresolved)

    conflicts_path = args.output_dir / "data/legacy_location_conflicts.tsv"
    with conflicts_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("sourceMod", "assetPath", "currentPointer", "translationVariants"))
        for (label, asset, pointer), translations in sorted(conflicts.items()):
            writer.writerow((label, asset, pointer, " || ".join(sorted(translations))))

    originals = defaultdict(set)
    for original, korean in memory:
        originals[original].add(korean)
    summary = {
        "matchedOccurrences": sum(item["count"] for item in memory.values()),
        "uniquePairs": len(memory),
        "uniqueCurrentOriginals": len(originals),
        "ambiguousOriginals": sum(len(values) > 1 for values in originals.values()),
        "unresolvedOccurrences": len(unresolved),
        "conflictingLocations": len(conflicts),
        "perMod": per_mod,
    }
    with (args.output_dir / "legacy_alignment_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
