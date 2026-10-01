"""Systematic tone/literalness/length QA over the ENTIRE deployed pak.

Generalizes qa_context_review.py (which only covered worklist_new.tsv/
batch_*.tsv, ~6,700 rows) to all 182k EN/KO pairs in pak_pairs.tsv, extracted
directly from mods/zz_translation_female.pak by extract_pak_pairs.py. This is
the "check the completed pak directly" methodology from docs/batch_log.md
2026-09-28, applied at full scale instead of one tsv group at a time.

Not an error list -- a triage report, sorted so the most likely genuine
problems surface first within each category.
"""
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(sys.maxsize)

BASE = Path(__file__).parent.parent
IN = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "data/pak_pairs.tsv"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else BASE / "data/qa_pak_context_report.tsv"


QUOTE_CHARS = "\"'“”‘’()"
_DECO_RE = re.compile(r"\^[^;]+;|\[[^\]]*]|<[^>]*>|[" + re.escape(QUOTE_CHARS) + "]")


def strip_deco(text):
    return _DECO_RE.sub("", text)


def tone(text):
    clean = strip_deco(text).strip()
    polite = len(re.findall(r"(?:습니다|습니까|세요|십시오|해요|예요|이에요|군요|네요|죠)(?=[.!?…\n]|$)", clean))
    plain = len(re.findall(r"(?:한다|했다|이다|였다|된다|됐다|없다|있다|하라|해라|인가|냐|군)(?=[.!?…\n]|$)", clean))
    casual = len(re.findall(r"(?:해|야|거야|잖아|겠어|했어|됐어|없어|있어|구나)(?=[.!?…\n]|$)", clean))
    if polite and (plain or casual):
        return "mixed-in-string"
    if polite:
        return "polite"
    if casual:
        return "casual"
    if plain:
        return "plain"
    return "neutral"


LITERAL_PATTERNS = re.compile(
    r"당신은 (?:찾아|찾았)|그것은|이것은|할 수 있어요,|것입니다,|에 대해 배웠어요|"
    r"지속적 생존|정면 대미지|더 나은 날을 봤|호흡 불가|측정 불가능할 정도|"
    r"되어집니다|되어졌다|여겨집니다|할 수 있게 됩니다,|"
    r"하는 것을 원(?:합니다|한다|해요)|그리고 그리고|매우 매우|정말 정말|"
    r"에 의해 만들어졌|그것을 (?:가지고|사용하여)|그들은 (?:모두|전부)|"
    r"당신의 (?:것|친구|적)|우리들은|저것은"
)

DOUBLE_PARTICLE = re.compile(r"(을을|를를|은은|는는|이이(?!다)|가가(?!요)|와와|과과|도도|만만)")

UI_POINTER_KEYS = ("title", "name", "label", "shortdescription", "subtitle", "button")
UI_ASSET_KEYS = ("/interface/", ".activeitem", ".item", ".statuseffect")
DIALOGUE_ASSET_KEYS = ("/cinematics/", "/dialog/", "/radiomessages/", "/quests/", ".questtemplate")

SKIP_POINTER = re.compile(r"objectname$|materialname$|/id$|^/id$", re.I)


def load_rows():
    with IN.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            yield row


def main():
    rows = list(load_rows())
    print("loaded pairs:", len(rows))

    asset_rows = defaultdict(list)
    ui_rows = []
    literal_rows = []
    dup_particle_rows = []
    truncated_rows = []
    untranslated_rows = []

    for row in rows:
        asset = row["asset"]
        pointer = row["pointer"]
        en = row["english"]
        ko = row["korean"]
        if SKIP_POINTER.search(pointer):
            continue
        if not re.search(r"[A-Za-z]{3,}", en):
            continue  # not real prose (pure symbols/numbers/single tokens)

        low_asset = asset.lower()
        low_ptr = pointer.lower()

        t = tone(ko)
        item = {"asset": asset, "pointer": pointer, "english": en, "korean": ko, "tone": t}

        if any(k in low_asset for k in DIALOGUE_ASSET_KEYS):
            asset_rows[asset].append(item)

        is_ui = any(k in low_asset for k in UI_ASSET_KEYS)
        is_compact = any(k in low_ptr for k in UI_POINTER_KEYS)
        if is_ui and is_compact and len(en) <= 48:
            visible = re.sub(r"\^[^;]+;", "", ko)
            if len(visible) >= 24 and len(visible) >= len(en) * 0.9:
                ui_rows.append(item | {"ratio": round(len(visible) / max(1, len(en)), 2)})

        if LITERAL_PATTERNS.search(ko):
            literal_rows.append(item)

        if DOUBLE_PARTICLE.search(strip_deco(ko)):
            dup_particle_rows.append(item)

        visible_en = strip_deco(en)
        visible_ko = strip_deco(ko)
        if len(visible_en) >= 120 and len(visible_ko) <= len(visible_en) * 0.35:
            truncated_rows.append(item | {"ratio": round(len(visible_ko) / max(1, len(visible_en)), 2)})

        if visible_ko.strip() and visible_ko.strip() == visible_en.strip():
            untranslated_rows.append(item)

    style_groups = []
    for asset, items in asset_rows.items():
        counts = Counter(item["tone"] for item in items)
        voiced = counts["polite"] + counts["plain"] + counts["casual"] + counts["mixed-in-string"]
        if voiced >= 3 and counts["polite"] and (counts["plain"] or counts["casual"]):
            style_groups.append((voiced, asset, counts, items))
    style_groups.sort(reverse=True, key=lambda v: v[0])

    with OUT.open("w", encoding="utf-8", newline="") as handle:
        w = csv.writer(handle, delimiter="\t")
        w.writerow(["kind", "asset", "pointer", "tone_or_ratio", "english", "korean"])
        for _, asset, counts, items in style_groups:
            summary = ",".join(f"{k}={v}" for k, v in sorted(counts.items()))
            for item in items:
                w.writerow(["STYLE_MIX", asset, item["pointer"], summary, item["english"], item["korean"]])
        for item in sorted(ui_rows, key=lambda v: v["ratio"], reverse=True):
            w.writerow(["UI_LENGTH", item["asset"], item["pointer"], item["ratio"], item["english"], item["korean"]])
        for item in literal_rows:
            w.writerow(["LITERAL", item["asset"], item["pointer"], item["tone"], item["english"], item["korean"]])
        for item in dup_particle_rows:
            w.writerow(["DUP_PARTICLE", item["asset"], item["pointer"], item["tone"], item["english"], item["korean"]])
        for item in sorted(truncated_rows, key=lambda v: v["ratio"]):
            w.writerow(["TRUNCATED", item["asset"], item["pointer"], item["ratio"], item["english"], item["korean"]])
        for item in untranslated_rows:
            w.writerow(["UNTRANSLATED", item["asset"], item["pointer"], "", item["english"], item["korean"]])

    print("style groups:", len(style_groups), "rows:", sum(len(g[3]) for g in style_groups))
    print("ui length candidates:", len(ui_rows))
    print("literal candidates:", len(literal_rows))
    print("dup particle candidates:", len(dup_particle_rows))
    print("truncated candidates:", len(truncated_rows))
    print("untranslated leftovers:", len(untranslated_rows))
    print("report:", OUT)


if __name__ == "__main__":
    main()
