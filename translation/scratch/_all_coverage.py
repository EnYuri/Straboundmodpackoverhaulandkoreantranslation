# Full untranslated-text survey across every installed content pak/dir plus
# vanilla packed.pak. Coverage = a .patch for that asset path exists in one of
# the translation paks; additionally simulates patch application in filename
# order so that patches whose test ops fail are reported as 'broken'
# (effectively untranslated in-game).
import sys, io, os, re, json, csv
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

SB = r"E:\My Games\steamapps\common\Starbound"
MODS = SB + r"\mods"
OUT = r"data\coverage_survey.tsv"
SUM = r"data\coverage_survey_summary.txt"

TRANSLATION_PAKS = {
    'zz_translation_female.pak',
    'zz_localeko_highpriority_20260927.pak',
    '-9998_trans_sbkor_0.98_structfix.pak',
}
# providers that never contain game text worth scanning
SKIP_PROVIDERS = TRANSLATION_PAKS | {'zz_female_overhaul.pak', 'zzz_diag_objdump'}

TEXT_EXTS = {
    'item', 'consumable', 'thrownitem', 'activeitem', 'augment', 'currency',
    'flashlight', 'inspectiontool', 'chest', 'legs', 'head', 'back',
    'object', 'codex', 'questtemplate', 'npctype', 'tenant', 'species',
    'dialog', 'converse', 'madness', 'collection', 'statuseffect',
    'effectsource', 'tech', 'config', 'aiitem', 'mission', 'cinematic',
    'radiomessages', 'codexlearn', 'matitem', 'liquiditem', 'spawnitem',
    'crewcontract', 'crewmember', 'weaponability', 'tooltip',
}
TEXT_KEYS = {
    'shortdescription', 'description', 'title', 'subtitle', 'itemName',
    'objectName', 'label', 'text', 'caption', 'greeting', 'completionText',
    'turnInDescription', 'questText', 'bountyText', 'upgradeDescription',
    'tooltipText', 'paneTitle', 'windowTitle', 'message', 'flavorText',
    'chatTitle', 'subtitleText',
}
NON_TEXT_VAL = re.compile(r'^[\w\-./\\:]+$')
SENTENCE = re.compile(r'[A-Za-z]{2,} [A-Za-z]{2,}|[A-Z][a-z]{3,}')

ws = re.compile(r'\s')


def looks_display_text(v):
    if not isinstance(v, str) or not v.strip():
        return False
    if not SENTENCE.search(v):
        return False
    if v.startswith('/') or v.endswith(('.png', '.ogg', '.wav', '.json', '.frames')):
        return False
    return True


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


def find_text(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in TEXT_KEYS and looks_display_text(v):
                acc[k] = v
            elif isinstance(v, (dict, list)):
                find_text(v, acc)
    elif isinstance(o, list):
        for x in o:
            find_text(x, acc)


def ptr_parts(p):
    return [s.replace('~1', '/').replace('~0', '~') for s in p.strip('/').split('/')]


def ptr_get(doc, p):
    cur = doc
    for part in ptr_parts(p):
        if isinstance(cur, dict):
            cur = cur[part]
        elif isinstance(cur, list):
            cur = cur[int(part)]
        else:
            raise KeyError(p)
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


def apply_patch(doc, ops):
    """engine semantics: first failing op aborts the whole patch (atomic).
    returns list of failing ops (empty = applied)"""
    import copy
    fails = []
    flat = []
    flat_ops(ops, flat)
    tmp = copy.deepcopy(doc)
    for i, op in enumerate(flat):
        kind, path = op.get('op'), op.get('path', '')
        try:
            if kind == 'test':
                if ptr_get(tmp, path) != op.get('value'):
                    fails.append((i, path, op.get('value'), ptr_get(tmp, path)))
                    break
            elif kind in ('replace', 'add'):
                ptr_set(tmp, path, op.get('value'), insert=(kind == 'add'))
            elif kind == 'remove':
                ptr_del(tmp, path)
        except KeyError:
            fails.append((i, path, op.get('value'), '<missing>'))
            break
        except Exception:
            fails.append((i, path, op.get('value'), '<err>'))
            break
    if not fails:
        doc.clear() if isinstance(doc, dict) else doc.__setitem__(slice(None), tmp)
        if isinstance(doc, dict):
            doc.update(tmp)
    return fails


# ---------- enumerate providers ----------
providers = []  # (name, kind, reader)
providers.append(('packed.pak', 'pak', Pak(SB + r"\assets\packed.pak")))
for fn in sorted(os.listdir(MODS), key=str.lower):
    fp = os.path.join(MODS, fn)
    if fn.endswith('.pak'):
        try:
            providers.append(('mods/' + fn, 'pak', Pak(fp)))
        except Exception as e:
            print('!! cannot open', fn, e)
    elif os.path.isdir(fp):
        providers.append(('mods/' + fn + '/', 'dir', fp))

# pass1: real text assets + where they live (last provider wins)
base_of = {}          # asset -> provider name
text_of = {}          # asset -> {field: value}
patches_of = {}       # asset -> [ (provider, ops_json_bytes) ] in load order
prov_stats = {}

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
        ext = path.rsplit('.', 1)[-1].lower() if '.' in path else ''
        if ext not in TEXT_EXTS:
            continue
        try:
            doc = parse_sb(read(path))
        except Exception:
            continue
        if not isinstance(doc, (dict, list)):
            continue
        acc = {}
        find_text(doc, acc)
        if acc:
            base_of[path] = name
            text_of[path] = acc

print('providers:', len(providers), '| text assets:', len(text_of),
      '| assets with any patch:', len(patches_of))

# pass2: coverage + simulate apply
rows = []
prov_summary = {}
covered = broken = uncovered = 0
order = {n: i for i, (n, k, r) in enumerate(providers)}

for path, fields in sorted(text_of.items()):
    prov = base_of[path]
    plist = sorted(patches_of.get(path, []), key=lambda t: order[t[0]])
    t_patches = [(n, b) for n, b in plist if n.split('/')[-1] in TRANSLATION_PAKS]
    status = 'uncovered'
    fail_detail = ''
    if t_patches:
        try:
            doc = parse_sb(providers[[i for i, x in enumerate(providers)
                                      if x[0] == prov][0]][2].read(path))
        except Exception:
            doc = None
        t_fail = False
        if doc is not None:
            for n, b in plist:
                try:
                    ops = json.loads(b.decode('utf-8'))
                except Exception:
                    continue
                fails = apply_patch(doc, ops)
                if fails and n.split('/')[-1] in TRANSLATION_PAKS:
                    t_fail = True
                    fail_detail = json.dumps(fails[:2], ensure_ascii=False)[:200]
                    break
        status = 'broken' if t_fail else 'covered'
    if status == 'covered':
        covered += 1
    elif status == 'broken':
        broken += 1
    else:
        uncovered += 1
    ps = prov_summary.setdefault(prov, [0, 0, 0])
    ps[0 if status == 'covered' else 1 if status == 'broken' else 2] += 1
    if status != 'covered':
        fld, val = next(iter(fields.items()))
        rows.append([prov, path, status, fld,
                     ws.sub(' ', val)[:90], fail_detail])

with open(OUT, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['provider', 'asset', 'status', 'sample_field', 'sample_en', 'fail'])
    w.writerows(rows)

lines = ['%s | covered=%d broken=%d uncovered=%d' % (p, *prov_summary[p])
         for p in sorted(prov_summary)]
total = 'TOTAL text=%d covered=%d broken=%d uncovered=%d' % (
    len(text_of), covered, broken, uncovered)
with open(SUM, 'w', encoding='utf-8') as f:
    f.write(total + '\n' + '\n'.join(sorted(lines)))
print(total)
print('uncovered+broken rows:', len(rows), '->', OUT)
for p in sorted(prov_summary, key=lambda x: -prov_summary[x][2])[:25]:
    c, b, u = prov_summary[p]
    if u or b:
        print('  %-70s covered=%d broken=%d uncovered=%d' % (p, c, b, u))
