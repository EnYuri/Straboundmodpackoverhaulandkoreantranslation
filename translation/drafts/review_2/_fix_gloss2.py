import csv,glob,collections,os

REPL=[
 ('에르치우스','에르키우스'),('얼치어스','에르키우스'),
 ('새터니언','새터니안'),('쿠에투스','콰이어투스'),('텔레브리움','텔레브리엄'),
]
PERROW={
 '103561':('루인 킬러','루인킬러'),
 '125888':('제작 스테이션','제작대'),
 '122248':('사용 가능 재료','재료가 있는 것만 보기'),
 '101956':('순간이동 가게는 많은 선택지를 줘애','텔레포터 가게는 많은 선택지를 준다'),
 '80744':('관통 피해','찌르기 피해'),
 '80375':('카타나 패리','카타나 패링'),
 '112396':('독성 패리','독성 패링'),
 '89550':('타격 보호막','피격 방패'),
 '125690':('독소 어설트 라이플','독소 돌격소총'),
 '126110':('어설트 소총','돌격소총'),
 '88904':('이지설트','에지솔트'),
 '91117':('이지설트','에지솔트'),
 '94433':('지식부 요새','미니크녹 요새'),
 '121634':('제르케시움','제르세슘'),
 '83302':('마기록','매지락'),
 '114241':('마지록','매지락'),
 '83257':('마법탄도','매지샷도'),
 '96773':('매직샷','매지샷'),
 '113645':('연합 체계','연합 시스템'),
 '47501':('MEGA-TRINK 방어구','메가 트링크 갑옷'),
 '52400':('뼈 가공 스테이션','뼈 세공대'),
 '81397':('가죽 작업대','가죽 세공대'),
 '65872':('융합실','핵융합로'),
 '66380':('게아신','기트신'),
 '66399':('게아신','기트신'),
 '127202':('소름 - 혼자가 아니다','겁먹음 - 혼자가 아니다'),
 '112132':('(대검)','(브로드소드)'),
}
tot=collections.Counter()
for f in sorted(glob.glob('translations/*.tsv')):
    rows=list(csv.reader(open(f,encoding='utf-8-sig',newline=''),delimiter='\t',quoting=csv.QUOTE_MINIMAL))
    n=0
    for r in rows:
        if len(r)<2: continue
        orig=r[1]
        for a,b in REPL: r[1]=r[1].replace(a,b)
        if '[CORPORATE KAPPA TRAIT]' in r[1]:
            r[1]=r[1].replace('[CORPORATE KAPPA TRAIT]','[캇파사 특성]')
        if '[Corpo Kappa]' in r[1]:
            r[1]=r[1].replace('[Corpo Kappa]','[캇파사]')
        if r[0] in PERROW:
            a,b=PERROW[r[0]]
            if a in r[1]: r[1]=r[1].replace(a,b)
            else: print('MISS',r[0],a,'|',r[1][:70])
        if r[1]!=orig: n+=1
    if n:
        csv.writer(open(f,'w',encoding='utf-8',newline=''),delimiter='\t',quoting=csv.QUOTE_MINIMAL,lineterminator='\n').writerows(rows)
        tot[os.path.basename(f)]=n
print('files:',len(tot),'rows:',sum(tot.values()))
