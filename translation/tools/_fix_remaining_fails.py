# Clean up remaining test-op fails reported by the effective-doc verify pass.
# Rules per failing test op that has an explicit 'value':
#   - path missing from effective doc            -> drop the whole op group
#   - current value contains Hangul (earlier KO pak owns the slot)
#                                                 -> reassert test to current value so our replace wins
#   - current value exists but is non-Korean     -> source text changed; drop the group (stale KO)
# Test ops without 'value' are existence checks; leave them untouched.
import sys, io, json, re, collections, pickle, copy
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")

exec(open('_verify_all_tests.py', encoding='utf-8').read().split('stats = collections.Counter()')[0])

HANGUL = re.compile(r'[가-힯-힣ㄱ-ㅎㅏ-ㅣ]')
APPLY = '--apply' in sys.argv

fails = {}
with open('data/verify_fails.tsv', encoding='utf-8') as f:
    for ln in f:
        p = ln.rstrip('\n').split('\t')
        if p and p[0]:
            fails[p[0]] = int(p[1]) if len(p) > 1 else 0

stats = collections.Counter()
overrides = {}
for name in fails:
    try:
        doc = json.loads(tr.read(name).decode('utf-8'))
    except Exception:
        stats['unparseable'] += 1
        continue
    sdoc = provider_src(name[:-6].lower())
    if sdoc is None:
        stats['no_src'] += 1
        continue
    groups = iter_groups(doc)
    stats['groups_seen'] += len(groups)
    newdoc = []
    changed = False
    for g in groups:
        tests = [o for o in g if isinstance(o, dict) and o.get('op') == 'test' and 'value' in o]
        stats['tests_seen'] += len(tests)
        drop = False
        for o in tests:
            cur, ex = ptr_get(sdoc, o['path'])
            if ex and cur == o['value']:
                continue
            if not ex:
                drop = True
                stats['drop_missing'] += 1
                break
            if isinstance(cur, str) and HANGUL.search(cur):
                o['value'] = cur
                stats['reassert_ko'] += 1
                changed = True
            else:
                drop = True
                stats['drop_changed'] += 1
                break
        if drop:
            stats['group_dropped'] += 1
            changed = True
            continue
        newdoc.append(g)
    if changed:
        # normalize to nested-groups form when the doc contained any nesting;
        # only a pure flat doc (no list elements at all) stays flat
        if any(isinstance(g, list) for g in doc):
            out = newdoc
        else:
            out = [o for g in newdoc for o in g]
        overrides[name] = json.dumps(out, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        stats['rewritten'] += 1

with io.open('data/_fix_remaining_out.txt', 'w', encoding='utf-8') as f:
    f.write('fails keys: %d\n' % len(fails))
    f.write(str(dict(stats)) + '\n')
    f.write('patches rewritten: %d\n' % len(overrides))
    if '/IFD_statuseffects.config.patch' in fails:
        _doc = json.loads(tr.read('/IFD_statuseffects.config.patch').decode('utf-8'))
        _sd = provider_src('/ifd_statuseffects.config')
        _nf = 0
        for _g in _doc:
            for _o in (_g if isinstance(_g, list) else [_g]):
                if isinstance(_o, dict) and _o.get('op') == 'test':
                    _c, _e = ptr_get(_sd, _o.get('path', ''))
                    if not _e or _c != _o.get('value'):
                        _nf += 1
        f.write('ifd refails: %d, groups: %d\n' % (_nf, len(_doc)))
if APPLY and overrides:
    sys.path.insert(0, 'tools')
    from pak_writer import write_pak
    write_pak(TR, TR, overrides)
    with io.open('data/_fix_remaining_out.txt', 'a', encoding='utf-8') as f:
        f.write('applied\n')
