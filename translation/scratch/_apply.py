# -*- coding: utf-8 -*-
# Usage: python scratch/_apply.py data/_uncov_ko_X.tsv [more.tsv ...]
import sys, io, csv, collections, pickle, re, json, os, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:/My Games/steamapps/common/Starbound")
sys.path.insert(0, "tools")
import pak, sbjson, pak_writer

csv.field_size_limit(10**7)
TR = r"E:/My Games/steamapps/common/Starbound/mods/zz_translation_female.pak"
KEBAB = re.compile(r'^[a-z]+(-[a-z]+)+$')
IDTOK = re.compile(r'^[A-Za-z_0-9]+$')
CAMEL = re.compile(r'^[a-z]+[A-Z0-9][A-Za-z0-9_]*$')

def skip(v):
    s = v.strip()
    if KEBAB.match(s): return True
    return ' ' not in s and IDTOK.match(s) and (len(s) > 12 or CAMEL.match(s) or s.islower() or s.isupper() or re.search(r'[0-9_]', s))

rows = [r for r in pickle.load(open('data/_uncov_rows.pkl', 'rb')) if not skip(r[3])]
tm = {}
for r in csv.DictReader(open('data/pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
    if r['english'] and r['korean'] and r['english'] != r['korean'] and re.search(r'[가-힣]', r['korean']):
        tm.setdefault(r['english'], r['korean'])

todo = collections.defaultdict(list)
norm = {}
for fn, path, leaf, val in rows:
    if val not in tm:
        todo[val].append((fn, path))
        norm.setdefault(val.replace('\r\n', '\n'), val)

ko = {}
for f in sys.argv[1:]:
    for r in csv.DictReader(open(f, encoding='utf-8-sig'), delimiter='\t'):
        if r.get('en') and r.get('ko'):
            ko[r['en']] = r['ko']

per_file = collections.defaultdict(list)
missed = []
for en, k in ko.items():
    key = en if en in todo else norm.get(en)
    if key:
        for fn, path in todo[key]:
            per_file[fn].append((path, key, k))
    else:
        missed.append(en)
print('missed:', len(missed), 'files:', len(per_file), 'ops:', sum(len(v) for v in per_file.values()))

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
for m in missed[:10]:
    print('MISS:', m[:100])
