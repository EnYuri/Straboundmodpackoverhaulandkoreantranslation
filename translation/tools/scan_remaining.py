#!/usr/bin/env python3
# Full scan of all remaining untranslated content mods:
#   scope = content-review + defer-technical + defer-adult-assets
#           + merged translation paks (existing-translation-source minus
#             pure translation paks FU_KO/sbkor) + FrackinUniverse pak
#           + unpacked directory mods in mods/
# Emits:
#   rest_targets.tsv   - kept rows (mod, pak, asset, pointer, english, category, suggestion, inPatchAsset)
#   rest_excluded.tsv  - dropped rows with reason
#   rest_worklist.tsv  - unique new-translation + tm-multi strings for manual work
#   rest_summary.json
import csv, json, os, re, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from pak import Pak
from align_merged_translations import parse_json

MODS = ROOT / "mods"
VANILLA = ROOT / "assets" / "packed.pak"

TEXT_EXTENSIONS = {
    ".activeitem", ".animation", ".behavior", ".cinematic", ".codex", ".config",
    ".consumable", ".item", ".liquid", ".liqitem", ".matitem",
    ".monstertype", ".npctype", ".object", ".patch", ".projectile",
    ".questtemplate", ".radiomessages", ".recipe", ".species", ".stagehand",
    ".statuseffect", ".tech", ".tenant", ".tooltip", ".treasurepools",
    ".vehicle", ".weaponability", ".weather", ".aimission", ".sbvn",
}
VISIBLE_KEYS = {
    "apexdescription", "aviandescription", "caption", "description",
    "florandescription", "glitchdescription", "humandescription",
    "hylotldescription", "label", "message", "messages", "name",
    "novakiddescription", "objective", "shortdescription", "subtitle",
    "text", "title", "tooltip", "value",
}
ASCII_WORD = re.compile(r"[A-Za-z]{2}")
HANGUL = re.compile(r"[가-힣]")
IDENT_LIKE = re.compile(r"^[A-Za-z0-9_.:+-]+$")
NON_TEXT_LEAF = re.compile(
    r"(image|icon|path|file|sound|music|script|name|id|type|projectile|item|"
    r"liquid|material|block|dungeon|quest|mission|recipe|tenant|pool|table|"
    r"frames?|palette|color|status|effect|animation|particle|emitter|slot|"
    r"parameter|key|flag|tag|trigger|action|itemList|drop)$", re.I)
UNUSED_SEGMENTS = {
    "unused", "legacy", "old", "deprecated", "disabled", "backup",
    "obsolete", "removed", "wip", "p_deprecated", "deprecated_special",
}
PLACEHOLDER_TEXTS = {"replace me", "placeholder", "todo", "lorem ipsum", "test"}
PARAM_REF = re.compile(r"^<[\w.\-]+>$")
MARKUP = re.compile(r"\^(?:#[0-9a-fA-F]{3,8}|[a-zA-Z]+);?")
CODE_LIKE = re.compile(
    r"function\s*\(|->|=>|==|!=|\|\||&&"
    r"|\b(?:self|world|storage|sb|config|animator|status|item|entity|player|monster|npc|mcontroller|widget|canvas|pane)\.[A-Za-z_]"
    r"|\w+\s*\([^)]*\)\s*\{")
PATH_LIKE = re.compile(r"^[A-Za-z0-9_\-]+[/\\][A-Za-z0-9_\-./\\]+$")
SCHEMA_POINTER = re.compile(r"/(?:listTemplate|schema|itemSchema|buttonTemplate)\b", re.I)
PUA = re.compile(r"[-]")


def norm(s):
    return " ".join(MARKUP.sub("", s).lower().split())


def text_only(s):
    """strip color/markup tags and private-use glyph icons before checking
    whether a string actually contains real English words - a bare
    ``^#09ff00;`` color tag or glyph-only bark line otherwise reads as
    "contains letters" purely from its hex digits (2026-09-27 fix)."""
    return PUA.sub("", MARKUP.sub("", s))


def norm_key(s):
    return s.strip().replace("\r\n", "\n")


def cand_visible(v):
    """inventory candidate() rules for strings at known-visible keys"""
    if not isinstance(v, str) or HANGUL.search(v) or not ASCII_WORD.search(text_only(v)):
        return False
    s = v.strip()
    if not s or s.startswith(("/", "?", "$", "scripts/")):
        return False
    if " " not in s and IDENT_LIKE.fullmatch(s):
        return False
    return True


def cand_loose(v):
    """missed-worklist is_text() for array elements / unknown keys"""
    t = v.strip() if isinstance(v, str) else ""
    if len(t) < 4 or HANGUL.search(t) or " " not in t:
        return False
    if not ASCII_WORD.search(text_only(t)) or t.startswith(("/", "~", "?")):
        return False
    return True


def classify(english, asset, pointer):
    """returns exclusion reason or None (mirrors clean_translation_candidates)"""
    a = asset.lower()
    if a.endswith(".behavior"):
        return "behavior-tree-parameter"
    segs = {s for s in re.split(r"[/\\]", a) if s}
    if segs & UNUSED_SEGMENTS:
        return "unused-or-deprecated-asset"
    stripped = MARKUP.sub("", english).strip()
    if not stripped:
        return "markup-only"
    if PARAM_REF.match(stripped):
        return "parameter-reference"
    if stripped.lower() in PLACEHOLDER_TEXTS or SCHEMA_POINTER.search(pointer):
        return "template-placeholder"
    if CODE_LIKE.search(english):
        return "code-like-string"
    if PATH_LIKE.match(stripped):
        return "asset-path-identifier"
    return None


def walk_strings(node, pointer="", key_hint=""):
    """yield (pointer, string, key_hint) for every string node"""
    if isinstance(node, dict):
        is_op = {"op", "path", "value"}.issubset(node)
        for k, v in node.items():
            child = f"{pointer}/{escape_ptr(k)}"
            hint = k.lower()
            if is_op and k == "value":
                # string(s) inside a patch op value: hint from op.path leaf
                leaf = str(node.get("path", "")).rstrip("/").split("/")[-1].lower()
                yield from walk_strings(v, child, leaf or hint)
            else:
                yield from walk_strings(v, child, hint)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_strings(v, f"{pointer}/{i}", key_hint)
    elif isinstance(node, str):
        yield pointer, node, key_hint


def escape_ptr(k):
    return k.replace("~", "~0").replace("/", "~1")


def find_test_spans(doc):
    spans = set()
    def rec(n, p):
        if isinstance(n, dict):
            if n.get("op") == "test":
                spans.add(p)
            for k, v in n.items():
                rec(v, p + "/" + escape_ptr(k))
        elif isinstance(n, list):
            for i, v in enumerate(n):
                rec(v, f"{p}/{i}")
    rec(doc, "")
    return spans


def op_info_for_pointer(doc, pointer):
    """for a string at `pointer` inside a patch doc, return (op, value_suffix)"""
    parts = pointer.lstrip("/").split("/")
    # find the op node: walk until we hit a dict with op/path/value
    cur = doc
    consumed = 0
    node = None
    for i, part in enumerate(parts):
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, list):
            cur = cur[int(part)]
        elif isinstance(cur, dict):
            cur = cur[part]
        else:
            return None, None
        if isinstance(cur, dict) and {"op", "path", "value"}.issubset(cur):
            node = cur
            consumed = i + 1
            break
    if node is None:
        return None, None
    rest = parts[consumed:]
    # first element of rest should be 'value'
    if rest and rest[0] == "value":
        suffix = "/" + "/".join(rest[1:]) if len(rest) > 1 else ""
        return node, suffix
    return node, None


def load_tm():
    """en_norm -> set(korean) from all prior translation sources"""
    tm = defaultdict(set)
    def add(eng, kor):
        if eng and kor:
            tm[norm_key(eng)].add(kor)
    for fn, ec, kc in (("data/translation_memory.tsv", "currentOriginal", "existingKorean"),
                       ("data/legacy_translation_memory.tsv", "currentOriginal", "legacyKorean")):
        with open(HERE / fn, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                add(r[ec], r[kc])
    # primary worklist batches: id = row index into worklist_new
    wl = []
    with open(HERE / "data/worklist_new.tsv", encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            wl.append(r["englishText"])
    for bf in sorted((HERE / "translations").glob("batch_*.tsv")):
        with open(bf, encoding="utf-8-sig", newline="") as fh:
            for r in csv.reader(fh, delimiter="\t"):
                if len(r) < 2 or not r[0].isdigit():
                    continue
                i = int(r[0])
                if i < len(wl):
                    add(wl[i], r[1])
    # missed worklist batches: id column in missed_worklist
    id2eng = {}
    with open(HERE / "data/missed_worklist.tsv", encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            id2eng[r["id"]] = r["englishText"]
    for bf in sorted((HERE / "translations").glob("missed_*.tsv")):
        with open(bf, encoding="utf-8-sig", newline="") as fh:
            for r in csv.reader(fh, delimiter="\t"):
                if len(r) < 2 or r[0] == "id":
                    continue
                add(id2eng.get(r[0], ""), r[1])
    # tm-multi picks
    p = HERE / "data/tm_multi_chosen.tsv"
    if p.exists():
        with open(p, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                add(r["english"], r["chosen"])
    return tm


def load_coverage():
    """(assetPath, jsonPointer) already translated by installed translation patches"""
    covered = set()
    for fn in ("fu.tsv", "sbkor.tsv"):
        with open(HERE / "alignment" / fn, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                if r["status"].startswith("aligned") and r["targetAsset"]:
                    covered.add((r["targetAsset"].lower(), r["jsonPointer"]))
    # installed overlay paks: their patch ops cover (base, op.path)
    # NOTE (2026-09-27): localeko_gic_legacy/localeko_extended_story_legacy/
    # localeko_black_armory_legacy were merged into female_translation.pak and no
    # longer exist standalone; female_translation.pak is now the real active
    # coverage source and must be checked instead, or every asset it already
    # translated is misreported as untranslated.
    # NOTE (2026-09-28, 4차): zz_localeko_elithian_low_20260927/krakoth_low_20260927/
    # nuggubs_low_20260927/plushbound_low_20260927 were likewise merged into
    # female_translation.pak (see docs/batch_log.md "2026-09-28 (4차)") and moved out
    # of mods/ to translation/_archive/replaced-installed-20260922/low_paks_merged_20260928/;
    # kept in this list (harmless, `if not p.exists(): continue` below skips them)
    # only so the list still documents which paks were folded in, not because they
    # are still expected to exist standalone.
    for pakname in ("zz_translation_female.pak", "zz_localeko_postload.pak",
                    "zz_localeko_highpriority_20260927.pak",
                    "zz_localeko_elithian_low_20260927.pak",
                    "zz_localeko_krakoth_low_20260927.pak",
                    "zz_localeko_nuggubs_low_20260927.pak",
                    "zz_localeko_plushbound_low_20260927.pak",
                    "localeko_gic_legacy.pak", "localeko_extended_story_legacy.pak",
                    "localeko_black_armory_legacy.pak"):
        p = MODS / pakname
        if not p.exists():
            continue
        pak = Pak(str(p))
        for a in pak.index:
            if not a.endswith(".patch"):
                continue
            # asset paths are case-insensitive on Starbound's filesystem, but
            # a mod's own folder casing ("MATERIALS" vs "materials") often
            # differs from what the translation overlay recorded, so an exact
            # string match silently drops real coverage (2026-09-27 fix).
            base = a[:-len(".patch")].lower()
            try:
                ops = parse_json(pak.read(a))
            except Exception:
                continue
            # patch docs are either a flat list of op-dicts, or a list of
            # sub-lists grouping a test+replace pair per element (the format
            # female_translation.pak's custom writer uses) - flatten both.
            for el in ops if isinstance(ops, list) else []:
                group = el if isinstance(el, list) else [el]
                for o in group:
                    if isinstance(o, dict) and o.get("path"):
                        covered.add((base, o["path"]))
    return covered


def scope_paks():
    """pak filename -> category for everything still needing translation"""
    scope = {}
    for r in csv.DictReader(open(HERE / "data/target_classification.tsv", encoding="utf-8-sig", newline=""), delimiter="\t"):
        cat, pak = r["category"], r["pak"]
        if cat in ("content-review", "defer-technical", "defer-adult-assets"):
            scope[pak] = cat
        elif cat == "existing-translation-source":
            # merged translation+content paks still have untranslated English
            if "FU_KO" in pak or "sbkor" in pak:
                continue
            scope[pak] = "merged-translation-pak"
        elif cat == "priority-legacy-alignment" and "FrackinUniverse" in pak:
            scope[pak] = "frackin-universe"
    return scope


def iter_assets(source_path):
    """yield (assetPath, raw_bytes) for a pak file or an unpacked mod dir"""
    if source_path.is_dir():
        for f in sorted(source_path.rglob("*")):
            if not f.is_file():
                continue
            rel = "/" + f.relative_to(source_path).as_posix()
            if Path(rel).suffix.lower() in TEXT_EXTENSIONS:
                try:
                    yield rel, f.read_bytes()
                except OSError:
                    continue
    else:
        pak = Pak(str(source_path))
        for a in pak.index:
            if Path(a).suffix.lower() in TEXT_EXTENSIONS:
                yield a, pak.read(a)


def main():
    scope = scope_paks()
    tm = load_tm()
    covered = load_coverage()
    kept, excluded = [], []
    counts = Counter()

    sources = [(MODS / name, name, cat) for name, cat in scope.items()]
    for d in sorted(MODS.iterdir()):
        if d.is_dir():
            sources.append((d, d.name + "/", "dir-mod"))

    for src, name, cat in sources:
        if not src.exists():
            counts[f"missing-pak:{name}"] += 1
            continue
        for asset, raw in iter_assets(src):
            try:
                doc = parse_json(raw)
            except Exception:
                counts["unparsed"] += 1
                continue
            is_patch = asset.lower().endswith(".patch")
            test_spans = find_test_spans(doc) if is_patch else set()
            for pointer, text, hint in walk_strings(doc):
                if is_patch:
                    if any(pointer == ts or pointer.startswith(ts + "/") for ts in test_spans):
                        excluded.append((name, cat, asset, pointer, text, "patch-test-value"))
                        continue
                    leaf = pointer.rstrip("/").split("/")[-1]
                    if NON_TEXT_LEAF.search(leaf):
                        excluded.append((name, cat, asset, pointer, text, "patch-nontext-leaf"))
                        continue
                    ok = cand_loose(text)
                else:
                    ok = cand_visible(text) if hint in VISIBLE_KEYS else cand_loose(text)
                if not ok:
                    continue
                reason = classify(text, asset, pointer)
                if reason:
                    excluded.append((name, cat, asset, pointer, text, reason))
                    continue
                # coverage: regular assets exact; patch docs only for replace ops
                if not is_patch and (asset.lower(), pointer) in covered:
                    excluded.append((name, cat, asset, pointer, text, "already-translated"))
                    continue
                variants = tm.get(norm_key(text))
                if variants:
                    category = "tm-single" if len(variants) == 1 else "tm-multi"
                    sugg = next(iter(variants)) if len(variants) == 1 else " || ".join(sorted(variants))
                else:
                    category, sugg = "new-translation", ""
                kept.append({
                    "sourceMod": name, "category": cat, "assetPath": asset,
                    "jsonPointer": pointer, "englishText": text, "keyHint": hint,
                    "tmCategory": category, "suggestedKorean": sugg,
                    "inPatchAsset": "1" if is_patch else "0",
                })

    with open(HERE / "data/rest_targets.tsv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, ["sourceMod", "category", "assetPath", "jsonPointer",
                                "englishText", "keyHint", "tmCategory",
                                "suggestedKorean", "inPatchAsset"],
                           delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(kept)
    with open(HERE / "data/rest_excluded.tsv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(("sourceMod", "category", "assetPath", "jsonPointer",
                    "englishText", "excludedReason"))
        w.writerows(excluded)

    # worklist: unique strings needing manual translation (new + tm-multi)
    strings = defaultdict(lambda: {"count": 0, "mods": set(), "hints": Counter(), "sugg": set(), "cat": "new-translation"})
    for r in kept:
        if r["tmCategory"] == "tm-single":
            continue
        key = norm_key(r["englishText"])
        s = strings[key]
        s["count"] += 1
        s["mods"].add(r["sourceMod"])
        s["hints"][r["keyHint"]] += 1
        if r["suggestedKorean"]:
            s["sugg"].add(r["suggestedKorean"])
        if r["tmCategory"] == "tm-multi":
            s["cat"] = "tm-multi"
    with open(HERE / "data/rest_worklist.tsv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(("id", "count", "englishText", "tmCategory", "suggestedKorean",
                    "keyHints", "mods"))
        for i, (eng, s) in enumerate(sorted(strings.items(), key=lambda kv: (-kv[1]["count"], kv[0]))):
            w.writerow((i, s["count"], eng, s["cat"],
                        sorted(s["sugg"])[0] if s["sugg"] else "",
                        "|".join(k for k, _ in s["hints"].most_common(3)),
                        "|".join(sorted(s["mods"]))))

    summary = {
        "keptRows": len(kept),
        "keptUniqueEnglish": len({norm_key(r["englishText"]) for r in kept}),
        "excludedRows": len(excluded),
        "worklistUnique": len(strings),
        "byCategory": dict(Counter(r["tmCategory"] for r in kept)),
        "excludedReasons": dict(Counter(e[5] for e in excluded).most_common()),
        "perModTop": Counter(r["sourceMod"] for r in kept).most_common(20),
    }
    (HERE / "archive/rest_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False)[:4000])


if __name__ == "__main__":
    main()
