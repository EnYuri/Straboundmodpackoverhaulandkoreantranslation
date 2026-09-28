import csv,glob,re,collections,os

# global safe replacements (substring)
REPL=[
 ('순간이동 장치','텔레포터'),('순간이동장치','텔레포터'),('순간이동기','텔레포터'),
 ('히로틀','하이로틀'),('러슬링','러스틀링'),('미니크노그','미니크녹'),
 ('팝탑','팝톱'),('숏소드','소검'),('쇼트소드','소검'),('유탄발사기','유탄 발사기'),
 ('그랜드 프로텍터','대보호자'),('대수호자','대보호자'),('오카수스','오카서스'),
 ('평화유지군','피스키퍼'),('에스터','에스더'),('카파','캇파'),('사우모스','타우모스'),
 ('사투르니안','새터니안'),('테렌 보호국','행성 보호국'),('트링키언','트링크'),
 ('아에기안','에지안'),('에기안','에지안'),('아에기','에지'),('에이기','에지'),('에기','에지'),
]
# per-row contextual fixes
PERROW={
 # Shortsword -> 소검
 '58125':('천사 단도','천사 소검'),
 '107826':('밝은 단검','밝은 소검'),
 '109035':('솔라리움 단검','솔라리움 소검'),
 # leafy-ones
 '104939':('나뭇잎족','잎사귀 종족'),
 '107796':('잎-사람들에게 죽은 생물의 유해로','잎사귀 종족이 죽인 생물의 유해로'),
 # Floran third-person restored
 '51643':('맛있을까 궁금하다','플로란이 맛있을까 궁금하다'),
 '80707':('힘들다고 들었다','힘들다고 플로란이 들었다'),
 '80708':('힘들었다고 들었다','힘들었다고 플로란이 들었다'),
 '99485':('보기만 해도 기분 안 좋다','플로란은 보기만 해도 기분 안 좋다'),
 '114925':('독 있다고 들었다','독 있다고 플로란이 들었다'),
 '118223':('이 고기 큐브 맛이 궁금하다','이 고기 큐브 맛이 플로란은 궁금하다'),
 # Spooked verb usage
 '61820':('플로란도 이 생물에 소름 끼쳐!','플로란도 이 생물에 겁먹었다!'),
 '75249':('이 호박엔 안 놀란다!','난 이 호박에 겁먹지 않는다!'),
}
tot=collections.Counter()
for f in sorted(glob.glob('translations/*.tsv')):
    rows=list(csv.reader(open(f,encoding='utf-8-sig',newline=''),delimiter='\t',quoting=csv.QUOTE_MINIMAL))
    n=0
    for r in rows:
        if len(r)<2: continue
        orig=r[1]
        for a,b in REPL: r[1]=r[1].replace(a,b)
        if r[0] in PERROW:
            a,b=PERROW[r[0]]
            if a in r[1]: r[1]=r[1].replace(a,b)
            else: print('PERROW MISS',r[0],a,'|',r[1][:60])
        if r[1]!=orig: n+=1
    if n:
        csv.writer(open(f,'w',encoding='utf-8',newline=''),delimiter='\t',quoting=csv.QUOTE_MINIMAL,lineterminator='\n').writerows(rows)
        tot[os.path.basename(f)]=n
print('files:',len(tot),'rows:',sum(tot.values()))
