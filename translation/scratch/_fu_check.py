# Verify fu_ko_all.tsv alignment against scratch/_fu_uniq.txt:
# tag preservation, newline counts, and name/desc type sanity.
import io
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ko = {}
for f in ["data/fu_ko.tsv", "data/fu_ko2.tsv", "data/fu_ko3.tsv"]:
    for line in open(f, encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if len(p) == 2:
            ko[int(p[0])] = p[1]

uniq = {}
cur = None
buf = []
for line in open("scratch/_fu_uniq.txt", encoding="utf-8"):
    m = re.match(r"### (\d+) x(\d+)", line)
    if m:
        if cur is not None:
            uniq[cur] = "\n".join(buf).rstrip("\n")
        cur = int(m.group(1))
        buf = []
    else:
        buf.append(line.rstrip("\n"))
uniq[cur] = "\n".join(buf).rstrip("\n")

print("uniq:", len(uniq), "ko:", len(ko))
print("missing idx:", [i for i in uniq if i not in ko][:20])

tag = re.compile(r"\^[#a-zA-Z0-9]+;")
bad = []
for i, en in uniq.items():
    k = ko.get(i, "").replace("\\n", "\n")
    if sorted(tag.findall(en)) != sorted(tag.findall(k)):
        bad.append(("tag", i, en[:50]))
    if en.count("\n") != k.count("\n"):
        bad.append(("nl", i, en[:50]))
    en_name = len(en) < 70 and "\n" not in en
    if en_name and len(k) > 80:
        bad.append(("name->desc", i, en[:50]))
    if len(en) > 80 and len(k) < 25:
        bad.append(("desc->name", i, en[:50]))
print("issues:", len(bad))
for b in bad[:30]:
    print(b)
