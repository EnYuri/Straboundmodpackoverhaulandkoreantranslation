# -*- coding: utf-8 -*-
# Batch41: confirmed mistranslations, typos and glossary violations collected
# during the full dialogue-bank line review (12,603-row _dialog_review.txt).
# Every entry was verified against the live deployed pak (direct op read).
import sys, io, json

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak
from pak_writer import write_pak

TARGET = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"

SUBS = {
    # ---- landlord honorific: 영주님 -> 집주인님 (14 rows, all landlord ctx) ----
    ('/dialog/atprk_devouttenant.config.patch', '/beacon/default/default/2'):
        [('영주님', '집주인님')],
    ('/dialog/merchant.config.patch', '/beacon/nightar/default/0'):
        [('영주님', '집주인님')],
    ('/dialog/merchant.config.patch', '/enclosedArea/nightar/default/0'):
        [('영주님', '집주인님')],
    ('/dialog/merchant.config.patch', '/follow/nightar/default/0'):
        [('영주님', '집주인님')],
    ('/dialog/merchant.config.patch', '/follow/nightar/default/4'):
        [('영주님', '집주인님')],
    ('/dialog/merchant.config.patch', '/merchantEnd/nightar/default/0'):
        [('영주님', '집주인님')],
    ('/dialog/merchant.config.patch', '/rent/nightar/default/1'):
        [('영주님', '집주인님')],
    ('/dialog/merchant.config.patch', '/welcome/nightar/nightar/0'):
        [('영주님', '집주인님')],
    ('/npcs/foolcook.npctype.patch', '/scriptConfig/dialog/merchant/welcome/default/default/2'):
        [('영주님', '집주인님')],
    ('/npcs/foolcook.npctype.patch', '/scriptConfig/dialog/merchant/welcome/default/glitch/default/2'):
        [('영주님', '집주인님')],
    ('/npcs/foolcook.npctype.patch', '/scriptConfig/dialog/merchant/welcome/tenant/arrivedHome/beacon/default/default/1'):
        [('영주님', '집주인님')],
    ('/npcs/foolcook.npctype.patch', '/scriptConfig/dialog/merchant/welcome/tenant/arrivedHome/beacon/default/default/2'):
        [('영주님', '집주인님')],
    ('/npcs/foolcook.npctype.patch', '/scriptConfig/dialog/merchant/welcome/tenant/arrivedHome/beacon/glitch/default/1'):
        [('영주님', '집주인님')],
    ('/npcs/foolcook.npctype.patch', '/scriptConfig/dialog/merchant/welcome/tenant/arrivedHome/beacon/glitch/default/2'):
        [('영주님', '집주인님')],
    # ---- glossary: Protectorate -> 보호국 (19 rows) ----
    ('/codex/LEGACY/THE_WAR_ON_MARS/CHAPTER_0/3_CRASH/gic_twom_guerilla/gic_twom_guerilla.codex.patch', '/contentPages/0'):
        [('수호자레이트', '보호국')],
    ('/monsters/LEGACY/gic_oldversion_protectorateknight/gic_oldversion_protectorateknight.monstertype.patch', '/shortdescription'):
        [('수호자레이트', '보호국')],
    ('/objects/STANDARD/gic_proweaponcratelarge/gic_proweaponcratelarge.object.patch', '/description'):
        [('수호자레이트', '보호국')],
    ('/objects/STANDARD/gic_proweaponcratemedium/gic_proweaponcratemedium.object.patch', '/description'):
        [('수호자레이트', '보호국')],
    ('/objects/STATIC_VEHICLES/SPAWNABLES/gic_mg2750_turret_spawnerobject/gic_mg2750_turret_spawnerobject.object.patch', '/description'):
        [('수호자레이트', '보호국')],
    ('/objects/STATIC_VEHICLES/gic_protectorate_beluga/gic_protectorate_beluga.object.patch', '/shortdescription'):
        [('수호자레이트', '보호국')],
    ('/objects/STATIC_VEHICLES/gic_protectorate_bobcat/gic_protectorate_bobcat.object.patch', '/description'):
        [('수호자레이트', '보호국')],
    ('/objects/STATIC_VEHICLES/gic_protectorate_bobcat/gic_protectorate_bobcat.object.patch', '/shortdescription'):
        [('수호자레이트', '보호국')],
    ('/objects/STATIC_VEHICLES/gic_protectorate_skydancer_floatingwreck/gic_protectorate_skydancer_floatingwreck.object.patch', '/description'):
        [('수호자레이트', '보호국')],
    ('/objects/STATIC_VEHICLES/gic_protectorate_skydancer_floatingwreck/gic_protectorate_skydancer_floatingwreck.object.patch', '/shortdescription'):
        [('수호자레이트', '보호국')],
    ('/objects/TOMBS/gic_loyalistmemorial/gic_loyalistmemorial.object.patch', '/description'):
        [('수호자레이트', '보호국')],
    ('/objects/ship/gic_protectorateship_human/gic_protectorateship_human.object.patch', '/description'):
        [('수호자레이트', '보호국')],
    ('/objects/ship/gic_protectorateship_human/gic_protectorateship_human.object.patch', '/shortdescription'):
        [('수호자레이트', '보호국')],
    ('/objects/wired/gic_spiritsummon/gic_spiritsummon_protectoratefootsoldier.object.patch', '/description'):
        [('수호자레이트', '보호국')],
    ('/objects/wired/gic_spiritsummon/gic_spiritsummon_protectoratefootsoldier.object.patch', '/shortdescription'):
        [('수호자레이트', '보호국')],
    ('/objects/wired/gic_spiritsummon/gic_spiritsummon_protectorateundeadknight.object.patch', '/description'):
        [('수호자레이트', '보호국')],
    ('/objects/wired/gic_spiritsummon/gic_spiritsummon_protectorateundeadknight.object.patch', '/shortdescription'):
        [('수호자레이트', '보호국')],
    ('/objects/wired/gic_spiritsummon/gic_spiritsummon_protectorateundeadpaladin.object.patch', '/description'):
        [('수호자레이트', '보호국')],
    ('/objects/wired/gic_spiritsummon/gic_spiritsummon_protectorateundeadpaladin.object.patch', '/shortdescription'):
        [('수호자레이트', '보호국')],
    # ---- glossary: Grand Protector -> 고위 수호자 (5 rows) ----
    ('/objects/protectorate/objects/protectorategardenbench/protectorategardenbench.object.patch', '/slimepersonDescription'):
        [('그랜드 수호자', '고위 수호자')],
    ('/objects/protectorate/objects/protectorateportrait3/protectorateportrait3.object.patch', '/slimepersonDescription'):
        [('그랜드 수호자', '고위 수호자')],
    ('/objects/protectorate/objects/protectorateportraitold/protectorateportraitold.object.patch', '/avianDescription'):
        [('그랜드 수호자', '고위 수호자')],
    ('/objects/protectorate/objects/protectorateportraitold/protectorateportraitold.object.patch', '/description'):
        [('그랜드 수호자', '고위 수호자')],
    ('/objects/protectorate/objects/protectorateportraitold/protectorateportraitold.object.patch', '/hylotlDescription'):
        [('그랜드 수호자', '고위 수호자')],
    # ---- typo: 늑고위 -> 늑대 (2 rows) ----
    ('/items/WEAPONS/MELEE/SWORD/gic_wolfguardian_scimitar/gic_wolfguardian_scimitar_playerpose.activeitem.patch', '/shortdescription'):
        [('늑고위', '늑대')],
    ('/items/WEAPONS/MELEE/SWORD/gic_wolfguardian_scimitar/gic_wolfguardian_scimitar_playerpose_backhand.activeitem.patch', '/shortdescription'):
        [('늑고위', '늑대')],
    # ---- FFS floor ordering / drop pod / misc ----
    ('/radiomessages/ffs_radiomessages.radiomessages.patch', '/ffs0_0_0/text'):
        [('탈출 포드', '드롭 포드')],
    ('/radiomessages/ffs_radiomessages.radiomessages.patch', '/ffs_breadnut1_0_0/text'):
        [('탈출 포드', '드롭 포드')],
    ('/radiomessages/ffs_radiomessages_hc.radiomessages.patch', '/ffs0_0_0_hc/text'):
        [('탈출 포드', '드롭 포드')],
    ('/radiomessages/ffs_radiomessages.radiomessages.patch', '/ffs0_3_1/text'):
        [('1층 지하실이다', '지하 1층이다')],
    ('/radiomessages/ffs_radiomessages.radiomessages.patch', '/ffs0_5_15/text'):
        [('4층 지하로 가', '지하 4층으로 가')],
    ('/radiomessages/ffs2_radiomessages_hc.radiomessages.patch', '/ffs2_5_6b_3_hc/text'):
        [('긴 여정 대신에', '기나긴 고행 대신에')],
    ('/radiomessages/ffs2_radiomessages.radiomessages.patch', '/ffs2_lastboss_1_18/text'):
        [('여기서 꺼내줘', '여기서 빼줘')],
    ('/radiomessages/ffs2_radiomessages.radiomessages.patch', '/ffs2_lastboss_2_8/text'):
        [('격추해!', '쓰러뜨려!')],
    ('/radiomessages/ffs_mission_radiomessages.radiomessages.patch', '/ffs_cultistmission_lastline2/text'):
        [('너도 그렇다', '너도 마찬가지다')],
    ('/radiomessages/ffs2_radiomessages.radiomessages.patch', '/ffs2_6_14/text'):
        [('컬트 추종자들한테', '광신도들한테')],
    # ---- White Crow -> 화이트 크로우 ----
    ('/radiomessages/ffs2_radiomessages.radiomessages.patch', '/ffs2_9_1/text'):
        [('화이트 크로를', '화이트 크로우를')],
    ('/radiomessages/ffs2_radiomessages.radiomessages.patch', '/ffs2_f4_23/text'):
        [('화이트 크로의', '화이트 크로우의')],
    ('/radiomessages/ffs2_radiomessages.radiomessages.patch', '/ffs2_lastboss_1_19/senderName'):
        [('화이트 크로 크루', '화이트 크로우 크루')],
    ('/radiomessages/ffs2_radiomessages.radiomessages.patch', '/ffs2_lastboss_2_5/senderName'):
        [('화이트 크로 크루', '화이트 크로우 크루')],
    # ---- TTPP: Coock is a name, not a rooster; misc tone ----
    ('/radiomessages/ttppmission.radiomessages.patch', '/ttppmission1e2/text'):
        [('내 수탉 돌려줘', '내 쿡을 돌려줘')],
    ('/radiomessages/ttppmission.radiomessages.patch', '/ttppmission2f1/text'):
        [('터질 것 같네', '꽉 차 있네')],
    ('/radiomessages/ttppmission.radiomessages.patch', '/ttppmission3u5/text'):
        [('더 커졌어', '더 커져라')],
    # ---- mwhaddon main story ----
    ('/radiomessages/mwhaddon_mission_mainStory.radiomessages.patch', '/mwhaddon_mission_mainStory_chapter2_1_7/text'):
        [('당황스럽네', '의아하네')],
    ('/radiomessages/mwhaddon_mission_mainStory.radiomessages.patch', '/mwhaddon_mission_mainStory_chapter2_3_5/text'):
        [('길을 비켜라', '길을 비워라')],
    ('/radiomessages/mwhaddon_mission_mainStory.radiomessages.patch', '/mwhaddon_mission_mainStory_chapter2_3_10/text'):
        [('또 결정을 흡수', '또 수정을 흡수')],
    ('/radiomessages/mwhaddon_mission_mainStory.radiomessages.patch', '/mwhaddon_mission_mainStory_chapter3_1_10/text'):
        [('전차 선로', '트램 선로')],
    ('/radiomessages/mwhaddon_mission_mainStory.radiomessages.patch', '/mwhaddon_mission_mainStory_chapter3_3_5/text'):
        [('폭력적인 반응', '격렬한 반응')],
    ('/radiomessages/mwhaddon_mission_mainStory.radiomessages.patch', '/mwhaddon_mission_mainStory_chapter2_2_11/text'):
        [('선배을', '선배를')],
    # ---- mwhaddon side story ----
    ('/radiomessages/mwhaddon_mission_sideStory.radiomessages.patch', '/mwhaddon_mission_horizon_2_10/text'):
        [('요양실', '회복실')],
    ('/radiomessages/mwhaddon_mission_sideStory.radiomessages.patch', '/mwhaddon_mission_horizon_3_4/text'):
        [('또 다른 무리가 감지되었다', '또 다른 지뢰 무리가 감지됐다')],
    ('/radiomessages/mwhaddon_mission_sideStory.radiomessages.patch', '/mwhaddon_mission_horizon_4_8/text'):
        [('시험 제작소', '시험 제조 공장')],
    # ---- thea instances ----
    ('/radiomessages/thea-instances.radiomessages.patch', '/vanguardmechunlock8/text'):
        [('점프젯', '점프제트')],
    ('/radiomessages/thea-instances.radiomessages.patch', '/vanguardmechunlock10/text'):
        [('뛰어나가서', '밖으로 뛰어내려')],
    ('/radiomessages/thea-instances.radiomessages.patch', '/remnantsplinter-foundgoal/text'):
        [('에너지들의', '에너지의')],
    # ---- atprk pin comments ----
    ('/radiomessages/atprk_planetpincomments.radiomessages.patch', '/atprk_planetpincomment_ocean3/text'):
        [('따분하게 불편', '끔찍하게 불편')],
    ('/radiomessages/atprk_planetpincomments.radiomessages.patch', '/atprk_planetpincomment_alien4/text'):
        [('내 말인데?', '그런 모양인데?')],
    # ---- arcana ----
    ('/radiomessages/arcana_mission_seekerIntro.radiomessages.patch', '/arcana_mission_seekerIntro_3_2/text'):
        [('튀는 탄환', '통통 튀는 탄환')],
    # ---- gico / gicexp ----
    ('/radiomessages/gico_messages.radiomessages.patch', '/gico_lion_village_arena_meetup/text'):
        [('네가 자신에게 쓸모 있을 거라', '네가 족장님께 쓸모 있을 거라')],
    ('/radiomessages/gicexp_missions.radiomessages.patch', '/esc_exp_story_1/text'):
        [('넌 그들과 달라', '넌 그들 일당이 아니야')],
    ('/radiomessages/gicexp_missions.radiomessages.patch', '/esc_exp_story_rebel_3/text'):
        [('테러리스트 쏴버릴', '테러리스트를 쏴버릴')],
    # ---- hellishdemon ----
    ('/radiomessages/hellishdemon.radiomessages.patch', '/hellishdemon33/text'):
        [("네가 '용감하다'고 자신할 수 있어?", "네가 '용감한' 척할 자신이 있어?")],
    # ---- lofty irisil pickmeup ----
    ('/radiomessages/lofty_irisil_pickmeup.radiomessages.patch', '/lofty_irisil_pickMeUp_welcomeToOurHome_2/text'):
        [('갈고리 걸이', '그래플링 훅')],
    ('/radiomessages/lofty_irisil_pickmeup.radiomessages.patch', '/lofty_irisil_pickMeUp_completeRedRoom/text'):
        [('리로케이터', '재배치기')],
    ('/radiomessages/lofty_irisil_pickmeup.radiomessages.patch', '/lofty_irisil_pickMeUp_redBunnyPuzzleInstructions/text'):
        [('이건 나용이다', '이건 나를 위한 거다')],
    # ---- dialogue banks: naturalness / typos ----
    ('/dialog/avikanoutpost.config.patch', '/converse/avikan/glitch/11'):
        [('팔지는 의심스럽군', '팔 것 같지는 않군')],
    ('/dialog/avikanoutpost.config.patch', '/converse/avikan/trink/11'):
        [('팔지는 의심스럽군', '팔 것 같지는 않군')],
    ('/dialog/avikanoutpost.config.patch', '/converse/avikan/avikan/17'):
        [('평의회에서 저를 위해 찬성표를 던져 줄 수 있나?', '평의회에서 나를 지지해 줄 수 있나?')],
    ('/dialog/bartenderwoofie.config.patch', '/merchantEnd/avian/default/0'):
        [('번개 같은 방문이었네', '번개처럼 짧은 방문이었네')],
    ('/dialog/lucario.config.patch', '/converse/default/human/6'):
        [('내나 남에게', '나나 남에게')],
    ('/dialog/lucario.config.patch', '/converse/default/apex/15'):
        [('내 털은 곧네', '내 털은 쭉 뻗었네')],
    ('/dialog/saturnspaceconverse.config.patch', '/spacesaturnian/saturn/arachne/6'):
        [('온순한 편이야', '온순한 편이니')],
    ('/dialog/saturnspaceconverse.config.patch', '/spacesaturnian/saturn/satkyterran/7'):
        [('미라실 바깥의', '미라실 출신의')],
    ('/dialog/esc_corpus_empolyee.config.patch', '/converse/default/default/5'):
        [('연구개발 루나-테크 전투복 납품 받았대', '연구개발팀에서 루나-테크 전투복이 납품됐대')],
    ('/dialog/esc_corpus_empolyee.config.patch', '/greeting/default/default/7'):
        [('연구개발 루나-테크 전투복 납품 받았대', '연구개발팀에서 루나-테크 전투복이 납품됐대')],
    ('/dialog/viera.config.patch', '/wwvillagergreeting/default/default/8'):
        [('가볍게 안 봐', '가볍게 보지 않아')],
    ('/dialog/viera.config.patch', '/wwwayfarergreeting/default/default/8'):
        [('가볍게 안 봐', '가볍게 보지 않아')],
    ('/dialog/unboundvillagesecurity.config.patch', '/hail/default/default/0'):
        [('무분쟁 구역', '분쟁 금지 구역')],
    ('/dialog/unboundvillagesecurity.config.patch', '/hail/apex/default/6'):
        [('무분쟁 구역', '분쟁 금지 구역')],
    # ---- combat barks: fenerox register mix ----
    ('/dialog/combat.config.patch', '/outOfSight/fenerox/default/2'):
        [('적이 보입니까? 교전할 수 없습니다.', '적이 보이는가? 교전할 수 없다.')],
    ('/dialog/combat.config.patch', '/outOfSight/fenerox/default/3'):
        [('적이 사라졌습니까? 아니, 보이지 않습니다.', '적이 사라졌는가? 아니, 보이지 않는다.')],
    # ---- tentacles/sexbound ----
    ('/dialog/sexbound/en/notifications.config.patch', '/plugins/pregnant/abortion/0/default'):
        [('최선의 생각이 아니었을지도', '좋은 생각은 아니었을지도')],
    ('/dialog/sexbound/en/notifications.config.patch', '/plugins/pregnant/abortion/1/default'):
        [('최선의 생각이 아니었을지도', '좋은 생각은 아니었을지도')],
    ('/dialog/tentacles/pregnant.config.patch', '/7/text'):
        [('곤란 처지네', '곤란한 처지네')],
    ('/dialog/tentacles/human-pregnant.config.patch', '/7/text'):
        [('곤란 처지네', '곤란한 처지네')],
    ('/dialog/tentacles/human-pregnant.config.patch', '/24/text'):
        [('촉수 무리 안에서', '촉수 소굴 안에서')],
    ('/dialog/tentacles/hylotl-pregnant.config.patch', '/23/text'):
        [('이건 촉수 무리야~', '이건 촉수의 새끼야~')],
    ('/dialog/tentacles/hylotl-pregnant.config.patch', '/37/text'):
        [('씨앗으로', '씨받이로')],
    ('/dialog/tentacles/hylotl-pregnant.config.patch', '/41/text'):
        [('알들이이 나온다', '알들이이 들어간다')],
    # ---- objects ----
    ('/objects/cult_pillory/cult_pillory.object.patch', '/description'):
        [('칼(형틀)', '형틀')],
    ('/items/MATERIALS/tentacleblock.matitem.patch', '/shortdescription'):
        [('촉수 무리', '촉수 블록')],
    ('/objects/themed/sushibar/sushibarmenu/sushibarmenu.object.patch', '/avianDescription'):
        [('내 뱃속에 가장 쉬운 지', '내 뱃속에서 가장 편할지')],
    # ---- cinematic shrine maiden register ----
    ('/cinematics/CHARACTERS/SHRINEMAIDEN/gico_shrinemaiden_meeting_human_path.cinematic.patch', '/panels/4/text'):
        [('무녀랍니다', '무녀예요')],
    # ---- codex rank typo ----
    ('/codex/documents/scienceoutpost_kevin.codex.patch', '/contentPages/60'):
        [('홀릭스 이병', '홀릭스 이등병')],
}


def main():
    by_asset = {}
    for (asset, pointer), subs in SUBS.items():
        by_asset.setdefault(asset, []).append((pointer, subs))
    pk = Pak(TARGET)
    overrides = {}
    changed = 0
    missing = []
    for asset, ptr_subs in by_asset.items():
        try:
            doc = json.loads(pk.read(asset))
        except Exception as e:
            for pointer, _ in ptr_subs:
                missing.append((asset, pointer, f'read: {e}'))
            continue
        want = {}
        for pointer, subs in ptr_subs:
            want.setdefault(pointer, []).extend(subs)
        stack = list(doc)
        hit = 0
        seen = set()
        while stack:
            it = stack.pop()
            if isinstance(it, list):
                stack.extend(it)
            elif isinstance(it, dict) and it.get('op') in ('replace', 'add') \
                    and it.get('path') in want and isinstance(it.get('value'), str):
                seen.add(it['path'])
                v = it['value']
                nv = v
                for a, b in want[it['path']]:
                    nv = nv.replace(a, b)
                if nv != v:
                    it['value'] = nv
                    hit += 1
        if hit:
            overrides[asset] = json.dumps(doc, ensure_ascii=False, indent=2).encode('utf-8')
            changed += hit
        for pointer, _ in ptr_subs:
            if pointer not in seen:
                missing.append((asset, pointer, 'no replace/add op changed'))
    print('changed', changed, 'ops / pointers', len(SUBS))
    if missing:
        print('MISSING/UNCHANGED:')
        for m in missing:
            print('  ', m[0], m[1], m[2])
        return
    pk.f.close()
    print('wrote pak; entries', write_pak(TARGET, TARGET, overrides))


if __name__ == '__main__':
    main()
