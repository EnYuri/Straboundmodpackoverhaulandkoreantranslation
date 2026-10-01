#!/usr/bin/env python3
# Create translation patches for the 4 broken-survey assets that had no patch
# at all: Project_Redemption compat protectorate armor (x3, reuse lustling-path
# KOs) and vanilla fryingpan (fixed 'skillet' mistranslation; also correct the
# sibling starbound-path patch).
import sys, io, json, re
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

def group(path, en, ko):
    return [{"op": "test", "path": path, "value": en},
            {"op": "replace", "path": path, "value": ko}]

pr = Pak(SB + BS + "mods" + BS + "Project_Redemption_12.3_FU_SBKor_compat.pak")
pk = Pak(SB + BS + "assets" + BS + "packed.pak")
tr = Pak(TR)

KO = {
    'chest': {'sd': '수호자의 흉갑', 'd': '모두의 보호를 보장하기 위한 실험적 파워 아머.\n\n강력한 대시 테크 장착.'},
    'head':  {'sd': '수호자의 투구', 'd': '고귀한 대의의 얼굴.\n\n수호자의 스피어 테크 장착.'},
    'legs':  {'sd': '수호자의 그리브', 'd': '더 밝은 미래를 향해 행진하는 부츠.\n\n부츠 스러스터 장착.'},
}
overrides = {}
base = '/items/armors/protectorate/protectoratearmor/protectoratearmor.'
for part, ko in KO.items():
    a = base + part
    d = parse_sb(pr.read(a))
    doc = [group('/shortdescription', d['shortdescription'], ko['sd']),
           group('/description', d['description'], ko['d'])]
    overrides[a + '.patch'] = json.dumps(doc, ensure_ascii=False, indent=2).encode('utf-8')

fp = '/items/active/weapons/melee/axe/fryingpan.activeitem'
d = parse_sb(pk.read(fp))
fp_ko_d = '프라이팬 기술은 결코 주철을 능가할 수 없습니다.'
doc = [group('/description', d['description'], fp_ko_d),
       group('/shortdescription', d['shortdescription'], '프라이팬')]
overrides[fp + '.patch'] = json.dumps(doc, ensure_ascii=False, indent=2).encode('utf-8')

# fix sibling patch's mistranslated 'skillet' line too
sib = '/items/active/starbound/weapons/axes/fryingpan.activeitem.patch'
if sib in tr.index:
    sdoc = json.loads(tr.read(sib).decode('utf-8'))
    for g in sdoc:
        for o in (g if isinstance(g, list) else [g]):
            if isinstance(o, dict) and o.get('op') == 'replace' and o.get('path') == '/description':
                o['value'] = fp_ko_d
    overrides[sib] = json.dumps(sdoc, ensure_ascii=False, indent=2).encode('utf-8')

print('entries:', write_pak(TR, TR, overrides))
