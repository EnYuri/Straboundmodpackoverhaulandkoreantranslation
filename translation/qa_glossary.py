import csv
import glob
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

worklist = {
    row["id"]: row
    for row in csv.DictReader(
        open("rest_worklist.tsv", encoding="utf-8-sig", newline=""), delimiter="\t"
    )
}
translations = {}
files = {}
for batch_file in sorted(glob.glob("translations/rest_*.tsv")):
    for row in csv.reader(
        open(batch_file, encoding="utf-8-sig", newline=""), delimiter="\t"
    ):
        if row:
            translations[row[0]] = row[1]
            files[row[0]] = batch_file[13:]

issues = []
glossary = list(
    csv.DictReader(
        open("translation_glossary.tsv", encoding="utf-8-sig", newline=""),
        delimiter="\t",
    )
)
for term in glossary:
    if term["rule"] != "fixed":
        continue
    pattern = re.compile(
        r"(?<![A-Za-z0-9])" + re.escape(term["english"]) + r"(?![A-Za-z0-9])",
        re.IGNORECASE,
    )
    accepted = [term["korean"]]
    accepted.extend(
        value.strip() for value in term["alternatives"].split("|") if value.strip()
    )
    for row_id, korean in translations.items():
        english = worklist.get(row_id, {}).get("englishText", "")
        if pattern.search(english) and not any(value in korean for value in accepted):
            issues.append(
                (
                    row_id,
                    files[row_id],
                    term["english"],
                    term["korean"],
                    english,
                    korean,
                )
            )

with open("qa_glossary_report.tsv", "w", encoding="utf-8-sig", newline="") as output:
    writer = csv.writer(output, delimiter="\t", lineterminator="\n")
    writer.writerow(
        ["id", "file", "englishTerm", "preferredKorean", "englishText", "koreanText"]
    )
    writer.writerows(issues)

print("glossary rows:", len(glossary))
print("fixed-term candidates:", len(issues))
print(Counter(row[2] for row in issues).most_common())
