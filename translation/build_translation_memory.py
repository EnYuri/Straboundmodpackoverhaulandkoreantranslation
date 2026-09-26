import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
inputs = [ROOT / "alignment/fu.tsv", ROOT / "alignment/sbkor.tsv"]
pairs = Counter()
variants = defaultdict(Counter)
examples = defaultdict(list)

for input_path in inputs:
    with input_path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["status"] != "aligned-string":
                continue
            original = row["currentOriginal"].strip()
            korean = row["existingKorean"].strip()
            if not original or not korean:
                continue
            pairs[(original, korean)] += 1
            variants[original][korean] += 1
            if len(examples[(original, korean)]) < 3:
                examples[(original, korean)].append(row["targetAsset"] + row["jsonPointer"])

with (ROOT / "translation_memory.tsv").open("w", encoding="utf-8-sig", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("occurrences", "koreanVariants", "currentOriginal", "existingKorean", "examples"))
    for (original, korean), count in pairs.most_common():
        writer.writerow((count, len(variants[original]), original, korean,
                         " | ".join(examples[(original, korean)])))

with (ROOT / "glossary_candidates.tsv").open("w", encoding="utf-8-sig", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("occurrences", "variants", "currentOriginal", "preferredKorean", "alternatives"))
    candidates = []
    for original, korean_counts in variants.items():
        if "\n" in original or len(original) > 80:
            continue
        preferred, count = korean_counts.most_common(1)[0]
        alternatives = " | ".join(value for value, _ in korean_counts.most_common()[1:])
        candidates.append((sum(korean_counts.values()), len(korean_counts), original, preferred, alternatives))
    candidates.sort(key=lambda row: (-row[0], row[2].lower()))
    writer.writerows(candidates)

print({
    "alignedOccurrences": sum(pairs.values()),
    "uniquePairs": len(pairs),
    "uniqueOriginals": len(variants),
    "ambiguousOriginals": sum(1 for values in variants.values() if len(values) > 1),
})
