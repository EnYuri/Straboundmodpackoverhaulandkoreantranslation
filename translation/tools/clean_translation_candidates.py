"""Clean remaining translation candidates for the four legacy-translated mods.

Reads inventory candidates that were not covered by an exact legacy location
(legacy_remaining_candidates.tsv), removes identifiers/code/unused assets, and
tags the rest with an exact translation-memory suggestion when one exists.
"""
import csv
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CANDIDATES = HERE / "data/legacy_remaining_candidates.tsv"
TM_FILES = [HERE / "data/translation_memory.tsv", HERE / "data/legacy_translation_memory.tsv"]
UNRESOLVED = HERE / "data/legacy_unresolved.tsv"
OUT_CLEAN = HERE / "data/cleaned_translation_targets.tsv"
OUT_EXCLUDED = HERE / "data/excluded_candidates.tsv"
OUT_SUMMARY = HERE / "cleanup_summary.json"
OUT_UNRESOLVED = HERE / "data/unresolved_triage.tsv"

UNUSED_SEGMENTS = {
    "unused", "legacy", "old", "deprecated", "disabled", "backup",
    "obsolete", "removed", "wip", "p_deprecated", "deprecated_special",
}
PLACEHOLDER_TEXTS = {"replace me", "placeholder", "todo", "lorem ipsum", "test"}
PARAM_REF = re.compile(r"^<[\w.\-]+>$")
MARKUP = re.compile(r"\^(?:#[0-9a-fA-F]{3,8}|[a-zA-Z]+);?")
CODE_LIKE = re.compile(
    r"function\s*\(|->|=>|==|!=|\|\||&&"
    r"|\b(?:self|world|storage|sb|config|animator|status|item|entity|player|monster|npc|mcontroller|widget|canvas|pane)\.[A-Za-z_]"
    r"|\w+\s*\([^)]*\)\s*\{"
)
PATH_LIKE = re.compile(r"^[A-Za-z0-9_\-]+[/\\][A-Za-z0-9_\-./\\]+$")
SCHEMA_POINTER = re.compile(r"/(?:listTemplate|schema|itemSchema|buttonTemplate)\b", re.I)


def strip_markup(text):
    return MARKUP.sub("", text)


def classify(row):
    text = row["englishText"]
    asset = row["assetPath"].lower()
    pointer = row["jsonPointer"]
    leaf = pointer.rstrip("/").split("/")[-1].lower()

    if asset.endswith(".behavior"):
        return "behavior-tree-parameter"
    segments = {s for s in re.split(r"[/\\]", asset) if s}
    if segments & UNUSED_SEGMENTS:
        return "unused-or-deprecated-asset"
    stripped = strip_markup(text).strip()
    if not stripped:
        return "markup-only"
    if PARAM_REF.match(stripped):
        return "parameter-reference"
    if stripped.lower() in PLACEHOLDER_TEXTS or SCHEMA_POINTER.search(pointer):
        return "template-placeholder"
    if CODE_LIKE.search(text):
        return "code-like-string"
    if PATH_LIKE.match(stripped):
        return "asset-path-identifier"
    return None


def main():
    tm = defaultdict(set)
    for tm_file in TM_FILES:
        with tm_file.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            kor_col = "existingKorean" if "existingKorean" in reader.fieldnames else "legacyKorean"
            for row in reader:
                tm[row["currentOriginal"]].add(row[kor_col])

    clean, excluded = [], []
    with CANDIDATES.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            reason = classify(row)
            if reason:
                row["excludedReason"] = reason
                excluded.append(row)
                continue
            text = row["englishText"]
            variants = tm.get(text)
            if variants:
                row["category"] = "tm-single" if len(variants) == 1 else "tm-multi"
                row["suggestedKorean"] = next(iter(variants)) if len(variants) == 1 else " || ".join(sorted(variants))
            else:
                row["category"] = "new-translation"
                row["suggestedKorean"] = ""
            row["inPatchAsset"] = "1" if row["assetPath"].lower().endswith(".patch") else "0"
            clean.append(row)

    fields = ["sourceMod", "pak", "assetPath", "jsonPointer", "englishText",
              "category", "suggestedKorean", "inPatchAsset"]
    with OUT_CLEAN.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(clean)
    with OUT_EXCLUDED.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle, ["sourceMod", "pak", "assetPath", "jsonPointer",
                     "englishText", "excludedReason"],
            delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(excluded)

    summary = {"byMod": {}, "excludedReasons": {}, "uniqueTexts": {}}
    by_mod = defaultdict(list)
    for r in clean:
        by_mod[r["sourceMod"]].append(r)
    for mod, group in by_mod.items():
        cats = Counter(r["category"] for r in group)
        summary["byMod"][mod] = {
            "rows": len(group),
            "uniqueEnglish": len({r["englishText"] for r in group}),
            **dict(sorted(cats.items())),
        }
    summary["excludedReasons"] = dict(Counter(r["excludedReason"] for r in excluded).most_common())
    summary["uniqueTexts"] = {
        "cleanRows": len(clean),
        "cleanUniqueEnglish": len({r["englishText"] for r in clean}),
        "excludedRows": len(excluded),
    }

    # triage unresolved legacy translations
    triage = []
    with UNRESOLVED.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["status"] == "target-asset-missing":
                verdict = "content-removed-unrecoverable"
            elif row["status"] == "pointer-missing":
                verdict = "pointer-moved-needs-manual-relocation"
            else:
                verdict = "target-not-a-string"
            row["triage"] = verdict
            triage.append(row)
    with OUT_UNRESOLVED.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle, ["sourceMod", "assetPath", "legacyPointer", "status",
                     "legacyKorean", "triage"],
            delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(triage)
    summary["unresolvedTriage"] = dict(
        Counter(r["triage"] for r in triage).most_common())

    OUT_SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
