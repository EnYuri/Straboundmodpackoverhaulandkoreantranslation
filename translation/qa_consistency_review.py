"""Cross-check newly written Korean against the existing translation corpus.

This complements qa_translations.py and qa_missed.py.  It reports:
  * one English source translated in more than one way in the new batches;
  * a new translation that differs from an exact, single-form legacy memory;
  * established short glossary terms appearing in a source while their known
    Korean form (or any recorded alternative) is absent from the translation.

The glossary check is deliberately conservative: only alphabetic terms of one
to three words, at least three corpus occurrences, and no conflicting legacy
translation are considered.
"""

from __future__ import annotations

import csv
import glob
import io
import re
from collections import Counter, defaultdict
from pathlib import Path


BASE = Path(r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921")


def read_numbered_batches(pattern: str, multiline: bool) -> dict[str, str]:
    result: dict[str, str] = {}
    for filename in glob.glob(str(BASE / "translations" / pattern)):
        if multiline:
            current = None
            for raw in open(filename, encoding="utf-8"):
                line = raw.rstrip("\n")
                match = re.match(r"^(\d+)\t(.*)$", line)
                if match:
                    current = match.group(1)
                    result[current] = match.group(2)
                elif current is not None:
                    result[current] += "\n" + line
        else:
            text = open(filename, encoding="utf-8", newline="").read()
            for row in csv.reader(io.StringIO(text), delimiter="\t"):
                if len(row) >= 2 and row[0].strip():
                    result[row[0].strip()] = row[1]
    return result


def load_new_rows() -> list[dict[str, str]]:
    with open(BASE / "worklist_new.tsv", encoding="utf-8-sig", newline="") as handle:
        work = list(csv.DictReader(handle, delimiter="\t"))
    translations = read_numbered_batches("batch_*.tsv", multiline=True)
    return [
        {
            "set": "new",
            "id": str(index),
            "english": row["englishText"],
            "korean": translations.get(str(index), ""),
            "context": row.get("exampleLocations", ""),
        }
        for index, row in enumerate(work)
    ]


def load_missed_rows() -> list[dict[str, str]]:
    with open(BASE / "missed_worklist.tsv", encoding="utf-8-sig", newline="") as handle:
        work = {row["id"]: row for row in csv.DictReader(handle, delimiter="\t")}
    translations = read_numbered_batches("missed_*.tsv", multiline=False)
    return [
        {
            "set": "missed",
            "id": key,
            "english": work[key]["englishText"],
            "korean": value,
            "context": "",
        }
        for key, value in translations.items()
        if key in work
    ]


rows = load_new_rows() + load_missed_rows()

# Exact legacy memory, retaining only sources with one recorded Korean form.
legacy: dict[str, Counter[str]] = defaultdict(Counter)
with open(BASE / "translation_memory.tsv", encoding="utf-8-sig", newline="") as handle:
    for row in csv.DictReader(handle, delimiter="\t"):
        try:
            count = int(row["occurrences"])
        except (KeyError, ValueError):
            count = 1
        legacy[row["currentOriginal"]][row["existingKorean"]] += count

single_legacy = {
    english: next(iter(forms))
    for english, forms in legacy.items()
    if len(forms) == 1 and next(iter(forms))
}

report: list[dict[str, str]] = []

# Identical new source translated inconsistently across the two worklists.
new_forms: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
for row in rows:
    if row["korean"]:
        new_forms[row["english"]][row["korean"]].append(f'{row["set"]}:{row["id"]}')
for english, forms in new_forms.items():
    if len(forms) > 1:
        report.append(
            {
                "kind": "NEW_VARIANTS",
                "term": english,
                "expected": " | ".join(forms),
                "set": "",
                "id": "",
                "english": english,
                "korean": " || ".join(f"{ko} <{','.join(ids)}>" for ko, ids in forms.items()),
                "context": "",
            }
        )

# Exact conflicts with an unambiguous legacy entry.
for row in rows:
    expected = single_legacy.get(row["english"])
    if expected and row["korean"] and row["korean"] != expected:
        report.append(
            {
                "kind": "EXACT_LEGACY_CONFLICT",
                "term": row["english"],
                "expected": expected,
                **row,
            }
        )

# Conservative glossary: short alphabetic legacy sources with one Korean form
# and at least three uses.  Prefer terms with a capital or all-lowercase UI/
# mechanic wording, while excluding ordinary glue words that cause noise.
STOP = {
    "the", "and", "for", "with", "from", "this", "that", "your", "you",
    "are", "was", "not", "can", "has", "have", "into", "its", "item",
    "object", "description", "default", "unknown", "small", "large", "old",
    "new", "one", "two", "some", "more", "very", "here", "there",
}
term_rows: list[tuple[str, str, int]] = []
for english, forms in legacy.items():
    if len(forms) != 1:
        continue
    korean, count = next(iter(forms.items()))
    words = english.split()
    if not (1 <= len(words) <= 3 and 3 <= len(english) <= 32 and count >= 3):
        continue
    if not re.fullmatch(r"[A-Za-z][A-Za-z' -]*", english):
        continue
    if english.lower() in STOP or any(word.lower() in STOP for word in words if len(words) == 1):
        continue
    if not korean or korean == english or re.search(r"[\[\]{}<>^]", korean):
        continue
    term_rows.append((english, korean, count))

# Longest terms first, preventing a shorter nested term from duplicating a hit.
term_rows.sort(key=lambda item: (-len(item[0]), -item[2], item[0]))
for row in rows:
    source = row["english"]
    target = row["korean"]
    if not target:
        continue
    seen_spans: list[tuple[int, int]] = []
    for term, expected, count in term_rows:
        match = re.search(rf"(?<![A-Za-z]){re.escape(term)}(?![A-Za-z])", source, re.IGNORECASE)
        if not match or any(match.start() >= a and match.end() <= b for a, b in seen_spans):
            continue
        seen_spans.append(match.span())
        if expected not in target:
            report.append(
                {
                    "kind": "GLOSSARY_ABSENT",
                    "term": term,
                    "expected": f"{expected} (legacy uses={count})",
                    **row,
                }
            )

out = BASE / "qa_consistency_report.tsv"
with open(out, "w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=["kind", "term", "expected", "set", "id", "english", "korean", "context"],
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(report)

counts = Counter(row["kind"] for row in report)
print(f"rows checked: {len(rows)}")
print(f"issues: {len(report)} {dict(counts)}")
print(f"report: {out}")
