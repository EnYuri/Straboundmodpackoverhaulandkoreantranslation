import io,sys,re
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
KEYS = ["투하 포드","드롭 포드","조금만","전차 선로","트램 선로","기관사","제인","여군주","안나야","애나야","시커","알들이","위하-","석화된 촉수' 교단","신형 레드","새 레드","지하","컬트","촉수 떼","촉수 둥지","촉수 블록","둥지","영주님","집주인","컬티스트","광신도"]
rows=[]
with open('data/pak_pairs.tsv',encoding='utf-8') as f:
    head=f.readline()
    for ln in f:
        t=ln.rstrip('\n').split('\t')
        if len(t)<4: continue
        rows.append((t[0],t[1],t[2],t[3]))
print(len(rows))
for k in KEYS:
    hits=[r for r in rows if k in r[3]]
    if not hits:
        print(f"\n===== {k}  (0) ====="); continue
    print(f"\n===== {k}  ({len(hits)}) =====")
    for r in hits[:16]:
        print(f"  {r[0]}/{r[1]}")
        print(f"    EN: {r[2][:150]}")
        print(f"    KO: {r[3][:150]}")
