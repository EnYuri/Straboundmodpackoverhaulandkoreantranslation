import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent
STAR = BASE.parents[1]
sys.path.insert(0, str(STAR))

from pak import Pak
from pak_writer import write_pak

PENDING_PAK = BASE / "female_translation.pak.REVIEW_PENDING"
PAIRS = BASE / "pak_pairs_pending.tsv"


def corrected(english, korean):
    value = korean
    if re.search(r"\bEithne\b", english, re.I):
        for variant in ("에이스네", "아이스네"):
            value = value.replace(variant, "에이트네")
    if re.search(r"\bthe Ancients\b", english, re.I):
        value = value.replace("에인션트", "고대인")
    if re.search(r"\bMagicite\b", english, re.I):
        for variant in ("마지사이트", "매직사이트", "매지사이트", "매직석", "마법석", "마기석"):
            value = value.replace(variant, "마기사이트")
    if re.search(r"K['’]Rakoth", english, re.I):
        value = value.replace("K'Rakoth", "크라코스").replace("K’Rakoth", "크라코스")
        value = value.replace("K'라코탄", "크라코탄").replace("K’라코탄", "크라코탄")
        value = value.replace("크라코스an", "크라코탄")
    value = value.replace("고대인는", "고대인은")
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
    for asset, pointer in {key for key in changes}:
        if asset in overrides:
            continue
        doc = json.loads(pak.read(asset))
        stack = list(doc)
        while stack:
            item = stack.pop()
            if isinstance(item, list):
                stack.extend(item)
            elif isinstance(item, dict) and item.get("op") == "replace":
                key = (asset, item.get("path"))
                replacement = changes.get(key, {}).get(item.get("value"))
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
