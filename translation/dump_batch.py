#!/usr/bin/env python3
# Dump a slice of rest_worklist.tsv (new-translation rows only) for manual translation.
# usage: python dump_batch.py <start_id> <end_id>
# Private-use glyphs are shown as ⟦E024⟧; add_batch.py converts them back.
import csv, re, sys
start, end = int(sys.argv[1]), int(sys.argv[2])
done = set()
import glob
for bf in glob.glob("translations/rest_*.tsv"):
    for r in csv.reader(open(bf, encoding="utf-8-sig", newline=""), delimiter="\t"):
        if r and r[0] != "id" and r[0].isdigit():
            done.add(int(r[0]))
sys.stdout.reconfigure(encoding="utf-8")
for r in csv.DictReader(open("rest_worklist.tsv", encoding="utf-8-sig", newline=""), delimiter="\t"):
    i = int(r["id"])
    if i < start or i > end or r["tmCategory"] == "tm-multi" or i in done:
        continue
    hint = r["keyHints"].split("|")[0]
    cnt = r["count"]
    txt = re.sub(r"[-]", lambda m: "⟦%04X⟧" % ord(m.group(0)), r["englishText"])
    print(f"{i}\t[{cnt}x {hint}]\t{txt}")
