import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent
summary = json.loads((ROOT / "inventory/mod_summary.json").read_text(encoding="utf-8"))

ACTIVE_TRANSLATIONS = re.compile(r"(?i)(^|[-_+])(trans|ko|kor|korean)([-_+.]|$)|FU_KO|sbkor")
LEGACY_TARGETS = {
    "FrackinUniverse_contents_729480149.pak": "FU_KO + 백업본",
    "Galaxy_in_Conflict_contents_2754886445.pak": "구 GiC 병합 번역",
    "Extended_Story_contents_899795176.pak": "구 Extended Story 병합 번역",
    "Black_Armory_4.2.5_FU_NEKI_compat.pak": "구 Black Armory 병합 번역",
    "NonEKI_9_FU_compat.pak": "구 NonEKI 병합 번역",
}
TECHNICAL = re.compile(
    r"(?i)(compat|patch|fix|framework|library|lib\b|optimizer|manytabs|support|tweaks|music|reversion|dependency)"
)
ADULT_ASSET = re.compile(r"(?i)(^|[_-])(sxb|sexbound)|lustbound|lustling|porn|pov")

rows = []
counts = Counter()
for item in summary:
    filename = item["file"]
    searchable = " ".join(str(item.get(key) or "") for key in ("file", "name", "friendlyName"))
    if not item["candidateStrings"]:
        category, basis = "exclude-no-candidates", "표시 문자열 후보 0건"
    elif filename in LEGACY_TARGETS:
        category, basis = "priority-legacy-alignment", LEGACY_TARGETS[filename]
    elif ACTIVE_TRANSLATIONS.search(filename):
        category, basis = "existing-translation-source", "활성 번역/병합 pak"
    elif ADULT_ASSET.search(searchable):
        category, basis = "defer-adult-assets", "Sexbound/성인 장면 계열 우선순위 제외"
    elif TECHNICAL.search(searchable):
        category, basis = "defer-technical", "호환·패치·라이브러리 계열 자동 추정"
    else:
        category, basis = "content-review", "사용자 노출 문자열이 있는 콘텐츠 후보"
    counts[category] += 1
    rows.append((category, filename, item.get("name") or "", item.get("friendlyName") or "",
                 item["candidateAssets"], item["candidateStrings"], basis))

rows.sort(key=lambda row: (row[0], -row[5], row[1].lower()))
with (ROOT / "data/target_classification.tsv").open("w", encoding="utf-8-sig", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("category", "pak", "sourceName", "friendlyName", "candidateAssets",
                     "candidateStrings", "basis"))
    writer.writerows(rows)

(ROOT / "target_classification_summary.json").write_text(
    json.dumps(counts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(counts, ensure_ascii=False))
