#!/usr/bin/env python3
# Repair 'broken' patch entries: for each (provider, asset) flagged broken in
# coverage_survey.tsv, re-align every failing test op to the provider asset's
# CURRENT value at the same JSON pointer. If the pointer no longer exists,
# try to locate the test string elsewhere in the doc and repoint the op;
# otherwise drop the dead op pair. Keeps KO replace values untouched.
# NOTE: no literal backslash escapes in source (chr(92)/chr(13)/chr(10) only)
# so the file survives transport unharmed.
import csv, json, sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
csv.field_size_limit(10**8)
sys.path.insert(0, r"E:" + chr(92) + "My Games" + chr(92) + "steamapps" + chr(92) + "common" + chr(92) + "Starbound")
sys.path.insert(0, r"E:" + chr(92) + "My Games" + chr(92) + "steamapps" + chr(92) + "common" + chr(92) + "Starbound" + chr(92) + "translation" + chr(92) + "translation-baseline-20260921" + chr(92) + "tools")
from pak import Pak
from pak_writer import write_pak

BS = chr(92)
CR = chr(13)
LF = chr(10)
SB = "E:" + BS + "My Games" + BS + "steamapps" + BS + "common" + BS + "Starbound"
MODS = SB + BS + "mods"
TR = MODS + BS + "zz_translation_female.pak"

def parse_sb(raw):
    # Lenient Starbound JSON: strip // and /* */ comments outside strings,
    # escape literal CR/LF inside strings.
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
    body = ''.join(out)
    body = re.sub(r',(\s*[}\]])', r'\1', body)
    return json.loads(body)

def ptr_get(doc, path):
    parts = [p for p in path.split('/') if p != '']
    node = doc
    for p in parts:
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
    # Yield op groups whether the doc is a list of op-lists or a flat op list.
    if all(isinstance(g, list) for g in doc):
        return doc
    groups, cur = [], []
    for op in doc:
        if isinstance(op, dict) and op.get('op') == 'test' and cur:
            groups.append(cur)
            cur = []
        cur.append(op)
    if cur:
        groups.append(cur)
    return groups

def provider_pak(prov):
    if prov == 'packed.pak':
        return Pak(os.path.join(SB, 'assets', 'packed.pak'))
    return Pak(os.path.join(MODS, prov.split('/')[-1]))

survey_rows = [r for r in csv.reader(open('data/coverage_survey.tsv', encoding='utf-8'), delimiter='\t') if len(r) >= 3 and r[2] == 'broken']
targets = sorted({(r[0], r[1]) for r in survey_rows})
print('broken (provider,asset) pairs:', len(targets))

tr = Pak(TR)
ci = {}
for k in tr.index:
    ci.setdefault(k.lower(), []).append(k)
provs = {}
overrides = {}
stats = {'reassert': 0, 'repoint': 0, 'drop': 0, 'ok': 0, 'noasset': 0, 'nopatch': 0}
drop_log = []
for prov, asset in targets:
    patch_keys = ci.get((asset + '.patch').lower(), [])
    if not patch_keys:
        stats['nopatch'] += 1
        continue
    if prov not in provs:
        try:
            provs[prov] = provider_pak(prov)
        except Exception:
            provs[prov] = None
    ppak = provs[prov]
    if ppak is None or asset not in ppak.index:
        stats['noasset'] += 1
        continue
    try:
        src = parse_sb(ppak.read(asset))
    except Exception as e:
        stats['noasset'] += 1
        continue
    for patch_path in patch_keys:
        try:
            doc = json.loads(tr.read(patch_path).decode('utf-8'))
        except Exception:
            continue
        groups = iter_groups(doc)
        new_groups = []
        changed = False
        for g in groups:
            ops = [o for o in g if isinstance(o, dict)]
            if not ops:
                new_groups.append(g)
                continue
            test_ops = [o for o in ops if o.get('op') == 'test']
            if not test_ops:
                new_groups.append(g)
                continue
            keep = True
            for t in test_ops:
                cur, exists = ptr_get(src, t.get('path', ''))
                if exists and cur == t.get('value'):
                    stats['ok'] += 1
                    continue
                if exists and isinstance(cur, str):
                    stats['reassert'] += 1
                    t['value'] = cur
                    changed = True
                    continue
                tv = t.get('value')
                if isinstance(tv, str):
                    hits = find_value_paths(src, tv)
                    if hits:
                        stats['repoint'] += 1
                        t['path'] = hits[0]
                        changed = True
                        continue
                keep = False
                stats['drop'] += 1
                changed = True
                drop_log.append((prov, asset, t.get('path'), str(tv)[:60]))
                break
            if keep:
                new_groups.append(g)
        if changed:
            if all(isinstance(g, list) for g in doc):
                out_doc = new_groups
            else:
                out_doc = [o for g in new_groups for o in g]
            overrides[patch_path] = json.dumps(out_doc, ensure_ascii=False, indent=2).encode('utf-8')

print('stats:', stats)
print('patches to rewrite:', len(overrides))
print('dropped op groups:', len(drop_log))
for d in drop_log[:15]:
    print('  drop', d)
if '--apply' in sys.argv and overrides:
    print('entries:', write_pak(TR, TR, overrides))
