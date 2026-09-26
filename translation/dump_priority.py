#!/usr/bin/env python3
# Dump the next N undone new-translation rows, prioritizing lore/quest/dialogue text
# over generic item/object description text (per user request 2026-09-23).
# usage: python dump_priority.py <count>
import csv, re, sys, glob

count = int(sys.argv[1]) if len(sys.argv) > 1 else 150

# Base item description keys (what the item IS/DOES) are HIGH priority - needed to know
# what an item actually is. Only RACE-SPECIFIC flavor variants (nekidescription, etc,
# i.e. the "조사" text-type: bonus per-race flavor text stacked on an item) are LOW priority.
GENERIC_DESC_KEYS = set(['description','shortdescription','longdescription'])
GENERIC_DESC_PREFIXES = ('description',)  # covers description2, description3, ...

LOW_KEYS = set(['label','title','name','value','category',
'customlabels','displaytitle','subtitle','ranks','categoryblacklist','categorywhitelist','alkey'])

def is_low_priority(kh):
    parts = kh.lower().split('|')
    def part_is_low(p):
        if p in GENERIC_DESC_KEYS or p.startswith(GENERIC_DESC_PREFIXES):
            return False
        return p in LOW_KEYS or p.endswith('description')
    return all(part_is_low(p) for p in parts)

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
        rows.append(r)

high = [r for r in rows if not is_low_priority(r["keyHints"])]
low = [r for r in rows if is_low_priority(r["keyHints"])]
high.sort(key=lambda r: int(r["id"]))
low.sort(key=lambda r: int(r["id"]))

print(f"# high-priority remaining: {len(high)}, low-priority remaining: {len(low)}", file=sys.stderr)

selected = high[:count]
if len(selected) < count:
    selected += low[:count - len(selected)]

sys.stdout.reconfigure(encoding="utf-8")
for r in selected:
    i = int(r["id"])
    hint = r["keyHints"].split("|")[0]
    cnt = r["count"]
    txt = re.sub(r"[-]", lambda m: "⟦%04X⟧" % ord(m.group(0)), r["englishText"])
    nl = txt.count(chr(10))
    mark = f" NL{nl}" if nl else ""
    txt = txt.replace(chr(10), chr(92)+"n")
    print(f"{i}\t[{cnt}x {hint}]{mark}\t{txt}")
