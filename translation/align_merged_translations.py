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
TEXT_EXTENSIONS = {
    ".activeitem", ".animation", ".behavior", ".cinematic", ".codex",
    ".config", ".consumable", ".frames", ".item", ".liquid", ".liqitem",
    ".matitem", ".monstertype", ".npctype", ".object", ".patch",
    ".projectile", ".questtemplate", ".recipe", ".species", ".stagehand",
    ".statuseffect", ".tech", ".tenant", ".tooltip", ".treasurepools",
    ".vehicle", ".weather",
}


def strip_json_comments(text):
    """Remove JSONC comments without touching comment markers inside strings."""
    output = []
    index = 0
    in_string = False
    escaped = False
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif char == '"':
            in_string = True
            output.append(char)
            index += 1
        elif char == "/" and next_char == "/":
            index += 2
            while index < len(text) and text[index] not in "\r\n":
                index += 1
        elif char == "/" and next_char == "*":
            index += 2
            while index + 1 < len(text) and text[index:index + 2] != "*/":
                index += 1
            index = min(index + 2, len(text))
        else:
            output.append(char)
            index += 1
    return "".join(output)


def remove_trailing_commas(text):
    """Remove commas before ] or } while preserving string contents."""
    output = []
    index = 0
    in_string = False
    escaped = False
    while index < len(text):
        char = text[index]
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if char == '"':
            in_string = True
            output.append(char)
            index += 1
            continue
        if char == ",":
            lookahead = index + 1
            while lookahead < len(text) and text[lookahead].isspace():
                lookahead += 1
            if lookahead < len(text) and text[lookahead] in "]}":
                index += 1
                continue
        output.append(char)
        index += 1
    return "".join(output)


def parse_json(data):
    text = data.decode("utf-8-sig")
    # Starbound accepts literal newlines/tabs in a number of dialogue strings.
    return json.loads(remove_trailing_commas(strip_json_comments(text)), strict=False)


def pointer_part(value):
    return str(value).replace("~", "~0").replace("/", "~1")


def walk_korean(value, pointer=""):
    if isinstance(value, str):
        if HANGUL.search(value):
            yield pointer, value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from walk_korean(child, f"{pointer}/{pointer_part(key)}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_korean(child, f"{pointer}/{index}")


def resolve_pointer(document, pointer):
    if pointer == "":
        return document
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


def patch_key(operation):
    if not isinstance(operation, dict):
        return None
    return operation.get("op"), operation.get("path"), operation.get("from")


def align_patch(legacy, current):
    """Match patch operations by semantic identity, falling back to array position."""
    current_by_key = {}
    if isinstance(current, list):
        for index, operation in enumerate(current):
            key = patch_key(operation)
            if key is not None:
                current_by_key.setdefault(key, []).append((index, operation))
    for legacy_index, operation in enumerate(legacy if isinstance(legacy, list) else []):
        for relative_pointer, korean in walk_korean(operation):
            key = patch_key(operation)
            matches = current_by_key.get(key, []) if key is not None else []
            if len(matches) == 1:
                current_index, current_operation = matches[0]
                try:
                    original = resolve_pointer(current_operation, relative_pointer)
                    yield f"/{legacy_index}{relative_pointer}", f"/{current_index}{relative_pointer}", "patch-key-match", original, korean
                except KeyError:
                    yield f"/{legacy_index}{relative_pointer}", "", "pointer-missing", "", korean
            elif isinstance(current, list) and legacy_index < len(current):
                try:
                    original = resolve_pointer(current[legacy_index], relative_pointer)
                    yield f"/{legacy_index}{relative_pointer}", f"/{legacy_index}{relative_pointer}", "patch-index-match", original, korean
                except KeyError:
                    yield f"/{legacy_index}{relative_pointer}", "", "pointer-missing", "", korean
            else:
                yield f"/{legacy_index}{relative_pointer}", "", "pointer-missing", "", korean


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("legacy_pak", type=Path)
    parser.add_argument("current_pak", type=Path)
    args = parser.parse_args()

    legacy_pak = Pak(str(args.legacy_pak))
    current_pak = Pak(str(args.current_pak))
    counts = Counter()
    rows = []
    diagnostics = []

    for asset_path, (_, size) in sorted(legacy_pak.index.items()):
        if Path(asset_path).suffix.lower() not in TEXT_EXTENSIONS or size > 16 * 1024 * 1024:
            continue
        data = legacy_pak.read(asset_path)
        if not any(marker in data for marker in (b"\xea", b"\xeb", b"\xec", b"\xed")):
            continue
        try:
            legacy_document = parse_json(data)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            counts["legacy-unparsed-assets"] += 1
            diagnostics.append((asset_path, "legacy-unparsed", str(error)))
            continue

        korean_values = list(walk_korean(legacy_document))
        if not korean_values:
            continue
        counts["legacy-korean-assets"] += 1
        counts["legacy-korean-strings"] += len(korean_values)

        if asset_path not in current_pak.index:
            counts["target-asset-missing"] += len(korean_values)
            rows.extend((asset_path, pointer, "", "target-asset-missing", "", korean)
                        for pointer, korean in korean_values)
            continue
        try:
            current_document = parse_json(current_pak.read(asset_path))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            counts["current-unparsed"] += len(korean_values)
            diagnostics.append((asset_path, "current-unparsed", str(error)))
            rows.extend((asset_path, pointer, "", "current-unparsed", "", korean)
                        for pointer, korean in korean_values)
            continue

        if asset_path.endswith(".patch"):
            aligned = align_patch(legacy_document, current_document)
        else:
            def align_regular():
                for pointer, korean in korean_values:
                    try:
                        yield pointer, pointer, "pointer-match", resolve_pointer(current_document, pointer), korean
                    except KeyError:
                        yield pointer, "", "pointer-missing", "", korean
            aligned = align_regular()

        for legacy_pointer, current_pointer, status, original, korean in aligned:
            if status in {"pointer-match", "patch-key-match", "patch-index-match"}:
                if isinstance(original, str):
                    if HANGUL.search(original):
                        status = "current-already-korean"
                    else:
                        status = status.replace("match", "string")
                else:
                    status = "matched-nonstring"
            counts[status] += 1
            rendered_original = original if isinstance(original, str) else (
                json.dumps(original, ensure_ascii=False) if original != "" else ""
            )
            rows.append((asset_path, legacy_pointer, current_pointer, status,
                         rendered_original, korean))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("assetPath", "legacyPointer", "currentPointer", "status",
                         "currentOriginal", "legacyKorean"))
        writer.writerows(rows)

    diagnostics_path = args.output.with_suffix(args.output.suffix + ".diagnostics.tsv")
    with diagnostics_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("assetPath", "status", "error"))
        writer.writerows(diagnostics)

    result = {
        "legacyFile": str(args.legacy_pak),
        "legacyName": legacy_pak.meta.get("name"),
        "currentFile": str(args.current_pak),
        "currentName": current_pak.meta.get("name"),
        "counts": dict(sorted(counts.items())),
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
