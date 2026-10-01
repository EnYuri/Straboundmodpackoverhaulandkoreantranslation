import sys, io, json, re, collections, pickle, copy
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
src = open('_verify_all_tests.py', encoding='utf-8').read()
exec(src.split('stats = collections.Counter()')[0])
rows = []
for name in tr.index:
    if not name.endswith('.patch'):
        continue
    try:
        doc = json.loads(tr.read(name).decode('utf-8'))
    except Exception:
        continue
    sdoc = provider_src(name[:-6].lower())
    if sdoc is None:
        rows.append((name, 'NO_SRC', '', '', ''))
        continue
    for g in iter_groups(doc):
        for o in g:
            if isinstance(o, dict) and o.get('op') == 'test' and 'value' in o:
                cur, ex = ptr_get(sdoc, o['path'])
                if not ex or cur != o['value']:
                    rows.append((name, o['path'],
                                 json.dumps(o['value'], ensure_ascii=False)[:80],
                                 'exists' if ex else 'missing',
                                 json.dumps(cur, ensure_ascii=False)[:80] if ex else ''))
with io.open('data/_fails_dump.txt', 'w', encoding='utf-8') as out:
    out.write(str(len(rows)) + ' failing tests\n')
    for r in rows:
        out.write('\t'.join(r) + '\n')
print('done', len(rows))
