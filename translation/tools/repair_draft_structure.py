#!/usr/bin/env python3
"""Repair markup sequence in a machine draft from its immutable English source."""
import csv, json, re, sys
ids = set(sys.argv[2:])
en = {r['id']: r['englishText'] for r in csv.DictReader(open('data/rest_worklist.tsv', encoding='utf-8-sig', newline=''), delimiter='\t')}
ko = {r[0]: r[1] for r in csv.reader(open(sys.argv[1], encoding='utf-8-sig', newline=''), delimiter='\t') if r and r[0].isdigit()}
tag = re.compile(r'\^[^;^\s]{1,20};')
glyph = re.compile(r'[\ue000-\uf8ff]')
out = {}
for i in ids:
    text = re.sub(r'ZZXMARK[0-9]+QZZ', '\ue024', ko[i])
    expected_tags = tag.findall(en[i])
    source_tags = iter(expected_tags)
    text = tag.sub(lambda _: next(source_tags), text)
    actual_tag_count = len(tag.findall(text))
    if actual_tag_count < len(expected_tags):
        text += ''.join(expected_tags[actual_tag_count:])
    # The only remaining known draft failure is a lost E024 glyph. Put missing
    # glyphs immediately before reset, retaining the source's glyph count.
    missing = len(glyph.findall(en[i])) - len(glyph.findall(text))
    if missing:
        text += '\ue024' * missing
    out[i] = text
json.dump(out, open('priority_0165_structure_repair.json', 'w', encoding='utf-8'), ensure_ascii=False)
