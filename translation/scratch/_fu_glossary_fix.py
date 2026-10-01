# Batch46 glossary corrections: 팝탑->팝톱, 콰이에투스->콰이어투스, 텔레브리움->텔레브리엄
# inside the deployed pak's replace values, then mirror to data TSVs.
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, "tools")
from pak import Pak  # noqa: E402
from pak_writer import write_pak  # noqa: E402

DEPLOY = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
FIX = [("팝탑", "팝톱"), ("콰이에투스", "콰이어투스"), ("텔레브리움", "텔레브리엄")]

p = Pak(DEPLOY)
overrides = {}
count = 0
for name in p.index:
    if not name.endswith(".patch"):
        continue
    raw = p.read(name)
    try:
        doc = json.loads(raw)
    except Exception:
        continue
    changed = False

    def walk(node):
        global count, changed
        if isinstance(node, dict):
            v = node.get("value")
            if node.get("op") == "replace" and isinstance(v, str):
                for a, b in FIX:
                    if a in v:
                        node["value"] = v = v.replace(a, b)
                        changed = True
                        count += 1
        elif isinstance(node, list):
            for x in node:
                walk(x)

    walk(doc)
    if changed:
        overrides[name] = json.dumps(doc, ensure_ascii=False).encode("utf-8")

print("ops fixed:", count, "files:", len(overrides))
try:
    print("entries:", write_pak(DEPLOY, DEPLOY, overrides))
except PermissionError:
    print("locked; tmp:", len(Pak(DEPLOY + ".tmp_write").index))
    sys.exit(3)

# mirror in data files
for path in ["data/fu_work.tsv", "data/fu_ko.tsv", "data/fu_ko2.tsv", "data/fu_ko3.tsv"]:
    s = open(path, encoding="utf-8").read()
    orig = s
    for a, b in FIX:
        s = s.replace(a, b)
    if s != orig:
        open(path, "w", encoding="utf-8").write(s)
        print("updated", path)
