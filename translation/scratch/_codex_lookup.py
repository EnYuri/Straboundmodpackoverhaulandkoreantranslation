# -*- coding: utf-8 -*-
# Codex review pass 2: locate every occurrence of collected KO terms in
# data/pak_pairs.tsv. Prints asset/pointer/EN/KO for deciding standard forms.
import sys, io, csv
sys.stdout.reconfigure(encoding='utf-8')

TERMS = sys.argv[1:]
rows = list(csv.reader(open(r"data\pak_pairs.tsv", encoding='utf-8-sig'), delimiter='\t'))
hdr = rows[0]; rows = rows[1:]
for term in TERMS:
    hits = [(a,p,e,k) for a,p,e,k in rows if term in k]
    print(f"### '{term}' -> {len(hits)} hits")
    for a,p,e,k in hits[:60]:
        k1 = k.replace('\n',' | ')
        e1 = e.replace('\n',' | ')
        print(f"  {a} {p}\n    EN: {e1[:160]}\n    KO: {k1[:160]}")
    if len(hits) > 60: print(f"  ... +{len(hits)-60} more")
