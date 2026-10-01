#!/usr/bin/env python3
# Fix c946 leaf-key fan-out: 'caption' ko values were spread to every
# /gui/**/caption leaf. Restore per-caption correct translations.
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BS = chr(92)
sys.path.insert(0, "E:" + BS + "My Games" + BS + "steamapps" + BS + "common" + BS + "Starbound")
sys.path.insert(0, "E:" + BS + "My Games" + BS + "steamapps" + BS + "common" + BS + "Starbound" + BS + "translation" + BS + "translation-baseline-20260921" + BS + "tools")
from pak import Pak
from pak_writer import write_pak

TR = "E:" + BS + "My Games" + BS + "steamapps" + BS + "common" + BS + "Starbound" + BS + "mods" + BS + "zz_translation_female.pak"

# asset patch -> {en_test_value -> correct ko}
FIXES = {
    '/Objects/Terminal/digitalstorage_terminal.config.patch': {
        '1': '1', '10': '10', '100': '100', '1000': '1000',
        'Get': '가져오기', 'Sort': '정렬', 'Craft': '제작', 'Back': '뒤로',
    },
    '/Objects/TransferNode/digitalstorage_transfernode.config.patch': {
        'Save': '저장', 'Load': '불러오기', 'Back': '뒤로',
        'Replace': '교체', 'Replace Me': '교체',
    },
    '/Objects/FilterFormatter/digitalstorage_filterformatter.config.patch': {
        'Clear': '지우기', 'Blacklist': '블랙리스트',
    },
}

tr = Pak(TR)
overrides = {}
for path, fixes in FIXES.items():
    doc = json.loads(tr.read(path).decode('utf-8'))
    for g in doc:
        en = None
        rep = None
        for o in (g if isinstance(g, list) else [g]):
            if not isinstance(o, dict):
                continue
            if o.get('op') == 'test' and isinstance(o.get('value'), str):
                en = o['value']
            if o.get('op') == 'replace':
                rep = o
        if rep is not None and en in fixes:
            rep['value'] = fixes[en]
    overrides[path] = json.dumps(doc, ensure_ascii=False, indent=2).encode('utf-8')

print('entries:', write_pak(TR, TR, overrides))
