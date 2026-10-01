# Propagate user's manual *_ko_*.tsv edits into the deployed pak.
# For each drift row from _drift_check, update the replace op value.
# - sat_names.tsv: keep the pak's existing glyph/color prefix, swap only the name text.
# - skip rows differing only by leading/trailing whitespace.
import sys, io, json, csv, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
csv.field_size_limit(sys.maxsize)
APPLY = '--apply' in sys.argv

FILES = [
    ('c2957_ko_01.tsv', 'c2957'), ('gcyber_ko_01.tsv', 'gcyber'),
    ('gic_ko_09b.tsv', 'gic'), ('gic_ko_12.tsv', 'gic'),
    ('gicx_ko_01.tsv', 'gicx'), ('gicx_ko_03.tsv', 'gicx'),
    ('lfw_ko.tsv', 'lfw'), ('lfw_ko_manual.tsv', 'lfw'),
    ('ow_ko_03.tsv', 'ow'), ('rsr_ko_01.tsv', 'rsr'), ('rsr_ko_02.tsv', 'rsr'),
    ('sat_ko_01.tsv', 'sat'), ('sat_ko_03.tsv', 'sat'), ('sat_ko_04.tsv', 'sat'),
    ('sat_ko_04b.tsv', 'sat'), ('sat_ko_05.tsv', 'sat'), ('sat_ko_06.tsv', 'sat'),
    ('sat_names.tsv', 'sat'),
]
tr = Pak(TR)

def load_ko(path):
    rows, cur_id, cur = {}, None, []
    for ln in io.open(path, encoding='utf-8').read().split('\n'):
        m = re.match(r'^(\d+)\t(.*)$', ln)
        if m:
            if cur_id is not None:
                rows[cur_id] = '\n'.join(cur)
            cur_id, cur = m.group(1), [m.group(2)]
        else:
            cur.append(ln)
    if cur_id is not None:
        rows[cur_id] = '\n'.join(cur)
    return rows

unfold = lambda s: s.replace('\\n', '\n')
GLYPH_PREFIX = re.compile(r'^(\^(?:cyan|#?[0-9A-Fa-f]{6}|white|yellow|orange|red|green|blue|gray);|[-])+')

applied = skipped_ws = nopatch = 0
overrides = collections.defaultdict(lambda: json.loads(b'[]'))
changed_files = {}
report = []
for ko_file, pfx in FILES:
    uniq = json.load(io.open(BASE + '\\data\\' + pfx + '_uniq.json', encoding='utf-8'))
    work = list(csv.DictReader(io.open(BASE + '\\data\\' + pfx + '_work.tsv', encoding='utf-8-sig'), delimiter='\t'))
    en2slots = collections.defaultdict(list)
    for w in work:
        en2slots[w['en']].append((w['asset'], w['field']))
    ko = load_ko(BASE + '\\data\\' + ko_file)
    is_names = ko_file == 'sat_names.tsv'
    for rid, kov in sorted(ko.items(), key=lambda kv: int(kv[0]) if kv[0].isdigit() else 0):
        en = uniq.get(rid)
        if en is None:
            continue
        want = unfold(kov)
        for asset, field in en2slots.get(en, []):
            pname = asset + '.patch'
            if pname not in tr.index:
                hits = [k for k in tr.index if k.lower() == pname.lower()]
                if not hits:
                    continue
                pname = hits[0]
            if pname not in changed_files:
                changed_files[pname] = json.loads(tr.read(pname).decode('utf-8'))
            doc = changed_files[pname]
            for g in doc:
                ops = g if isinstance(g, list) else [g]
                for o in ops:
                    if not isinstance(o, dict) or o.get('op') != 'replace':
                        continue
                    p = str(o.get('path', ''))
                    if p.rsplit('/', 1)[-1] != field and p != field:
                        continue
                    testv = None
                    for o2 in ops:
                        if isinstance(o2, dict) and o2.get('op') == 'test' and o2.get('path') == p:
                            testv = o2.get('value')
                    if testv is not None and testv != en:
                        continue
                    cur = o.get('value')
                    if not isinstance(cur, str):
                        continue
                    if is_names:
                        m = GLYPH_PREFIX.match(cur)
                        prefix = m.group(0) if m else ''
                        new_val = prefix + want if not want.startswith('^') else want
                        if cur == new_val or cur.strip() == new_val.strip():
                            continue
                        report.append((ko_file, asset, p, cur[:60], new_val[:60]))
                        o['value'] = new_val
                        applied += 1
                    else:
                        if cur == want or cur.strip() == want.strip():
                            continue
                        report.append((ko_file, asset, p, cur[:60], want[:60]))
                        o['value'] = want
                        applied += 1

for pname, doc in changed_files.items():
    overrides[pname] = json.dumps(doc, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

print('ops to update:', applied)
print('patch files touched:', len(overrides))
with io.open('data/_user_tsv_apply.tsv', 'w', encoding='utf-8') as f:
    for r in report:
        f.write('\t'.join(x.replace('\n', '\\n') for x in r) + '\n')
if APPLY and overrides:
    sys.path.insert(0, 'tools')
    from pak_writer import write_pak
    write_pak(TR, TR, overrides)
    print('applied')
