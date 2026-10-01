# Verify index alignment between scratch/_arcana_uniq.txt (authoritative
# first-seen uniq order, "### N xM" headers) and data/arcana_ko.tsv.
# Flag rows where KO plausibly belongs to a different EN.
import io
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ko = {}
for line in open("data/arcana_ko.tsv", encoding="utf-8"):
    p = line.rstrip("\n").split("\t")
    if len(p) == 2:
        ko[int(p[0])] = p[1]

uniq = {}
cur = None
buf = []
for line in open("scratch/_arcana_uniq.txt", encoding="utf-8"):
    m = re.match(r"### (\d+) x(\d+)", line)
    if m:
        if cur is not None:
            uniq[cur] = "\n".join(buf).rstrip("\n")
        cur = int(m.group(1))
        buf = []
    else:
        buf.append(line.rstrip("\n"))
if cur is not None:
    uniq[cur] = "\n".join(buf).rstrip("\n")

print("uniq:", len(uniq), "ko:", len(ko))
issues = []
for i in sorted(uniq):
    en = uniq[i]
    k = ko.get(i)
    if k is None:
        issues.append((i, "MISSING", en, ""))
        continue
    en_is_ident = bool(re.match(r"^[\w./]+$", en)) and ("_" in en or "/" in en)
    en_is_name = len(en) < 70 and "\n" not in en and not en_is_ident
    ko_is_desc = len(k) > 70 or "\\n" in k
    ko_is_ident = bool(re.match(r"^[\w./]+$", k)) and "_" in k
    if en_is_name and ko_is_desc:
        issues.append((i, "NAME->DESC?", en, k))
    elif not en_is_ident and not en_is_name and not ko_is_desc and not ko_is_ident and len(k) < 30:
        issues.append((i, "DESC->NAME?", en, k))
for i, f, en, k in issues:
    print(i, f, "| EN:", repr(en[:80]), "| KO:", repr(k[:80]))
print("total flagged:", len(issues))
