import csv, glob, re, sys, collections, json
sys.stdout.reconfigure(encoding="utf-8")

TAG = re.compile(r'\^[^;^\s]{1,20};')
PH = re.compile(r'%s|%\d+|\{[^}]{1,20}\}|<[A-Za-z_][A-Za-z0-9_]*>|\$\{[^}]+\}')
PUA = re.compile(r'[-]')
INPUT = re.compile(r'\[(?:FIRE|ALT-FIRE|Alt-Fire|ALT|CRIT|SHIFT|UP|Down|DOWN|Jump|LEFT-MOUSE|RIGHT-MOUSE|A|D)\]')

def load_tsv(fn, id_field=None, text_field="englishText"):
    """returns dict id(str) -> english text. If id_field is None, use 0-based row index as id."""
    out = {}
    with open(fn, encoding="utf-8-sig", newline="") as fh:
        r = csv.DictReader(fh, delimiter="\t")
        for i, row in enumerate(r):
            rid = row[id_field] if id_field else str(i)
            out[rid] = row.get(text_field, "")
    return out

def load_translations(pattern):
    ko = {}
    src = {}
    dupes = []
    stray = 0
    for fn in sorted(glob.glob(pattern)):
        with open(fn, encoding="utf-8-sig", newline="") as fh:
            r = csv.reader(fh, delimiter="\t")
            rows = list(r)
            # some groups (elithian/krakoth/nuggubs/plushbound) have a real
            # "id\tkorean" header row; others (batch/missed/rest*) have NONE --
            # their very first line is real id=N data. Only actually drop the
            # first line when it does NOT look like a data row (id, ...).
            if rows and not rows[0][0].isdigit():
                rows = rows[1:]
            for row in rows:
                if not row or not row[0]:
                    continue
                rid = row[0]
                if not rid.isdigit():
                    stray += 1
                    continue
                text = row[1] if len(row) > 1 else ""
                if rid in ko:
                    dupes.append((rid, src[rid], fn))
                    continue
                ko[rid] = text
                src[rid] = fn
    return ko, src, dupes, stray

groups = [
    ("elithian", "elithian_low_worklist.tsv", None, "translations/elithian_*.tsv"),
    ("krakoth", "krakoth_low_worklist.tsv", None, "translations/krakoth_*.tsv"),
    ("nuggubs", "nuggubs_low_worklist.tsv", None, "translations/nuggubs_*.tsv"),
    ("plushbound", "plushbound_low_worklist.tsv", None, "translations/plushbound_*.tsv"),
    ("worklist_new(batch)", "worklist_new.tsv", None, "translations/batch_*.tsv"),
    ("missed", "missed_worklist.tsv", "id", "translations/missed_*.tsv"),
    ("rest_priority", "rest_worklist.tsv", "id", "translations/rest_priority_*.tsv"),
    ("rest", "rest_worklist.tsv", "id", "translations/rest_[0-9]*.tsv"),
]

glossary = list(csv.DictReader(open("translation_glossary.tsv", encoding="utf-8-sig", newline=""), delimiter="\t"))
fixed_terms = []
for term in glossary:
    if term["rule"] != "fixed":
        continue
    pattern = re.compile(r"(?<![A-Za-z0-9])" + re.escape(term["english"]) + r"(?![A-Za-z0-9])", re.IGNORECASE)
    accepted = [term["korean"]]
    accepted.extend(v.strip() for v in term["alternatives"].split("|") if v.strip())
    fixed_terms.append((term["english"], pattern, accepted))

summary = {}
all_struct_issues = []
all_gloss_issues = []

for name, wl_file, id_field, batch_glob in groups:
    try:
        wl = load_tsv(wl_file, id_field=id_field)
    except FileNotFoundError:
        print(f"[skip] {name}: worklist {wl_file} not found")
        continue
    ko, src, dupes, stray = load_translations(batch_glob)
    struct_rows = []
    gloss_rows = []
    for rid, text in ko.items():
        e = wl.get(rid)
        if e is None:
            continue
        iss = []
        if e.count("\n") != text.count("\n"): iss.append("lines")
        if collections.Counter(TAG.findall(e)) != collections.Counter(TAG.findall(text)): iss.append("tags")
        if collections.Counter(PH.findall(e)) != collections.Counter(PH.findall(text)): iss.append("placeholders")
        if collections.Counter(PUA.findall(e)) != collections.Counter(PUA.findall(text)): iss.append("glyphs")
        if collections.Counter(INPUT.findall(e)) != collections.Counter(INPUT.findall(text)): iss.append("inputtoken")
        if iss:
            struct_rows.append((name, rid, src[rid], ",".join(iss)))
        for term_en, pattern, accepted in fixed_terms:
            if pattern.search(e) and not any(v in text for v in accepted):
                gloss_rows.append((name, rid, src[rid], term_en, accepted[0], e[:80], text[:80]))
    missing = sorted((set(wl) - set(ko)), key=lambda x: int(x))
    summary[name] = {
        "worklist_rows": len(wl),
        "translated_rows": len(ko),
        "missing_rows": len(missing),
        "dup_rows": len(dupes),
        "stray_lines": stray,
        "struct_issues": len(struct_rows),
        "gloss_issues": len(gloss_rows),
    }
    all_struct_issues.extend(struct_rows)
    all_gloss_issues.extend(gloss_rows)
    print(f"{name}: worklist={len(wl)} translated={len(ko)} missing={len(missing)} dup={len(dupes)} stray={stray} struct_issues={len(struct_rows)} gloss_issues={len(gloss_rows)}")

with open("qa_all_struct.tsv", "w", encoding="utf-8-sig", newline="") as out:
    w = csv.writer(out, delimiter="\t", lineterminator="\n")
    w.writerow(["group", "id", "file", "issues"])
    w.writerows(all_struct_issues)

with open("qa_all_glossary.tsv", "w", encoding="utf-8-sig", newline="") as out:
    w = csv.writer(out, delimiter="\t", lineterminator="\n")
    w.writerow(["group", "id", "file", "englishTerm", "preferredKorean", "englishText", "koreanText"])
    w.writerows(all_gloss_issues)

print()
print("TOTAL struct issues:", len(all_struct_issues))
print("TOTAL gloss issues:", len(all_gloss_issues))
print(json.dumps(summary, ensure_ascii=False, indent=2))
