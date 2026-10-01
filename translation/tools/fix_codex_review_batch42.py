# -*- coding: utf-8 -*-
# Batch42: codex prose manual-review corrections (23,957-row _codex_review.txt
# full read-through). Rule types:
#   global  - plain substring applied to every KO patch value
#   guarded - applied only when the EN source matches en_guard
#   scoped  - applied only inside matching asset / pointer
# Default is a dry run printing every match; --apply writes the pak.
import sys, io, json, re, csv

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak
from pak_writer import write_pak

TARGET = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
PAIRS = r"data\pak_pairs.tsv"

# (label, ko_pattern, replacement, en_guard_regex, asset_guard_regex, ptr_regex, is_regex)
RULES = [
    # ---------- typos / prose corrections ----------
    ('legend', '전설 이상도 아니게', '전설에 불과하게', None, None, None, False),
    ('better safe than sorry', '만일이 낫지 후회보다', '후회하느니 미리 조심하는 게 낫다', None, None, None, False),
    ('assignment notes', '현 임무 네 메모', '현 임무에 관한 네 메모', None, None, None, False),
    ('defense-line clause', '방어벽 형태의 여러 겹의 방어선으로, 도시를', '방어벽 형태의 여러 겹의 방어선이 도시를', None, None, None, False),
    ('minerals specks', '미네랄, 반점, 비타민', '미네랄, 알갱이, 비타민', None, None, None, False),
    ('aegi history desc', '에지니아 민족의 요약된 기록 역사.', '에지니아인의 기록된 역사 요약본.', None, None, None, False),
    ('fad dessert', '차 같은 반흔한 알타 디저트', '차 같은 인기 있는 알타 디저트', None, None, None, False),
    ('watering device 1', '이 급수 용액은', '이 급수 장치는', None, None, None, False),
    ('watering device 2', '살덩이 흙에 뿌리는 급수 용액입니다', '살덩이 흙에 물을 주는 급수 장치입니다', None, None, None, False),
    ('antorash title', '골동품과 단지들', '안토라시 관광 안내', None, r'ct_antorash', r'/title', False),
    ('excited for you', '우리 꼬마야, 네가 정말 자랑스럽고, 너도 그러길 바라', '우리 꼬마야, 정말 기대된다, 너도 그러길 바라', None, None, None, False),
    ('angel rebellion dup', '천사 반란군^reset;의 일부다', '천사 반란^reset;의 일부다', None, None, None, False),
    ('dreadful age', '이것은 정말 암흑의 시대가 두렵다', '이건 정말 두려운 암흑의 시대다', None, None, None, False),
    ('take the mantle', '국방부의 표면을 자처하는', '국방부의 계승자를 자처하는', None, None, None, False),
    ('logging cache', '벌목 저장소', '로깅 캐시', None, None, None, False),
    ('ruin biomass', '유적 생물량', '루인 생물량', None, None, None, False),
    ('radioactive bulbs', '방사성 혹', '방사성 구근', None, None, None, False),
    ('kevin mute 1', '묵언이다', '벙어리다', None, r'scienceoutpost_kevin', None, False),
    ('kevin mute 2', '묵언을', '벙어리인 걸', None, r'scienceoutpost_kevin', None, False),
    ('apex-is typo', '에이페는', '에이펙스는', None, None, None, False),
    ('guests aboard', '타고 있었지', '있었지', None, None, None, False),
    ('stack->bundle', '더미', '묶음', None, r'networkguide', r'/contentPages/7', False),
    ('terminal->device', '단자', '단말기', None, r'networkguide', r'/contentPages/15', False),
    ('bridge spelling', '브릿지', '브리지', None, r'networkguide', None, False),
    ('jamming toc', '기능 고장', '걸림', None, r'project45manual', r'/contentPages/0', False),
    ('fusion', '핵융합 반응', '융합 반응', None, r'arcana_codex_misc_2', None, False),
    ('normal rank', r'\[보통\]', '[일반]', None, r'gico_trial_warning', None, True),
    ('execrations', '저주가 너희의', '엑세크레이션이 너희의', None, r'horizonMission_5', None, False),
    ('withering', '대시들', '대위더링', None, r'starforge-witherlore', None, False),
    ('loot monsters', '몬스터 약탈', '몬스터 루팅', None, r'starforge-lootmonsterlore', None, False),
    ('miniknog rise 1', '미니크녹의 발기 동안', '미니크녹이 부상하던 시기에', None, None, None, False),
    ('miniknog rise 2', '초기 발기 시간에', '초기 부상 시기에', None, None, None, False),
    ('look to ourselves', '스스로를 바라고', '스스로에게 의지하고', None, None, None, False),
    ('darts', '다츠는', '다트는', None, r'ct_alta_dart', None, False),
    ('sprinkler', '자동 물뿌리개', '자동 스프링클러', None, None, None, False),
    ('tricorder', '삼안경서', '트라이코더', None, None, None, False),
    ('redacted 1', r'\[기밀\]', '[삭제됨]', None, r'bigapecodexmeeting', None, True),
    ('redacted 2', r'\[검열됨\]', '[삭제됨]', None, r'bigapecodexmeeting', None, True),
    ('redacted 3', r'\[Redacted\]', '[삭제됨]', None, None, None, True),
    ('la-voe dash', '라-보', '라보에', None, None, None, False),

    # ---------- Green Word -> 녹색 언어 ----------
    ('greenword 1', '녹색 언어씀', '녹색 언어', None, None, None, False),
    ('greenword 2', '녹색 언어이 널', '녹색 언어가 널', None, None, None, False),
    ('greenword 3', '푸른 말씀', '녹색 언어', None, None, None, False),
    ('greenword 4', '초록의 말씀', '녹색 언어', None, None, None, False),
    ('greenword 5', '초록 말씀', '녹색 언어', None, None, None, False),

    # ---------- proper-noun unification ----------
    ('moogle', '모그리', '모글', None, None, None, False),
    ('exousian', '엑소시안', '엑수시안', None, None, None, False),
    ('kyterran', '카이테란', '키테란', None, None, None, False),
    ('waspmim', '왐미밈', '와스프밈', None, None, None, False),
    ('praetor', '프라이터', '프라이토르', None, None, None, False),
    ('impersonator 1', '위장의 대가', '대모방자', None, None, None, False),
    ('impersonator 2', '그랜드 임퍼소네이터', '대모방자', None, None, None, False),
    ('thornwing 1', '손윙', '쏜윙', None, None, None, False),
    ('thornwing 2', '가시날개', '쏜윙', None, r'(?:codex|items|objects)/', None, False),
    ('ambiri', '앰비리', '암비리', None, None, None, False),
    ('coralgrower', '코럴그로워', '코럴그로어', None, None, None, False),
    ('mcvicar', '맥비카', '맥비커', None, None, None, False),
    ('hiraki', '히라키 코레일', '히라키 코랄레', None, None, None, False),
    ('glimrecus', '글림를레쿠스', '글림레쿠스', None, None, None, False),
    ('moonshadow', '문셰도우', '달그림자', None, None, None, False),
    ('viridescent 1', '비리데센트', '비리데슨트', None, None, None, False),
    ('viridescent 2', '비리데선트', '비리데슨트', None, None, None, False),
    ('badlands', '배드랜즈', '배드랜드', None, None, None, False),
    ('arcanian', '아케이니안', '아르카니안', None, None, None, False),
    ('lophani', '로푸니', '로퍼니', None, None, None, False),
    ('cygnus', '시그누스', '시그너스', None, None, None, False),
    ('cluex', '클룩스', '클루엑스', None, None, None, False),
    ('laenathin', '라에나신', '라에나틴', None, r'/codex/felin/', None, False),
    ('hakuuki', '하쿠키', '하쿠우키', None, None, None, False),
    ('serpent', '서펜트', '서펀트', None, None, None, False),
    ('davin', '다빈', '데이빈', None, None, None, False),
    ('matthew', '매슈', '매튜', None, None, None, False),
    ('seonha', '세온하', '선하', None, None, None, False),
    ('morragh', '모라흐', '모라그', None, None, None, False),
    ('woof pack', '멍멍 무리', '우프 무리', None, None, None, False),
    ('oinker 1', '오잉킹', '오잉키서', None, None, None, False),
    ('oinker 2', '오잉커서', '오잉키서', None, None, None, False),
    ('tea lad', '차를 사랑하는 청년', 'Tea-Loving Lad', None, None, None, False),
    ('lady nox', '녹스 여주인', '녹스 여주', None, None, None, False),
    ('fushi', '후시', '후치', None, r'pf_hylotlreligion2', None, False),
    ('noolith', '놀리스', '누올리스', r'Noolith', None, None, False),
    ('irisil pl', '아이리실', '이리실', None, None, None, False),
    ('irisa sg', '아이리사', '이리사', None, None, None, False),
    ('xi 1', r'(?<![가-힣])짜이', "짜'이", None, None, None, True),
    ('xi 2', "X'i", "짜'이", None, None, None, False),
    ('uscm full', '통합 우주 기업 군대', '범우주 우주 기업군', None, None, None, False),
    ('cosmic lords', '우주의 군주들', '코스모스의 군주들', None, None, None, False),
    ('astromancer', '성점술사', '아스트로맨서', None, None, None, False),
    ('solar guardian', '솔라 가디언', '태양 수호자', None, None, None, False),
    ('high magus 1', '하이 마구스', '대마법사', None, None, None, False),
    ('high magus 2', '상급 마법사', '대마법사', None, None, None, False),
    ('job armor', '잡 방어구', '직업 갑옷', None, None, None, False),
    ('matriarch', '여가장', '여족장', None, r'funightarhistory5', None, False),
    ('starry cultist 1', '별의 광신도들', '스타리 컬티스트', None, None, None, False),
    ('starry cultist 2', '별의 광신도', '스타리 컬티스트', None, None, None, False),
    ('starry cultist 3', '별빛 신도들', '스타리 컬티스트', None, None, None, False),
    ('star garden', '스타리 정원', '스타리 가든', None, None, None, False),
    ('starcrab', '별게', '스타크랩', None, r'om_starry', None, False),
    ('stella panfish', '스텔라 부채물고기', '스텔라 팬피시', None, None, None, False),

    # ---------- Terrene org names ----------
    ('terrene bare', r'(?<![가-힣A-Za-z])테렌(?=의| |\.|,|!|\?|$|\n)', '테레네', None, None, None, True),
    ('terrene protectorate', '행성 보호국', '테레네 보호국', None, None, None, False),
    ('terrene peacekeeper', '행성 피스키퍼', '테레네 피스키퍼', None, None, None, False),
    ('terrene guardians', '행성 가디언즈', '테레네 가디언즈', None, None, None, False),
    ('terrene electorate', '행성 선거단', '테레네 선거단', None, None, None, False),
    ('terrene guard', '행성 수호대', '테레네 가드', None, None, None, False),
    ('terrene law', '"행성" 법 집행관', '"테레네" 법 집행관', None, None, None, False),

    # ---------- Viera: the Wood -> 숲 ----------
    ('the wood art', '더 우드', '숲', None, r'viera', None, False),
    ('the wood bare', r'(?<![가-힣A-Za-z])우드(?=의|은|는|이|가|을|를|와|과|로|에|께|서|도|만| |\.|,|!|\?|$|\n|:)', '숲', None, r'viera', None, True),

    # ---------- Viera misc ----------
    ('viera sniper', '비에라 스나이퍼', '비에라 저격수', None, None, None, False),
    ('trickster trial', '사기꾼의 시련', '트릭스터의 시련', None, None, None, False),
    ('dalmascan', r'달마스카(?!의|들)', '달마스칸', None, r'viera|dalmascan', None, True),

    # ---------- Saturn weapons ----------
    ('light bow', '빛의 활', '라이트 보우', None, r'saturnlightbow', None, False),
    ('baton staff', '배통', '지휘봉', None, r'saturnmagicstaff', None, False),
    ('baton bee', '벌 배통', '벌 지휘봉', None, None, None, False),
    ('baton ice', '얼음 배통', '얼음 지휘봉', None, None, None, False),

    # ---------- Horizon ----------
    ('world horizon', '세계의 지평선', '월드 호라이즌', None, r'horizon_2', r'/title', False),
    ('horizon machines', '지평선의 전투 기계', '호라이즌의 전투 기계', None, r'receipt_execration', None, False),

    # ---------- Woofie ----------
    ('blood woof', '블러드 우프', '피의 우프', None, r'woofie_priceandtime\.codex', None, False),
    ('blood wolf', '핏빛 털의 늑대', '블러드 울프', None, r'woofie_priceandtime3', None, False),
    ('captain 1', '선장의 흥분에', '대위의 흥분에', None, r'woofie_priceandtime2', None, False),
    ('captain 2', '책임자여', '대위님', None, r'woofie_priceandtime2', None, False),
    ('captain 3', '대장님', '대위님', None, r'woofie_priceandtime3', None, False),
    ('lustful whip', '러스트풀 위프', '색욕의 채찍', None, r'eblovelywhipscodex', None, False),
    ('for lady nox', '녹스 님을 위해', '녹스 여주를 위해', 'Lady Nox', None, None, False),
    ('krakothan a', '크라코스', '크라코탄', (r"K'Rakothan", r"K'Rakoths?(?!an)"), None, None, False),
    ('krakothan b', '크라코탄', '크라코스', (r"K'Rakoths?(?!an)", r"K'Rakothan"), None, None, False),
    ('aeon a', '아이온', '에이언', r'Aeon', None, None, False),
    ('aeon b', r'(?<![가-힣])이온', '에이언', r'Aeon', None, None, True),
    ('navigator', '항해자', '내비게이터', r'Navigator', None, None, False),
    ('harvester', '하베스터', '수확자', r'Harvester(?! ?Beam)', None, None, False),
    ('megacorp', '거대기업', '메가코프', r'[Mm]egacorp', None, None, False),
    ('tomb keeper 1', '무덤 수호자', '무덤지기', None, r'fuaviantombkeeper', None, False),
    ('tomb keeper 2', '무덤 경비병', '무덤지기', None, r'fuaviantombkeeper', None, False),
    ('tomb keeper 3', '묘지기', '무덤지기', None, r'fuaviantombkeeper', None, False),
    ('vep name', '잔재 진화 과정', '베스티지-에보 프로세스', None, None, None, False),
]


def load_en_map():
    csv.field_size_limit(10**8)
    m = {}
    with open(PAIRS, encoding='utf-8-sig') as f:
        for r in csv.reader(f, delimiter='\t'):
            if len(r) >= 4:
                m[(r[0], r[1])] = r[2]
    return m


def main():
    apply = '--apply' in sys.argv
    en_map = load_en_map()
    pk = Pak(TARGET)
    overrides = {}
    stats = {lbl: [0, 0] for lbl, *_ in RULES}  # [hits, skipped-guard]
    changed_fields = 0
    for asset in pk.index:
        if not asset.endswith('.patch'):
            continue
        try:
            doc = json.loads(pk.read(asset))
        except Exception:
            continue
        if not isinstance(doc, list):
            continue
        touched = False
        stack = list(doc)
        while stack:
            it = stack.pop()
            if isinstance(it, list):
                stack.extend(it)
                continue
            if not (isinstance(it, dict) and it.get('op') in ('replace', 'add')
                    and isinstance(it.get('value'), str)):
                continue
            path = it.get('path', '')
            v = it['value']
            nv = v
            for lbl, pat, rep, eg, ag, pg, isre in RULES:
                if ag and not re.search(ag, asset):
                    continue
                if pg and not re.search(pg, path):
                    continue
                if eg:
                    en = en_map.get((asset, path))
                    pos, neg = eg if isinstance(eg, tuple) else (eg, None)
                    bad = (en is None or not re.search(pos, en)
                           or (neg and en and re.search(neg, en)))
                    if bad:
                        if pat in nv or (isre and re.search(pat, nv)):
                            stats[lbl][1] += 1
                        continue
                flags = 0
                if isre:
                    nnv = re.sub(pat, rep, nv)
                else:
                    nnv = nv.replace(pat, rep)
                if nnv != nv:
                    stats[lbl][0] += 1
                    nv = nnv
            if nv != v:
                it['value'] = nv
                touched = True
        if touched:
            overrides[asset] = json.dumps(doc, ensure_ascii=False, indent=2).encode('utf-8')
            changed_fields += sum(1 for _ in [1])
    for lbl, *_ in RULES:
        h, s = stats[lbl]
        print(f'{h:4d} hit  {s:4d} guard-skip  {lbl}')
    print(f'\nassets touched: {len(overrides)}')
    if apply:
        pk.f.close()
        print('wrote pak; entries', write_pak(TARGET, TARGET, overrides))
    else:
        print('dry run — pass --apply to write')


if __name__ == '__main__':
    main()
