#!/usr/bin/env python3
# Normalize patch entry paths to provider-canonical asset casing and merge
# case-variant duplicate patch files into a single canonical patch.
# Conflict rules (same JSON path covered by multiple op groups):
#   - same source file: later group wins (patch apply semantics)
#   - different files: a group whose test ops pass against the current
#     provider asset beats one whose tests fail
#   - otherwise prefer the all-lowercase variant (newer campaign content)
# Output file lives at the provider-canonical patch path.
import os, sys, io, json, struct, pickle, collections, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BS = chr(92)
CR = chr(13)
LF = chr(10)
sys.path.insert(0, "E:" + BS + "My Games" + BS + "steamapps" + BS + "common" + BS + "Starbound")
sys.path.insert(0, "E:" + BS + "My Games" + BS + "steamapps" + BS + "common" + BS + "Starbound" + BS + "translation" + BS + "translation-baseline-20260921" + BS + "tools")
from pak import Pak
from pak_writer import _vlq, load_meta_blob

SB = "E:" + BS + "My Games" + BS + "steamapps" + BS + "common" + BS + "Starbound"
MODS = SB + BS + "mods"
TR = MODS + BS + "zz_translation_female.pak"

_store = pickle.load(open('data/_canon_cases.pkl', 'rb'))
CASES = _store['cases']
OWNER = _store['owner']

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

def canonical_base(lk):
    votes = CASES.get(lk)
    if not votes:
        return lk
    w = votes.most_common()
    top = [c for c, n in w if n == w[0][1]]
    if len(top) > 1 and lk in top:
        return lk
    return w[0][0]

def group_paths(g):
    return {o.get('path') for o in g if isinstance(o, dict) and o.get('path')}

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

def group_sig(g):
    return json.dumps(g, ensure_ascii=False, sort_keys=True)

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

tr = Pak(TR)
groups = collections.defaultdict(list)
for k in tr.index:
    if k.endswith('.patch'):
        groups[k[:-6].lower()].append(k)

_src_cache = {}
def provider_src(lk):
    if lk in _src_cache:
        return _src_cache[lk]
    src = None
    pp = OWNER.get(lk)
    if pp:
        try:
            pk = Pak(pp)
            a = canonical_base(lk)
            if a in pk.index:
                src = parse_sb(pk.read(a))
        except Exception:
            src = None
    _src_cache[lk] = src
    return src

def group_tests_pass(g, src):
    if src is None:
        return None
    tests = [o for o in g if isinstance(o, dict) and o.get('op') == 'test']
    if not tests:
        return True  # no test op = applies unconditionally
    for t in tests:
        cur, exists = ptr_get(src, t.get('path', ''))
        if not exists or cur != t.get('value'):
            return False
    return True

overrides = {}
deletes = set()
stats = {'dup_merge': 0, 'rename': 0, 'noop': 0, 'keep_earlier': 0,
         'exact_dup': 0, 'later_wins': 0, 'samefile_later': 0}
drop_log = []

for lk, variants in groups.items():
    canon_patch = canonical_base(lk) + '.patch'
    if len(variants) == 1:
        v = variants[0]
        if v == canon_patch:
            stats['noop'] += 1
            continue
        # singleton at non-canonical case -> rename
        overrides[canon_patch] = tr.read(v)
        deletes.add(v)
        stats['rename'] += 1
        continue

    # variants processed in index sort order: later file's group wins a path
    # conflict (matches in-game last-wins), EXCEPT when the later group's test
    # fails while the earlier one passes -> keep the working earlier group.
    ordered = sorted(variants)
    src = provider_src(lk)
    merged, seen, covered = [], set(), {}
    for v in ordered:
        try:
            doc = json.loads(tr.read(v).decode('utf-8'))
        except Exception:
            continue
        for g in iter_groups(doc):
            sig = group_sig(g)
            if sig in seen:
                stats['exact_dup'] += 1
                continue
            gp = group_paths(g)
            clash = gp & set(covered)
            if not clash:
                seen.add(sig)
                for pth in gp:
                    covered[pth] = v
                merged.append(g)
                continue
            idx = None
            for i, mg in enumerate(merged):
                if group_paths(mg) & clash:
                    idx = i
                    break
            owner_v = covered[next(iter(clash))]
            ep = group_tests_pass(merged[idx], src)
            np_ = group_tests_pass(g, src)
            # later file wins unless its group provably fails test (dead op)
            keep_new = (owner_v == v) or (np_ is not False)
            if keep_new:
                if owner_v != v:
                    drop_log.append((lk, v, owner_v, json.dumps(g, ensure_ascii=False)[:200], json.dumps(merged[idx], ensure_ascii=False)[:200], 'later_wins'))
                for pth in group_paths(merged[idx]):
                    covered.pop(pth, None)
                merged[idx] = g
                seen.add(sig)
                for pth in gp:
                    covered[pth] = v
                if owner_v == v:
                    stats['samefile_later'] += 1
                else:
                    stats['later_wins'] += 1
            else:
                stats['keep_earlier'] += 1
                drop_log.append((lk, owner_v, v, json.dumps(merged[idx], ensure_ascii=False)[:200], json.dumps(g, ensure_ascii=False)[:200], 'keep_earlier'))

    overrides[canon_patch] = json.dumps(merged, ensure_ascii=False, indent=2).encode('utf-8')
    for v in variants:
        if v != canon_patch:
            deletes.add(v)
    stats['dup_merge'] += 1

import csv
print('stats:', stats)
print('overrides:', len(overrides), 'deletes:', len(deletes), 'kept-earlier drops:', len(drop_log))
with open('data/dedupe_conflicts.tsv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['asset_lower', 'kept_variant', 'dropped_variant', 'kept_group', 'dropped_group', 'reason'])
    for d in drop_log:
        w.writerow(d)
if '--apply' not in sys.argv:
    sys.exit(0)

meta_blob = load_meta_blob(TR)
p = Pak(TR)
files = {}
for name in p.index:
    if name not in deletes:
        files[name] = p.read(name)
files.update(overrides)
del p
buf = bytearray(b"SBAsset6" + b"\x00" * 8)
index_entries = []
for name in sorted(files):
    data = files[name]
    off = len(buf)
    buf += data
    index_entries.append((name.encode("utf-8"), off, len(data)))
index_off = len(buf)
buf += meta_blob
buf += _vlq(len(index_entries))
for name, off, n in index_entries:
    buf += _vlq(len(name)) + name + struct.pack(">QQ", off, n)
buf[8:16] = struct.pack(">Q", index_off)
tmp_path = TR + ".tmp_write"
with open(tmp_path, "wb") as f:
    f.write(bytes(buf))
os.replace(tmp_path, TR)
print('entries:', len(files))
