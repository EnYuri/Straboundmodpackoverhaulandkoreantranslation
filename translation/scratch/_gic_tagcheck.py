# Compare tag counts EN vs KO for flagged indices in the GiC batch.
import re, os, csv

BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
KO = os.path.join(BASE, "data", "gic_ko_02.tsv")

ko = {}
for l in open(KO, encoding="utf-8"):
    i, t = l.rstrip("\n").split("\t", 1)
    ko[int(i)] = t

# find the uniq source list - search scratch/data for the dump
cands = []
for root, _, files in os.walk(BASE):
    for fn in files:
        if "gic" in fn.lower() and fn.endswith((".txt", ".tsv")):
            cands.append(os.path.join(root, fn))
print("\n".join(cands))
