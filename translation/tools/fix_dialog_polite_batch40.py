# -*- coding: utf-8 -*-
# Batch40: residual honorific infixes inside already-converted dialogue lines
# (syllable-internal 시 that str-based infix cleanup could not reach), plus
# manually verified single-line translation errors from the bank review.
import csv, sys, io, json
from collections import defaultdict

csv.field_size_limit(sys.maxsize)
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak
from pak_writer import write_pak

ROOT = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
TARGET = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"

SUBS = {
    # residual honorific infixes left after conv (lines already plain-styled)
    ('/dialog/atprk_devouttenant.config.patch', '/converse/default/default/4'):
        [('자비로우셨다', '자비로웠다')],
    ('/dialog/avikanoutpost.config.patch', '/converse/avikan/default/1'):
        [('생물이실까?', '생물일까?')],
    ('/dialog/avikanoutpost.config.patch', '/converse/avikan/hylotl/5'):
        [('주실 수 있나?', '줄 수 있나?')],
    ('/dialog/avikanoutpost.config.patch', '/converse/avikan/avikan/17'):
        [('주실 수 있나?', '줄 수 있나?')],
    ('/dialog/avikanoutpost.config.patch', '/converse/avikan/avikan/22'):
        [('있으신가?', '있는가?')],
    ('/dialog/avikanoutpost.config.patch', '/converse/avikan/avikan/24'):
        [('필요하신가?', '필요한가?')],
    ('/dialog/avikanoutpost.config.patch', '/converse/avikan/avikan/28'):
        [('있으신가?', '있는가?')],
    ('/dialog/avikanoutpost.config.patch', '/converse/avikan/avikan/43'):
        [('여행하시며', '여행하며'), ('있으신가?', '있는가?')],
    ('/dialog/avikanoutpost.config.patch', '/converse/avikan/avikan/44'):
        [('있으신가?', '있는가?')],
    ('/dialog/bartenderwoofie.config.patch', '/merchantStart/glitch/default/0'):
        [('오신 걸', '온 걸')],
    ('/dialog/bartenderwoofie.config.patch', '/tout/hylotl/default/1'):
        [('필요하신 물건', '필요한 물건')],
    ('/dialog/commands.config.patch', '/lounge/glitch/default/2'):
        [('쉬실 건가?', '쉴 건가?')],
    ('/dialog/hookerconverse.config.patch', '/converse/glitch/default/1'):
        [('싶으신가?', '싶은가?')],
    ('/dialog/lucario.config.patch', '/converse/default/hylotl/12'):
        [('주실 수 있나?', '줄 수 있나?')],
    ('/quests/mwhaddon_quests/mwhaddon_quests_arcana_vendor_3/mwhaddon_quests_arcana_vendor_3_scan.questtemplate.patch', '/text'):
        [('오신 걸', '온 걸')],
    ('/quests/STORY/alliance/alliancestorystart.questtemplate.patch', '/scriptConfig/radioMessages/secondMessage/text'):
        [('탈출하신 걸', '탈출한 걸')],
    ('/quests/atprk_relicseekerhq/atprk_rishaanquest1.questtemplate.patch', '/scriptConfig/radioMessages/uniqueProgress/atprk-gildedportrait-tailed/text'):
        [('삼으셨던', '삼았던')],
    ('/dialog/sb_friendlyminer.config.patch', '/rent/avian/default/0'):
        [('축복해주셨어', '축복해줬어')],
    ('/dialog/saturnWaspmim.config.patch', '/hail/saturn/apiarian/4'):
        [('말씀하셨지', '말했지')],
    ('/dialog/saturnspaceconverse.config.patch', '/spacesaturnwasp/saturn/apiarian/4'):
        [('말씀하셨지', '말했지')],
    # fully-polite lines in casual-majority banks (never selected / left mixed)
    ('/dialog/r-peacekeeperconverse.config.patch', '/converse/apex/default/0'):
        [('도와드리겠습니다!', '도와주겠다!'), ('안 돼요.', '안 돼.'), ('바쁘거든요.', '바쁘거든.')],
    ('/dialog/r-peacekeeperconverse.config.patch', '/converse/apex/default/2'):
        [('기회예요!', '기회야!')],
    ('/dialog/r-peacekeeperconverse.config.patch', '/converse/apex/default/4'):
        [('갖게 됐어요.', '갖게 됐어.')],
    ('/dialog/r-peacekeeperconverse.config.patch', '/converse/apex/default/7'):
        [('없을 겁니다.', '없을 거다.')],
    ('/dialog/r-peacekeeperconverse.config.patch', '/converse/apex/default/9'):
        [('바랍니다.', '바란다.')],
    ('/dialog/r-peacekeeperconverse.config.patch', '/converse/avian/default/4'):
        [('안녕하신가.', '안녕.')],
    ('/dialog/r-peacekeeperconverse.config.patch', '/converse/novakid/default/9'):
        [('안녕하신가!', '안녕!')],
    ('/radiomessages/ffs2_radiomessages.radiomessages.patch', '/ffs2_5_6/text'):
        [('안녕하신가,', '안녕,')],
    ('/dialog/merchant.config.patch', '/severe/fumantizi/default/1'):
        [('빨리 고쳐요,', '빨리 고쳐,')],
    ('/dialog/catgrumble.config.patch', '/severe/cat/default/0'):
        [('요구합니다.', '요구해.')],
    ('/dialog/catgrumble.config.patch', '/severe/cat/default/2'):
        [('떠날 거예요.', '떠날 거야.')],
    # single-line translation/particle errors collected during bank review
    ('/radiomessages/ffs_radiomessages.radiomessages.patch', '/ffs0_3_1/text'):
        [('1층 지할이다', '1층 지하실이다')],  # restore: earlier infix ate 지하실->지할
    ('/dialog/USCMdisbanded.config.patch', '/converse/default/default/16'):
        [('USCM를', 'USCM을')],
    ('/dialog/bartenderwoofie.config.patch', '/severe/avian/default/0'):
        [('내 술집을 고쳐 줘야겠다!', '내 술집을 고쳐줘!')],  # EN: I need YOU to fix
    ('/dialog/lucario.config.patch', '/converse/default/default/0'):
        [('네 존재 신비.', '네 존재가 신비롭군.')],
    ('/dialog/viera.config.patch', '/wwvillagergreeting/default/default/8'):
        [('네 존재 가볍게 안 봐', '네 존재를 가볍게 안 봐')],
    ('/dialog/viera.config.patch', '/wwwayfarergreeting/default/default/8'):
        [('네 존재 가볍게 안 봐', '네 존재를 가볍게 안 봐')],
}


def fix(asset, pointer, ko):
    if (asset, pointer) in SUBS:
        for a, b in SUBS[(asset, pointer)]:
            ko = ko.replace(a, b)
    return ko


def main():
    changes = defaultdict(dict)
    for row in csv.DictReader(open(ROOT + r'\pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
        ko = row['korean']
        new = fix(row['asset'], row['pointer'], ko)
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
    print('changed', changed, 'fields; expected', n)
    if changed != n:
        print('MISMATCH - aborting write')
        return
    pk.f.close()
    print('wrote pak; entries', write_pak(TARGET, TARGET, overrides))


if __name__ == '__main__':
    main()
