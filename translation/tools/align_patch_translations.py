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

HANGUL = re.compile(r"[가-힣]")
LINE_COMMENT = re.compile(r"//[^\r\n]*")
BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
TRAILING_COMMA = re.compile(r",\s*([}\]])")


def parse_json(data):
    text = data.decode("utf-8")
    text = BLOCK_COMMENT.sub("", text)
    text = LINE_COMMENT.sub("", text)
    text = TRAILING_COMMA.sub(r"\1", text)
    return json.loads(text)


def resolve_pointer(document, pointer):
    current = document
    for raw_part in pointer.lstrip("/").split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            raise KeyError(pointer)
    return current


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("translation_pak", type=Path)
    parser.add_argument("source_paks", nargs="+", type=Path)
    args = parser.parse_args()

    translation = Pak(str(args.translation_pak))
    sources = [Pak(str(path)) for path in args.source_paks]
    rows = []
    counts = Counter()

    for patch_path in sorted(path for path in translation.index if path.endswith(".patch")):
        try:
            operations = parse_json(translation.read(patch_path))
        except (UnicodeDecodeError, json.JSONDecodeError):
            counts["unparsedPatch"] += 1
            continue
        if not isinstance(operations, list):
            continue
        target_path = patch_path[:-6]
        source = next((pak for pak in sources if target_path in pak.index), None)
        document = None
        if source:
            try:
                document = parse_json(source.read(target_path))
            except (UnicodeDecodeError, json.JSONDecodeError):
                counts["unparsedTarget"] += 1
        for operation in operations:
            if not isinstance(operation, dict):
                continue
            korean = operation.get("value")
            if not isinstance(korean, str) or not HANGUL.search(korean):
                continue
            pointer = operation.get("path", "")
            if source is None:
                status, original = "target-not-in-sources", ""
            elif document is None:
                status, original = "target-unparsed", ""
            else:
                try:
                    original = resolve_pointer(document, pointer)
                    status = "aligned-string" if isinstance(original, str) else "aligned-nonstring"
                except KeyError:
                    status, original = "path-missing", ""
            counts[status] += 1
            rows.append((patch_path, target_path, pointer, status,
                         source.meta.get("name", "") if source else "",
                         original if isinstance(original, str) else json.dumps(original, ensure_ascii=False),
                         korean))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("patchAsset", "targetAsset", "jsonPointer", "status", "sourceName",
                         "currentOriginal", "existingKorean"))
        writer.writerows(rows)
    print(json.dumps(counts, ensure_ascii=False))


if __name__ == "__main__":
    main()
