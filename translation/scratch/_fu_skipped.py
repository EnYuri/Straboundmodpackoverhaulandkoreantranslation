# List fu_work.tsv rows that apply skipped (field not a top-level str),
# then resolve their real JSON pointer paths for manual patch entries.
import csv
import io
import json
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
csv.field_size_limit(10 ** 8)
from pak import Pak  # noqa: E402

pk = Pak(r"E:\My Games\steamapps\common\Starbound\mods\FrackinUniverse_contents_729480149.pak")


def parse_sb(raw):
    s = raw.decode("utf-8", "replace")
    s = re.sub(r"//[^\n]*", "", s)
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    out = []
    ins = False
    for i, c in enumerate(s):
        if c == '"' and (i == 0 or s[i - 1] != chr(92)):
            ins = not ins
        out.append("\\r" if ins and c == "\r" else "\\n" if ins and c == "\n" else c)
    return json.loads(re.sub(r",(\s*[}\]])", r"\1", "".join(out)))


def find(o, target, path=""):
    res = []
    if isinstance(o, dict):
        for k, v in o.items():
            p = path + "/" + k
            if isinstance(v, str) and v == target:
                res.append((p, v))
            else:
                res += find(v, target, p)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            res += find(x, target, f"{path}/{i}")
    return res


for r in csv.reader(open("data/fu_work.tsv", encoding="utf-8"), delimiter="\t"):
    if len(r) < 4 or not r[3]:
        continue
    try:
        doc = parse_sb(pk.read(r[0]))
    except Exception:
        print("PARSE FAIL", r[0])
        continue
    if not isinstance(doc.get(r[1]), str):
        print(r[0][-55:], "|", r[1], "|", r[2][:45])
        for pp, v in find(doc, r[2]):
            print("    ptr:", pp)
