import sys,io,os,json,time,re,collections
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
sys.path.insert(0,r'E:/My Games/steamapps/common/Starbound')
sys.path.insert(0,'tools')
import pak,sbjson,pak_writer
TR=r'E:/My Games/steamapps/common/Starbound/mods/zz_translation_female.pak'
pk=pak.Pak(TR)

# test-EN -> correct KO (applies to any replace/add paired with that test)
FIX={
'The incense is a tribute to our ancestors, reminding us of our strength and survival.':'향은 조상들께 바치는 공물이야. 우리의 힘과 생존을 되새기게 해주지.',
'The fragrance rising from the altar lifts my spirits, honoring those who soared before us.':'제단에서 피어오르는 향기가 내 마음을 북돋운다. 먼저 날아간 이들을 기리는 냄새야.',
'Incenssse on altar! Sssmell good! Helpss plantss remember friends who passssed.':'제단에 향이이! 냄새 좋아아! 식물이 떠나간 친구들 기억하게 도와줘엇.',
'Solemn. This incense on the altar holds profound significance; it resonates with my core.':'엄숙함. 제단의 향은 심오한 의미를 지니고 있다. 내 코어와 공명하는군.',
'This incense on the altar comforts me, a warm embrace in our sorrow.':'제단의 향이 나를 위로해준다. 슬픔 속의 따뜻한 포옹 같아.',
'The scent wafting from the altar brings serenity; a perfect moment for reflection.':'제단에서 퍼져 나오는 향기가 평온을 가져다준다. 사색하기에 완벽한 순간이다.',
'The sacrifice wreath represents our resilience, a tribute to those who fought for us.':'제물 화환은 우리의 회복력을 상징한다. 우리를 위해 싸운 이들에게 바치는 헌사지.',
'The wreath is a beautiful tribute, celebrating lives that soared before us.':'화환은 아름다운 헌사다. 우리보다 먼저 날아간 삶들을 기념하네.',
'Wreath made of cloth and feathersss! Representsss friendship, life, and the circle of nature!':'천이랑 깃털로 만든 화환이다아! 우정과 생명, 자연의 순환을 나타내엇!',
'Solemn. The sacrifice wreath holds deep significance, a reflection of collective memory.':'엄숙함. 제물 화환은 깊은 의미를 지닌다. 집단 기억의 반영이다.',
"This sacred wreath embodies our reverence, a serene reminder of life's fragility.":'이 신성한 화환은 우리의 경외를 담고 있네. 삶의 덧없음을 조용히 일깨워주는군.',
'Even in death, traditions are a hinder to progress.':'죽음에조차 전통은 발전을 가로막는군.',
"Let's never forget our passed ones and honor them.":'떠난 이들을 절대 잊지 말고 기리도록 하자.',
'Floran is curiousss about lost warriors..':'플로란은 떠나간 전사들이 궁금하다아.',
'Solemn. One shall seek the strength and certainty of steel. ':'엄숙함. 강철의 힘과 확실함을 찾아야 한다. ',
'It does remind me the traditions of some old nation on earth..':'지구의 어떤 옛 나라 전통이 생각나네.',
'The funeral rites of a civilization and how they honor their dead says a lot about their society.':'한 문명의 장례 의식과 죽은 이를 기리는 방식은 그 사회에 대해 많은 걸 말해준다.',
"That's quite fancy for the dead, but that feels alright.":'죽은 이 치고 꽤 화려하구만. 그래도 나쁘지 않아.',
'The tribute platter signifies our respect, enriching our connection to those lost.':'공물 쟁반은 우리의 경의를 상징한다. 떠난 이들과의 유대를 깊게 하지.',
'The tribute platter represents our bond beyond the stars, honoring the memories of our kin.':'공물 쟁반은 별 너머까지 이어진 우리의 유대를 나타내. 우리 식구의 기억을 기리는 거야.',
'Platter with fabric and fruits! Honor fallen friends, celebrate their return to nature!':'천이랑 열매가 담긴 쟁반! 쓰러진 친구들을 기리고 자연으로의 귀환을 축하하엇!',
'The tribute platter serves as a vessel of memory, intertwining past with present.':'공물 쟁반은 기억의 그릇 역할을 한다. 과거와 현재를 엮어내는군.',
'The offering signifies purity and reflection, an homage through scents and flavors.':'이 공물은 순수함과 사색을 의미한다. 향기와 맛으로 바치는 헌사지.',
'The aroma of incense mingling with the kiri fruits recalls the warmth of our shared moments.':'향의 향기와 키리 열매가 어우러져 함께한 순간의 따뜻함을 떠올리게 해.',
'Kiri fruits and incenssse! A harmony of life and ssspirit, connecting us to the earth.':'키리 열매랑 향이이! 생명과 영혼의 조화, 우리를 대지와 이어줘엇.',
'The platter serves as a data-link to our memories, encoded in the fragrances and tastes.':'쟁반은 기억으로의 데이터 링크 역할을 한다. 향기와 맛에 부호화되어 있군.',
'The pots of incense and cups unite us, offering a moment of contemplation and connection.':'향 화분과 잔들이 우리를 하나로 묶어준다. 사색과 교감의 순간을 선사하지.',
'The fragrant incense and shared cups evoke the spirit of camaraderie, celebrating our unity.':'향기로운 향과 함께 나누는 잔이 동지애를 불러일으켜. 우리의 결속을 축하하는 거야.',
'Pots and cups! A sssacred gathering of aromas and tassstes, enhancing our bond with nature.':'화분이랑 잔이다아! 향기와 맛의 신성한 모임, 자연과의 유대를 키워줘엇.',
'The pots of incense interface with our memories, while cups enable shared experiences in code.':'향 화분은 우리의 기억과 연결되고, 잔들은 공유된 경험을 코드로 가능하게 한다.',
"Wrapped flowers express honor and reverence, a vibrant tribute to those we've lost.":'포장된 꽃은 명예와 경외를 표현한다. 떠난 이들에게 바치는 생생한 헌사지.',
'These flowers signify our appreciation, a tribute to our ancestors that transcends time.':'이 꽃들은 우리의 감사를 나타내. 시간을 초월해 조상들에게 바치는 헌사야.',
'The bouquet encapsulates emotions, coded in petals—a tangible expression of remembrance.':'꽃다발은 감정을 꽃잎에 부호화해 담아낸다. 추모의 실체적 표현이군.',
'Regional Weaponry':'지역 무기',
'Survival Kit':'생존 키트',
"''The human mind is the next frontier, and we are its pioneers.''":"''인간의 정신이 다음 개척지이며, 우리가 그 개척자다.''",
'A forge for creating equipment out of metal.':'금속으로 장비를 만드는 대장간이다.',
'I can turn ores into good quality equipment from here.':'여기서 광석을 좋은 품질의 장비로 바꿀 수 있네.',
'This replicator enables me to create high quality equipment from good quality materials.':'이 복제기로 좋은 재료를 고품질 장비로 만들 수 있군.',
'An industrial furnace perfect for crafting titanium and other alloys.':'타이타늄과 다른 합금 제작에 완벽한 산업용 용광로다.',
'An industrial furnace, hot enough to smelt titanium and other materials.':'타이타늄과 다른 재료를 제련할 만큼 뜨거운 산업용 용광로다.',
'A very hot, imposing, industrial furnace. I can make stronger materials with this.':'아주 뜨겁고 위압감 있는 산업용 용광로다. 이걸로 더 강한 재료를 만들 수 있다.',
'An atomic furnace. Perfect for making even stronger alloys.':'원자로 용광로다. 더욱 강한 합금을 만들기에 완벽하다.',
'An atomic furnace. This device is powerful enough to create refined ore and alloys.':'원자로 용광로다. 정제 광물과 합금을 만들 만큼 강력한 장치다.',
'An atomic furnace. I can make refined ore and alloys with this.':'원자로 용광로다. 이걸로 정제 광물과 합금을 만들 수 있다.',
'^orange;Hazard Lab Table^white;':'^orange;위험물 실험대^white;',
}

ov={};tot=0
for fn in pk.index:
    if not fn.endswith('.patch'):continue
    try:d=sbjson.parse_sb(pk.read(fn).decode('utf-8-sig'))
    except:continue
    ch=[0]
    def walk(o):
        if isinstance(o,list):
            tests={x.get('path'):x.get('value') for x in o if isinstance(x,dict) and x.get('op')=='test'}
            for x in o:
                if isinstance(x,dict) and x.get('op') in ('replace','add'):
                    p=x.get('path')
                    if p in tests and isinstance(tests[p],str) and tests[p] in FIX and x.get('value')!=FIX[tests[p]]:
                        x['value']=FIX[tests[p]];ch[0]+=1
                elif isinstance(x,(list,dict)):walk(x)
        elif isinstance(o,dict):
            for v in o.values():
                if isinstance(v,(list,dict)):walk(v)
    walk(d)
    if ch[0]:
        ov[fn]=json.dumps(d,ensure_ascii=False,separators=(',',':')).encode('utf-8')
        tot+=ch[0]
        print(fn[-60:],'->',ch[0])
print('files:',len(ov),'ops:',tot)
if '--apply' in sys.argv and ov:
    pak_writer.write_pak(TR+'.staged',TR,ov);del pk
    for i in range(60):
        try:os.replace(TR+'.staged',TR);print('replaced');break
        except PermissionError:time.sleep(5)
