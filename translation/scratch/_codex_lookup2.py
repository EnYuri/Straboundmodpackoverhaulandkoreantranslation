# -*- coding: utf-8 -*-
# Codex review pass 2b: per-asset occurrence counts for name-variant terms.
import sys, io, csv
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

TERMS = sys.argv[1:]
rows = list(csv.reader(open(r"data\pak_pairs.tsv", encoding='utf-8-sig'), delimiter='\t'))[1:]
for term in TERMS:
    hits = [(a,p,e,k) for a,p,e,k in rows if term in k]
    print(f"### '{term}' -> {len(hits)} hits")
    for a,c in Counter(x[0] for x in hits).most_common(30):
        print(f"    {c:4d}  {a}")
    # show one sample KO line per distinct asset group
    seen=set()
    for a,p,e,k in hits:
        if a in seen: continue
        seen.add(a)
        if len(seen)>8: break
        print(f"      e.g. {a} {p}: {k[:120].replace(chr(10),' | ')}")
