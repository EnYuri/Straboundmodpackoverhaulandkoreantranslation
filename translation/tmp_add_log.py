import io

p = 'docs/batch_log.md'
s = open(p, encoding='utf-8').read()
entry = """- 배치 0386(ID 108313~108428, 알타 문서 개요 시리즈 — EDS/ADMU/CEN/에너지원/장비 세트,
  문·드론 묘사) 50개는 구조·용어 QA를 통과했다. `Alternia`→`알테르니아`,
  `Ceterai project`→`세테라이 프로젝트`, `nivera sentia`→`니베라 센티아`,
  `Miara`→`미아라`, `bionical/bionicas`→`바이오니칼/바이오니카`,
  `Archangel Xequeyzriel`→`대천사 세퀘이즈리엘`, `Enviro`→`환경 세트`,
  `ADMU`→`자동 방어 기동 유닛` 적용.
"""
marker = '## 배치 기록 (최신순)\n\n'
assert marker in s
s = s.replace(marker, marker + entry, 1)
open(p, 'w', encoding='utf-8').write(s)

p2 = 'README.md'
s2 = open(p2, encoding='utf-8').read()
s2 = s2.replace('배치 0385 완료 시점', '배치 0386 완료 시점')
s2 = s2.replace('`rest_priority_0385.tsv`', '`rest_priority_0386.tsv`')
s2 = s2.replace('high-priority remaining: 13,879', 'high-priority remaining: 13,829')
s2 = s2.replace('`rest_priority_0386.tsv`부터 이어 간다.', '`rest_priority_0387.tsv`부터 이어 간다.')
open(p2, 'w', encoding='utf-8').write(s2)
print('log+readme updated')
