# -*- coding: utf-8 -*-
# For 'broken' survey assets: simulate full chain, list fields still English at end.
import sys, io, os, re, json, csv, copy, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

SB = r"E:\My Games\steamapps\common\Starbound"
MODS = SB + r"\mods"
TRANSLATION_PAKS = {'zz_translation_female.pak', 'zz_localeko_highpriority_20260927.pak',
                    '-9998_trans_sbkor_0.98_structfix.pak'}
SKIP_PROVIDERS = TRANSLATION_PAKS | {'zz_female_overhaul.pak', 'zzz_diag_objdump'}


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
    cur.pop(int(parts[-1])) if isinstance(cur, list) else cur.pop(parts[-1], None)


def flat_ops(ops, out):
    for o in ops:
        if isinstance(o, list):
            flat_ops(o, out)
        elif isinstance(o, dict):
            out.append(o)


def apply_atomic(doc, ops):
    flat = []
    flat_ops(ops, flat)
    tmp = copy.deepcopy(doc)
    try:
        for op in flat:
            k, p = op.get('op'), op.get('path', '')
            if k == 'test':
                if ptr_get(tmp, p) != op.get('value'):
                    return None
            elif k in ('replace', 'add'):
                ptr_set(tmp, p, op.get('value'), insert=(k == 'add'))
            elif k == 'remove':
                ptr_del(tmp, p)
    except Exception:
        return None
    return tmp


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
             'animation', 'sound', 'effect', 'projectile', 'script', 'quests',
             'inventoryIcon', 'dualImage', 'muzzleFlash', 'renderLayer',
             'vehicleImage', 'directives', 'firingDirectives', 'config',
             'startSegmentImage', 'segmentImage', 'endSegmentImage',
             'endCollideSegmentImage', 'emptyInventoryIcon', 'filledInventoryIcon'}


def looks_english(s):
    if not re.search(r'[A-Za-z]', s) or re.search(r'[가-힣]', s):
        return False
    body = re.sub(r'\^\S{1,8};', '', s).strip()
    if re.match(r'^[\w\-./\\:]+\.\w+$', s):
        return False
    if re.match(r'^[\w\-./\\:]+$', body) and ' ' not in body:
        return False
    return True


providers = [('packed.pak', 'pak', Pak(SB + r"\assets\packed.pak"))]
for fn in sorted(os.listdir(MODS), key=str.lower):
    fp = os.path.join(MODS, fn)
    if fn.endswith('.pak'):
        try:
            providers.append(('mods/' + fn, 'pak', Pak(fp)))
        except Exception:
            pass
    elif os.path.isdir(fp):
        providers.append(('mods/' + fn + '/', 'dir', fp))

readers = {n: r for n, k, r in providers}
order = {n: i for i, (n, k, r) in enumerate(providers)}
base_of = {}
patches_of = {}
for name, kind, reader in providers:
    if kind == 'pak':
        idx, read = reader.index, reader.read
    else:
        idx = []
        for root, _, files in os.walk(reader):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), reader).replace('\\', '/')
                idx.append('/' + rel)

        def make_read(base):
            return lambda p: open(os.path.join(base, p.lstrip('/')), 'rb').read()
        read = make_read(reader)
    skip = name.split('/')[-1] in SKIP_PROVIDERS or name.endswith('/')
    for path in idx:
        if path.endswith('.metadata'):
            continue
        if path.endswith('.patch'):
            real = path[:-6]
            if not skip or name.split('/')[-1] in TRANSLATION_PAKS:
                patches_of.setdefault(real, []).append((name, read(path)))
            continue
        if skip:
            continue
        base_of[path] = name

rows = list(csv.reader(open('data/coverage_survey.tsv', encoding='utf-8'), delimiter='\t'))[1:]
targets = [r[1] for r in rows if r[2] == 'broken']
out = []
for path in targets:
    base = base_of.get(path)
    if base is None:
        continue
    try:
        doc = parse_sb(readers[base].read(path))
    except Exception:
        continue
    for n, b in sorted(patches_of.get(path, []), key=lambda t: order[t[0]]):
        try:
            ops = json.loads(b.decode('utf-8'))
        except Exception:
            continue
        r = apply_atomic(doc, ops)
        if r is not None:
            doc = r
    acc = []
    walk(doc, '', acc)
    for p, v in acc:
        leaf = p.rsplit('/', 1)[-1]
        if leaf in ID_LEAVES or leaf.isdigit():
            continue
        if looks_english(v):
            out.append((path, p, v))

print('english fields left after full chain:', len(out))
w = csv.writer(open('data/final_english.tsv', 'w', encoding='utf-8', newline=''), delimiter='\t')
w.writerow(['asset', 'field', 'en'])
for t in out:
    w.writerow(t)
for t in out:
    print(t[0], '|', t[1], '|', t[2][:90].replace('\n', '\\n'))
