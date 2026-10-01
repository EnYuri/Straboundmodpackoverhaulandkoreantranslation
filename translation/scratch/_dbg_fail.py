# -*- coding: utf-8 -*-
# Debug: for given asset, simulate chain and print the exact failing zz op.
import sys, io, os, re, json, csv, copy
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, "tools")
from pak import Pak

SB = r"E:\My Games\steamapps\common\Starbound"
MODS = SB + r"\mods"
TP = 'zz_translation_female.pak'
TRANSLATION_PAKS = {TP, 'zz_localeko_highpriority_20260927.pak', '-9998_trans_sbkor_0.98_structfix.pak'}
SKIP = TRANSLATION_PAKS | {'zz_female_overhaul.pak', 'zzz_diag_objdump'}

g = {}
prefix = open('scratch/_resync_zz.py', encoding='utf-8').read().split('providers =')[0]
prefix = '\n'.join(l for l in prefix.splitlines()
                   if 'TextIOWrapper' not in l and 'sys.stdout' not in l)
exec(prefix, g)
parse_sb = g['parse_sb']; ptr_parts = g['ptr_parts']; ptr_get = g['ptr_get']
ptr_set = g['ptr_set']; ptr_del = g['ptr_del']; flat_ops = g['flat_ops']
apply_atomic = g['apply_patch_atomic']; MISSING = g['MISSING']

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
        read = (lambda base: lambda p: open(os.path.join(base, p.lstrip('/')), 'rb').read())(reader)
    skip = name.split('/')[-1] in SKIP or name.endswith('/')
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

print('base_of size:', len(base_of), '| providers:', len(providers))
targets = sys.argv[1:]
if not targets:
    targets = [r[0] for r in csv.reader(
        open('data/attr_broken2.tsv', encoding='utf-8'), delimiter='\t')][1:8]
for path in targets:
    base = base_of.get(path)
    if base is None:
        print('===', path, '| NO BASE — providers having it:',
              [n for n, k, r in providers if k == 'pak' and path in r.index][:5])
        continue
    doc = parse_sb(readers[base].read(path))
    plist = sorted(patches_of.get(path, []), key=lambda t: order[t[0]])
    print('===', path, '| base:', base, '| patches:', [t[0].split('/')[-1] for t in plist])
    for n, b in plist:
        try:
            ops = json.loads(b.decode('utf-8'))
        except Exception:
            continue
        flat = []
        flat_ops(ops, flat)
        tmp = copy.deepcopy(doc)
        failop = None
        try:
            for op in flat:
                k, p = op.get('op'), op.get('path', '')
                if k == 'test':
                    a = ptr_get(tmp, p)
                    if a is MISSING or a != op.get('value'):
                        failop = (op, a)
                        break
                elif k in ('replace', 'add'):
                    ptr_set(tmp, p, op.get('value'), insert=(k == 'add'))
                elif k == 'remove':
                    ptr_del(tmp, p)
        except Exception as e:
            failop = ('EXC', e)
        if failop:
            print('  FAILS:', n.split('/')[-1], '|', json.dumps(failop, ensure_ascii=False, default=repr)[:300])
        else:
            doc = tmp
            print('  ok   :', n.split('/')[-1])
