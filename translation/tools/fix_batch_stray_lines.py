import csv, glob, sys

sys.stdout.reconfigure(encoding="utf-8")

fixed_files = 0
fixed_entries = 0

for fn in sorted(glob.glob("translations/batch_*.tsv")):
    with open(fn, encoding="utf-8-sig", newline="") as f:
        r = csv.reader(f, delimiter="\t")
        raw_rows = list(r)
        # batch_*.tsv files have NO header row -- the first line is real
        # id=N data. Do not consume it as a header.
        header = None

    entries = []  # list of [id, korean]
    current_id = None
    current_lines = []
    merged_here = 0

    def flush():
        if current_id is not None:
            entries.append([current_id, "\n".join(current_lines)])

    for row in raw_rows:
        if row and row[0].isdigit():
            flush()
            current_id = row[0]
            current_lines = [row[1] if len(row) > 1 else ""]
        else:
            if current_id is None:
                # stray content before any id seen; skip (shouldn't happen)
                continue
            merged_here += 1
            if not row:
                current_lines.append("")
            else:
                current_lines.append("\t".join(row))
    flush()

    if merged_here:
        with open(fn, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerows(entries)
        fixed_files += 1
        fixed_entries += merged_here
        print(f"{fn}: merged {merged_here} stray lines into their parent rows ({len(entries)} entries total)")

print()
print(f"TOTAL: {fixed_files} files repaired, {fixed_entries} stray lines merged")
