"""Glossary compliance QA against the ACTUALLY DEPLOYED pak (pak_pairs.tsv,
from extract_pak_pairs.py), not translations/*.tsv snapshots -- per the
2026-09-28 methodological lesson (id-based tsv QA is unreliable; only the
live pak reflects what players see).

Checks every `rule == fixed` glossary term against every EN/KO pair whose
English contains that term (word-boundary match), flagging rows where the
Korean doesn't contain the preferred term or any listed alternative.
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

csv.field_size_limit(sys.maxsize)
BASE = Path(__file__).parent

pairs_path = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "pak_pairs.tsv"
out = Path(sys.argv[2]) if len(sys.argv) > 2 else BASE / "qa_pak_glossary_report.tsv"
pairs = list(csv.DictReader(open(pairs_path, encoding="utf-8-sig", newline=""), delimiter="\t"))
glossary = list(csv.DictReader(open(BASE / "translation_glossary.tsv", encoding="utf-8-sig", newline=""), delimiter="\t"))

issues = []
for term in glossary:
    if term["rule"] != "fixed":
        continue
    pattern = re.compile(r"(?<![A-Za-z0-9])" + re.escape(term["english"]) + r"(?![A-Za-z0-9])", re.IGNORECASE)
    accepted = [term["korean"]] + [v.strip() for v in term["alternatives"].split("|") if v.strip()]
    for row in pairs:
        english = re.sub(r"https?://[^\s)\"'<>]+", "", row["english"])
        if pattern.search(english) and not any(v in row["korean"] for v in accepted):
            issues.append((row["asset"], row["pointer"], term["english"], term["korean"], row["english"], row["korean"]))

with out.open("w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["asset", "pointer", "englishTerm", "preferredKorean", "englishText", "koreanText"])
    w.writerows(issues)

print("pairs checked:", len(pairs))
print("glossary fixed terms:", sum(1 for t in glossary if t["rule"] == "fixed"))
print("violations:", len(issues))
print(Counter(row[2] for row in issues).most_common(30))
print("report:", out)
