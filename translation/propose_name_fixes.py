"""Generate fix proposals for name-consistency flags (v3).

Reads name_refs_missing.tsv / name_refs_variant.tsv written by
scan_name_consistency.py v3 (ko_expected / ko_target are already resolved
per-row, including AMB path-similarity picks and glossary/overrides).

Works on the RAW Korean text: a clean-text view with a char->raw index map,
so ^color; tags and newlines are preserved untouched.

Per flag:
  VARIANT  - KO already contains a registered non-target variant string:
             splice that substring out, splice target in (+particle repair).
  TSPAN    - the name sits inside a ^color;...^reset; span: replace the
             span's inner name words (keeping counts/punctuation).
  WORD     - free text: locate span by target-token anchors, extend over
             adjacent noun-words, then positional word-diff inside the span.
  NONE     - cannot locate a divergent rendering (paraphrase) -> review.
  REVIEW   - low-confidence flag (single common word / unresolved AMB).
  JUNKCANON- target itself looks like prose, not a name -> review.

Output: name_fix_proposals.tsv
"""
import csv
import re
from collections import Counter
from pathlib import Path

BASE = Path(__file__).parent
csv.field_size_limit(10_000_000)

TAG_RE = re.compile(r"\^[A-Za-z0-9#]*;")
KO_RE = re.compile(r"[가-힣]")
WORD_RE = re.compile(r"\S+")

# tokens that must never be rewritten/dropped by name replacement:
# digits, percents, counts ('5개', 'x3'), and list connectors ('얼음 및 독 저항')
FROZEN_RE = re.compile(r"^[\d%.,xX]+$|^\d+\s*개$|^x\s*\d+$")
# signed/percent/multiplier numbers are stat values ('+120', '15%', 'x1.15');
# the word right before one is a stat label, never a name variant
STAT_RE = re.compile(r"^[+−\-~][\d.,]+%?$|^[\d.,]+%$|^[xX][\d.,]+$")
CONNECTORS = {"및", "그리고", "또는", "혹은", "와", "과", "또", "등", "또한"}
TRAIL_PUNCT = ".,!?…:;'\"”’)]}»〔〉》"
# dual-particle template notation '은(는)', '이(가)' - jong form first
DUAL_TAIL = re.compile(r"(은|이|을|과|으로)\((는|가|을|와|로)\)?$")


def frozen(w):
    t = w.strip(TRAIL_PUNCT)
    return not KO_RE.search(t) or bool(FROZEN_RE.match(t)) or t in CONNECTORS

# postposition syllables that may terminate a name's last word; multi-char
# compounds are tried first so '스테이션에서는' splits as +'에서는'
PARTICLES = ("에서는", "에게서", "으로는", "로는", "에는", "에서도", "로도",
             "으로도", "로서", "으로서", "에게는", "한테는", "부터는",
             "까지는", "조차도", "조차", "이라도", "라도", "밖에",
             "에게", "한테", "에서", "으로", "로", "은", "는", "이", "가",
             "을", "를", "과", "와", "도", "만", "의", "에", "께", "보다",
             "처럼", "까지", "부터", "랑", "이랑", "하고", "이고")


def strip_tags(s):
    return TAG_RE.sub("", s)


def has_jong(ch):
    return "가" <= ch <= "힣" and (ord(ch) - 0xAC00) % 28 != 0


def clean_with_map(s):
    """Return (clean_text, map) where map[i] = raw offset of clean char i."""
    out, m = [], []
    i = 0
    while i < len(s):
        mm = TAG_RE.match(s, i)
        if mm:
            i = mm.end()
            continue
        out.append(s[i])
        m.append(i)
        i += 1
    return "".join(out), m


def raw_start(cmap, cpos):
    return cmap[cpos]


def raw_end(cmap, cend):
    """Raw offset just past clean char at index cend-1 (keeps trailing tags)."""
    return cmap[cend - 1] + 1


# particles that are also common word-final syllables (adnominals '검은',
# names ending in 로/과/도 like '용광로') - they split only when the stem
# keeps >=2 syllables; '을/를' and multi-char particles are unambiguous
AMBIG_PARTICLES = {"은", "는", "이", "가", "에", "의", "로", "와", "과",
                   "나", "도", "만", "께", "랑", "이랑", "로", "조차",
                   "라도", "밖에"}


def split_particle(word):
    """'반지를' -> ('반지','를'); '장치)는' -> ('장치',')는');
    '스테이션에서는' -> ('스테이션','에서는'); '반응로' -> ('반응','로').

    Strips trailing punctuation and postpositions repeatedly (max 2).
    Ambiguous particles (AMBIG_PARTICLES) require a >=2-syllable stem so
    '사이', '정도', '검은' stay intact. Callers that need certainty should
    also compare the unstripped word - '반응로' may be a whole name."""
    w = word
    trail = ""
    splits = 0
    while splits < 2:
        while w and w[-1] in TRAIL_PUNCT:
            trail = w[-1] + trail
            w = w[:-1]
        # '발사기은(는)' -> ('발사기', '은(는)') - template kept whole
        dm = DUAL_TAIL.search(w)
        if dm and len(w) - len(dm.group(0)) >= 1:
            return w[:dm.start()], w[dm.start():] + trail
        found = None
        for p in sorted(PARTICLES, key=len, reverse=True):
            need = 2 if p in AMBIG_PARTICLES else 1
            if w.endswith(p) and len(w) - len(p) >= need:
                found = p
                break
        if found is None:
            return w, trail
        trail = found + trail
        w = w[:-len(found)]
        splits += 1
    return w, trail


def ends_with_particle(word):
    stem, tail = split_particle(word)
    return bool(tail)


def lone_particle(word):
    """'를', '의' standing alone as a word: a clause boundary, not content."""
    return word.strip(TRAIL_PUNCT) in PARTICLES


def dice(a, b):
    def bg(s):
        s = s.replace(" ", "")
        return Counter(s[i:i + 2] for i in range(len(s) - 1))
    A, B = bg(a), bg(b)
    if not A or not B:
        return 0.0
    inter = sum((A & B).values())
    return 2 * inter / (sum(A.values()) + sum(B.values()))


# ---- particle repair -------------------------------------------------------

JONG_PAIRS = {"은": "는", "이": "가", "을": "를", "과": "와", "으로": "로"}
NOJONG_PAIRS = {"는": "은", "가": "이", "를": "을", "와": "과", "로": "으로"}
ALL_ALT = sorted(set(JONG_PAIRS) | set(NOJONG_PAIRS), key=len, reverse=True)


def alt_particle(p, want_jong):
    """Map particle `p` to its counterpart for the requested 받침 state."""
    if want_jong and p in NOJONG_PAIRS:
        return JONG_PAIRS_VALUE(p)
    if not want_jong and p in JONG_PAIRS:
        return JONG_PAIRS[p]
    return p


def JONG_PAIRS_VALUE(p):
    # inverse lookup not needed: NOJONG->JONG mapping is fixed
    return {"는": "은", "가": "이", "를": "을", "와": "과", "로": "으로"}.get(p, p)


def fix_particle_in_tail(stem_new, tail):
    """Given replacement stem `stem_new` and a `tail` that may begin with an
    alternating particle (e.g. '을.', '으로') or a dual-particle template
    ('은(는)'), return repaired tail."""
    dm = re.match(r"(은|이|을|과|으로)\((는|가|을|와|로)\)", tail)
    if dm and stem_new:
        jp, np_ = dm.group(1), dm.group(2)
        if has_jong(stem_new[-1]):
            return tail
        return np_ + "(" + jp + ")" + tail[dm.end():]
    for p in ALL_ALT:
        if tail.startswith(p):
            want = has_jong(stem_new[-1]) if stem_new else False
            if p in JONG_PAIRS and not want:
                return JONG_PAIRS[p] + tail[len(p):]
            if p in NOJONG_PAIRS and want:
                return JONG_PAIRS_VALUE(p) + tail[len(p):]
            return tail
    return tail


def repair_following_particle(raw, insert_end_raw, canon):
    """After splicing `canon` ending at raw offset insert_end_raw, if the next
    syllable is a particle whose 받침 requirement mismatches canon's last
    char, swap it."""
    last = canon.rstrip()[-1:] if canon.strip() else ""
    if not last or not ("가" <= last <= "힣"):
        return raw
    tail = raw[insert_end_raw:]
    fixed = fix_particle_in_tail(canon.rstrip(), tail)
    if fixed != tail:
        return raw[:insert_end_raw] + fixed
    return raw


# ---- span location ---------------------------------------------------------

def words_of(clean):
    return [(m.start(), m.end(), m.group(0)) for m in WORD_RE.finditer(clean)]


def align_diff(clean, canon):
    """Alignment-driven name replacement in clean text.

    Aligns canon tokens to KO words by substring containment ('전초기지는'
    covers canon '전초' and '기지'). Unaligned canon tokens are paired 1:1
    with unaligned KO words at the same name position (head/middle/tail);
    trailing particles on replaced words are repaired. Pure inserts are only
    allowed when the neighbouring word clearly terminates the name region
    (frozen token or particle-ended word). Returns (cstart, cend, new_text)
    or None when the shape is too ambiguous to touch safely.
    """
    ws = words_of(clean)
    kw = [w for _, _, w in ws]
    cw = canon.split()
    if not kw or not cw:
        return None

    def tok_claim(tok, w):
        # single-syllable tokens ('자') only claim an exact word stem -
        # substring matching lets '자' land inside '자라나는'
        if len(tok) == 1:
            return split_particle(w)[0] == tok
        return tok in w

    # align each canon token to the first unclaimed word containing it;
    # a second pass lets one word cover several canon tokens ('전초기지는'
    # covers '전초' and '기지') so merged compounds are recognised as
    # aligned instead of leaking the diff into neighbouring words
    atok = {}
    used = set()
    for ci, tok in enumerate(cw):
        for wi, w in enumerate(kw):
            if wi not in used and tok_claim(tok, w):
                atok[ci] = wi
                used.add(wi)
                break
    for ci, tok in enumerate(cw):
        if ci in atok:
            continue
        for wi, w in enumerate(kw):
            if tok_claim(tok, w):
                atok[ci] = wi
                break
    if not atok or sorted(atok.values()) != [atok[c] for c in sorted(atok)]:
        # no anchor or reordered name: accept only an exact stem-multiset
        # window ('펠리노어 고대 도시에' ~ '고대 도시 펠리노어')
        stems = [split_particle(w)[0] for w in kw]
        n = len(cw)
        for i in range(len(kw) - n + 1):
            if Counter(stems[i:i + n]) == Counter(cw):
                return (ws[i][0], ws[i + n - 1][0] + len(stems[i + n - 1]),
                        " ".join(cw))
        return None
    claimed = set(atok.values())
    covers = {}
    for c, p in atok.items():
        covers.setdefault(p, []).append(c)
    # a claimed word whose stem is more than its covered canon tokens is a
    # merged/variant form ('갑옷제작소' covering only '제작') - unless it
    # carries latin chars/parens, which are acronym prefixes to keep
    dirty = {}
    for wi, cs in covers.items():
        stem, _ = split_particle(ws[wi][2])
        concat = "".join(cw[c] for c in sorted(cs))
        # a claimed word is clean if EITHER the whole word or its stripped
        # stem equals the covered tokens - '반응로' is a whole name, while
        # '역마차로' is '역마차'+로
        cands = {re.sub(r"[^가-힣]", "", ws[wi][2].rstrip(TRAIL_PUNCT)),
                 re.sub(r"[^가-힣]", "", stem)}
        if concat in cands or re.search(r"[A-Za-z0-9(]", ws[wi][2]):
            continue
        # plural-generic ('몬스터들' for 'The monster') or separator-joined
        # list words ('총기·화살제작') are prose, not name variants - bail
        if concat + "들" in cands or "·" in ws[wi][2] or "/" in ws[wi][2]:
            return None
        dirty[wi] = sorted(cs)
    ac = sorted(atok)
    c_first, c_last = ac[0], ac[-1]
    w_first, w_last = atok[c_first], atok[c_last]
    missing = [c for c in range(len(cw)) if c not in atok]

    # words directly followed by a stat value ('체력 +120') are stat labels;
    # excluding them from extras stops them being claimed as name variants
    statlab = {i for i in range(len(kw) - 1)
               if STAT_RE.match(kw[i + 1].strip(TRAIL_PUNCT))}

    l_ex = []
    j = w_first - 1
    while j >= 0 and j not in claimed and j not in statlab \
            and not frozen(ws[j][2]) and not ends_with_particle(ws[j][2]) \
            and not lone_particle(ws[j][2]):
        l_ex.insert(0, j)
        j -= 1
    r_ex = []
    j = w_last + 1
    while j < len(kw) and j not in claimed and j not in statlab:
        # a token that is frozen after its particle is stripped ('2개가' ->
        # '2개') or a lone particle ('를', '의') is a boundary: stop without
        # claiming it
        if frozen(ws[j][2]) or frozen(split_particle(ws[j][2])[0]) \
                or lone_particle(ws[j][2]):
            break
        r_ex.append(j)
        if ends_with_particle(ws[j][2]):
            break
        j += 1
    inner_ex = [i for i in range(w_first, w_last + 1)
                if i not in claimed and i not in statlab
                and not frozen(ws[i][2]) and not lone_particle(ws[i][2])]
    extras = l_ex + inner_ex + r_ex

    def slot(c):
        L = max((atok[x] for x in atok if x < c), default=-1)
        R = min((atok[x] for x in atok if x > c), default=len(kw))
        return L, R

    emits = {wi: set(cs) for wi, cs in dirty.items()}
    assign = {}
    ins_head, ins_tail = [], []
    slots = {}
    for c in missing:
        slots.setdefault(slot(c), []).append(c)
    for (L, R), cs in slots.items():
        dirt = [wi for wi in emits if L <= wi <= R]
        if dirt:
            emits[dirt[0]] |= set(cs)
            continue
        ex = [i for i in extras if L < i < R]
        if len(ex) > len(cs):
            return None
        # an extra word joined to a list separator is a list item, not a
        # name variant - '눈, 얼음, 슬러시' must not turn '슬러시' into
        # '저항'
        for i in ex:
            if "/" in kw[i] or "·" in kw[i] or kw[i].endswith(",") \
                    or (i > 0 and (kw[i - 1].endswith(",")
                                   or kw[i - 1].endswith("/"))):
                return None
        for c, i in zip(cs, ex):
            assign[i] = c
        leftover = cs[len(ex):]
        if leftover:
            if L == -1:
                ins_head += leftover
            elif R == len(kw):
                ins_tail += leftover
            else:
                return None  # insertion between two words is unsafe
    if ins_head or ins_tail:
        # pure insertion needs a HARD boundary on the outer side: a word
        # ending in punctuation or a frozen token. A bare particle ('는',
        # '을') on the inner side is enough.
        def hard(w):
            tail = split_particle(w)[1]
            return frozen(w) or any(ch in TRAIL_PUNCT for ch in tail)

        before_ok = w_first == 0 or (hard(ws[w_first - 1][2])
                                     if ins_head
                                     else ends_with_particle(ws[w_first - 1][2])
                                     or frozen(ws[w_first - 1][2]))
        after_ok = w_last == len(kw) - 1 or (hard(ws[w_last + 1][2])
                                             if ins_tail
                                             else
                                             ends_with_particle(ws[w_last + 1][2])
                                             or frozen(ws[w_last + 1][2]))
        if not (before_ok and after_ok):
            return None
        # inserting a rank-prefixed canon when the boundary word is also a
        # rank word duplicates the title ('지휘관 안드로스 갈바넥 사령관')
        RANK_END = "관장령사왕님"
        if ins_head and w_last < len(kw) - 1:
            nxt = split_particle(kw[w_last + 1])[0]
            if cw[ins_head[-1]].endswith(tuple(RANK_END)) \
                    and nxt.endswith(tuple(RANK_END)):
                return None
        if ins_tail and w_first > 0:
            prv = split_particle(kw[w_first - 1])[0]
            if cw[ins_tail[-1]].endswith(tuple(RANK_END)) \
                    and prv.endswith(tuple(RANK_END)):
                return None
    if not assign and not ins_head and not ins_tail and not any(
            len(emits[wi]) != len(dirty[wi]) for wi in emits):
        return None  # canon tokens all present already

    # if a dirty word absorbed missing tokens, adjacent leftover extras are
    # likely modifiers of the OLD name ('극심한 열기' -> would emit
    # '극한 열' but keep '극심한' beside it) - too tangled, reject
    if emits:
        leftover_extras = [i for i in extras if i not in assign]
        if any(abs(i - wi) == 1 for wi in emits for i in leftover_extras):
            return None

    lo = min([w_first] + [i for i in assign])
    hi = max([w_last] + [i for i in assign])
    lo = min([lo] + [wi for wi in emits])
    hi = max([hi] + [wi for wi in emits])
    # hi_is_name: the last word IS exactly its covered tokens ('반응로' ==
    # '반응로'), so the span must end at the word end, not at a stripped
    # stem that would orphan a name-final particle syllable ('로')
    hi_cov = set(covers.get(hi, []))
    if hi in assign:
        hi_cov.add(assign[hi])
    if hi in emits:
        hi_cov |= emits[hi]
    hi_is_name = hi_cov and re.sub(r"[^가-힣]", "",
                                   kw[hi].rstrip(TRAIL_PUNCT)) == \
        "".join(cw[c] for c in sorted(hi_cov))
    # the span's last word emits only its stem; its particle (if any) lives
    # outside the replaced text and is fixed by repair_following_particle.
    # this keeps tag boundaries ('유물^reset;과') out of the splice.
    # leading non-word chars on the first word ("''보호국은") wrap the name,
    # not the name itself - keep them outside the splice content
    lead_punct = ""
    m = re.match(r"^[^가-힣A-Za-z0-9^]+", kw[lo])
    if m:
        lead_punct = m.group(0)

    parts = []
    if ins_head:
        parts.append(" ".join(cw[c] for c in ins_head))
    for i in range(lo, hi + 1):
        last = (i == hi)
        if i in emits:
            t = " ".join(cw[c] for c in sorted(emits[i]))
        elif i in assign:
            t = cw[assign[i]]
        else:
            t = kw[i].rstrip(TRAIL_PUNCT) if last and hi_is_name \
                else (split_particle(kw[i])[0] if last else kw[i])
        if i == lo:
            t = t[len(lead_punct):] if t.startswith(lead_punct) else t
        if not last and (i in assign or i in emits):
            t += fix_particle_in_tail(split_particle(t)[0],
                                      split_particle(kw[i])[1])
        parts.append(t)
    if ins_tail:
        parts.append(" ".join(cw[c] for c in ins_tail))
    if parts:
        parts[0] = lead_punct + parts[0]
    if hi_is_name:
        end_txt = kw[hi].rstrip(TRAIL_PUNCT)
    else:
        end_txt = split_particle(kw[hi])[0]
    return (ws[lo][0], ws[hi][0] + len(end_txt), " ".join(parts))


def tag_spans_raw(raw):
    """Yield (inner_start, inner_end) for each ^...; span in RAW text.
    Inner text runs until the next ^ tag or newline. Spans opened by
    ^reset; are plain prose, not name spans - skipped."""
    for m in re.finditer(r"\^([A-Za-z0-9#]*);", raw):
        if m.group(1).lower() == "reset":
            continue
        s = m.end()
        j = s
        while j < len(raw) and raw[j] not in "^":
            if raw[j] == "\n":
                break
            j += 1
        yield s, j


def propose_missing(ko, canon):
    # sentence-final punctuation on the canonical ('이끼 낀 돌무더기.') would
    # double with the text's own period; names never carry it
    canon = canon.strip().rstrip(".!?…")
    if not canon:
        return ("NONE", 0, "", ko)
    clean, cmap = clean_with_map(ko)

    # A) tag-span: name inside ^color;...^reset; style spans. When several
    # spans could host the name, pick the one most similar to the canon -
    # '포도 매쉬' ~ '포도 매시' beats bare '포도' (grapes).
    best = None
    for s_raw, e_raw in tag_spans_raw(ko):
        seg = ko[s_raw:e_raw]
        inner = seg.strip()
        if not inner:
            continue
        inner_txt = re.sub(r"\d+\s*(?:개|x|X)\b|x\s*\d+|\d+\s*x", "", inner).strip()
        # generous cap: align_diff returns a tight window anyway, and names
        # sit inside longer colored phrases ('그 탑에 사는 대마법사, 빈더밀')
        if len(inner_txt.split()) > max(len(canon.split()) + 3, 7):
            continue
        res = align_diff(inner, canon)
        if res is None:
            continue
        ls, le, ntxt = res
        sc = dice(inner_txt, canon)
        if best is None or sc > best[0]:
            best = (sc, s_raw, e_raw, seg, inner, res)
    if best is not None:
        sc, s_raw, e_raw, seg, inner, res = best
        ls, le, ntxt = res
        lead = len(seg) - len(seg.lstrip())
        rs = s_raw + lead + ls
        re_ = s_raw + lead + le
        new = ko[:rs] + ntxt + ko[re_:]
        lastw = split_particle(ntxt.strip().split()[-1])[0]
        new = repair_following_particle(new, rs + len(ntxt), lastw)
        return ("TSPAN", sc, inner, new)

    # B) free-text span via token alignment
    res = align_diff(clean, canon)
    if res:
        s, e, txt = res
        sc = dice(clean[s:e], canon)
        rs, re_ = cmap[s], raw_end(cmap, e)
        new = ko[:rs] + txt + ko[re_:]
        lastw = split_particle(txt.strip().split()[-1])[0]
        new = repair_following_particle(new, rs + len(txt), lastw)
        return ("WORD", sc, clean[s:e], new)
    return ("NONE", 0, "", ko)


VERB_ENDINGS = ("세요", "하세요", "합시다", "봅시다", "입니다", "습니다",
                "해요", "이다", "했다", "한다", "됩니다", "해라", "어라",
                "것이다", "된다", "있어", "없어", "해줘", "주세요",
                "다고", "는데", "지만", "어요", "아요", "잖아", "거든",
                "지마", "해야", "하자", "할게", "할까", "해봐", "가봐",
                "보세요", "보자", "하겠", "겠어", "란다", "구나", "구만",
                "더라", "더군", "십니다", "옵니다", "어서", "이에요", "예요")


def bounded_variant(ko, v, target):
    """Word-boundary aware variant replacement: '철괴' must not match inside
    '철괴뭉치'; a particle tail right after the variant is allowed. Returns
    the repaired text or None when no safe occurrence exists."""
    clean, cmap = clean_with_map(ko)
    start = 0
    while True:
        pos = clean.find(v, start)
        if pos < 0:
            return None
        nxt = clean[pos + len(v):pos + len(v) + 1]
        prev = clean[pos - 1:pos]
        if prev and prev in "-/·_":
            start = pos + 1       # inside a longer compound ('인스타-프로이트')
            continue
        if (not prev or not ("가" <= prev <= "힣")) and \
                (not nxt or not ("가" <= nxt <= "힣")
                 or any(nxt == p[:1] for p in PARTICLES)):
            rs, re_ = cmap[pos], raw_end(cmap, pos + len(v))
            new = ko[:rs] + target + ko[re_:]
            return repair_following_particle(new, rs + len(target), target)
        start = pos + 1


def junk_target(canon):
    # '또는'/length catch prose canons; trailing 은/는/을/를/의 catches a glued
    # particle (names legitimately end in 이/가/에 so those are excluded).
    # >5 tokens or a verb ending means the 'canonical' is a sentence, not a
    # name ('꿀벌과 관련된 모든 종류의 아이템을 만들어 보세요')
    c = canon.rstrip()
    return (not c or "또는" in c or len(c) > 40 or len(c.split()) > 5
            or c.endswith(("은", "는", "을", "를", "의"))
            or any(c.endswith(v) for v in VERB_ENDINGS))


def main():
    # en_names a human approved after reviewing the REVIEW tier - these get
    # a real align_diff pass instead of being parked. The variant-side list
    # is separate: generic-word names (Soldier, Medic) are safe only where a
    # known variant string already exists, never for missing-name insertions.
    def load_names(fn):
        p = BASE / fn
        if not p.exists():
            return set()
        return {ln.strip().lower() for ln in
                p.read_text(encoding="utf-8-sig").splitlines()
                if ln.strip() and not ln.startswith("#")}
    approved = load_names("approved_names.txt")
    approved_var = load_names("approved_ambvar.txt")

    # extra_variants.tsv: human-curated transliteration/spelling variants
    # that never appear in a name field, so the registry can't see them
    # ('오르바이드' for 'Orbide'/'오바이드'). Columns: en_name, variant_ko.
    extra_variants = {}
    evp = BASE / "extra_variants.tsv"
    if evp.exists():
        for r in csv.DictReader(evp.open(encoding="utf-8-sig"),
                                delimiter="\t"):
            extra_variants.setdefault(r["en_name"].strip().lower(),
                                      []).append(r["variant_ko"].strip())

    flags = []
    for fn, kind in [("name_refs_missing.tsv", "missing"),
                     ("name_refs_variant.tsv", "variant")]:
        for r in csv.DictReader((BASE / fn).open(encoding="utf-8-sig"), delimiter="\t"):
            flags.append((kind, r))

    out = []
    for kind, r in flags:
        nm, ko = r["en_name"], r["korean"]
        target = strip_tags(r.get("ko_target") or r.get("ko_expected") or "").strip()
        variants = [v.strip() for v in (r.get("ko_variants") or "").split("|") if v.strip()]
        amb = r.get("amb", "")
        if junk_target(target):
            out.append([r.get("pak", ""), r["asset"], r["pointer"], nm, target,
                        "JUNKCANON", "0", "", ko, ko, amb])
            continue
        if kind == "variant":
            clean_ko = strip_tags(ko)
            used = sorted((v for v in variants if v != target and v in clean_ko),
                          key=len, reverse=True)
            if not used:
                out.append([r.get("pak", ""), r["asset"], r["pointer"], nm, target,
                            "VNONE", "0", "", ko, ko, amb])
                continue
            v = used[0]
            new = bounded_variant(ko, v, target)
            if new is None:
                out.append([r.get("pak", ""), r["asset"], r["pointer"], nm, target,
                            "VNONE", "0", "", ko, ko, amb])
                continue
            method = "VARIANT" if amb != "?" else "AMBVAR"
            vd, td = v.replace(" ", ""), target.replace(" ", "")
            if method == "AMBVAR" and nm.lower() in approved_var:
                method = "VARIANT"  # canon verified by manual inspection
            elif method == "AMBVAR" and dice(v, target) >= 0.7 \
                    and (vd not in td or vd == td):
                # near-identical spelling variants unify harmlessly even
                # when the EN name is ambiguous ('매싱튠'~'매싱 튠').
                # strict-substring growth ('곡괭이'->'철 곡괭이') adds a
                # modifier, so it still needs review; equal-despace is a
                # pure spacing fix ('빈티지 저격 소총'->'빈티지 저격소총')
                method = "VARIANT"
            out.append([r.get("pak", ""), r["asset"], r["pointer"], nm, target,
                        method, "1.0", v, new, ko, amb])
        else:
            # curated unregistered variants ('모파이트' for Morphite) get a
            # bounded VARIANT fix even when the flag itself is REVIEW tier
            for ev in extra_variants.get(nm.lower(), ()):
                new = bounded_variant(ko, ev, target)
                if new and new != ko:
                    out.append([r.get("pak", ""), r["asset"], r["pointer"],
                                nm, target, "VARIANT", "1.0", ev, new, ko,
                                amb])
                    break
            else:
                if (r.get("tier") == "REVIEW" or amb == "?") \
                        and nm.lower() not in approved:
                    out.append([r.get("pak", ""), r["asset"], r["pointer"],
                                nm, target, "REVIEW", "0", "", ko, ko, amb])
                    continue
                method, sc, span, new = propose_missing(ko, target)
                out.append([r.get("pak", ""), r["asset"], r["pointer"], nm,
                            target, method, f"{sc:.2f}", span, new, ko, amb])
            continue

    with (BASE / "name_fix_proposals.tsv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["pak", "asset", "pointer", "en_name", "canonical",
                    "method", "sim", "old_span", "new_ko", "korean", "amb"])
        for row in out:
            w.writerow(row)

    print("proposals:", dict(Counter(r[5] for r in out)), "total", len(out))


if __name__ == "__main__":
    main()
