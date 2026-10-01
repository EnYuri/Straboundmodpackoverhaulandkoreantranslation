# Untranslated-coverage batch tool.
# Usage:
#   python tools/untrans_batch.py extract <provider-substr> <out_tsv>
#       -> rows: asset \t field \t en \t ko(reused-or-empty) \t reuse_src
#   python tools/untrans_batch.py apply <filled_tsv> [--apply]
#       -> builds X.patch entries (test=live EN, replace=ko), writes pak.
#
# Reuse: exact EN match against data/pak_pairs.tsv gives the existing Korean
# rendering for free (keeps wording consistent across duplicated item text).
import sys, io, os, re, json, csv
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\tools")
from pak import Pak
from pak_writer import write_pak

SB = r"E:\My Games\steamapps\common\Starbound"
MODS = SB + r"\mods"
TR = MODS + r"\zz_translation_female.pak"
SURV = r"data\coverage_survey.tsv"
PAIRS = r"data\pak_pairs.tsv"
csv.field_size_limit(10 ** 8)

TEXT_KEYS = {'shortdescription', 'description', 'title', 'subtitle', 'itemName',
             'objectName', 'label', 'text', 'caption', 'greeting',
             'completionText', 'turnInDescription', 'questText', 'bountyText',
             'upgradeDescription', 'tooltipText', 'paneTitle', 'windowTitle',
             'message', 'flavorText', 'chatTitle', 'subtitleText'}
SENTENCE = re.compile(r'[A-Za-z]{2,} [A-Za-z]{2,}|[A-Z][a-z]{3,}')


def parse_sb(raw):
    s = raw.decode('utf-8', errors='replace')
    s = re.sub(r'//[^\n]*', '', s)
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    out = []
    ins = False
    for i, c in enumerate(s):
        if c == '"' and (i == 0 or s[i - 1] != chr(92)):
            ins = not ins
        out.append('\\r' if ins and c == '\r' else '\\n' if ins and c == '\n' else c)
    return json.loads(re.sub(r',(\s*[}\]])', r'\1', ''.join(out)))


def find_text(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in TEXT_KEYS and isinstance(v, str) and v.strip() and SENTENCE.search(v) \
               and not v.startswith('/') and not v.endswith(('.png', '.ogg', '.wav', '.json', '.frames')):
                acc[k] = v
            elif isinstance(v, (dict, list)):
                find_text(v, acc)
    elif isinstance(o, list):
        for x in o:
            find_text(x, acc)


def provider_pak(prov):
    name = prov.split('/')[-1]
    return Pak(os.path.join(MODS, name)), name


def en_ko_map():
    m = {}
    with open(PAIRS, encoding='utf-8') as f:
        for r in csv.reader(f, delimiter='\t'):
            if len(r) >= 4 and r[2] and r[3]:
                m.setdefault(r[2], r[3])
    return m


if sys.argv[1] == 'extract':
    substr, out_tsv = sys.argv[2], sys.argv[3]
    rows = [r for r in csv.reader(open(SURV, encoding='utf-8'), delimiter='\t')]
    todo = [r for r in rows[1:] if r[2] == 'uncovered' and substr in r[0]]
    m = en_ko_map()
    done, out = 0, []
    by_prov = {}
    for r in todo:
        by_prov.setdefault(r[0], []).append(r[1])
    for prov, paths in by_prov.items():
        pk, pname = provider_pak(prov)
        for path in paths:
            try:
                doc = parse_sb(pk.read(path))
            except Exception:
                continue
            acc = {}
            find_text(doc, acc)
            for fld, en in acc.items():
                ko = m.get(en, '')
                if ko:
                    done += 1
                out.append([path, fld, en, ko, 'reuse' if ko else ''])
    with open(out_tsv, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['asset', 'field', 'en', 'ko', 'src'])
        w.writerows(out)
    print('rows:', len(out), 'reused:', done, 'todo:', len(out) - done, '->', out_tsv)

elif sys.argv[1] == 'apply':
    tsv = sys.argv[2]
    rows = [r for r in csv.reader(open(tsv, encoding='utf-8'), delimiter='\t')]
    prov_map = {}
    for r in rows[1:]:
        if len(r) >= 4 and r[3].strip():
            prov_map.setdefault(r[0], {})[r[1]] = r[3]
    # locate each asset's provider pak via survey
    surv = {}
    for r in csv.reader(open(SURV, encoding='utf-8'), delimiter='\t'):
        if len(r) >= 2:
            surv[r[1]] = r[0]
    paks = {}
    overrides = {}
    bad = 0
    for path, fmap in prov_map.items():
        prov = surv.get(path)
        if not prov:
            print('  no provider', path)
            continue
        if prov not in paks:
            paks[prov], _ = provider_pak(prov)
        try:
            doc = parse_sb(paks[prov].read(path))
        except Exception:
            print('  unreadable', path)
            continue
        ops = []
        for fld, ko in fmap.items():
            cur = doc.get(fld)
            if not isinstance(cur, str):
                bad += 1
                continue
            ops.append([{"op": "test", "path": "/" + fld, "value": cur},
                        {"op": "replace", "path": "/" + fld, "value": ko}])
        if ops:
            overrides[path + '.patch'] = json.dumps(ops, ensure_ascii=False, indent=2).encode('utf-8')
    print('patches:', len(overrides), 'fields skipped:', bad)
    if '--apply' in sys.argv and overrides:
        print('wrote pak; entries', write_pak(TR, TR, overrides))
    else:
        print('dry run')
