"""Terminology-consistency scanner: quest text vs item names (and beyond).

Builds a registry  EN display-name -> KO variants  from name-bearing pointers
in all_pairs.tsv, then scans every translated string for references to those
names: EN text contains the item/quest name but KO text lacks the canonical
KO spelling -> the player sees a different name in the quest than on the item.

Canonical selection (v3):
  - glossary `fixed` terms always win (translation_glossary.tsv)
  - canon_overrides.tsv (hand-curated) wins over everything
  - otherwise score each variant by:
      asset class  (/items/ < /objects/ < /npcs|quests/ < /dungeons/ < /tiles/)
      field rank   (shortdescription < title < name < displayName < subtitle)
      deployed-pak count (female_translation occurrences)
      total count
  - when a name has several distinct KO spellings (AMB), each flagged
    reference is resolved per-row by path-token overlap between the
    referencing asset and each variant's defining assets; unresolved rows
    fall back to the global canon and are marked amb=?

Outputs:
  name_registry.tsv      EN name -> every KO variant w/ counts+assets+is_canon
  name_conflicts.tsv     same EN name -> several KO spellings
  name_refs_missing.tsv  EN name referenced in text, canonical KO absent
  name_refs_variant.tsv  EN name referenced, non-canonical KO variant used
"""
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).parent.parent
csv.field_size_limit(10_000_000)

NAME_KEYS = {"shortdescription", "title", "name", "displayName", "subtitle"}
CANON_ORDER = ["shortdescription", "title", "name", "displayName", "subtitle"]
FIELD_RANK = {f: i for i, f in enumerate(CANON_ORDER)}

# asset classes ranked by how "item-name-like" they are
CLASS_RANK = [("/items/", 0), ("/objects/", 1), ("/npcs/", 2), ("/quests/", 2),
              ("/species/", 2), ("/monsters/", 2), ("/vehicles/", 2),
              ("/dungeons/", 3), ("/tiles/", 4), ("/liquids/", 4)]

TAG_RE = re.compile(r"\^[A-Za-z0-9#]*;")
KO_RE = re.compile(r"[가-힣]")

# path tokens that carry no mod/object identity
NOISE_TOK = {"objects", "items", "quests", "npcs", "tiles", "dungeons", "species",
             "liquids", "dialog", "conversations", "interface", "generic",
             "object", "matitem", "item", "questtemplate", "npctype", "patch",
             "activeitem", "material", "the", "of", "create", "make", "craft",
             "quest", "config", "codex", "ai", "aimission", "radiomessages",
             "cinematics", "monsters", "weapons", "melee", "ranged", "armor",
             "active", "consumable", "augment", "blueprint", "path"}


def basename(ptr):
    return ptr.rstrip("/").rsplit("/", 1)[-1]


def strip_tags(s):
    return TAG_RE.sub("", s)


def class_rank(asset):
    a = asset.lower()
    for k, v in CLASS_RANK:
        if k in a:
            return v
    return 5


def path_tokens(asset):
    toks = re.split(r"[/_.\-\\.]+", asset.lower())
    return {t for t in toks if t and t not in NOISE_TOK}


VERB_ENDINGS = ("세요", "하세요", "합시다", "봅시다", "입니다", "습니다",
                "해요", "이다", "했다", "한다", "됩니다", "해라", "어라",
                "것이다", "된다", "있어", "없어", "해줘", "주세요",
                "다고", "는데", "지만", "어요", "아요", "잖아", "거든",
                "지마", "해야", "하자", "할게", "할까", "해봐", "가봐",
                "보세요", "보자", "하겠", "겠어", "란다", "구나", "구만",
                "더라", "더군", "십니다", "옵니다", "어서", "이에요", "예요")


def junk_ko(ks):
    """Same prose-vs-name test as propose_name_fixes.junk_target: a canon
    candidate that is actually a sentence must not win canon selection."""
    c = ks.rstrip()
    return (not c or "또는" in c or len(c) > 40 or len(c.split()) > 5
            or c.endswith(("은", "는", "을", "를", "의"))
            or any(c.endswith(v) for v in VERB_ENDINGS))


def load_glossary_fixed():
    fixed = {}
    gp = BASE / "data/translation_glossary.tsv"
    if gp.exists():
        for gr in csv.DictReader(gp.open(encoding="utf-8-sig"), delimiter="\t"):
            if gr.get("rule") == "fixed" and gr.get("english") and gr.get("korean"):
                fixed[gr["english"].strip().lower()] = gr["korean"].strip()
    return fixed


def load_overrides():
    """Hand-curated canon overrides: english<TAB>canonical_ko"""
    ov = {}
    op = BASE / "data/canon_overrides.tsv"
    if op.exists():
        for row in csv.reader(op.open(encoding="utf-8-sig"), delimiter="\t"):
            if len(row) >= 2 and row[0].strip() and not row[0].startswith("#"):
                ov[row[0].strip().lower()] = row[1].strip()
    return ov


def main():
    rows = list(csv.DictReader((BASE / "all_pairs.tsv").open(encoding="utf-8-sig"), delimiter="\t"))
    print("rows:", len(rows))
    glossary_fixed = load_glossary_fixed()
    overrides = load_overrides()
    print("glossary fixed:", len(glossary_fixed), "overrides:", len(overrides))

    # ---------- registry ----------
    registry = defaultdict(list)  # en -> list of (ko, field, pak, asset)
    for r in rows:
        en, ko, ptr = r["english"], r["korean"], r["pointer"]
        if not en or not ko or not KO_RE.search(ko):
            continue
        f = basename(ptr)
        if f not in NAME_KEYS:
            continue
        e = strip_tags(en).strip()
        if not (4 <= len(e) <= 60) or "\n" in e:
            continue
        if not re.search(r"[A-Za-z]", e):
            continue
        registry[e].append((ko, f, r["pak"], r["asset"]))

    print("unique EN names:", len(registry))

    # ---------- per-variant stats + canonical pick ----------
    canon = {}          # en -> canonical KO (tag-stripped)
    vinfo = {}          # en -> {ko_stripped: {cnt,ft,score,assets}}
    for en, lst in registry.items():
        vs = {}
        for ko, f, pk, a in lst:
            ks = strip_tags(ko).strip()
            if not ks:
                continue
            d = vs.setdefault(ks, {"cnt": 0, "ft": 0, "class": 9, "field": 9,
                                   "assets": [], "tok": set()})
            d["cnt"] += 1
            if "female_translation" in pk:
                d["ft"] += 1
            d["class"] = min(d["class"], class_rank(a))
            d["field"] = min(d["field"], FIELD_RANK.get(f, 9))
            if len(d["assets"]) < 8:
                d["assets"].append(a)
            d["tok"] |= path_tokens(a)
        vinfo[en] = vs
        low = en.lower()
        if low in overrides:
            canon[en] = overrides[low]
        elif low in glossary_fixed:
            canon[en] = glossary_fixed[low]
        else:
            # skip prose-looking variants: a sentence value is not a name,
            # prefer the next candidate instead of poisoning the canon
            good = {k: d for k, d in vs.items() if not junk_ko(k)}
            if not good:
                canon[en] = ""  # all variants look like prose - suppress
                continue
            canon[en] = min(good.items(),
                            key=lambda kv: (kv[1]["class"], kv[1]["field"],
                                            -kv[1]["ft"], -kv[1]["cnt"]))[0]

    # ---------- name_registry.tsv ----------
    with (BASE / "data/name_registry.tsv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["english", "ko_variant", "is_canon", "count", "ft_count",
                    "class_rank", "field_rank", "assets"])
        for en in sorted(registry, key=str.lower):
            for ko, d in sorted(vinfo[en].items(), key=lambda kv: -kv[1]["cnt"]):
                w.writerow([en, ko, "1" if ko == canon[en] else "", d["cnt"],
                            d["ft"], d["class"], d["field"],
                            "|".join(d["assets"][:5])])

    # ---------- type A: same EN name, several KO ----------
    conflicts = []
    for en, lst in registry.items():
        kos = Counter(strip_tags(k).strip() for k, *_ in lst)
        kos = Counter({k: v for k, v in kos.items() if k})
        if len(kos) > 1:
            conflicts.append((en, kos, canon[en]))
    conflicts.sort(key=lambda x: -sum(x[1].values()))

    with (BASE / "data/name_conflicts.tsv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["english", "canonical", "variant", "count", "amb", "assets_sample"])
        for en, kos, c in conflicts:
            for ko, n in kos.most_common():
                w.writerow([en, c, ko, n, "AMB",
                            "|".join(vinfo[en][ko]["assets"][:4])])
    print("name conflicts:", len(conflicts))

    # ---------- matcher ----------
    first_word = defaultdict(list)
    for en in registry:
        tok = re.findall(r"[A-Za-z0-9']+", en)
        if not tok:
            continue
        pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(en) + r"(?:e?s)?(?![A-Za-z])")
        first_word[tok[0].lower()].append((en, pat))
    for lst in first_word.values():
        lst.sort(key=lambda t: -len(t[0]))  # longest first

    def find_names(text):
        """Return {en_name: (start,end)} with shorter matches contained inside
        a longer name's span suppressed (e.g. 'Crystal' inside 'Crystal Lake')."""
        spans = {}
        toks = list(re.finditer(r"[A-Za-z0-9']+", text))
        for m in toks:
            for en, pat in first_word.get(m.group(0).lower(), ()):
                mm = pat.search(text, max(0, m.start() - 2))
                if mm:
                    spans.setdefault(en, mm.span())
        keep = {}
        items = sorted(spans.items(), key=lambda kv: -(kv[1][1] - kv[1][0]))
        for en, sp in items:
            if any(sp[0] >= k[0] and sp[1] <= k[1] for k in keep.values()):
                continue  # contained in a longer matched name
            keep[en] = sp
        return keep

    name_fields = {en: sorted({f for _, f, _, _ in lst}) for en, lst in registry.items()}

    def resolve_target(nm, ref_asset):
        """For AMB names pick the variant whose defining assets share the most
        path tokens with the referencing asset. The flag's own asset is
        excluded (a quest's own title is not the entity the text references).
        Score = shared path tokens + 2 * shared basename tokens; needs >=3
        to count as resolved. Returns (ko, ambflag)."""
        vs = vinfo[nm]
        if len(vs) <= 1 or nm.lower() in overrides or nm.lower() in glossary_fixed:
            return canon[nm], ""
        rtok = path_tokens(ref_asset)
        rbase = path_tokens(basename(ref_asset))
        best_sc = 0
        cands = []
        for ko, d in vs.items():
            toks = set()
            btoks = set()
            for a in d["assets"]:
                if a == ref_asset:
                    continue  # self-reference: ignore
                toks |= path_tokens(a)
                btoks |= path_tokens(basename(a))
            if not toks:
                continue
            sc = len(rtok & toks) + 2 * len(rbase & btoks)
            if sc >= best_sc:
                best_sc = sc
                cands.append((sc, ko))
        if best_sc >= 3:
            cands = [k for s, k in cands if s == best_sc]
            # prefer the global canon among equally-scored candidates
            if canon[nm] in cands:
                return canon[nm], "AMB"
            return sorted(cands, key=lambda k: (-vinfo[nm][k]["ft"], -vinfo[nm][k]["cnt"]))[0], "AMB"
        return canon[nm], "?"

    # ---------- type B scan ----------
    missing = []   # canonical KO absent entirely
    variant = []   # a non-canonical variant used instead
    seen_m, seen_v = set(), set()
    for r in rows:
        en, ko, ptr, asset, pak = r["english"], r["korean"], r["pointer"], r["asset"], r["pak"]
        if not en or not ko or not KO_RE.search(ko):
            continue
        if len(en) < 5:
            continue
        f = basename(ptr)
        ko_stripped = strip_tags(ko)
        found = find_names(en)
        for nm, sp in found.items():
            if f in NAME_KEYS and strip_tags(en).strip() == nm:
                # This row defines the name, not a reference. But when a
                # hand-curated/glossary canon exists and this definition
                # itself uses a variant, flag it (amb='DEF') so the item or
                # object name gets unified too - otherwise refs would point
                # at a name no entity displays.
                if canon.get(nm) and (nm.lower() in overrides or nm.lower() in glossary_fixed):
                    ks0 = strip_tags(ko).strip()
                    if ks0 and ks0 != strip_tags(canon[nm]) and ks0 in {
                            strip_tags(k).strip() for k, *_ in registry[nm]}:
                        key = (pak, asset, ptr, nm, canon[nm])
                        if key not in seen_v:
                            seen_v.add(key)
                            variant.append((pak, asset, ptr, nm, canon[nm],
                                            "|".join(sorted(vinfo[nm], key=lambda k: -vinfo[nm][k]['cnt'])),
                                            "DEF", "|".join(name_fields[nm]), en, ko))
                continue
            if not canon.get(nm):
                continue  # all-KO-variants-are-prose name, suppressed
            kos_here = {strip_tags(k).strip() for k, *_ in registry[nm]}
            kos_here.discard("")
            target, amb = resolve_target(nm, asset)
            if nm in ko or nm in ko_stripped:
                continue  # name kept verbatim in English -> consistent
            if any(s in ko_stripped for s in kos_here):
                if strip_tags(target) not in ko_stripped:
                    key = (pak, asset, ptr, nm, target)
                    if key not in seen_v:
                        seen_v.add(key)
                        variant.append((pak, asset, ptr, nm, target,
                                        "|".join(sorted(vinfo[nm], key=lambda k: -vinfo[nm][k]['cnt'])),
                                        amb, "|".join(name_fields[nm]), en, ko))
                continue
            scope = "QUEST" if "quest" in asset.lower() else ("TEXT" if f in {"text", "completiontext", "turnindescription", "failuretext", "description", "longdescription", "radiomessages", "dialog"} else "OTHER")
            key = (pak, asset, ptr, nm, target)
            if key in seen_m:
                continue
            seen_m.add(key)
            # tier: single common-word names are only credible when the EN
            # occurrence is wrapped in a ^color; tag (the game's own name
            # marker); multiword/distinctive names are always kept.
            tagged = bool(re.search(r"\^[A-Za-z0-9#]*;[^A-Za-z0-9\n]*" + re.escape(en[sp[0]:sp[1]]), en))
            single = len(nm.split()) == 1
            tier = "AUTO" if (tagged or not single) else "REVIEW"
            if amb == "?":
                tier = "REVIEW"
            missing.append((scope, tier, pak, asset, ptr, nm, target,
                            "|".join(sorted(vinfo[nm], key=lambda k: -vinfo[nm][k]['cnt'])),
                            amb, "|".join(name_fields[nm]), en, ko))

    with (BASE / "data/name_refs_missing.tsv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["scope", "tier", "pak", "asset", "pointer", "en_name",
                    "ko_expected", "ko_variants", "amb", "name_fields", "english", "korean"])
        for row in sorted(missing, key=lambda x: (x[0] != "QUEST", x[1] != "AUTO", x[3])):
            w.writerow(row)

    with (BASE / "data/name_refs_variant.tsv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["pak", "asset", "pointer", "en_name", "ko_target",
                    "ko_variants", "amb", "name_fields", "english", "korean"])
        for row in variant:
            w.writerow(row)

    print("missing-name refs:", len(missing), "of which QUEST:", sum(1 for m in missing if m[0] == "QUEST"))
    print("variant-name refs:", len(variant))


if __name__ == "__main__":
    main()
