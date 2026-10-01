#!/usr/bin/env python3
# Fix glossary violations found by qa_pak_glossary.py in the deployed pak.
# For each flagged (asset,pointer) patch row, rewrite the KO replace-value
# per the ordered substring rules / explicit overrides below.
import csv, json, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
csv.field_size_limit(10**8)
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\tools")
from pak import Pak
from pak_writer import write_pak

TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"

SUBS = [
    # DEF -> 방어력 family (order matters: longer first)
    ('방패 방어 효율', '방패 방어력 효율'),
    ('방어:', '방어력:'),
    ('방어 +15', '방어력 +15'),
    ('방어 +20', '방어력 +20'),
    ('ATK + DEF', 'ATK + 방어력'),
    ('ATK, DEF', 'ATK, 방어력'),
    # Alt Fire
    ('보조 사격', '보조 발사'),
    # materials / names
    ('비올리움', '바이올륨'),
    ('오카수스', '오카서스'),
    ('체리라', '체레라'),
    ('히로틀', '하이로틀'),
    ('힐로틀', '하이로틀'),
    # stats
    ('치명타율', '치명타 확률'),
    ('저격 소총', '저격소총'),
    # equipment names
    ('난폭꾼의 대검', '난폭꾼의 브로드소드'),
    ('NPC 대검', 'NPC 브로드소드'),
    ('유탄발사기', '유탄 발사기'),
    ('기절탄 발사기', '기절 유탄 발사기'),
    # factions / characters
    ('지상 보호국', '행성 보호국'),
    ('평화유지군', '피스키퍼'),
    ('치안유지대', '피스키퍼'),
    ('대보호자', '고위 수호자'),
    ('미니노그', '미니크녹'),
    ('에스터', '에스더'),
    ('분분마루', '붕붕마루'),
    ('액티아스의 정령 마법사들은 달빛으로 마법에 힘을 불어넣는다.', '액티안 스커트'),
    # objects / tech
    ('알타 제작 스테이션', '알타 제작대'),
    ('Enternia 모드', '에터니아 모드'),
    ('차원문 연구소', '포털 연구소'),
    ('바위로 된 문이', '바위로 된 포털이'),
    ('순간이동기', '텔레포터'),
    ('순간이동 탄', '텔레포터 탄'),
    ('비축 탄약', '예비 탄약'),
    ('AP탄', '철갑탄'),
    ('스턴 스피어', '기절 스피어'),
    ('200HP 회복', '200HP 재생'),
    ('장비 대신 패리에 사용하는', '패링 대신 장비를 사용하는'),
    ('(모든 원형)', '(모든 아키타입)'),
]

# explicit whole-KO overrides for stub-swapped descriptions
EXPLICIT = {
    ('/items/armors/saturn/Hat Conversions/legacyglitch/glitch-tier1/satglitchtier1.head', '/description'):
        '많은 새터니안이 글리치식 단조를 받아들이기 시작했다. 마을 경비병은 글리치 갑옷을 좋아한다.',
    ('/items/armors/saturn/Hat Conversions/legacyglitch/glitch-tier2/satglitchtier2.head', '/description'):
        '많은 새터니안이 글리치식 단조를 받아들이기 시작했다. 마을 경비병은 글리치 갑옷을 좋아한다.',
    ('/items/armors/saturn/Hat Conversions/legacyglitch/glitch-tier3/satglitchtier3.head', '/description'):
        '많은 새터니안이 글리치식 단조를 받아들이기 시작했다. 마을 경비병은 글리치 갑옷을 좋아한다.',
    ('/items/armors/saturn/Hat Conversions/legacyglitch/glitch-tier4/satglitchtier4.head', '/description'):
        '새터니안들이 글리치식 단조를 받아들이기 시작했지만, 그들의 갑옷은 장식용으로 가장 알맞다.',
    ('/items/armors/saturn/Hat Conversions/legacyglitch/glitch-tier4B/satglitchtier4B.head', '/description'):
        '이 투구는 얼굴을 가리며 눈을 글리치처럼 빛나게 한다. 그게 이것의 전부다.',
    ('/items/armors/saturn/Hat Conversions/legacyglitch/glitch-tier5accelerator/satglitchtier5accelerator.head', '/description'):
        '새터니안들이 글리치식 단조를 받아들이기 시작했지만, 그들의 갑옷은 장식용으로 가장 알맞다.',
    ('/items/armors/saturn/Hat Conversions/legacyglitch/glitch-tier5manipulator/satglitchtier5manipulator.head', '/description'):
        '이 철 투구는 글리치 마법사의 투구를 본땄다. 글리치 마법사에게 투구가 왜 필요할까?',
}

rows = list(csv.DictReader(open('data/qa_pak_glossary_report.tsv', encoding='utf-8-sig'), delimiter='\t'))
pk = Pak(TR)
overrides = {}
fixed = 0
skipped = []
for r in rows:
    asset = r['asset']
    if not asset.endswith('.patch'):
        asset = asset + '.patch' if not asset.endswith('patch') else asset
    # report 'asset' column is the patch path already? check
    key = r['asset']
    if not key.endswith('.patch'):
        key = key
    ko = r['koreanText']
    expl = EXPLICIT.get((r['asset'].replace('.patch',''), r['pointer']))
    new_ko = expl if expl else ko
    if not expl:
        for a, b in SUBS:
            new_ko = new_ko.replace(a, b)
    if new_ko == ko:
        skipped.append((r['asset'], r['pointer'], r['englishTerm']))
        continue
    ppath = r['asset']
    if not ppath.endswith('.patch'):
        ppath = ppath  # already patch path per report
    try:
        doc = json.loads(pk.read(ppath).decode('utf-8'))
    except Exception as e:
        print('unreadable', ppath, e); continue
    hit = False
    for group in doc:
        if isinstance(group, list):
            for op in group:
                if op.get('op') == 'replace' and op.get('path') == r['pointer'] and op.get('value') == ko:
                    op['value'] = new_ko
                    hit = True
        elif isinstance(group, dict):
            for op in group.get('ops', [group]):
                if op.get('op') == 'replace' and op.get('path') == r['pointer'] and op.get('value') == ko:
                    op['value'] = new_ko
                    hit = True
    if not hit:
        skipped.append((r['asset'], r['pointer'], 'no-op-match'))
        continue
    overrides[ppath] = json.dumps(doc, ensure_ascii=False, indent=2).encode('utf-8')
    fixed += 1
print('fixed:', fixed, 'skipped:', len(skipped))
for s in skipped[:20]:
    print('  ', s)
if '--apply' in sys.argv and overrides:
    print('entries:', write_pak(TR, TR, overrides))
