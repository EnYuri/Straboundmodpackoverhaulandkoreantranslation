import csv, glob, re, sys, io, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
TOK = re.compile(r'<[A-Za-z_][A-Za-z0-9_]*>')
KORTOK = re.compile(r'<[가-힣][가-힣0-9_ ]*>')

# Confirmed literal bracketed text (narrative asides / redactions / jokes), not runtime tokens.
KNOWN_LITERAL = {
    '<알 수 없음>', '<알 수 없는 횡설수설>',
    '<동작에 따라 고개를 흔들며 파형을 관찰>', '<막대에 맞춰 감미로운 비트를 쿵쾅거림>',
    '<어둠 속에서 어떤 속삭임이 들린다>', '<소곤소곤 커져가는 소리>',
    '<여기에 대상자 이름을 입력하세요>', '<여기에 겨울왕국 농담을 삽입하세요>',
    '<알 수 없는 아이템>', '<회로 이름>', '<유용한 정보>', '<현상금 이름>', '<아르고 호의 선장>',
}

# <unknown> in FU codex pages is literal redaction text rendered as-is; translating
# it to a Korean bracket is the intended localization, not a token break.
ALLOWED_LOSS = {'<unknown>'}

# Rows whose EN cell is a bare asset path (image specs like "...png:<frame>") hold a
# misaligned leftover KO string; they are known positional-alignment artifacts.
ASSET_EN = re.compile(r'^/[A-Za-z0-9_/.]+\.[a-z]+:')

# Statuses that generate_legacy_overlays.py / apply_alignment_to_unpacked.py emit into
# overlay assets ('aligned-string' covers the fu.tsv patch schema).
MATCHED = {'aligned-string', 'pointer-string', 'patch-key-string', 'patch-index-string'}

# (path/glob, en_col, ko_col). Rows where en_col is empty are KO-bracket-checked only.
# sbkor.tsv is excluded: it is the shipped vanilla Korean and its dropped tokens are upstream choices.
FILES = [
    ('alignment/fu.tsv', 5, 6),
    ('alignment/gic.tsv', 4, 5),
    ('alignment/extended_story.tsv', 4, 5),
    ('alignment/black_armory.tsv', 4, 5),
    ('alignment/noneki.tsv', 4, 5),
    ('translation_memory.tsv', 2, 3),
    ('legacy_translation_memory.tsv', 3, 4),
]

rows = []
for path, ecol, kcol in FILES:
    try:
        data = list(csv.reader(open(path, encoding='utf-8-sig', newline=''), delimiter='\t'))
    except FileNotFoundError:
        continue
    for i, r in enumerate(data):
        if len(r) <= max(ecol, kcol) or ASSET_EN.match(r[ecol]):
            continue
        # Only statuses emitted into overlays by generate_legacy_overlays.py matter here.
        if path.startswith('alignment/') and len(r) > 3 and r[3] not in MATCHED:
            continue
        en_tok = collections.Counter(TOK.findall(r[ecol]))
        ko_tok = collections.Counter(TOK.findall(r[kcol]))
        kor = [t for t in KORTOK.findall(r[kcol]) if t not in KNOWN_LITERAL]
        issues = []
        missing = en_tok - ko_tok
        missing = collections.Counter({t: c for t, c in missing.items() if t not in ALLOWED_LOSS})
        if missing:
            issues.append('lost tokens: ' + ','.join(sorted(missing)))
        if kor:
            issues.append('ko brackets: ' + ','.join(kor))
        if issues:
            rows.append((path, i + 1, '; '.join(issues)))

with open('qa_tokens_report.tsv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['file', 'line', 'issues'])
    w.writerows(rows)
print('affected rows:', len(rows))
print(collections.Counter(r[0] for r in rows))
