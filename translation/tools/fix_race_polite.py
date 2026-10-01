# Race-description polite-ending -> plain/informal converter.
# Convention (HANDOFF): <race>Description fields are player internal monologue;
# formal endings (습니다/이에요/어요/죠/세요 etc.) are out of voice.
# Generic description/longDescription fields stay formal and are excluded.
import csv, sys, io, re, json
from collections import defaultdict, Counter

csv.field_size_limit(sys.maxsize)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak
from pak_writer import write_pak

ROOT = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
TARGET = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"

RACE_RX = re.compile(r'(\w+)[Dd]escription$')
GENERIC = {'longdescription', 'shortdescription', 'turnindescription',
           'defaultdescription', 'genericdescription', 'passivedescription',
           'defaultrecruitdescription', 'inspectiondescription',
           'recruitdescription', 'completiondescription', 'nonehintdescription',
           'selecttechdescription', 'scandescription', 'sktestdescription',
           'itemdescription', 'fueldescription'}

# exact word -> word (irregulars, imperatives, ambiguous)
WORD = {
    # 습니다 verbs -> 는다
    '뽑습니다': '뽑는다', '낳습니다': '낳는다', '믿습니다': '믿는다',
    '넣습니다': '넣는다', '받습니다': '받는다', '맡습니다': '맡는다',
    '찾습니다': '찾는다', '먹습니다': '먹는다', '접습니다': '접는다',
    '겪습니다': '겪는다', '숨습니다': '숨는다', '보입니다': '보인다',
    '얻습니다': '얻는다', '방해받습니다': '방해받는다', '적습니다': '적다',
    # 습니까 -> 을까
    '있습니까': '있을까', '않습니까': '않을까', '않았습니까': '않았을까',
    '먹겠습니까': '먹을까',
    # ㅂ니다 exceptions: 르-irregular adjectives, 아니다, noun+다 lookalikes,
    # 것+ㅂ니다
    '깁니다': '길다', '느립니다': '느리다', '다릅니다': '다르다',
    '큽니다': '크다', '빠릅니다': '빠르다', '예쁩니다': '예쁘다',
    '아닙니다': '아니다', '겁니다': '거다', '바구니다': '바구니다',
    '도가니다': '도가니다', '주머니다': '주머니다', '기립니다': '기인다',
    '감사드립니다': '감사드린다',
    # imperatives -> casual
    '조심하세요': '조심해', '쉬세요': '쉬어', '가져가세요': '가져가',
    '떠나세요': '떠나', '마세요': '마셔', '후원해주세요': '후원해줘',
    '확인하세요': '확인해', '주세요': '줘', '찢어내세요': '찢어내',
    '만드세요': '만들어', '요리하세요': '요리해', '바꾸세요': '바꿔',
    '도와주세요': '도와줘', '안녕하세요': '안녕', '던져보세요': '던져봐',
    '바꿔보세요': '바꿔봐', '두세요': '둬', '하세요': '해',
    '즐기세요': '즐겨', '끄세요': '꺼', '힘내세요': '힘내',
    '사용하세요': '사용해', '달려가세요': '달려가', '안심하세요': '안심해',
    '만나보세요': '만나봐', '앉으세요': '앉아', '가세요': '가',
    '찌르세요': '찔러', '올려주세요': '올려줘', '덤벼보세요': '덤벼봐',
    '잡아주세요': '잡아줘', '내쉬세요': '내셔', '잠드세요': '잠들어',
    '찢어버리세요': '찢어버려', '설치하세요': '설치해', '클릭하세요': '클릭해',
    '탈출하세요': '탈출해', '나가세요': '나가', '드세요': '먹어',
    '여보세요': '이봐', '마시오': '마셔', '쉬시오': '쉬어',
    '떠나시오': '떠나', '보급하십시오': '보급해', '조심하십시오': '조심해',
    '묶으십시오': '묶어', '마십시오': '마셔', '생각해보세요': '생각해봐',
    '찾아보세요': '찾아봐', '축하합시다': '축하하자',
    '식물이요': '식물이다', '아니에요': '아니야', '거에요': '거야',
    '잊어버리세요': '잊어버려',
    # 이+ㅂ니다 verbs mistaken for noun+입니다
    '들여다보입니다': '들여다보인다', '움직입니다': '움직인다',
    '깜빡입니다': '깜빡인다', '반짝입니다': '반짝인다', '돋보입니다': '돋보인다',
    # spacing fixes
    '역할을합니다': '역할을 한다', '일을합니다': '일을 한다',
    '수영을하러갑니다': '수영을 하러 간다', '냄새가납니다': '냄새가 난다',
    '나게합니다': '나게 한다', '놀라게합니다': '놀라게 한다',
    '떠올리게합니다': '떠올리게 한다', '즐겁게합니다': '즐겁게 한다',
    '혼란스럽게합니다': '혼란스럽게 한다', '감사합니다': '감사',
}

# -합니다 adjectives -> -하다 (everything else -합니다 -> -한다)
HADA_ADJ = {
    '가득', '가혹', '간단', '강력', '강렬', '강', '건전', '건조', '견고',
    '겸손', '고소', '과도', '궁금', '기발', '기이', '깨끗', '끔찍', '능숙',
    '만족', '만', '매콤', '무관심', '무궁무진', '무방', '민감', '바삭',
    '분명', '불과', '불길', '불안정', '불안', '불쾌', '불편', '불확실',
    '비슷', '뾰족', '사악', '선명', '섬세', '세밀', '순수', '스타일리시',
    '쌀쌀', '안전', '약', '영리', '완벽', '우아', '유사', '유용', '유쾌',
    '익숙', '적당', '적합', '절묘', '정교', '정확', '조밀', '짜릿',
    '쫄깃', '참신', '충분', '친숙', '쾌활', '탱탱', '특별', '튼튼',
    '편안', '푹신', '풍부', '필요', '행복', '현명', '화려', '확실',
    '흐릿', '흔', '흡사', '훌륭', '딱딱', '당당', '단단', '단순',
    '달콤', '독특', '거대', '부족',
}

# nouns ending in 요 (not polite endings)
YO_NOUNS = {'필요', '주요', '담요', '비료', '재료', '자료', '음료', '중요',
            '고요', '동요', '표고'}

def jong(ch):
    return (ord(ch) - 0xAC00) % 28 if 0xAC00 <= ord(ch) <= 0xD7A3 else 0

def swap_jong(ch, src, dst):
    return chr(ord(ch) - src + dst)

unmatched = Counter()

def conv_word(m):
    w = m.group(0)
    if w in WORD:
        return WORD[w]
    if w in YO_NOUNS:
        return w
    if w.endswith('습니다'):
        return w[:-3] + '다'          # adj / past-tense / 있다·없다 all safe
    if w.endswith('입니다'):
        return w[:-3] + '이다'
    if w.endswith('하십니까'):
        return w[:-4] + '하나'
    if w.endswith('야합니다'):
        return w[:-4] + '야 한다'
    if w.endswith('습니까'):
        return w[:-3] + '을까'
    # Xㅂ니다 : vowel-final stem + bieup -> drop bieup, add nieun + 다
    if w.endswith('니다') and len(w) >= 3 and jong(w[-3]) == 17:
        stem_tail = swap_jong(w[-3], 17, 4)
        if w.endswith('합니다'):
            stem = w[:-3]
            return stem + ('하다' if stem in HADA_ADJ else '한다')
        return w[:-3] + stem_tail + '다'
    if w.endswith('네요'):
        return w[:-2] + '네'
    if w.endswith('군요'):
        return w[:-2] + '군'
    if w.endswith('이에요') or w.endswith('이예요'):
        return w[:-3] + '이다'
    if w.endswith('예요'):
        return w[:-2] + '다'
    if w.endswith('합시다'):
        return w[:-3] + '하자'
    if w.endswith('봅시다'):
        return w[:-3] + '보자'
    if w.endswith('지요'):
        return w[:-2] + '지'
    if w.endswith('죠'):
        return w[:-1] + '지'
    if w.endswith('어요'):
        return w[:-1]
    if w.endswith('아요'):
        return w[:-1]
    if w.endswith('해요'):
        return w[:-1]
    if w.endswith('여요'):
        return w[:-1]
    if w.endswith('이요'):
        return w[:-2] + '이다'
    if w.endswith('요') and len(w) >= 2:
        unmatched[w] += 1
        return w[:-1]
    unmatched[w] += 1
    return w

END_RX = re.compile(
    r"[가-힣]+(?:습니다|습니까|십니까|십니다|입니다|합니다|니다|"
    r"세요|십시오|시오|네요|군요|죠|지요|이에요|이예요|예요|어요|아요|해요|"
    r"여요|이요|합시다|봅시다|요)(?=[\s.!?…,;'\"()~^]|$)")

def conv_text(t):
    return END_RX.sub(conv_word, t)

def race_key_ok(last_seg):
    m = RACE_RX.search(last_seg)
    return bool(m) and (m.group(1) + 'description').lower() not in GENERIC

def walk_targets(node):
    # yields (container_dict, key) pairs for replace-op 'value's and plain
    # JSON string fields whose name ends with <race>Description
    stack = [node]
    while stack:
        it = stack.pop()
        if isinstance(it, list):
            stack.extend(it)
        elif isinstance(it, dict):
            if it.get('op') == 'replace' and isinstance(it.get('value'), str):
                seg = it.get('path', '').rsplit('/', 1)[-1]
                if race_key_ok(seg):
                    yield it, 'value'
            for k, v in it.items():
                if isinstance(v, str) and k != 'value' and race_key_ok(k):
                    yield it, k
                elif isinstance(v, (dict, list)):
                    stack.append(v)

def main():
    apply = '--apply' in sys.argv
    # dry run over the extracted pairs
    rows = list(csv.DictReader(open(ROOT + r'\pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'))
    n_fields = 0
    for row in rows:
        seg = row['pointer'].rsplit('/', 1)[-1]
        if not race_key_ok(seg):
            continue
        if conv_text(row['korean']) != row['korean']:
            n_fields += 1
    print('fields to change:', n_fields)
    print('unmatched (요-strip or kept):', len(unmatched))
    for w, c in unmatched.most_common(40):
        print('  %5d %s' % (c, w))
    if not apply:
        return

    pk = Pak(TARGET)
    overrides = {}
    changed = 0
    for asset in pk.index.keys():
        try:
            doc = json.loads(pk.read(asset))
        except Exception:
            continue
        hit = False
        for op, key in walk_targets(doc):
            new = conv_text(op[key])
            if new != op[key]:
                op[key] = new
                changed += 1
                hit = True
        if hit:
            overrides[asset] = json.dumps(doc, ensure_ascii=False, indent=2).encode('utf-8')
    del pk
    print('changed fields:', changed, 'assets:', len(overrides))
    print('entries:', write_pak(TARGET, TARGET, overrides))

if __name__ == '__main__':
    main()
