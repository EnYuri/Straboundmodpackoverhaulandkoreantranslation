import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parents[3]
sys.path.insert(0, str(ROOT))
from pak import Pak
from align_merged_translations import parse_json, pointer_part

TEXT_EXTENSIONS = {
    ".activeitem", ".behavior", ".cinematic", ".codex", ".config",
    ".consumable", ".item", ".liquid", ".liqitem", ".matitem",
    ".monstertype", ".npctype", ".object", ".patch", ".projectile",
    ".questtemplate", ".radiomessages", ".recipe", ".species", ".stagehand",
    ".statuseffect", ".tech", ".tenant", ".tooltip", ".treasurepools",
    ".vehicle", ".weaponability", ".weather",
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
def candidate(value):
    if not isinstance(value, str) or HANGUL.search(value) or not ASCII_WORD.search(value):
        return False
    stripped = value.strip()
    if not stripped or stripped.startswith(("/", "?", "$", "scripts/")):
        return False
    if re.fullmatch(r"[A-Za-z0-9_.:+-]+", stripped) and " " not in stripped:
        return False
    return True


def walk(node, pointer=""):
    if isinstance(node, dict):
        is_patch_operation = {"op", "path", "value"}.issubset(node)
        if is_patch_operation:
            leaf = str(node["path"]).rstrip("/").split("/")[-1].lower()
            value = node["value"]
            if leaf in VISIBLE_KEYS and candidate(value):
                yield f"{pointer}/value", value
        for key, value in node.items():
            child = f"{pointer}/{pointer_part(key)}"
            if not (is_patch_operation and key == "value") and key.lower() in VISIBLE_KEYS and candidate(value):
                yield child, value
            yield from walk(value, child)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk(value, f"{pointer}/{index}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("paks", nargs="*", type=Path)
    parser.add_argument("--pak-dir", action="append", type=Path, default=[])
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    pak_paths = list(args.paks)
    for pak_dir in args.pak_dir:
        pak_paths.extend(sorted(pak_dir.glob("*.pak")))

    rows = []
    summary = []
    for pak_path in pak_paths:
        pak = Pak(str(pak_path))
        count = 0
        assets = set()
        seen = set()
        for asset_path, (_, size) in pak.index.items():
            if Path(asset_path).suffix.lower() not in TEXT_EXTENSIONS or size > 16 * 1024 * 1024:
                continue
            raw = pak.read(asset_path)
            if not any(65 <= byte <= 90 or 97 <= byte <= 122 for byte in raw[:4096]):
                continue
            try:
                document = parse_json(raw)
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            for pointer, value in walk(document):
                identity = (asset_path, pointer, value)
                if identity in seen:
                    continue
                seen.add(identity)
                rows.append((pak_path.name, pak.meta.get("name", ""), asset_path, pointer, value))
                assets.add(asset_path)
                count += 1
        summary.append({
            "file": pak_path.name,
            "name": pak.meta.get("name"),
            "friendlyName": pak.meta.get("friendlyName"),
            "candidateAssets": len(assets),
            "candidateStrings": count,
        })

    with (args.output / "translatable_candidates.tsv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("pak", "sourceName", "assetPath", "jsonPointer", "englishText"))
        writer.writerows(rows)
    with (args.output / "mod_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    totals = Counter()
    totals["mods"] = len(summary)
    totals["candidateMods"] = sum(1 for row in summary if row["candidateStrings"])
    totals["assets"] = sum(row["candidateAssets"] for row in summary)
    totals["strings"] = len(rows)
    print(json.dumps(totals, ensure_ascii=False))


if __name__ == "__main__":
    main()
