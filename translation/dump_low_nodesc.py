#!/usr/bin/env python3
# Dump the next N undone rows excluding species appraisal texts (*description keys).
# usage: python dump_low_nodesc.py <count>
import csv, re, sys, glob

count = int(sys.argv[1]) if len(sys.argv) > 1 else 50

DESC_KEYS = set(['description', 'shortdescription', 'longdescription'])

def has_nondesc(kh):
    parts = kh.lower().split('|')
    for p in parts:
        if p in DESC_KEYS or p.startswith('description') or p.endswith('description'):
            continue
        return True
    return False

done = set()
for bf in glob.glob("translations/rest_*.tsv"):
    for r in csv.reader(open(bf, encoding="utf-8-sig", newline=""), delimiter="\t"):
        if r and r[0] != "id" and r[0].isdigit():
            done.add(int(r[0]))

rows = []
with open("rest_worklist.tsv", encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        i = int(r["id"])
        if r["tmCategory"] == "tm-multi" or i in done:
            continue
        if has_nondesc(r["keyHints"]):
            rows.append(r)

rows.sort(key=lambda r: int(r["id"]))
print(f"# non-desc remaining: {len(rows)}", file=sys.stderr)

sys.stdout.reconfigure(encoding="utf-8")
for r in rows[:count]:
    i = int(r["id"])
    hint = r["keyHints"].split("|")[0]
    cnt = r["count"]
    txt = re.sub(r"[-]", lambda m: "⟦%04X⟧" % ord(m.group(0)), r["englishText"])
    nl = txt.count(chr(10))
    mark = f" NL{nl}" if nl else ""
    txt = txt.replace(chr(10), chr(92)+"n")
    print(f"{i}\t[{cnt}x {hint}]{mark}\t{txt}")
