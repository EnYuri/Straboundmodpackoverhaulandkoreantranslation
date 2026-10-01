# Reclassify 'broken' rows from coverage_survey.tsv: an asset is effectively
# covered if, after applying every X.patch in load order (failed test ops
# abort only their own op), the fields the translation patch targeted end up
# Korean or were last written by a translation pak.
import sys, io, os, re, json, csv
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

SB = r"E:\My Games\steamapps\common\Starbound"
MODS = SB + r"\mods"
SURV = r"data\coverage_survey.tsv"
OUT = r"data\coverage_broken_detail.tsv"
TRANSLATION_PAKS = {
    'zz_translation_female.pak',
    'zz_localeko_highpriority_20260927.pak',
    '-9998_trans_sbkor_0.98_structfix.pak',
}
HANGUL = re.compile(r'[가-힯]')
TEXT_KEYS = {'shortdescription', 'description', 'title', 'subtitle', 'itemName',
             'objectName', 'label', 'text', 'caption', 'greeting',
             'completionText', 'turnInDescription', 'questText', 'bountyText',
             'upgradeDescription', 'tooltipText', 'paneTitle', 'windowTitle',
             'message', 'flavorText', 'chatTitle', 'subtitleText'}


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


def ptr_parts(p):
    return [s.replace('~1', '/').replace('~0', '~') for s in p.strip('/').split('/')]


def ptr_get(doc, p):
    cur = doc
    for part in ptr_parts(p):
        cur = cur[part] if isinstance(cur, dict) else cur[int(part)]
    return cur


def ptr_set(doc, p, val, insert=False):
    parts = ptr_parts(p)
    cur = doc
    for part in parts[:-1]:
        cur = cur[part] if isinstance(cur, dict) else cur[int(part)]
    last = parts[-1]
    if isinstance(cur, list):
        if last == '-':
            cur.append(val)
        else:
            i = int(last)
            cur.insert(i, val) if insert else cur.__setitem__(i, val)
    else:
        cur[last] = val


def ptr_del(doc, p):
    parts = ptr_parts(p)
    cur = doc
    for part in parts[:-1]:
        cur = cur[part] if isinstance(cur, dict) else cur[int(part)]
    last = parts[-1]
    cur.pop(int(last)) if isinstance(cur, list) else cur.pop(last, None)


def flat(ops, out):
    for o in ops:
        if isinstance(o, list):
            flat(o, out)
        elif isinstance(o, dict):
            out.append(o)


def apply_ops(doc, ops):
    """apply ops, aborting only ops that fail; return per-path last-writer is
    tracked outside via returned executed list"""
    fl = []
    flat(ops, fl)
    done = []
    for op in fl:
        kind, path = op.get('op'), op.get('path', '')
        try:
            if kind == 'test':
                if ptr_get(doc, path) != op.get('value'):
                    continue
            elif kind in ('replace', 'add'):
                ptr_set(doc, path, op.get('value'), insert=(kind == 'add'))
            elif kind == 'remove':
                ptr_del(doc, path)
            else:
                continue
            done.append(op)
        except Exception:
            continue
    return done


# providers in load order
providers = []
providers.append(('packed.pak', Pak(SB + r"\assets\packed.pak")))
for fn in sorted(os.listdir(MODS), key=str.lower):
    if fn.endswith('.pak'):
        try:
            providers.append(('mods/' + fn, Pak(os.path.join(MODS, fn))))
        except Exception:
            pass
order = {n: i for i, (n, p) in enumerate(providers)}
dirs = []
for fn in sorted(os.listdir(MODS), key=str.lower):
    fp = os.path.join(MODS, fn)
    if os.path.isdir(fp):
        idx = set()
        for root, _, files in os.walk(fp):
            for f in files:
                idx.add('/' + os.path.relpath(os.path.join(root, f), fp).replace('\\', '/'))
        dirs.append(('mods/' + fn + '/', fp, idx))

csv.field_size_limit(10 ** 8)
rows = list(csv.reader(open(SURV, encoding='utf-8'), delimiter='\t'))[1:]
broken = [(r[0], r[1]) for r in rows if r[2] == 'broken']
print('broken assets to rescan:', len(broken))


def read_asset(provider, path):
    if provider == 'packed.pak':
        return providers[0][1].read(path)
    for n, p in providers:
        if n == provider:
            return p.read(path)
    raise KeyError(provider)


def all_patches(path):
    out = []
    pp = path + '.patch'
    for n, p in providers:
        if pp in p.index:
            out.append((n, p.read(pp)))
    for n, fp, idx in dirs:
        if pp in idx:
            out.append((n, open(os.path.join(fp, pp.lstrip('/')), 'rb').read()))
    return sorted(out, key=lambda t: order.get(t[0], 9999))


final_en = []
for prov, path in broken:
    try:
        doc = parse_sb(read_asset(prov, path))
    except Exception:
        continue
    lastwriter = {}
    for n, b in all_patches(path):
        try:
            ops = json.loads(b.decode('utf-8'))
        except Exception:
            continue
        for op in apply_ops(doc, ops):
            if op.get('op') in ('replace', 'add'):
                lastwriter[op.get('path')] = (n, op.get('value'))
    # fields the translation pak meant to translate
    tfields = set()
    for n, b in all_patches(path):
        if n.split('/')[-1] not in TRANSLATION_PAKS:
            continue
        try:
            ops = json.loads(b.decode('utf-8'))
        except Exception:
            continue
        fl = []
        flat(ops, fl)
        for op in fl:
            if op.get('op') == 'replace':
                tfields.add(op.get('path'))
    enleft = []
    for tp in tfields or ['/shortdescription', '/description', '/title']:
        try:
            v = ptr_get(doc, tp)
        except Exception:
            continue
        if isinstance(v, str) and re.search(r'[A-Za-z]', v) and not HANGUL.search(v):
            w = lastwriter.get(tp, ('<none>', ''))
            if w[0].split('/')[-1] not in TRANSLATION_PAKS:
                enleft.append((tp, w[0].split('/')[-1], v[:60]))
    if enleft:
        final_en.append((prov, path, enleft[:3]))

print('truly-english after simulation:', len(final_en))
with open(OUT, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['provider', 'asset', 'field', 'last_writer', 'en'])
    for prov, path, fs in final_en:
        for tp, lw, v in fs:
            w.writerow([prov, path, tp, lw, v])
import collections
c = collections.Counter(x[0] for x in final_en)
for p, n in c.most_common(20):
    print('  %-65s %d' % (p, n))
