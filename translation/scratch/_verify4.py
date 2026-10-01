import io,sys,re
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
rows=[]
with open('data/pak_pairs.tsv',encoding='utf-8') as f:
    head=f.readline()
    for ln in f:
        t=ln.rstrip('\n').split('\t')
        if len(t)<4: continue
        rows.append((t[0],t[1],t[2],t[3]))
# targeted pointers to check current values
PTRS = [
 '/dialog/tentacles/hylotl-pregnant.config.patch',
 'ffs0_0_0','ffs0_3_1','ffs0_5_15','ffs0_5_0','ffs_breadnut1_0_0',
 'ttppmission1e','ttppmission2f1','ffs2_lastboss_0_8','ffs2_8_12',
 'ffs2_9_1','ffs2_f4_23','ffs2_f3_9','ffs2_8_1','ffs2_9_9',
 'mwhaddon_mission_horizon_4_6','mwhaddon_mission_mainStory_chapter2_1_7',
 'vanguardmechunlock','combat.config.patch',
]
for r in rows:
    for p in PTRS:
        if p in r[0] or p in r[1]:
            print(f"  {r[0]}/{r[1]}")
            print(f"    EN: {r[2][:160]}")
            print(f"    KO: {r[3][:160]}")
            break
