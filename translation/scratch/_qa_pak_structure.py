"""Structural integrity QA directly against the live installed pak: verifies
that ^color; tags, <Token> placeholders, and [Bracket Hint] input tokens are
preserved with the same multiset between English and Korean for every
extracted pair in pak_pairs.tsv. This checks a different bug class than
qa_pak_context.py's natural-language heuristics -- broken/missing/reordered
runtime formatting, which causes visible glitches or crashes in-game.
"""
import csv
import re
from collections import Counter

COLOR_TAG = re.compile(r"\^[A-Za-z#0-9]*;")
ANGLE_TOKEN = re.compile(r"<[A-Za-z_][A-Za-z0-9_.]*>")
BRACKET_HINT = re.compile(r"\[[A-Za-z][A-Za-z0-9 _+\-]*\]")

rows = []
with open("data/pak_pairs.tsv", encoding="utf-8-sig", newline="") as f:
    r = csv.DictReader(f, delimiter="\t")
    for row in r:
        rows.append(row)

print("total pairs:", len(rows))

color_mismatch = []
token_mismatch = []
bracket_mismatch = []

for row in rows:
    en = row["english"]
    ko = row["korean"]
    en_colors = Counter(COLOR_TAG.findall(en))
    ko_colors = Counter(COLOR_TAG.findall(ko))
    if en_colors != ko_colors:
        color_mismatch.append(row)

    en_tok = Counter(ANGLE_TOKEN.findall(en))
    ko_tok = Counter(ANGLE_TOKEN.findall(ko))
    if en_tok != ko_tok:
        token_mismatch.append(row)

    en_brk = Counter(BRACKET_HINT.findall(en))
    ko_brk = Counter(BRACKET_HINT.findall(ko))
    if en_brk != ko_brk:
        bracket_mismatch.append(row)

print("color tag mismatches:", len(color_mismatch))
print("<Token> mismatches:", len(token_mismatch))
print("[Bracket] mismatches:", len(bracket_mismatch))


def write(fname, items):
    with open(fname, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["asset", "pointer", "english", "korean"])
        for row in items:
            w.writerow([row["asset"], row["pointer"], row["english"], row["korean"]])


write("_struct_color_mismatch.tsv", color_mismatch)
write("_struct_token_mismatch.tsv", token_mismatch)
write("_struct_bracket_mismatch.tsv", bracket_mismatch)
print("wrote reports")
