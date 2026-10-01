# Compare user-edited *_ko_*.tsv values against the deployed pak.
# For each row (id -> ko), resolve id->EN via uniq.json, EN->(asset,field) via work.tsv,
# then find replace ops in the asset's .patch whose path leaf == field and test == EN.
import sys, io, json, csv, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
csv.field_size_limit(sys.maxsize)

FILES = [
    ('c2957_ko_01.tsv', 'c2957'),
    ('gcyber_ko_01.tsv', 'gcyber'),
    ('gic_ko_09b.tsv', 'gic'),
    ('gic_ko_12.tsv', 'gic'),
    ('gicx_ko_01.tsv', 'gicx'),
    ('gicx_ko_03.tsv', 'gicx'),
    ('lfw_ko.tsv', 'lfw'),
    ('lfw_ko_manual.tsv', 'lfw'),
    ('ow_ko_03.tsv', 'ow'),
    ('rsr_ko_01.tsv', 'rsr'),
    ('rsr_ko_02.tsv', 'rsr'),
    ('sat_ko_01.tsv', 'sat'),
    ('sat_ko_03.tsv', 'sat'),
    ('sat_ko_04.tsv', 'sat'),
    ('sat_ko_04b.tsv', 'sat'),
    ('sat_ko_05.tsv', 'sat'),
    ('sat_ko_06.tsv', 'sat'),
    ('sat_names.tsv', 'sat'),
]

tr = Pak(TR)

def load_ko(path):
    rows = {}
    txt = io.open(path, encoding='utf-8').read()
    cur_id, cur = None, []
    for ln in txt.split('\n'):
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

def unfold(s):
    return s.replace('\\n', '\n')

results = []
for ko_file, pfx in FILES:
    uniq = json.load(io.open(BASE + '\\data\\' + pfx + '_uniq.json', encoding='utf-8'))
    work = list(csv.DictReader(io.open(BASE + '\\data\\' + pfx + '_work.tsv', encoding='utf-8-sig'), delimiter='\t'))
    en2slots = collections.defaultdict(list)
    for w in work:
        en2slots[w['en']].append((w['asset'], w['field']))
    ko = load_ko(BASE + '\\data\\' + ko_file)
    ndrift = nok = nmiss = 0
    for rid, kov in sorted(ko.items(), key=lambda kv: int(kv[0])):
        en = uniq.get(rid)
        if en is None:
            continue
        slots = en2slots.get(en, [])
        if not slots:
            nmiss += 1
            continue
        want = unfold(kov)
        for asset, field in slots:
            pname = asset + '.patch'
            if pname not in tr.index:
                # case-insensitive fallback
                hits = [k for k in tr.index if k.lower() == pname.lower()]
                if not hits:
                    continue
                pname = hits[0]
            try:
                doc = json.loads(tr.read(pname).decode('utf-8'))
            except Exception:
                continue
            for g in doc:
                for o in (g if isinstance(g, list) else [g]):
                    if not isinstance(o, dict):
                        continue
                    p = str(o.get('path', ''))
                    leaf = p.rsplit('/', 1)[-1]
                    if leaf != field and p != field:
                        continue
                    if o.get('op') == 'replace':
                        # match the sibling test value if present
                        testv = None
                        for o2 in (g if isinstance(g, list) else [g]):
                            if isinstance(o2, dict) and o2.get('op') == 'test' and o2.get('path') == p:
                                testv = o2.get('value')
                        if testv is not None and testv != en:
                            continue
                        nok += 1
                        if o.get('value') != want:
                            ndrift += 1
                            results.append((ko_file, asset, p, en, o.get('value'), want))
    print('%s: rows=%d checked=%d drift=%d no-slot=%d' % (ko_file, len(ko), nok, ndrift, nmiss))

with io.open('data/_drift_report.tsv', 'w', encoding='utf-8') as f:
    f.write('file\tasset\tpath\ten\tpak_ko\ttsv_ko\n')
    for r in results:
        f.write('\t'.join(x.replace('\n', '\\n')[:200] for x in r) + '\n')
print('total drift rows:', len(results))
