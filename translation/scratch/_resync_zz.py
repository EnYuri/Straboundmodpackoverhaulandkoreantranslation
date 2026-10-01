# -*- coding: utf-8 -*-
# Resync zz_translation_female.pak test ops against the document state that
# actually exists when the patch applies (base + all earlier patches, each
# applied atomically: a patch with a failing test aborts wholesale).
# - test mismatch -> set test value to actual
# - test path missing -> drop the whole op-group (nothing exists to translate)
# - replace/add/remove on missing paths -> drop that op
import sys, io, os, re, json, csv, copy, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:/My Games/steamapps/common/Starbound")
sys.path.insert(0, "tools")
from pak import Pak
import pak_writer

SB = r"E:/My Games/steamapps/common/Starbound"
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


MISSING = object()


def ptr_get(doc, p):
    cur = doc
    for part in ptr_parts(p):
        if isinstance(cur, dict):
            if part not in cur:
                return MISSING
            cur = cur[part]
        elif isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except Exception:
                return MISSING
        else:
            return MISSING
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


def apply_patch_atomic(doc, ops):
    """engine semantics: any failure aborts the whole patch. Returns ok."""
    flat = []
    flat_ops(ops, flat)
    tmp = copy.deepcopy(doc)
    try:
        for op in flat:
            kind, path = op.get('op'), op.get('path', '')
            if kind == 'test':
                cur = tmp
                for part in ptr_parts(path):
                    cur = cur[part] if isinstance(cur, dict) else cur[int(part)]
                if cur != op.get('value'):
                    return False
            elif kind in ('replace', 'add'):
                ptr_set(tmp, path, op.get('value'), insert=(kind == 'add'))
            elif kind == 'remove':
                ptr_del(tmp, path)
    except Exception:
        return False
    return tmp


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

targets = [r[0] for r in csv.reader(open('data/attr_broken2.tsv', encoding='utf-8'), delimiter='\t')][1:]
print('targets:', len(targets))

ov = {}
stats = collections.Counter()
for path in targets:
    base = base_of.get(path)
    if base is None:
        stats['nobase'] += 1
        continue
    try:
        doc = parse_sb(readers[base].read(path))
    except Exception:
        stats['noparse'] += 1
        continue
    plist = sorted(patches_of.get(path, []), key=lambda t: order[t[0]])
    zis = [i for i, t in enumerate(plist) if t[0].split('/')[-1] == TP]
    if not zis:
        stats['no_zz'] += 1
        continue
    zi = zis[-1]
    for n, b in plist[:zi]:
        try:
            ops = json.loads(b.decode('utf-8'))
        except Exception:
            continue
        r = apply_patch_atomic(doc, ops)
        if r is not False:
            doc = r
    try:
        zzops = json.loads(plist[zi][1].decode('utf-8'))
    except Exception:
        stats['zzparse'] += 1
        continue

    changed = [False]

    def fix_group(g):
        if not isinstance(g, list):
            return g
        out = []
        for op in g:
            if not isinstance(op, dict):
                out.append(op)
                continue
            kind, p = op.get('op'), op.get('path', '')
            if kind == 'test':
                actual = ptr_get(doc, p)
                if actual is MISSING:
                    stats['drop_test'] += 1
                    changed[0] = True
                    continue  # drop test AND any sibling writes to same path
                if actual != op.get('value'):
                    op = dict(op)
                    op['value'] = copy.deepcopy(actual)
                    stats['resync'] += 1
                    changed[0] = True
                out.append(op)
            elif kind in ('replace', 'remove') and ptr_get(doc, p) is MISSING:
                stats['drop_write'] += 1
                changed[0] = True
                continue
            else:
                out.append(op)
        return out

    if zzops and isinstance(zzops, list) and all(isinstance(g, list) for g in zzops):
        newops = [fix_group(g) for g in zzops]
        newops = [g for g in newops if g]
    else:
        newops = fix_group(zzops)

    if changed[0]:
        real = path + '.patch' if not path.endswith('.patch') else path
        ov[real] = json.dumps(newops, ensure_ascii=False,
                              separators=(',', ':')).encode('utf-8')
        stats['files'] += 1

print(dict(stats))
pak_writer.write_pak(os.path.join(MODS, TP) + '.staged', os.path.join(MODS, TP), ov)
os.replace(os.path.join(MODS, TP) + '.staged', os.path.join(MODS, TP))
print('replaced', len(ov), 'patch files')
