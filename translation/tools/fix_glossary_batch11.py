"""Eleventh fix batch (2026-09-28). Origin: manual STYLE_MIX review of the
medium-size dialogue assets (allianceoutpost 93, atprk_devouttenant 52,
commands 63, elpissecurity 66, esc_corpus_empolyee 41, ffs_alice/jessie,
hookerconverse 32, lustiahint1converse 12, r-guardiancaptainconverse 9,
r-peacekeeperconverse 71, saturnKytaguard 84, saturnWaspmim 144,
sb_friendlyminer 56, sexbound notifications 41, sgD03MU/merchant 19,
smitewoofie 26, unboundvillagesecurity 65, USCMdisbanded 33, sb_commands 6).

All pairs verified against pak_pairs.tsv before fixing. Highlights:

- Terrene Guardians faction name unified to 가디언즈 (union.codex canonical
  "행성 가디언즈"). 수호자(들)/수호자단/가디언(들) variants were impossible to
  keep because Protector is already fixed to 수호자, producing ambiguous lines
  like "us Guardians" -> "우리 수호자들" read as Protectors.
- Terrene Electorate -> 행성 선거단 (선거단 dominant 13:5; 선거국/지상 선거구
  unified). Follows the union.codex "행성 X" convention (행성 보호국 etc).
- Big Ape -> 빅 에이프 (glossary fixed, leader-name context only): two stray
  큰형님 occurrences fixed.
- Residual Glitch emotion prefixes missed by batch10's violation-file sweep:
  위협적임. (15x, all verified prefix-position), 유혹함. -> 유혹.
- K'Rakoth spelling 크레이코스 -> 크라코스 (3x); K'Rakoth Codex Kappa 카파 ->
  캇파 (glossary fixed 캇파).
- Apiarian 아피어리안 -> 아피아리안 (12:1 dominant).
- commands.config: "I'll get that" -> 가져올게 mistranslation (operate =
  manipulate a switch, not fetch), captain -> 선장님 where 대장 was used for
  the ship captain (boss stays 대장).
- sb_friendlyminer glitch Welcoming prefix was dropped entirely -> restored.
- Assorted register unifications inside single-asset dialogue pools and one
  clause-attachment misreading in r-guardianconverse ("whatever destroyed our
  home" attached to the wrong clause).
"""
import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

BASE = Path(__file__).parent.parent
SRC_PAK = STAR / "mods" / "zz_translation_female.pak"
OUT_PAK = BASE / "female_translation.pak.NEW15"

REPLACEMENTS = [
    # ---- USCMdisbanded ----
    ("우리 형무소 행성행이 될 뻔한 적이 있어", "우리 형벌 식민지행이 될 뻔한 적이 있어"),
    ("USCM이 사라진 게 슬프다고는 말 못 하겠어요. 근데 포로들이 다 어떻게 됐는지는 궁금하네요.",
     "USCM이 사라진 게 슬프다고는 말 못 하겠어. 근데 포로들이 다 어떻게 됐는지는 궁금하네."),

    # ---- allianceoutpost ----
    ("아벤토르 갤리엇", "아벤토르 갈리옷"),

    # ---- corpus-wide residuals ----
    ("위협적임.", "위협."),
    ("크레이코스", "크라코스"),
    ("크라코스 코덱스 카파", "크라코스 코덱스 캇파"),
    ("유혹함.", "유혹."),

    # ---- commands.config ----
    ("이 구역을 안전하게 확보하겠습니다, 대장.", "이 구역을 안전하게 확보하겠습니다, 선장님."),
    ("그거 내가 가져올게.", "그건 내가 처리할게."),
    ("그거 대신 가져다줄게.", "그건 내가 대신 처리해줄게."),
    # "Don't mind if I do!" is used for both lounge rest and cooking stations;
    # keep a context-neutral idiom
    ("내가 해도 상관없어요!", "마다할 이유 없지!"),

    # ---- hookerconverse ----
    ("네 몸매가 정말 멋지다고 말하면, 날 원망할 거야?",
     "네 몸매가 멋지다고 말하면, 날 꽉 안아줄 거야?"),

    # ---- lustiahint1converse (register unified to the file's casual tone) ----
    ("안녕하세요! 러스티아에 오신 걸 환영해요! 섹시하고 흥분되는 모든 것의 메트로폴리스죠!",
     "안녕! 러스티아에 온 걸 환영해! 섹시하고 흥분되는 모든 것의 메트로폴리스야!"),
    ("도시의 웅장한 중심축이야", "도시의 거대한 대물이야"),
    ("본탑 옆에, 저희 동물학자가 있어요. 어떤 분들은 몬스터랑 하는 걸 더 좋아하는데, 그것도 괜찮아요! 그녀는 야릇한 재미를 위한 길들인 반려동물을 제공해요.",
     "본탑 옆에는 우리 동물학자가 있어. 어떤 이들은 몬스터랑 하는 걸 더 좋아하는데, 그것도 괜찮아! 그녀가 야릇한 재미를 위한 길들인 반려동물을 제공하지."),

    # ---- Terrene Guardians faction -> 가디언즈 / Electorate -> 선거단 ----
    ("테린 수호자 선장으로서", "행성 가디언즈 선장으로서"),
    ("수호자단의 대장으로서, 나는 이렇게 끔찍한 일은 처음 겪는다.",
     "가디언즈의 선장으로서, 나는 이렇게 끔찍한 일은 처음 겪는다."),
    ("가디언이 조종사 훈련을 가르쳐준다는 게", "가디언즈가 조종사 훈련을 가르쳐준다는 게"),
    ("수호자단의 대장으로 사는 건", "가디언즈의 선장으로 사는 건"),
    ("일 하려고 가디언에 들어온 게", "일 하려고 가디언즈에 들어온 게"),
    ("선거국에 남은 건 우리 수호자들뿐인 줄", "선거단에 남은 건 우리 가디언즈뿐인 줄"),
    ("행성 가디언이 봉사하러 왔습니다", "행성 가디언즈가 봉사하러 왔습니다"),
    ("가디언들이 우리 고향을 파괴한 게 뭐든, 전성기였다 해도 맞설 수 있었을지 의심스러워. 누구라도 그럴 수 있었을지 의심스러워.",
     "우리 고향을 파괴한 게 뭐든, 전성기의 가디언즈도 맞설 수 있었을지 의심스러워."),
    ("우리 가디언들도 난민이나", "우리 가디언즈도 난민이나"),
    ('더 이상 "행성" 가디언이 아니겠지', '더 이상 "행성" 가디언즈가 아니겠지'),
    ("가디언들이 무너지기도 전에", "가디언즈가 무너지기도 전에"),
    ("가디언의 자랑스러운 상징을 담은 스티커", "가디언즈의 자랑스러운 상징을 담은 스티커"),
    ("행성 수호자 스티커", "행성 가디언즈 스티커"),
    ("수호자들에서 복무한 이들을", "가디언즈에서 복무한 이들을"),
    ("테렌 가디언즈", "행성 가디언즈"),
    ("행성 수호자 로고를 본떠", "행성 가디언즈 로고를 본떠"),
    ("행성 가디언 등", "행성 가디언즈 등"),
    ("행성 선거국", "행성 선거단"),
    ("테레네 선거국", "행성 선거단"),
    ("지상 선거구", "행성 선거단"),
    ("선거국", "선거단"),
    ("행성 수호자들과 함께", "행성 가디언즈와 함께"),

    # ---- Big Ape (glossary fixed: leader name only) ----
    ("위대한 큰형님 만세!", "빅 에이프 만세!"),
    ("큰형님 정권이", "빅 에이프 정권이"),

    # ---- saturnWaspmim ----
    ("아피어리안은", "아피아리안은"),
    ("쥐이잉! 배신자! 쥐이잉!", "윙윙! 배신자! 윙윙!"),

    # ---- sb_friendlyminer (dropped Glitch prefix restored) ----
    ("광석을 찾으면 너와 좀 나누고 싶어.", "환영. 광석을 찾으면 너와 좀 나누고 싶어."),

    # ---- r-peacekeeperconverse: Officer -> 경관 unification ----
    ("<selfname> 장교다! 보호하러", "<selfname> 경관이다! 보호하러"),
    ("보안관이야. 선장님을 도와", "경관이야. 선장님을 도와"),

    # ---- penal colony -> 형벌 식민지 (residual) ----
    ("형무소 행성", "형벌 식민지"),
]

print("total replacement pairs:", len(REPLACEMENTS))


def _vlqr(buf, p):
    # MSB-first base-128 varint, matching pak.py rvu()
    v = 0
    while True:
        b = buf[p]
        p += 1
        v = (v << 7) | (b & 0x7F)
        if not (b & 0x80):
            return v, p


def vlq(v):
    # MSB-first base-128 varint, matching pak.py rvu() (no zigzag)
    stack = []
    while True:
        stack.append(v & 0x7F)
        v >>= 7
        if not v:
            break
    out = bytearray()
    for i, b in enumerate(reversed(stack)):
        out.append(b | 0x80 if i < len(stack) - 1 else b)
    return bytes(out)


def _key(buf, p):
    n, p = _vlqr(buf, p)
    return p + n


def _rjson_skip(buf, p):
    t = buf[p]
    p += 1
    if t == 1:
        return p
    if t == 2:
        return p + 8
    if t == 3:
        return p + 1
    if t == 4:
        _, p = _vlqr(buf, p)
        return p
    if t == 5:
        n, p = _vlqr(buf, p)
        return p + n
    if t == 6:
        n, p = _vlqr(buf, p)
        for _ in range(n):
            p = _rjson_skip(buf, p)
        return p
    if t == 7:
        n, p = _vlqr(buf, p)
        for _ in range(n):
            p = _key(buf, p)
            p = _rjson_skip(buf, p)
        return p
    raise ValueError("bad json type %d at %d" % (t, p))


def replace_in_value(v):
    if isinstance(v, str):
        changed = False
        for old, new in REPLACEMENTS:
            if old in v:
                v = v.replace(old, new)
                changed = True
        return v, changed
    if isinstance(v, list):
        out = []
        changed = False
        for x in v:
            x, c = replace_in_value(x)
            out.append(x)
            changed = changed or c
        return out, changed
    if isinstance(v, dict):
        out = {}
        changed = False
        for k, x in v.items():
            x, c = replace_in_value(x)
            out[k] = x
            changed = changed or c
        return out, changed
    return v, False


def main():
    d0 = SRC_PAK.read_bytes()
    off0 = struct.unpack(">Q", d0[8:16])[0]
    assert d0[off0:off0 + 5] == b"INDEX"
    p = off0 + 5
    nmeta, p = _vlqr(d0, p)
    for _ in range(nmeta):
        p = _key(d0, p)
        p = _rjson_skip(d0, p)
    meta_blob = d0[off0:p]

    src = Pak(str(SRC_PAK))
    files = {name: src.read(name) for name in src.index}
    print("base pak entries:", len(files))

    # needles must match the raw (JSON-escaped) bytes inside .patch files
    needles = [json.dumps(old, ensure_ascii=False)[1:-1].encode("utf-8")
               for old, _ in REPLACEMENTS]
    # verify each needle exists in the source before rewriting
    for old, needle in zip([r[0] for r in REPLACEMENTS], needles):
        if not any(needle in files[n] for n in files if n.endswith(".patch")):
            print("NEEDLE-MISS (source):", old[:80])
    assets_changed = 0
    for name in sorted(files):
        if not name.endswith(".patch"):
            continue
        data = files[name]
        if not any(n in data for n in needles):
            continue
        try:
            doc = json.loads(data)
        except Exception:
            continue
        new_doc, changed = replace_in_value(doc)
        if changed:
            files[name] = json.dumps(new_doc, ensure_ascii=False).encode("utf-8")
            assets_changed += 1
            print("fixed", name)

    buf = bytearray(b"SBAsset6" + b"\x00" * 8)
    index_entries = []
    for name in sorted(files):
        data = files[name]
        off = len(buf)
        buf += data
        index_entries.append((name.encode("utf-8"), off, len(data)))

    index_off = len(buf)
    buf += meta_blob
    buf += vlq(len(index_entries))
    for name, off, n in index_entries:
        buf += vlq(len(name)) + name + struct.pack(">QQ", off, n)
    buf[8:16] = struct.pack(">Q", index_off)

    OUT_PAK.write_bytes(bytes(buf))
    print("assets changed:", assets_changed)
    print("wrote", OUT_PAK, len(buf), "bytes,", len(index_entries), "entries")


if __name__ == "__main__":
    main()
