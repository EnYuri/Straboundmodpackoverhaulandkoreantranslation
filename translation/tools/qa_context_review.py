"""Prioritize new translations for human tone and compact-UI review.

The report is not an error list.  It ranks:
  * dialogue/cinematic assets mixing polite and plain sentence endings;
  * compact UI fields whose Korean value is unusually long;
  * literal Korean constructions worth reading in context.
"""

from __future__ import annotations

import csv
import glob
import re
from collections import Counter, defaultdict
from pathlib import Path


BASE = Path(r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921")


def load_translations() -> dict[int, str]:
    result: dict[int, str] = {}
    current = None
    for filename in glob.glob(str(BASE / "translations" / "batch_*.tsv")):
        for raw in open(filename, encoding="utf-8"):
            line = raw.rstrip("\n")
            match = re.match(r"^(\d+)\t(.*)$", line)
            if match:
                current = int(match.group(1))
                result[current] = match.group(2)
            elif current is not None:
                result[current] += "\n" + line
    return result


work = list(csv.DictReader(open(BASE / "data/worklist_new.tsv", encoding="utf-8-sig"), delimiter="\t"))
ko = load_translations()


def locations(text: str):
    for item in text.split(" | "):
        match = re.match(r"([^:]+):(/[^#]+)#(.*)$", item)
        if match:
            yield match.groups()


def tone(text: str) -> str:
    clean = re.sub(r"\^[^;]+;|\[[^]]*]|[\"'”“‘’()]", "", text).strip()
    # Count sentence-final markers instead of relying only on the last sentence.
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


asset_rows = defaultdict(list)
ui_rows = []
literal_rows = []
literal_patterns = re.compile(
    r"당신은 (?:찾아|찾았)|그것은|이것은|할 수 있어요,|것입니다,|에 대해 배웠어요|"
    r"지속적 생존|정면 대미지|더 나은 날을 봤|호흡 불가|측정 불가능할 정도"
)

for index, row in enumerate(work):
    target = ko.get(index, "")
    if not target:
        continue
    for mod, asset, pointer in locations(row.get("exampleLocations", "")):
        item = {
            "id": index,
            "mod": mod,
            "asset": asset,
            "pointer": pointer,
            "english": row["englishText"],
            "korean": target,
            "tone": tone(target),
        }
        if any(key in asset.lower() for key in ("/cinematics/", "/dialog/", "/radiomessages/", "/quests/")):
            asset_rows[(mod, asset)].append(item)
        is_ui = any(key in asset.lower() for key in ("/interface/", ".activeitem", ".item", ".statuseffect"))
        is_compact = any(key in pointer.lower() for key in ("title", "name", "label", "shortdescription", "subtitle", "button"))
        if is_ui and is_compact and len(row["englishText"]) <= 48:
            # Korean usually needs fewer glyphs.  Values over 24 glyphs and
            # longer than 90% of English are likely to need an in-game look.
            visible = re.sub(r"\^[^;]+;", "", target)
            if len(visible) >= 24 and len(visible) >= len(row["englishText"]) * 0.9:
                ui_rows.append(item | {"ratio": round(len(visible) / max(1, len(row["englishText"])), 2)})
        if literal_patterns.search(target):
            literal_rows.append(item)

style_groups = []
for (mod, asset), items in asset_rows.items():
    counts = Counter(item["tone"] for item in items)
    voiced = counts["polite"] + counts["plain"] + counts["casual"] + counts["mixed-in-string"]
    if voiced >= 3 and counts["polite"] and (counts["plain"] or counts["casual"]):
        style_groups.append((voiced, mod, asset, counts, items))
style_groups.sort(reverse=True, key=lambda value: value[0])

out = BASE / "data/qa_context_candidates.tsv"
with out.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t")
    writer.writerow(["kind", "id", "mod", "asset", "pointer", "tone_or_ratio", "english", "korean"])
    for _, mod, asset, counts, items in style_groups:
        summary = ",".join(f"{key}={value}" for key, value in sorted(counts.items()))
        for item in items:
            writer.writerow(["STYLE_MIX", item["id"], mod, asset, item["pointer"], summary,
                             item["english"], item["korean"]])
    for item in sorted(ui_rows, key=lambda value: value["ratio"], reverse=True):
        writer.writerow(["UI_LENGTH", item["id"], item["mod"], item["asset"], item["pointer"],
                         item["ratio"], item["english"], item["korean"]])
    for item in literal_rows:
        writer.writerow(["LITERAL", item["id"], item["mod"], item["asset"], item["pointer"],
                         item["tone"], item["english"], item["korean"]])

print("style groups:", len(style_groups), "rows:", sum(len(group[4]) for group in style_groups))
print("ui length candidates:", len(ui_rows))
print("literal candidates:", len(literal_rows))
print("report:", out)
