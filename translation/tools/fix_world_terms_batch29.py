import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent.parent
STAR = BASE.parents[1]
sys.path.insert(0, str(STAR))

from pak import Pak
from pak_writer import write_pak

PENDING_PAK = BASE / "backup_paks/female_translation.pak.REVIEW_PENDING"
PAIRS = BASE / "data/pak_pairs_pending.tsv"


def corrected(english, korean):
    value = korean
    if re.search(r"\bEnterash\b", english, re.I):
        value = value.replace("엔터라시", "엔테라시").replace("엔터래시", "엔테라시")
    if re.search(r"\bSolalei\b", english, re.I):
        value = value.replace("솔랄레이", "솔라레이")
    if re.search(r"\bTonna\b", english, re.I):
        value = value.replace("토나", "톤나")
    if re.search(r"\bTonnova\b", english, re.I):
        value = value.replace("토노바", "톤노바")
    if re.search(r"\bTsay\b", english, re.I):
        value = value.replace("짜이", "차이").replace("체이", "차이").replace("사이 정원", "차이 정원")
    if re.search(r"\bKoywa\b", english, re.I):
        value = value.replace("코이바", "코이와").replace("미코 코야", "미코 코이와")
    if re.search(r"\bAlterash(?:es|s)?\b", english, re.I):
        value = value.replace("알터래시", "알테라시").replace("얼터래시", "알테라시").replace("알테라쉬", "알테라시").replace("알테라시스", "알테라시")
    if re.search(r"\bFaacain\b", english, re.I):
        value = value.replace("파케인", "파아케인").replace("파아카인", "파아케인")
    if re.search(r"\bCeternia\b", english, re.I):
        value = value.replace("케테르니아", "세터니아").replace("세테르니아", "세터니아")
    if re.search(r"\bEnterite\b", english, re.I):
        value = value.replace("엔터라이트", "엔테라이트")
    if re.search(r"\bAlternia\b", english, re.I):
        value = value.replace("알터니아", "알테르니아").replace("얼터니아", "알테르니아")
    if re.search(r"\bEnternia\b", english, re.I):
        value = value.replace("엔테르니아", "에터니아").replace("엔터니아", "에터니아")
    if re.search(r"\bCeterai\b", english, re.I):
        value = value.replace("케테라이", "세테라이").replace("세터라이", "세테라이")
    if re.search(r"\bStardust\b", english, re.I) and not re.search(r"\bStardust (?:Core|Lite)\b", english):
        value = value.replace("별의 먼지", "스타더스트").replace("별가루", "스타더스트").replace("우주 먼지", "스타더스트").replace("우주먼지", "스타더스트").replace("성진", "스타더스트")
    if re.search(r"\bElithian\b", english, re.I) and "엘리시안" not in value:
        value = value.replace("엘리시아", "엘리시안")
    if re.search(r"\bhaven (?:gardens?|sprouts?)\b", english, re.I):
        value = value.replace("안식 정원", "헤이븐 정원").replace("안식처 새싹", "헤이븐 새싹")
    return value


def main():
    changes = defaultdict(dict)
    with PAIRS.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            new = corrected(row["english"], row["korean"])
            if new != row["korean"]:
                changes[(row["asset"], row["pointer"])][row["korean"]] = new

    pak = Pak(str(PENDING_PAK))
    overrides = {}
    changed = 0
    for asset in {asset for asset, _ in changes}:
        doc = json.loads(pak.read(asset))
        stack = list(doc)
        while stack:
            item = stack.pop()
            if isinstance(item, list):
                stack.extend(item)
            elif isinstance(item, dict) and item.get("op") == "replace":
                replacement = changes.get((asset, item.get("path")), {}).get(item.get("value"))
                if replacement is not None:
                    item["value"] = replacement
                    changed += 1
        overrides[asset] = json.dumps(doc, ensure_ascii=False, indent=2).encode("utf-8")

    expected = sum(len(values) for values in changes.values())
    assert changed == expected, (changed, expected)
    del pak
    count = write_pak(PENDING_PAK, PENDING_PAK, overrides)
    print(f"updated pending pak; changed {changed} fields in {len(overrides)} assets; entries {count}")


if __name__ == "__main__":
    main()
