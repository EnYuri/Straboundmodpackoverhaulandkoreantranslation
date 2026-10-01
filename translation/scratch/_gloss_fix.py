# -*- coding: utf-8 -*-
# Fix glossary violations in zz pak replace-values, per flagged (asset, pointer).
import sys, io, os, csv, json, re, time, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, 'tools')
import pak_writer
from pak import Pak

ZZ = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"

# term -> list of (wrong_ko, right_ko) applied to the flagged row's replace value
MAP = {
    'Miniknog': [('미니크노그', '미니크녹')],
    'Esther': [('에스터', '에스더')],
    'Saturnian': [('토성인', '새터니안'), ('새턴인', '새터니안')],
    'DEF': [('방어 +', '방어력 +'), ('방어+', '방어력+')],
    'Shortsword': [('쇼트소드', '소검'), ('숏소드', '소검'), ('단검', '소검')],
    'Violium': [('비올리움', '바이올륨')],
    'Aegisalt': [('이지살트', '에지솔트'), ('에지살트', '에지솔트')],
    'Grand Protector': [('대수호자', '고위 수호자')],
    'Teleporter': [('순간이동기', '텔레포터')],
    'Crafting Station': [('제작 스테이션', '제작대')],
    'Portal': [('차원문', '포털')],
    'Peacekeeper': [('평화유지대', '피스키퍼')],
    'Bunbunmaru': [('분분마루', '붕붕마루')],
    'United Systems': [('통합 체계', '연합 시스템')],
    'Zerchesium': [('제르체시움', '제르세슘')],
    'Shield Bash': [('실드 배시', '방패 강타')],
    'Cultivator': [('경작자', '컬티베이터'), ('재배자', '컬티베이터')],
    'sanctilite': [('성화석', '생크틸라이트')],
    'Aegi': [('아에기', '에지'), ('에이기', '에지'), ('에기', '에지')],
    'Faryth': [('패리스', '파리스')],
    'Occasus': [('오카수스', '오카서스')],
    'Terrene Protectorate': [('지상 보호국', '행성 보호국')],
    'Unexplored': [('미탐험이고', '미탐험 구역이고'), ('미탐험 ', '미탐험 구역 ')],
    'Assault Rifle': [('돌격 소총', '돌격소총')],
    'Parry': [('패리', '패링')],
    'Lustling': [('러스트링', '러스틀링')],
    'Vaash': [('바시', '바쉬')],
    'Thelean': [('텔리안', '텔레안')],
    'Figurine': [('조형물', '피규어')],
    'Nomada': [('노마드', '노마다')],
    'gheatsyn': [('게트신', '기트신')],
    'Knockback': [],  # handled manually below
}

# manual per-row replace overrides: (asset_suffix, pointer) -> new replace value
MANUAL = {
    ('r_impervious.legs', '/description'): '넉백조차 견뎌내는 불굴의 바지.',
}

rows = list(csv.DictReader(open('data/qa_pak_glossary_report.tsv', encoding='utf-8-sig'), delimiter='\t'))
per_asset = collections.defaultdict(list)  # patchfile -> [(pointer, term)]
for r in rows:
    per_asset[r['asset']].append((r['pointer'], r['englishTerm'], r['koreanText']))

pk = Pak(ZZ)
overrides = {}
stats = collections.Counter()


def flat(ops, out):
    for o in ops:
        if isinstance(o, list):
            flat(o, out)
        elif isinstance(o, dict):
            out.append(o)


for asset, items in per_asset.items():
    try:
        ops = json.loads(pk.read(asset).decode('utf-8'))
    except Exception as e:
        print('read fail', asset, e)
        continue
    fl = []
    flat(ops, fl)
    changed = False
    for pointer, term, oldko in items:
        m = None
        for op in fl:
            if op.get('op') == 'replace' and op.get('path') == pointer:
                m = op
                break
        if m is None:
            stats['no_replace_op'] += 1
            continue
        for suf, ptr in MANUAL:
            if asset.endswith(suf) and pointer == ptr:
                if m['value'] != MANUAL[(suf, ptr)]:
                    m['value'] = MANUAL[(suf, ptr)]
                    changed = True
                    stats['manual'] += 1
                break
        for wrong, right in MAP.get(term, []):
            if wrong in m.get('value', ''):
                m['value'] = m['value'].replace(wrong, right)
                changed = True
                stats['fix:' + term] += 1
    if changed:
        overrides[asset] = json.dumps(ops, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

print(dict(stats), '| files:', len(overrides))
del pk
if overrides:
    out = ZZ + '.staged'
    pak_writer.write_pak(out, ZZ, overrides)
    time.sleep(1)
    try:
        os.replace(out, ZZ)
        print('replaced')
    except PermissionError:
        print('staged kept:', out)
