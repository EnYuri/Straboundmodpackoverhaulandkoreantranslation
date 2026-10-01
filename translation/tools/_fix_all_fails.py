#!/usr/bin/env python3
# Comprehensive patch integrity pass over the whole translation pak.
# Per patch file, per op group:
#   A) drop replace ops that write Hangul into identifier fields
#      (/itemName, /objectName) - these corrupt the item registry.
#   B) for every failing test op, in order:
#      1. repoint: if the test value exists elsewhere in the doc, retarget
#         the op path (handles moved fields / shifted list indices)
#      2. reassert: if the path exists with a different value, set test
#         to the current value (EN text changed in place)
#      3. drop: path gone and text nowhere -> remove the whole op group
#         so it cannot fail the file
#   C) test ops with missing/null value: set to current value if path
#      exists, else drop group.
import sys, io, json, re, pickle, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BS = chr(92)
CR = chr(13)
LF = chr(10)
sys.path.insert(0, "E:" + BS + "My Games" + BS + "steamapps" + BS + "common" + BS + "Starbound")
sys.path.insert(0, "E:" + BS + "My Games" + BS + "steamapps" + BS + "common" + BS + "Starbound" + BS + "translation" + BS + "translation-baseline-20260921" + BS + "tools")
from pak import Pak
from pak_writer import write_pak

SB = "E:" + BS + "My Games" + BS + "steamapps" + BS + "common" + BS + "Starbound"
TR = SB + BS + "mods" + BS + "zz_translation_female.pak"
_store = pickle.load(open('data/_canon_cases.pkl', 'rb'))
CASES = _store['cases']
OWNER = _store['owner']
PATCHERS = _store['patchers']
HANGUL = re.compile(r'[가-힯-힣ㄱ-ㅎㅏ-ㅣ]')
IDENT = {'itemname', 'objectname'}

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

def find_value_paths(node, target, cur=''):
    hits = []
    if isinstance(node, dict):
        for k, v in node.items():
            np = cur + '/' + k.replace('~', '~0').replace('/', '~1')
            if v == target:
                hits.append(np)
            else:
                hits += find_value_paths(v, target, np)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            hits += find_value_paths(v, target, cur + '/' + str(i))
    return hits

def iter_groups(doc):
    if all(isinstance(g, list) for g in doc):
        return list(doc)
    groups, cur = [], []
    for op in doc:
        if isinstance(op, dict) and op.get('op') == 'test' and cur:
            groups.append(cur)
            cur = []
        cur.append(op)
    if cur:
        groups.append(cur)
    return groups

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
    # Effective document: base asset + every provider-side .patch applied
    # in pak load order (packed.pak first, then sorted mod filenames).
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
            if not pk2:
                continue
            if ppath in pk2.index:
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

overrides = {}
stats = collections.Counter()
ident_log = []
for name in tr.index:
    if not name.endswith('.patch'):
        continue
    lk = name[:-6].lower()
    try:
        doc = json.loads(tr.read(name).decode('utf-8'))
    except Exception:
        continue
    groups = iter_groups(doc)
    src = provider_src(lk)
    new_groups = []
    changed = False
    for g in groups:
        ops = [o for o in g if isinstance(o, dict)]
        # A) identifier KO replaces
        ident_ops = [o for o in ops if o.get('op') == 'replace' and str(o.get('path', '')).lstrip('/').lower() in IDENT and HANGUL.search(str(o.get('value', '')))]
        if ident_ops:
            changed = True
            ops = [o for o in ops if o not in ident_ops]
            ident_log.append((name, g))
            stats['ident_removed'] += len(ident_ops)
            if not ops:
                stats['ident_group_dropped'] += 1
                continue
        # B) failing tests
        keep = True
        for t in [o for o in ops if o.get('op') == 'test']:
            if src is None:
                break
            path = t.get('path', '')
            cur, exists = ptr_get(src, path)
            if exists and cur == t.get('value'):
                continue
            tv = t.get('value')
            if tv is None:
                if exists:
                    t['value'] = cur
                    changed = True
                    stats['test_value_filled'] += 1
                    continue
                keep = False
                stats['drop_nulltest'] += 1
                break
            # repoint first: same value elsewhere
            hits = find_value_paths(src, tv) if isinstance(tv, str) else []
            if hits:
                t['path'] = hits[0]
                # also retarget sibling ops in the same group on the old path
                for o in ops:
                    if o is not t and o.get('path') == path:
                        o['path'] = hits[0]
                changed = True
                stats['repointed'] += 1
                continue
            # reassert only for named-field paths; a different value at a
            # numeric index is a different logical entry -> drop the pair
            leaf = path.rstrip('/').split('/')[-1]
            if exists and not leaf.isdigit():
                t['value'] = cur
                changed = True
                stats['reasserted'] += 1
                continue
            keep = False
            stats['group_dropped'] += 1
            break
        if keep and ops:
            new_groups.append(ops)
        elif not keep:
            changed = True
    if changed:
        out_doc = new_groups if all(isinstance(g, list) for g in doc) else [o for g in new_groups for o in g]
        overrides[name] = json.dumps(out_doc, ensure_ascii=False, indent=2).encode('utf-8')

print(dict(stats))
print('patches rewritten:', len(overrides))
print('ident groups removed:', len(ident_log))
if '--apply' in sys.argv and overrides:
    print('entries:', write_pak(TR, TR, overrides))
