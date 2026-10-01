# -*- coding: utf-8 -*-
# Fix zz_translation_female.pak patches that self-abort:
# 1) duplicate write-groups for the same path inside one patch: keep the LAST
#    group only (its test then sees the true upstream value).
# 2) test mismatch vs pre-patch doc: resync test to actual.
# 3) ops on missing paths: drop them.
# Doc state is computed with engine-like atomic patch application
# (a patch with a failing op aborts wholesale).
import sys, io, os, re, json, csv, copy, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, "tools")
from pak import Pak
import pak_writer

SB = r"E:\My Games\steamapps\common\Starbound"
MODS = SB + r"\mods"
TP = 'zz_translation_female.pak'
TRANSLATION_PAKS = {TP, 'zz_localeko_highpriority_20260927.pak', '-9998_trans_sbkor_0.98_structfix.pak'}
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
        read = (lambda b: lambda p: open(os.path.join(b, p.lstrip('/')), 'rb').read())(reader)
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

targets = [r[0] for r in csv.reader(open('data/attr_broken2.tsv', encoding='utf-8'), delimiter='\t')][1:]
print('targets:', len(targets))

ov = {}
stats = collections.Counter()


def fix_ops(ops, doc):
    """ops = parsed patch (list). Returns (new_ops, changed).
    - duplicate writer-groups on one path: keep the LAST writer, drop the
      earlier groups' ops for that path (their tests compare to upstream value
      while the earlier write already changed it -> self-abort).
    - test mismatch vs pre-patch doc: resync test value to actual.
    - test/replace/remove on missing path: drop op."""
    changed = False
    # fully flatten nested op groups (some files nest 3 levels deep)
    flat = []
    flat_ops(ops, flat)

    # last writer index per path
    lastw = {}
    for i, op in enumerate(flat):
        if op.get('op') in ('replace', 'remove'):
            lastw[op.get('path', '')] = i

    keep = []
    for i, op in enumerate(flat):
        k, p = op.get('op'), op.get('path', '')
        # stale duplicate: a later op writes the same path
        if lastw.get(p, i) > i and k in ('test', 'replace', 'remove'):
            stats['drop_dup'] += 1
            changed = True
            continue
        actual = ptr_get(doc, p)
        if k == 'test':
            if actual is MISSING:
                stats['drop_op'] += 1
                changed = True
                continue
            if actual != op.get('value'):
                op = dict(op)
                op['value'] = copy.deepcopy(actual)
                stats['resync'] += 1
                changed = True
        elif k in ('replace', 'remove') and actual is MISSING:
            stats['drop_op'] += 1
            changed = True
            continue
        keep.append(op)
    return keep, changed


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
        r = apply_atomic(doc, ops)
        if r is not None:
            doc = r
    try:
        zzops = json.loads(plist[zi][1].decode('utf-8'))
    except Exception:
        stats['zzparse'] += 1
        continue
    newops, changed = fix_ops(zzops, doc)
    if changed:
        ov[path + '.patch'] = json.dumps(
            newops, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        stats['files'] += 1

print(dict(stats))
if ov:
    pak_writer.write_pak(os.path.join(MODS, TP) + '.staged', os.path.join(MODS, TP), ov)
    for _ in range(30):
        try:
            os.replace(os.path.join(MODS, TP) + '.staged', os.path.join(MODS, TP))
            print('replaced', len(ov), 'patch files')
            break
        except PermissionError:
            import time
            time.sleep(2)
else:
    print('no changes')
