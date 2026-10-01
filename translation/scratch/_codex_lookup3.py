# -*- coding: utf-8 -*-
# Print FULL EN+KO rows for rows matching KO substring, for exact rewrite decisions.
import sys, io, csv
sys.stdout.reconfigure(encoding='utf-8')
TERMS = sys.argv[1:]
rows = list(csv.reader(open(r"data\pak_pairs.tsv", encoding='utf-8-sig'), delimiter='\t'))[1:]
for term in TERMS:
    for a,p,e,k in rows:
        if term in k:
            print(f"### '{term}' @ {a} {p}")
            print(f"  EN: {e}")
            print(f"  KO: {k}")
            print()
