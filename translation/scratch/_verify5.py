import io,sys
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
EXACT = {
 '/radiomessages/ffs_radiomessages.radiomessages.patch//ffs0_0_0/text',
 '/radiomessages/ffs_radiomessages.radiomessages.patch//ffs0_3_1/text',
 '/radiomessages/ffs_radiomessages.radiomessages.patch//ffs0_5_15/text',
 '/radiomessages/ffs_radiomessages.radiomessages.patch//ffs_breadnut1_0_0/text',
 '/radiomessages/ffs_radiomessages_hc.radiomessages.patch//ffs0_0_0_hc/text',
 '/radiomessages/ttppmission.radiomessages.patch//ttppmission1e/text',
 '/radiomessages/ttppmission.radiomessages.patch//ttppmission1e2/text',
 '/radiomessages/ttppmission.radiomessages.patch//ttppmission2f1/text',
 '/radiomessages/ttppmission.radiomessages.patch//ttppmission3u5/text',
 '/radiomessages/ffs2_radiomessages.radiomessages.patch//ffs2_lastboss_0_8/text',
 '/radiomessages/ffs2_radiomessages.radiomessages.patch//ffs2_8_12/text',
 '/radiomessages/ffs2_radiomessages.radiomessages.patch//ffs2_9_1/text',
 '/radiomessages/ffs2_radiomessages.radiomessages.patch//ffs2_f4_23/text',
 '/radiomessages/ffs2_radiomessages.radiomessages.patch//ffs2_f3_9/text',
 '/radiomessages/ffs2_radiomessages.radiomessages.patch//ffs2_9_5/text',
 '/radiomessages/ffs2_radiomessages_hc.radiomessages.patch//ffs2_5_6b_3_hc/text',
 '/dialog/tentacles/hylotl-pregnant.config.patch//41/text',
 '/dialog/tentacles/hylotl-pregnant.config.patch//23/text',
 '/dialog/tentacles/hylotl-pregnant.config.patch//21/text',
 '/dialog/tentacles/human-pregnant.config.patch//24/text',
 '/dialog/tentacles/human-pregnant.config.patch//7/text',
 '/items/MATERIALS/tentacleblock.matitem.patch//shortdescription',
 '/radiomessages/mwhaddon_mission_mainStory.radiomessages.patch//mwhaddon_mission_mainStory_chapter2_1_7/text',
 '/radiomessages/mwhaddon_mission_mainStory.radiomessages.patch//mwhaddon_mission_mainStory_chapter2_3_5/text',
 '/radiomessages/mwhaddon_mission_mainStory.radiomessages.patch//mwhaddon_mission_mainStory_chapter3_1_10/text',
 '/radiomessages/mwhaddon_mission_mainStory.radiomessages.patch//mwhaddon_mission_mainStory_chapter3_3_5/text',
 '/radiomessages/mwhaddon_mission_sideStory.radiomessages.patch//mwhaddon_mission_horizon_2_2/text',
 '/radiomessages/mwhaddon_mission_sideStory.radiomessages.patch//mwhaddon_mission_horizon_3_4/text',
 '/radiomessages/thea-instances.radiomessages.patch//vanguardmechunlock8/text',
 '/radiomessages/thea-instances.radiomessages.patch//vanguardmechunlock10/text',
 '/radiomessages/thea-instances.radiomessages.patch//remnantsplinter-foundgoal/text',
 '/radiomessages/lofty_irisil_pickmeup.radiomessages.patch//lofty_irisil_pickMeUp_redBunnyPuzzleInstructions/text',
 '/radiomessages/lofty_irisil_pickmeup.radiomessages.patch//lofty_irisil_pickMeUp_gravityChatter2/text',
 '/radiomessages/lofty_irisil_pickmeup.radiomessages.patch//lofty_irisil_pickMeUp_completeRedRoom/text',
 '/radiomessages/lofty_irisil_pickmeup.radiomessages.patch//lofty_irisil_pickMeUp_welcomeToOurHome_2/text',
 '/radiomessages/ffs2_radiomessages.radiomessages.patch//ffs2_lastboss_1_18/text',
 '/radiomessages/ffs2_radiomessages.radiomessages.patch//ffs2_lastboss_2_8/text',
 '/radiomessages/ffs_radiomessages.radiomessages.patch//ffs0_lastboss_0_2/text',
 '/radiomessages/ffs_mission_radiomessages.radiomessages.patch//ffs_cultistmission_lastline2/text',
 '/radiomessages/gicexp_missions.radiomessages.patch//esc_exp_story_1/text',
 '/radiomessages/gico_messages.radiomessages.patch//gico_lion_village_arena_meetup/text',
 '/radiomessages/hellishdemon.radiomessages.patch//hellishdemon33/text',
 '/radiomessages/atprk_planetpincomments.radiomessages.patch//atprk_planetpincomment_ocean3/text',
 '/radiomessages/atprk_planetpincomments.radiomessages.patch//atprk_planetpincomment_alien4/text',
 '/radiomessages/arcana_mission_seekerIntro.radiomessages.patch//arcana_mission_seekerIntro_3_2/text',
 '/radiomessages/gicexp_missions.radiomessages.patch//esc_exp_story_rebel_3/text',
 '/radiomessages/mwhaddon_mission_sideStory.radiomessages.patch//mwhaddon_mission_horizon_4_8/text',
 '/radiomessages/mwhaddon_mission_sideStory.radiomessages.patch//mwhaddon_mission_horizon_2_11/text',
 '/radiomessages/mwhaddon_mission_sideStory.radiomessages.patch//mwhaddon_mission_horizon_2_10/text',
 '/radiomessages/mwhaddon_mission_mainStory.radiomessages.patch//mwhaddon_mission_mainStory_chapter2_3_10/text',
 '/radiomessages/ffs2_radiomessages.radiomessages.patch//ffs2_lastboss_1_19/senderName',
 '/radiomessages/ffs2_radiomessages.radiomessages.patch//ffs2_lastboss_2_5/senderName',
 '/dialog/combat.config.patch//outOfSight/fenerox/default/2',
 '/dialog/viera.config.patch//wwvillagergreeting/default/default/8',
 '/dialog/viera.config.patch//wwwayfarergreeting/default/default/8',
 '/dialog/saturnspaceconverse.config.patch//spacesaturnian/saturn/satkyterran/7',
 '/dialog/saturnspaceconverse.config.patch//spacesaturnian/saturn/arachne/6',
 '/dialog/esc_corpus_empolyee.config.patch//converse/default/default/5',
 '/dialog/esc_corpus_empolyee.config.patch//greeting/default/default/7',
 '/dialog/avikanoutpost.config.patch//converse/avikan/avikan/17',
 '/dialog/avikanoutpost.config.patch//converse/avikan/glitch/11',
 '/dialog/avikanoutpost.config.patch//converse/avikan/trink/11',
 '/dialog/bartenderwoofie.config.patch//merchantEnd/avian/default/0',
 '/dialog/lucario.config.patch//beacon/default/default/7',
 '/dialog/lucario.config.patch//converse/default/human/6',
 '/dialog/lucario.config.patch//converse/default/apex/15',
 '/dialog/unboundvillagesecurity.config.patch//hail/default/default/0',
 '/dialog/unboundvillagesecurity.config.patch//hail/apex/default/6',
 '/dialog/sexbound/en/notifications.config.patch//plugins/pregnant/abortion/0/default',
 '/dialog/sexbound/en/notifications.config.patch//plugins/pregnant/abortion/1/default',
 '/dialog/tentacles/pregnant.config.patch//7/text',
 '/objects/themed/sushibar/sushibarmenu/sushibarmenu.object.patch//avianDescription',
 '/objects/ship/aegi/aegishiplight/aegishiplightbroken.object.patch//avikanDescription',
 '/objects/ship/akkimari/akkimarishiplight/akkimarishiplightbroken.object.patch//avikanDescription',
 '/objects/ship/avikan/avikanshiplight/avikanshiplightbroken.object.patch//avikanDescription',
 '/objects/cult_pillory/cult_pillory.object.patch//description',
 '/cinematics/CHARACTERS/SHRINEMAIDEN/gico_shrinemaiden_meeting_human_path.cinematic.patch//panels/4/text',
}
found=set()
with open('data/pak_pairs.tsv',encoding='utf-8') as f:
    head=f.readline()
    for ln in f:
        t=ln.rstrip('\n').split('\t')
        if len(t)<4: continue
        key=t[0]+'//'+t[1]
        if key in EXACT:
            found.add(key)
            print(f"  {key}")
            print(f"    EN: {t[2][:170]}")
            print(f"    KO: {t[3][:170]}")
missing = EXACT - found
if missing:
    print("\nNOT FOUND:")
    for m in sorted(missing): print(" ", m)
