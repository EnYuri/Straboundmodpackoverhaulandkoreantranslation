import csv
from pathlib import Path

BASE = Path(__file__).parent.parent


def main():
    replacements = {
        "아에기": "에지",
        "유니온 깃발": "유니언 깃발",
        "델레안": "텔레안",
        "새턴인": "새터니안",
    }
    changed_files = 0
    changed_rows = 0
    for path in sorted((BASE / "translations").glob("customrace_batch_*.tsv")):
        with path.open(encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.reader(fh, delimiter="\t"))
        changed = False
        for row in rows:
            assert len(row) == 2, (path, row)
            original = row[1]
            for old, new in replacements.items():
                row[1] = row[1].replace(old, new)
            if row[1] != original:
                changed = True
                changed_rows += 1
        if changed:
            with path.open("w", encoding="utf-8-sig", newline="") as fh:
                csv.writer(fh, delimiter="\t", lineterminator="\n").writerows(rows)
            changed_files += 1
    print(f"changed {changed_rows} rows in {changed_files} files")


if __name__ == "__main__":
    main()
