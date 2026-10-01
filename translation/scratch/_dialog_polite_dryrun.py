# -*- coding: utf-8 -*-
# Dry-run: apply fix_race_polite.conv_text (extended) to minority-polite
# dialogue-bank lines. Exclusions:
#  - /cinematics/ assets (per-speaker voices, politeness is characterization)
#  - lines containing superior-address terms (politeness is motivated)
import csv, sys, io, re, collections
csv.field_size_limit(sys.maxsize)

# fix_race_polite lives in tools/ since the 2026-09-30 reorganization;
# run this module (and fix_dialog_polite_batch39.py) from the repo root.
sys.path.insert(0, 'tools')
import fix_race_polite as frp

EXTRA_WORD = {
    '거세요': '걸어', '구세요': '해', '되세요': '돼', '쓰세요': '써',
    '괜찮으세요': '괜찮아', '싶으세요': '싶어',
    '주십시오': '줘', '주의하십시오': '주의해',
    '계십니다': '계셔', '아십니까': '아나', '하십니다': '한다',
    '해주십니다': '해준다', '드립니다': '준다', '드릴게요': '줄게',
    '드릴까요': '줄까', '드립시다': '줍시다',
    '도와드릴게요': '도와줄게', '안내해드릴까요': '안내해줄까',
    '보여드릴게요': '보여줄게', '도와드릴까요': '도와줄까',
    '말씀드릴게요': '말할게', '싶으셨나요': '싶었나',
    '들어보셨나요': '들어봤나', '가지셔도': '가져도',
    '감사드립니다': '감사한다', '사과드립니다': '사과한다',
    '이시군요': '이군', '마셔보시겠어요': '마셔볼래',
    '생각하시나요': '생각하나', '죄송합니다': '죄송해',
    '누구세요': '누구야', '누구십니까': '누구냐',
    '뛰어드세요': '뛰어들어', '만드세요': '만들어',
    '계십니까': '계시나', '드시오': '드셔', '주무시오': '주무셔',
    '계시오': '계셔', '잡수시오': '잡수셔',
}
frp.WORD.update(EXTRA_WORD)

POS_VOWEL = {0, 1, 2, 3, 8, 9, 10, 11, 12}   # bright vowels

def vowel_idx(ch):
    return ((ord(ch) - 0xAC00) % 588) // 28 if 0xAC00 <= ord(ch) <= 0xD7A3 else -1

def jong(ch):
    return (ord(ch) - 0xAC00) % 28 if 0xAC00 <= ord(ch) <= 0xD7A3 else 0

def conj(stem):
    # plain imperative ending for a vowel-final stem
    if not stem or jong(stem[-1]):
        return None
    t = stem[-1]
    if t == '하':
        return stem[:-1] + '해'
    v = vowel_idx(t)
    if v in (8, 13):  # 오->와, 우->워 (vowel swap +28: ㅗ->ㅘ, ㅜ->ㅝ)
        return stem[:-1] + chr(ord(t) + 28)
    if v == 20:    # 이 -> 여 (기->겨, 리->려)
        return stem[:-1] + chr(ord(t) - 20 * 28 + 6 * 28)
    if v == 18:    # 으-stem (모으->모아, 쓰->써) and 르-irregular (기르->길러, 모르->몰라)
        if len(stem) >= 2 and jong(stem[-2]) == 0:
            pos = vowel_idx(stem[-2]) in POS_VOWEL
            if stem[-1] == '르':
                return stem[:-2] + chr(ord(stem[-2]) + 8) + ('라' if pos else '러')
            return stem[:-1] + ('아' if pos else '어')
        return stem[:-1] + chr(ord(t) - 18 * 28 + 4 * 28)
    if v >= 0:
        # stems ending in ㅏㅐㅑㅒㅓㅔㅕㅖ or compound vowels are already
        # correct imperatives (사, 지내, 둬, 봐 ...)
        return stem
    return None

def conv_word2(m):
    w = m.group(0)
    if w in ('마세요', '마십시오', '마시오'):
        # 마시다(drink) vs 말다(don't) disambiguation by preceding '하지'
        pre = m.string[:m.start()].rstrip()
        if pre.endswith('지'):
            return '마'
    if w in frp.WORD:
        return frp.WORD[w]
    if w.endswith('주세요'):
        return w[:-3] + '줘'
    if w.endswith('으세요'):
        # 있으세요->있어 (connective 으 after jong) vs 모으세요->모아 (stem 으)
        if len(w) >= 4 and jong(w[-4]) == 0:
            r = conj(w[:-2])
            if r:
                return r
        return w[:-3] + '어'
    if w.endswith('십시오'):
        r = conj(w[:-3])
        return r if r else w
    if w.endswith('시오'):
        r = conj(w[:-2])
        return r if r else w
    if w.endswith('세요'):
        r = conj(w[:-2])
        return r if r else w
    if w.endswith('하십니다'):
        return w[:-4] + '한다'
    if w.endswith('십니다'):
        return w[:-3] + '는다'
    if w.endswith('십니까'):
        return w[:-3] + '나'
    if w.endswith('니까'):
        # 합니까->하나 (ㅂ-formal question) vs 하니까 (reason clause) - keep
        if jong(w[-3]) == 17:
            return w[:-3] + chr(ord(w[-3]) - 17) + '나'
        return w
    if w.endswith('랍니다'):
        return w[:-3] + '란다'
    if w.endswith('랍니까'):
        return w[:-3] + '라나'
    return frp.conv_word(m)

END_RX = re.compile(
    r"[가-힣]+(?:습니다|습니까|십니까|십니다|니까|입니다|합니다|니다|"
    r"세요|십시오|시오|네요|군요|죠|지요|이에요|이예요|예요|어요|아요|해요|"
    r"여요|이요|합시다|봅시다|요)(?=[\s.!?…,;'\"()~^—–:]|$)")

def conv_text(t):
    return END_RX.sub(conv_word2, t)

# honorific infix cleanup applied AFTER ending conversion
INFIX = [
    ('주셔서', '줘서'), ('주시면', '주면'), ('주시리라', '주리라'),
    ('주셔야', '줘야'), ('주신다', '준다'), ('주신 ', '준 '),
    ('주셨', '줬'), ('하셨', '했'), ('찾으셨', '찾았'), ('하셔', '해'),
    ('으셨', '었'), ('오셨', '왔'),
    ('싶으시', '싶'), ('으시면', '으면'),
    ('이시군', '이군'), ('계시군', '계군'), ('계셨', '있었'),
    ('계신다', '있다'), ('계신 ', '있는 '), ('계시다', '있다'),
    ('계시지', '있지'),
    ('보시겠어', '볼래'), ('사고 싶으셨', '사고 싶었'),
    ('드렸', '줬'), ('드리겠', '주겠'), ('드리기', '주기'),
    ('하시는', '하는'), ('하시길', '하길'),
    ('하시지', '하지'), ('하시고', '하고'), ('하시기', '하기'),
    ('주시려', '주려'), ('주시는', '주는'), ('주시기', '주기'),
    ('주시면서', '주면서'), ('주시도', '주도'), ('주시길', '주길'),
    ('이신', '인'), ('싶으신', '싶은'), ('있으신', '있는'),
    ('없으신', '없는'), ('하신', '한'), ('오신', '온'), ('주실', '줄'),
    ('쉬실', '쉴'), ('우셨', '웠'), ('보셨', '봤'), ('하시며', '하며'),
    ('하시면', '하면'), ('시다간', '다간'), ('말씀하셨', '말했'),
    ('말씀하', '말하'),
]

# regex infixes needing context guards:
#   하실: honorific infix, but 지하실(basement) is a noun - block '지' prefix
#   드릴: honorific infix, but 드릴(drill tool) is a noun - require verb-tail lookahead
INFIX_RX = [
    (re.compile(r'(?<!지)하실'), '할'),
    (re.compile(r'드릴(?=\s*(?:게|까|수|것|일|테|지|걸|거|니|라|네|요|예정|참|생각|계획|차례|정도|듯))'), '줄'),
    (re.compile(r'이실(?=\s*(?:까|가|지|걸|거|수|것|니|라|네|요))'), '일'),
]

def post_fix(t):
    for a, b in INFIX:
        t = t.replace(a, b)
    for rx, b in INFIX_RX:
        t = rx.sub(b, t)
    return t

SUPERIOR = re.compile(r'(선장님|대장님|마님|국장님|사령관|지휘관|경관님|폐하|장군|나리|보스|주인님|교관|요원님|대사님|신관님|수석님|대부님|영주님|기사님|대령|소령|상관|주군|임금|왕|전하|저하|상사|선생님|교수님|박사님|형님|누님|어르신|스승님|장교님|제독님|함장님|원장님|총장님|여왕님|국왕님|어머님|아버님|신부님|단장님|빅 에이프|빅에이프|대위님|소위님|중위님|상사님|팀장님|반장님|간부님|의장님|관리자님|선배님)')

assets = set()
for f in ('data/style_mix_group2.tsv', 'data/style_mix_group3.tsv', 'data/stylemix_todo.tsv'):
    for ln in io.open(f, encoding='utf-8-sig'):
        p = ln.rstrip('\n').split('\t')
        if len(p) > 1 and p[0].startswith('/') and not p[0].startswith('/cinematics'):
            assets.add(p[0])

POL = END_RX   # unified detector: bank classification and line selection

banks = collections.defaultdict(lambda: [0, 0])
rows = []
for row in csv.DictReader(open('data/pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
    if row['asset'] not in assets:
        continue
    bank = row['pointer'].rsplit('/', 1)[0]
    banks[(row['asset'], bank)][0] += 1
    if POL.search(row['korean']):
        banks[(row['asset'], bank)][1] += 1
    rows.append(row)

out = io.open('scratch/_polite_dryrun.txt', 'w', encoding='utf-8')
skip = io.open('scratch/_polite_skipped.txt', 'w', encoding='utf-8')
n = nc = ns = 0
for row in rows:
    ko = row['korean']
    b = banks[(row['asset'], row['pointer'].rsplit('/', 1)[0])]
    if not POL.search(ko) or b[1] > max(2, b[0] * 0.25):
        continue
    if SUPERIOR.search(ko):
        ns += 1
        skip.write('%s\t%s\n  KO: %s\n' % (row['asset'], row['pointer'],
                  ko.replace('\n', ' / ')))
        continue
    new = post_fix(conv_text(ko))
    n += 1
    if new == ko:
        nc += 1
        continue
    out.write('%s\t%s\n  KO: %s\n  -> %s\n' % (row['asset'], row['pointer'],
              ko.replace('\n', ' / '), new.replace('\n', ' / ')))
out.write('\n=== SUMMARY ===\nmatched lines: %d  changed: %d  unchanged: %d  superior-skipped: %d\n'
          % (n, n - nc, nc, ns))
out.write('unmatched endings: %d\n' % len(frp.unmatched))
for w, c in frp.unmatched.most_common(80):
    out.write('  %4d %s\n' % (c, w))
out.close(); skip.close()
print('done')
