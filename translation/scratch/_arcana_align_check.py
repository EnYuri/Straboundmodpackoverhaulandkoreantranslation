# Align-check: rebuild the uniq EN list in the same first-seen order used by
# the fill script, join with data/arcana_ko.tsv by index, and flag rows where
# the KO looks wrong for the EN (identifier stubs, name/desc mismatches).
import csv
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
csv.field_size_limit(10 ** 8)

ko = {}
for line in open("data/arcana_ko.tsv", encoding="utf-8"):
    p = line.rstrip("\n").split("\t")
    if len(p) == 2:
        ko[int(p[0])] = p[1]

rows = list(csv.reader(open("data/arcana_work.tsv", encoding="utf-8"), delimiter="\t"))
uniq = []
seen = set()
for r in rows[1:]:
    if len(r) >= 4:
        pass
# rebuild uniq order from the ORIGINAL todo ordering: use 'en' column of every
# row (before fill, todo rows had empty ko; now filled). uniq = first-seen EN.
for r in rows[1:]:
    en = r[2]
    if en not in seen:
        seen.add(en)
        uniq.append(en)

print("uniq:", len(uniq), "ko:", len(ko))
for i, en in enumerate(uniq):
    k = ko.get(i, "<none>")
    ident = en.startswith("arcana_") or "_tile" in en
    en_is_name = len(en) < 60 and "\n" not in en and "^" not in en
    ko_is_desc = len(k) > 60 or "\n" in k
    flag = ""
    if ident:
        flag = "IDENT"
    elif en_is_name and ko_is_desc:
        flag = "NAME->DESC?"
    elif not en_is_name and not ko_is_desc and len(en) > 80 and len(k) < 30:
        flag = "DESC->NAME?"
    if flag:
        print(i, flag, "| EN:", repr(en[:70]), "| KO:", repr(k[:70]))
