# Fix literal backslash-n sequences in arcana KO translations: convert the
# two-character escape to real newlines in data/arcana_work.tsv, then rewrite
# the corresponding 'replace' values inside the deployed pak's .patch entries.
import csv
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, "tools")
csv.field_size_limit(10 ** 8)

from pak import Pak  # noqa: E402
from pak_writer import write_pak  # noqa: E402

DEPLOY = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
TSV = "data/arcana_work.tsv"

rows = list(csv.reader(open(TSV, encoding="utf-8"), delimiter="\t"))
fixed_rows = 0
overrides_needed = {}  # patch entry name -> {en: ko} for rows that had escapes
for r in rows[1:]:
    if len(r) >= 4 and r[3] and "\\n" in r[3]:
        r[3] = r[3].replace("\\n", "\n")
        fixed_rows += 1
        overrides_needed.setdefault(r[0] + ".patch", {})[r[2]] = r[3]

with open(TSV, "w", encoding="utf-8", newline="") as f:
    csv.writer(f, delimiter="\t").writerows(rows)
print("rows fixed:", fixed_rows, "patch files:", len(overrides_needed))

p = Pak(DEPLOY)
overrides = {}
changed_ops = 0
for pn, mapping in overrides_needed.items():
    doc = json.loads(p.read(pn))

    def walk(node):
        global changed_ops
        if isinstance(node, dict):
            if node.get("op") == "replace" and isinstance(node.get("value"), str) and "\\n" in node["value"]:
                node["value"] = node["value"].replace("\\n", "\n")
                changed_ops += 1
        elif isinstance(node, list):
            for x in node:
                walk(x)

    walk(doc)
    overrides[pn] = json.dumps(doc, ensure_ascii=False).encode("utf-8")

print("replace ops fixed:", changed_ops)
try:
    print("entries:", write_pak(DEPLOY, DEPLOY, overrides))
except PermissionError:
    print("locked; tmp entries:", len(Pak(DEPLOY + ".tmp_write").index))
    sys.exit(3)
