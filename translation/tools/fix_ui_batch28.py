import csv
import json
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

EXACT = {
    "[GIC:E] 지원 전투준비 재사용 대기 중": "[GIC:E] 지원 전략 대기 중",
    "[GIC:E] 방어 전투준비 재사용 대기 중": "[GIC:E] 방어 전략 대기 중",
    "[GIC:E] 공격 전투준비 재사용 대기 중": "[GIC:E] 공격 전략 대기 중",
}


def main():
    changes = defaultdict(dict)
    with PAIRS.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            if row["korean"] in EXACT:
                changes[(row["asset"], row["pointer"])][row["korean"]] = EXACT[row["korean"]]

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
