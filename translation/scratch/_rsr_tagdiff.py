# -*- coding: utf-8 -*-
import json, re

ROOT = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
uniq = {int(k): v for k, v in json.load(open(ROOT + "/data/rsr_uniq.json", encoding="utf-8")).items()}
ko = {}
for fn in ["rsr_ko_01", "rsr_ko_02", "rsr_ko_03"]:
    for l in open(f"{ROOT}/data/{fn}.tsv", encoding="utf-8"):
        if not l.strip():
            continue
        i, t = l.split("\t", 1)
        ko[int(i)] = t.rstrip("\n")

TAG = re.compile(r"\^[#a-zA-Z0-9]+;|\[[A-Z][A-Z\- ]+\]|\[EWS\]")
IDS = [102, 170, 172, 213, 215, 217, 238, 240, 242, 280, 282, 284, 344, 346,
       357, 359, 361, 373, 375, 377, 379, 381, 353]
out = open(f"{ROOT}/scratch/_rsr_tagdiff.txt", "w", encoding="utf-8")
for i in IDS:
    en, v = uniq[i], ko[i]
    out.write(f"=== {i}\nEN tags: {TAG.findall(en)}\nKO tags: {TAG.findall(v)}\n")
    out.write(f"EN nl={en.count(chr(10))}  KO nl={v.replace(chr(92)+'n',chr(10)).count(chr(10))}\n")
    out.write("EN: " + en.replace("\n", "<NL>") + "\n")
    out.write("KO: " + v + "\n\n")
out.close()
print("written")
