#!/usr/bin/env python3
# Full verification: evaluate EVERY test op in every patch entry of the
# translation pak against the corresponding provider asset's current value.
# Reports per-asset counts of failing test ops (truly broken patches).
import sys, io, json, re, pickle, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BS = chr(92)
CR = chr(13)
LF = chr(10)
sys.path.insert(0, "E:" + BS + "My Games" + BS + "steamapps" + BS + "common" + BS + "Starbound")
from pak import Pak

SB = "E:" + BS + "My Games" + BS + "steamapps" + BS + "common" + BS + "Starbound"
TR = SB + BS + "mods" + BS + "zz_translation_female.pak"
_store = pickle.load(open('data/_canon_cases.pkl', 'rb'))
CASES = _store['cases']
OWNER = _store['owner']
PATCHERS = _store['patchers']

def parse_sb(raw):
    s = raw.decode('utf-8', errors='replace')
    out = []
    i, n, ins = 0, len(s), False
    while i < n:
        c = s[i]
        if c == '"' and (i == 0 or s[i - 1] != BS):
            ins = not ins
            out.append(c)
            i += 1
            continue
        if not ins and c == '/' and i + 1 < n and s[i + 1] == '/':
            while i < n and s[i] != LF:
                i += 1
            continue
        if not ins and c == '/' and i + 1 < n and s[i + 1] == '*':
            i += 2
            while i + 1 < n and not (s[i] == '*' and s[i + 1] == '/'):
                i += 1
            i += 2
            continue
        if ins and c == CR:
            out.append(BS + 'r')
            i += 1
            continue
        if ins and c == LF:
            out.append(BS + 'n')
            i += 1
            continue
        out.append(c)
        i += 1
    return json.loads(re.sub(r',(\s*[}\]])', r'\1', ''.join(out)))

def ptr_get(doc, path):
    node = doc
    for p in [x for x in path.split('/') if x != '']:
        p = p.replace('~1', '/').replace('~0', '~')
        if isinstance(node, dict):
            if p not in node:
                return None, False
            node = node[p]
        elif isinstance(node, list):
            try:
                node = node[int(p)]
            except Exception:
                return None, False
        else:
            return None, False
    return node, True

def ptr_parts(path):
    return [x.replace('~1', '/').replace('~0', '~') for x in path.split('/') if x != '']

def ptr_parent(doc, path):
    parts = ptr_parts(path)
    node = doc
    for p in parts[:-1]:
        if isinstance(node, dict):
            if p not in node:
                return None, None
            node = node[p]
        elif isinstance(node, list):
            try:
                node = node[int(p)]
            except Exception:
                return None, None
        else:
            return None, None
    return node, (parts[-1] if parts else None)

def patch_apply_op(doc, op):
    kind = op.get('op')
    path = op.get('path', '')
    if kind == 'test':
        cur, exists = ptr_get(doc, path)
        return exists and cur == op.get('value')
    parent, key = ptr_parent(doc, path)
    if key is None:
        return False
    if kind in ('replace', 'add'):
        if isinstance(parent, dict):
            if kind == 'replace' and key not in parent:
                return False
            parent[key] = op.get('value')
            return True
        if isinstance(parent, list):
            if key == '-':
                parent.append(op.get('value'))
                return True
            try:
                i = int(key)
            except Exception:
                return False
            if kind == 'replace':
                if 0 <= i < len(parent):
                    parent[i] = op.get('value')
                    return True
                return False
            if 0 <= i <= len(parent):
                parent.insert(i, op.get('value'))
                return True
        return False
    if kind == 'remove':
        if isinstance(parent, dict) and key in parent:
            del parent[key]
            return True
        if isinstance(parent, list):
            try:
                i = int(key)
            except Exception:
                return False
            if 0 <= i < len(parent):
                parent.pop(i)
                return True
        return False
    if kind in ('move', 'copy'):
        fparent, fkey = ptr_parent(doc, op.get('from', ''))
        val = None
        if isinstance(fparent, dict) and fkey in fparent:
            val = fparent[fkey]
        elif isinstance(fparent, list):
            try:
                val = fparent[int(fkey)]
            except Exception:
                return False
        else:
            return False
        if kind == 'move':
            patch_apply_op(doc, {'op': 'remove', 'path': op.get('from', '')})
        return patch_apply_op(doc, {'op': 'add', 'path': path, 'value': val})
    return True

def iter_groups(doc):
    # Handle all-nested, flat, and mixed docs: list elements are groups;
    # bare dict ops accumulate into groups split at each 'test' op.
    groups, cur = [], []
    for el in doc:
        if isinstance(el, list):
            if cur:
                groups.append(cur)
                cur = []
            groups.append(el)
        else:
            if isinstance(el, dict) and el.get('op') == 'test' and cur:
                groups.append(cur)
                cur = []
            cur.append(el)
    if cur:
        groups.append(cur)
    return groups

def apply_patch_groups(doc, groups):
    for g in groups:
        ops = [o for o in g if isinstance(o, dict)]
        ok = True
        for o in ops:
            if o.get('op') == 'test' and not patch_apply_op(doc, o):
                ok = False
                break
        if not ok:
            continue
        for o in ops:
            if o.get('op') != 'test':
                patch_apply_op(doc, o)

def canonical_base(lk):
    votes = CASES.get(lk)
    if not votes:
        return lk
    return votes.most_common(1)[0][0]

tr = Pak(TR)
paks = {}
src_cache = {}
def provider_src(lk):
    if lk in src_cache:
        return src_cache[lk]
    src = None
    pp = OWNER.get(lk)
    if pp:
        if pp not in paks:
            try:
                paks[pp] = Pak(pp)
            except Exception:
                paks[pp] = None
        pk = paks[pp]
        if pk:
            a = canonical_base(lk)
            if a in pk.index:
                try:
                    src = parse_sb(pk.read(a))
                except Exception:
                    src = None
    if src is not None:
        import copy
        src = copy.deepcopy(src)
        for ppk_path, ppath in PATCHERS.get(lk, []):
            if ppk_path not in paks:
                try:
                    paks[ppk_path] = Pak(ppk_path)
                except Exception:
                    paks[ppk_path] = None
            pk2 = paks[ppk_path]
            if not pk2 or ppath not in pk2.index:
                continue
            try:
                pdoc = json.loads(pk2.read(ppath).decode('utf-8'))
            except Exception:
                try:
                    pdoc = parse_sb(pk2.read(ppath))
                except Exception:
                    continue
            apply_patch_groups(src, iter_groups(pdoc))
    src_cache[lk] = src
    return src

stats = collections.Counter()
fails = collections.Counter()
fail_samples = []
for name in tr.index:
    if not name.endswith('.patch'):
        continue
    lk = name[:-6].lower()
    src = provider_src(lk)
    if src is None:
        stats['no_provider_asset'] += 1
        continue
    try:
        doc = json.loads(tr.read(name).decode('utf-8'))
    except Exception:
        stats['unparseable_patch'] += 1
        continue
    flat = [o for g in doc for o in (g if isinstance(g, list) else [g])]
    ntest = nfail = 0
    for o in flat:
        if not isinstance(o, dict) or o.get('op') != 'test':
            continue
        ntest += 1
        cur, exists = ptr_get(src, o.get('path', ''))
        if not exists or cur != o.get('value'):
            nfail += 1
            if len(fail_samples) < 30:
                fail_samples.append((name, o.get('path'), str(o.get('value'))[:50], str(cur)[:50]))
    stats['patches'] += 1
    stats['test_ops'] += ntest
    if nfail:
        stats['patches_with_fails'] += 1
        stats['failed_ops'] += nfail
        fails[name] = nfail

print(dict(stats))
print('patches with failing ops:', len(fails))
for s in fail_samples[:20]:
    print(' ', s)
with open('data/verify_fails.tsv', 'w', encoding='utf-8') as f:
    for k, v in fails.most_common():
        f.write(f"{k}\t{v}\n")
