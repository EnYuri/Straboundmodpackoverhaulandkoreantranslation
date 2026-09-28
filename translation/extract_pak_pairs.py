"""Extract every EN/KO test/replace string pair directly from the deployed
mods/female_translation.pak, per the 2026-09-28 methodological lesson recorded
in docs/batch_log.md: translations/*.tsv id numbers are not trustworthy for
QA (rest_worklist.tsv gets regenerated with shifting ids), so any systematic
re-review must read the actual installed pak, not a tsv snapshot.

Output: pak_pairs.tsv (asset, pointer, english, korean), one row per
test/replace pair found in a .patch document's patch-groups.
"""
import csv
import json
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).parent / "pak_pairs.tsv"


def iter_pairs(doc):
    if not isinstance(doc, list):
        return
    tests = {}
    stack = list(reversed(doc))
    while stack:
        op = stack.pop()
        if isinstance(op, list):
            stack.extend(reversed(op))
            continue
        if not isinstance(op, dict):
            continue
        if op.get("op") == "test" and isinstance(op.get("value"), str):
            tests[op.get("path")] = op["value"]
        elif op.get("op") == "replace" and isinstance(op.get("value"), str):
            path = op.get("path")
            if path in tests and tests[path] != op["value"]:
                yield path, tests[path], op["value"]
                del tests[path]


def main():
    pak_path = Path(sys.argv[1]) if len(sys.argv) > 1 else STAR / "mods" / "female_translation.pak"
    pak = Pak(str(pak_path))
    rows = []
    bad = 0
    for asset in pak.index:
        if not asset.endswith(".patch"):
            continue
        try:
            doc = json.loads(pak.read(asset))
        except Exception:
            bad += 1
            continue
        for path, en, ko in iter_pairs(doc):
            rows.append((asset, path, en, ko))

    print("assets scanned:", sum(1 for a in pak.index if a.endswith(".patch")))
    print("bad json (pre-existing, skipped):", bad)
    print("pairs extracted:", len(rows))

    with OUT.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["asset", "pointer", "english", "korean"])
        for asset, ptr, en, ko in rows:
            w.writerow([asset, ptr, en, ko])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
