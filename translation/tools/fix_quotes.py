import csv, glob, io

id2eng = {}
for r in csv.DictReader(open('data/rest_worklist.tsv', encoding='utf-8-sig'), delimiter='\t'):
    id2eng[r['id']] = r['englishText']

def dump_cell(text):
    """Serialize one TSV cell; quote only when needed."""
    if '\n' in text or '"' in text or '\t' in text or text != text.strip():
        return '"' + text.replace('"', '""') + '"'
    return text

for bf in sorted(glob.glob('translations/rest_*.tsv')):
    rows = list(csv.reader(open(bf, encoding='utf-8-sig'), delimiter='\t'))
    entries = []  # (id, full text)
    cur_id, cur_lines = None, []
    def flush():
        if cur_id is not None:
            entries.append((cur_id, '\n'.join(cur_lines).rstrip('\n')))
    for r in rows:
        if r and r[0].isdigit() and len(r) >= 2:
            flush()
            cur_id, cur_lines = r[0], [r[1]]
        elif r:
            cur_lines.append('\t'.join(r))
        else:
            cur_lines.append('')
    flush()

    fixed = []
    changed = 0
    for rid, text in entries:
        eng = id2eng.get(rid)
        if eng is None:
            print('  !! no worklist id', rid, 'in', bf)
            fixed.append((rid, text)); continue
        new = text
        # collapse doubled quotes only if source doesn't contain them
        while '""' in new and '""' not in eng:
            new = new.replace('""', '"')
        while new.startswith('"') and not eng.startswith('"'):
            new = new[1:]
        while new.endswith('"') and not eng.endswith('"'):
            new = new[:-1]
        if new != text:
            changed += 1
        fixed.append((rid, new))

    out = io.StringIO()
    for rid, text in fixed:
        out.write(rid + '\t' + dump_cell(text) + '\n')
    new_content = out.getvalue()
    old_content = open(bf, encoding='utf-8-sig').read()
    if new_content != old_content:
        open(bf, 'w', encoding='utf-8-sig', newline='').write(new_content)
        print(bf, 'normalized;', changed, 'quote fixes,', len(fixed), 'entries')
