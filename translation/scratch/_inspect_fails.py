# -*- coding: utf-8 -*-
# Inspect failing test ops in zz_translation_female.pak: expected vs actual.
import sys, io, os, re, json, csv, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

SB = r"E:\My Games\steamapps\common\Starbound"
MODS = SB + r"\mods"
TP = 'zz_translation_female.pak'
TRANSLATION_PAKS = {TP, 'zz_localeko_highpriority_20260927.pak', '-9998_trans_sbkor_0.98_structfix.pak'}
SKIP_PROVIDERS = TRANSLATION_PAKS | {'zz_female_overhaul.pak', 'zzz_diag_objdump'}


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


def flat_ops(ops, out):
    for o in ops:
        if isinstance(o, list):
            flat_ops(o, out)
        elif isinstance(o, dict):
            out.append(o)


def apply_patch_detail(doc, ops):
    fails = []
    flat = []
    flat_ops(ops, flat)
    for i, op in enumerate(flat):
        kind, path = op.get('op'), op.get('path', '')
        try:
            if kind == 'test':
                actual = ptr_get(doc, path)
                if actual != op.get('value'):
                    fails.append((i, path, op.get('value'), actual))
            elif kind in ('replace', 'add'):
                ptr_set(doc, path, op.get('value'), insert=(kind == 'add'))
            elif kind == 'remove':
                ptr_del(doc, path)
        except Exception as e:
            fails.append((i, path, op.get('value'), '<missing>'))
    return fails


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
        idx = reader.index
        read = reader.read
    else:
        idx = []
        for root, _, files in os.walk(reader):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), reader).replace('\\', '/')
                idx.append('/' + rel)

        def make_read(base):
            return lambda p: open(os.path.join(base, p.lstrip('/')), 'rb').read()
        read = make_read(reader)
    skip_prov = name.split('/')[-1] in SKIP_PROVIDERS or name.endswith('/')
    for path in idx:
        if path.endswith('.metadata'):
            continue
        if path.endswith('.patch'):
            real = path[:-6]
            if not skip_prov or name.split('/')[-1] in TRANSLATION_PAKS:
                patches_of.setdefault(real, []).append((name, read(path)))
            continue
        if skip_prov:
            continue
        base_of[path] = name

# assets where zz_translation_female has a patch AND another earlier patch exists
targets = [r[0] for r in csv.reader(open('data/attr_zz_fails.tsv', encoding='utf-8'), delimiter='\t')][1:]
print('targets:', len(targets))

cats = collections.Counter()
samples = collections.defaultdict(list)
mismatch_rows = []
for path in targets:
    base = base_of.get(path)
    if base is None:
        cats['nobase'] += 1
        continue
    try:
        doc = parse_sb(readers[base].read(path))
    except Exception:
        cats['noparse'] += 1
        continue
    plist = sorted(patches_of.get(path, []), key=lambda t: order[t[0]])
    zz_idx = [i for i, t in enumerate(plist) if t[0].split('/')[-1] == TP]
    if not zz_idx:
        cats['no_zz'] += 1
        continue
    zi = zz_idx[-1]
    # apply all patches BEFORE the zz patch
    for n, b in plist[:zi]:
        try:
            ops = json.loads(b.decode('utf-8'))
        except Exception:
            continue
        apply_patch_detail(doc, ops)
    # now test zz's ops against current doc
    try:
        zzops = json.loads(plist[zi][1].decode('utf-8'))
    except Exception:
        cats['zzparse'] += 1
        continue
    flat = []
    flat_ops(zzops, flat)
    for i, op in enumerate(flat):
        if op.get('op') != 'test':
            continue
        try:
            actual = ptr_get(doc, op.get('path', ''))
        except Exception:
            actual = '<missing>'
        if actual != op.get('value'):
            key = 'missing' if actual == '<missing>' else 'value_mismatch'
            cats[key] += 1
            if len(samples[key]) < 12:
                samples[key].append((path, op.get('path'), repr(op.get('value'))[:80], repr(actual)[:80]))
            mismatch_rows.append([path, op.get('path'), repr(op.get('value'))[:200], repr(actual)[:200]])

print(dict(cats))
for k, ss in samples.items():
    print('=====', k)
    for s in ss:
        print('  ', s[0], '|', s[1], '| exp:', s[2], '| act:', s[3])
w = csv.writer(open('data/zz_test_mismatch.tsv', 'w', encoding='utf-8', newline=''), delimiter='\t')
w.writerow(['asset', 'path', 'expected', 'actual'])
w.writerows(mismatch_rows)
print('wrote data/zz_test_mismatch.tsv rows:', len(mismatch_rows))
