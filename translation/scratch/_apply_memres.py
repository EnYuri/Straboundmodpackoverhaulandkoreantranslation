# -*- coding: utf-8 -*-
# Directly patch (fn, path) rows whose EN value exists in the translation
# memory (pak_pairs) — values skipped by _apply.py's `val not in tm` filter.
import sys, io, csv, collections, pickle, re, json, os, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:/My Games/steamapps/common/Starbound")
sys.path.insert(0, "tools")
import pak, sbjson, pak_writer

csv.field_size_limit(10**7)
TR = r"E:/My Games/steamapps/common/Starbound/mods/zz_translation_female.pak"

tm = {}
for r in csv.DictReader(open('data/pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
    if r['english'] and r['korean'] and r['english'] != r['korean'] and re.search(r'[가-힣]', r['korean']):
        tm.setdefault(r['english'], r['korean'])
normtm = {re.sub(r'\r\n?', '\n', k): v for k, v in tm.items()}

rows = pickle.load(open('data/_uncov_rows.pkl', 'rb'))
per_file = collections.defaultdict(list)
for fn, path, leaf, val in rows:
    ko = tm.get(val) or normtm.get(re.sub(r'\r\n?', '\n', val))
    if ko:
        per_file[fn].append((path, val, ko))
print('files:', len(per_file), 'ops:', sum(len(v) for v in per_file.values()))

pk = pak.Pak(TR)
ov = {}
for fn, lst in per_file.items():
    if fn in pk.index:
        try:
            d = sbjson.parse_sb(pk.read(fn).decode('utf-8-sig'))
        except Exception:
            continue
    else:
        d = []
    grp = []
    for path, en, k in lst:
        grp.append({'op': 'test', 'path': path, 'value': en})
        grp.append({'op': 'replace', 'path': path, 'value': k})
    if isinstance(d, list):
        d.append(grp)
    else:
        d = [grp]
    ov[fn] = json.dumps(d, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
del pk

pak_writer.write_pak(TR + '.staged', TR, ov)
for i in range(60):
    try:
        os.replace(TR + '.staged', TR)
        print('replaced')
        break
    except PermissionError:
        time.sleep(5)
