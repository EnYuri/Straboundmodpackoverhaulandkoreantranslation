#!/usr/bin/env python3
# Pick the best TM candidate for each tm-multi row based on pointer voice.
import csv, re, os, sys, json, statistics

BASE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.dirname(os.path.dirname(BASE))
sys.path.insert(0, GAME)
sys.path.insert(0, BASE)
from pak import Pak
from align_merged_translations import parse_json

OVERLAY = {
    'GiC': os.path.join(GAME, 'tmp', 'translation-overlays-20260921', 'source-v3', 'localeko_gic_legacy'),
    'Extended Story': os.path.join(GAME, 'tmp', 'translation-overlays-20260921', 'source-v3', 'localeko_extended_story_legacy'),
    'Black Armory': os.path.join(GAME, 'tmp', 'translation-overlays-20260921', 'source-v3', 'localeko_black_armory_legacy'),
}
SRC_PAK = {
    'GiC': os.path.join(GAME, 'mods', 'Galaxy_in_Conflict_contents_2754886445.pak'),
    'Extended Story': os.path.join(GAME, 'mods', 'Extended_Story_contents_899795176.pak'),
    'Black Armory': os.path.join(GAME, 'mods', 'Black_Armory_4.2.5_FU_NEKI_compat.pak'),
}

GLITCH_LABELS = {'감성적', '감사', '실망', '위압', '슬픔', '주의', '경고', '진술', '혐오', '기쁨', '질투', '흥미',
                 '감탄', '분노', '후회', '안도', '우려', '공포', '지루', '확인', '정보', '감상적', '감정적',
                 '분석', '평가', '관찰', '의문', '궁금', '놀람', '경이', '두려움', '불안', '기대', '흥분'}

MANUAL = {
    'MATERIALS AVAILABLE': '사용 가능한 재료',
    'Beam to Ship': '함선으로 빔',
}

def style(v):
    if re.match(r'^[가-힣]{1,8}\.\s', v):
        return 'label'
    if re.search(r'(요|습니다|세요|네요|죠|까요)[^가-힣]*\s*$', v):
        return 'polite'
    if re.search(r'(해|야|지|냐|군|네|래)[^가-힣]*\s*$', v):
        return 'casual'
    return 'plain'

def pick(cands, ptr, eng):
    if eng in MANUAL:
        return MANUAL[eng]
    key = ptr.lstrip('/').lower()
    if 'florandescription' in key:
        order = {'casual': 0, 'plain': 1, 'label': 2, 'polite': 3}
        return min(cands, key=lambda c: (order[style(c)], 0 if '플로란' in c else 1, len(c)))
    if 'glitchdescription' in key:
        def gscore(c):
            m = re.match(r'^([가-힣]{1,8})\.\s*(.*)$', c)
            if not m:
                return (3, 0, len(c))
            rest = m.group(2)
            rest_plain = 0 if style(rest) == 'plain' else 1
            vocab = 0 if m.group(1) in GLITCH_LABELS else 1
            return (vocab, rest_plain, len(c))
        return min(cands, key=gscore)
    if 'description' in key:
        order = {'plain': 0, 'polite': 1, 'casual': 2, 'label': 3}
        return min(cands, key=lambda c: (order[style(c)], len(c)))
    # UI labels / names: prefer median length to avoid outliers
    if 'beam to' in eng.lower() and any('함선으로' in c for c in cands):
        cands = [c for c in cands if '함선으로' in c]
    med = statistics.median(len(c) for c in cands)
    order = {'plain': 0, 'polite': 1, 'casual': 2, 'label': 3}
    return min(cands, key=lambda c: (abs(len(c) - med), order[style(c)]))

def norm(s):
    return s.replace('\r\n', '\n')

def get_ptr(obj, path):
    cur = obj
    for part in path.lstrip('/').split('/'):
        if isinstance(cur, list):
            cur = cur[int(part)]
        elif isinstance(cur, dict):
            if part not in cur:
                return None
            cur = cur[part]
        else:
            return None
    return cur

def main():
    rows = list(csv.DictReader(open(os.path.join(BASE, 'cleaned_translation_targets.tsv'), encoding='utf-8-sig'), delimiter='\t'))
    tm = [r for r in rows if r['category'] == 'tm-multi']
    paks = {m: Pak(p) for m, p in SRC_PAK.items()}
    picked, merged, updated, skipped_src = [], 0, 0, 0
    for r in tm:
        cands = [c.strip() for c in r['suggestedKorean'].split(' || ') if c.strip()]
        if not cands:
            continue
        kor = pick(cands, r['jsonPointer'], r['englishText'])
        picked.append((r['sourceMod'], r['assetPath'], r['jsonPointer'], r['englishText'], kor, ' || '.join(cands)))
        try:
            asset = parse_json(paks[r['sourceMod']].read(r['assetPath']))
        except Exception:
            skipped_src += 1
            continue
        cur = get_ptr(asset, r['jsonPointer'])
        if not isinstance(cur, str) or norm(cur) != norm(r['englishText']):
            skipped_src += 1
            continue
        patch_rel = r['assetPath'].lstrip('/') + '.patch'
        od = OVERLAY[r['sourceMod']]
        fp = os.path.join(od, *patch_rel.split('/'))
        ops = []
        if os.path.exists(fp):
            ops = json.load(open(fp, encoding='utf-8'))
        hit = False
        for o in ops:
            if o.get('path') == r['jsonPointer'] and o.get('value') in cands:
                if o['value'] != kor:
                    o['value'] = kor
                    updated += 1
                hit = True
                break
        if not hit:
            ops.append({'op': 'replace', 'path': r['jsonPointer'], 'value': kor})
            merged += 1
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, 'w', encoding='utf-8', newline='').write(json.dumps(ops, ensure_ascii=False, indent=2) + '\n')
    with open(os.path.join(BASE, 'tm_multi_chosen.tsv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['mod', 'asset', 'pointer', 'english', 'chosen', 'candidates'])
        w.writerows(picked)
    print('picked:', len(picked), 'merged:', merged, 'updated:', updated, 'skipped_src:', skipped_src)

if __name__ == '__main__':
    main()
