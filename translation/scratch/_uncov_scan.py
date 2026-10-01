# -*- coding: utf-8 -*-
# Scan 'uncovered' survey assets: extract every text field still holding English.
import sys, io, os, re, json, csv, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

SB = r"E:\My Games\steamapps\common\Starbound"
MODS = SB + r"\mods"
SKIP = {'zz_translation_female.pak', 'zz_localeko_highpriority_20260927.pak',
        '-9998_trans_sbkor_0.98_structfix.pak', 'zz_female_overhaul.pak', 'zzz_diag_objdump'}


def parse_sb(raw):
    s = raw.decode('utf-8-sig', errors='replace')
    s = re.sub(r'//[^\n]*', '', s)
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    out = []
    ins = False
    for i, c in enumerate(s):
        if c == '"' and (i == 0 or s[i - 1] != chr(92)):
            ins = not ins
        if ins and ord(c) < 0x20:
            out.append({'\r': '\\r', '\n': '\\n', '\t': '\\t'}.get(c, '\\u%04x' % ord(c)))
        else:
            out.append(c)
    return json.loads(re.sub(r',(\s*[}\]])', r'\1', ''.join(out)))


def walk(o, pre, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, pre + '/' + k, acc)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, '%s/%d' % (pre, i), acc)
    elif isinstance(o, str):
        acc.append((pre, o))


ID_LEAVES = {'itemName', 'objectName', 'name', 'id', 'file', 'path', 'image',
             'icon', 'kind', 'type', 'species', 'category', 'tooltipKind',
             'animation', 'sound', 'effect', 'projectile', 'script', 'quests'}


def looks_english(s):
    if not re.search(r'[A-Za-z]', s):
        return False
    if re.search(r'[가-힣]', s):
        return False
    if re.match(r'^[\w\-./\\:]+$', s) and ' ' not in s and len(s) < 60:
        return False  # identifier/path-like
    return True


providers = []
for fn in sorted(os.listdir(MODS), key=str.lower):
    fp = os.path.join(MODS, fn)
    if fn.endswith('.pak'):
        try:
            providers.append(('mods/' + fn, Pak(fp)))
        except Exception:
            pass

base_of = {}
for name, pk in providers:
    if name.split('/')[-1] in SKIP:
        continue
    for path in pk.index:
        if not path.endswith(('.metadata', '.patch')):
            base_of[path] = name

rows = list(csv.reader(open('data/coverage_survey.tsv', encoding='utf-8'), delimiter='\t'))[1:]
uncov = [(r[0], r[1]) for r in rows if r[2] == 'uncovered']

readers = dict(providers)
todo = []
by_field = collections.Counter()
for prov, path in uncov:
    base = base_of.get(path)
    if base is None or base not in readers:
        continue
    try:
        doc = parse_sb(readers[base].read(path))
    except Exception:
        continue
    acc = []
    walk(doc, '', acc)
    for p, v in acc:
        leaf = p.rsplit('/', 1)[-1]
        if leaf in ID_LEAVES:
            continue
        if looks_english(v):
            todo.append((base, path, p, v))
            by_field[leaf] += 1

print('english fields remaining:', len(todo), '| assets:', len(set(t[1] for t in todo)))
for k, v in by_field.most_common(20):
    print('%-24s %d' % (k, v))
w = csv.writer(open('data/uncov_english.tsv', 'w', encoding='utf-8', newline=''), delimiter='\t')
w.writerow(['provider', 'asset', 'field', 'en'])
for t in todo:
    w.writerow(t)
