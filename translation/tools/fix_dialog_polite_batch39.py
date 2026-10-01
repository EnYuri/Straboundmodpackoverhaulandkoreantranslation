# -*- coding: utf-8 -*-
# Apply the reviewed minority-politeness dialogue conversion to the deployed
# pak. Reuses the dry-run module so the exact same line selection and
# conversion logic applies (excluding /cinematics and superior-address lines).
import csv, sys, io, json
from collections import defaultdict

csv.field_size_limit(sys.maxsize)
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak
from pak_writer import write_pak

ROOT = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
TARGET = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"

# importing the dry-run module recomputes banks/rows and re-emits the report
# (module lives in scratch/ since the 2026-09-30 cleanup)
sys.path.insert(0, ROOT + r"\scratch")
import _dialog_polite_dryrun as d


def main():
    changes = defaultdict(dict)
    for row in d.rows:
        ko = row['korean']
        b = d.banks[(row['asset'], row['pointer'].rsplit('/', 1)[0])]
        if not d.POL.search(ko) or b[1] > max(2, b[0] * 0.25):
            continue
        if d.SUPERIOR.search(ko):
            continue
        new = d.post_fix(d.conv_text(ko))
        if new != ko:
            changes[(row['asset'], row['pointer'])][ko] = new
    n = sum(len(v) for v in changes.values())
    print('rows to change:', n, 'in', len(changes), 'pointers')

    pk = Pak(TARGET)
    overrides = {}
    changed = 0
    for asset in {a for a, _ in changes}:
        doc = json.loads(pk.read(asset))
        stack = list(doc)
        found = False
        while stack:
            it = stack.pop()
            if isinstance(it, list):
                stack.extend(it)
            elif isinstance(it, dict) and it.get('op') == 'replace' and isinstance(it.get('value'), str):
                v = it['value']
                cand = changes.get((asset, it.get('path')), {})
                rep = cand.get(v)
                crlf = False
                if rep is None and '\r\n' in v:
                    rep = cand.get(v.replace('\r\n', '\n'))
                    crlf = rep is not None
                if rep is not None:
                    it['value'] = rep.replace('\n', '\r\n') if crlf else rep
                    changed += 1
                    found = True
        if found:
            overrides[asset] = json.dumps(doc, ensure_ascii=False, indent=2).encode('utf-8')
    print('changed', changed, 'fields; expected', n, '; assets untouched', len(changes) - len(overrides))
    if changed != n:
        print('MISMATCH - aborting write')
        return
    pk.f.close()  # Pak keeps the file open; Windows os.replace fails otherwise
    print('wrote pak; entries', write_pak(TARGET, TARGET, overrides))


if __name__ == '__main__':
    main()
