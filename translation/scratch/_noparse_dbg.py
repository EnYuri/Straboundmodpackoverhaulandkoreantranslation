# -*- coding: utf-8 -*-
# List broken-survey assets whose base still fails to parse, with error detail.
import sys, io, os, re, json, csv, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

SB = r"E:\My Games\steamapps\common\Starbound"
MODS = SB + r"\mods"


def parse_sb(raw):
    s = raw.decode('utf-8', errors='replace')
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
base_of = {}
for name, kind, reader in providers:
    if kind == 'pak':
        idx = reader.index
    else:
        idx = []
        for root, _, files in os.walk(reader):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), reader).replace('\\', '/')
                idx.append('/' + rel)
    for path in idx:
        if path.endswith(('.metadata', '.patch')) or name.endswith('/'):
            continue
        base_of[path] = name

rows = list(csv.reader(open('data/coverage_survey.tsv', encoding='utf-8'), delimiter='\t'))[1:]
bad = collections.Counter()
for r in rows:
    if r[2] != 'broken':
        continue
    path, base = r[1], base_of.get(r[1])
    if base is None:
        bad['nobase'] += 1
        continue
    try:
        parse_sb(readers[base].read(path))
    except Exception as e:
        bad['noparse'] += 1
        if bad['noparse'] <= 15:
            print(path, '|', base.split('/')[-1], '|', type(e).__name__, str(e)[:100])
print(dict(bad))
