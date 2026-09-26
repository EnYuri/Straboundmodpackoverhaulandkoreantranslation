import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pak import Pak

HANGUL = re.compile(r"[가-힣]")
QUOTED = re.compile(r'"(?:\\.|[^"\\])*"')
TEXT_EXTENSIONS = {
    ".activeitem", ".animation", ".behavior", ".cinematic", ".codex",
    ".config", ".consumable", ".frames", ".item", ".liquid", ".liqitem",
    ".lua", ".matitem", ".monstertype", ".npctype", ".object", ".patch",
    ".projectile", ".questtemplate", ".recipe", ".species", ".stagehand",
    ".statuseffect", ".tech", ".tenant", ".tooltip", ".treasurepools",
    ".vehicle", ".weather",
}


def extract_strings(text):
    seen = set()
    for match in QUOTED.finditer(text):
        token = match.group(0)
        try:
            value = json.loads(token)
        except json.JSONDecodeError:
            value = token[1:-1]
        if HANGUL.search(value) and value not in seen:
            seen.add(value)
            yield value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("paks", nargs="+", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    rows = []
    source_rows = []
    frequency = Counter()
    for pak_path in args.paks:
        pak = Pak(str(pak_path))
        source_count = 0
        asset_count = 0
        for asset_path, (_, size) in pak.index.items():
            if Path(asset_path).suffix.lower() not in TEXT_EXTENSIONS or size > 16 * 1024 * 1024:
                continue
            data = pak.read(asset_path)
            if not any(marker in data for marker in (b"\xea", b"\xeb", b"\xec", b"\xed")):
                continue
            text = data.decode("utf-8", "replace")
            strings = list(extract_strings(text))
            if not strings:
                continue
            asset_count += 1
            for value in strings:
                rows.append((pak_path.name, pak.meta.get("name", ""), asset_path, value))
                frequency[value] += 1
                source_count += 1
        source_rows.append({
            "file": str(pak_path),
            "name": pak.meta.get("name"),
            "version": pak.meta.get("version"),
            "friendlyName": pak.meta.get("friendlyName"),
            "koreanAssets": asset_count,
            "koreanStrings": source_count,
        })

    with (args.output / "korean_strings.tsv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("pak", "sourceName", "assetPath", "koreanText"))
        writer.writerows(rows)

    with (args.output / "sources.json").open("w", encoding="utf-8") as handle:
        json.dump(source_rows, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    with (args.output / "frequency.tsv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("count", "koreanText"))
        for value, count in frequency.most_common():
            writer.writerow((count, value))

    print(json.dumps({
        "sources": len(source_rows),
        "assets": sum(row["koreanAssets"] for row in source_rows),
        "strings": len(rows),
        "uniqueStrings": len(frequency),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
