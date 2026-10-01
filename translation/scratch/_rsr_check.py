# -*- coding: utf-8 -*-
import json, re, sys

ROOT = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
uniq = {int(k): v for k, v in json.load(open(ROOT + "/data/rsr_uniq.json", encoding="utf-8")).items()}

for fn in ["rsr_ko_01", "rsr_ko_02", "rsr_ko_03"]:
    d = open(f"{ROOT}/data/{fn}.tsv", "rb").read()
    lines = d.split(b"\r\n") if b"\r\n" in d else d.split(b"\n")
    print(fn, "phys lines:", len(lines), "LF:", d.count(b"\n"), "CRLF:", d.count(b"\r\n"),
          "lit-bsn:", d.count(b"\\n"), "dbl-bsn:", d.count(b"\\\\"))

ko = {}
dup = []
for fn in ["rsr_ko_01", "rsr_ko_02", "rsr_ko_03"]:
    for l in open(f"{ROOT}/data/{fn}.tsv", encoding="utf-8"):
        if not l.strip():
            continue
        i, t = l.split("\t", 1)
        i = int(i)
        if i in ko:
            dup.append(i)
        ko[i] = t.rstrip("\n")

print("ko rows:", len(ko), "dups:", dup)
missing = [i for i in sorted(uniq) if i not in ko]
print("missing:", missing)

TAG = re.compile(r"\^[#a-zA-Z0-9]+;|\[[A-Z][A-Z\- ]+\]|\[EWS\]")
td, nd = [], []
for i, v in ko.items():
    en = uniq.get(i, "")
    if sorted(TAG.findall(en)) != sorted(TAG.findall(v)):
        td.append(i)
    if en.count("\n") != v.replace("\\n", "\n").count("\n"):
        nd.append(i)
print("tag diffs:", td)
print("nl diffs:", nd)
