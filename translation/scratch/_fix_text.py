# -*- coding: utf-8 -*-
# Fix in-place: for patch ops where a test op value == EN, set the following
# replace op's value to the full KO translation. Used to repair ops written by
# _apply.py whose KO was truncated to the repr() preview length.
import sys, io, csv, json, os, time, pickle, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:/My Games/steamapps/common/Starbound")
sys.path.insert(0, "tools")
import pak, sbjson, pak_writer

TR = r"E:/My Games/steamapps/common/Starbound/mods/zz_translation_female.pak"
csv.field_size_limit(10**7)

sys.path.insert(0, "scratch")
from _ko_text import KO

SL = pickle.load(open("scratch/_vals_text_1cb2.pkl", "rb"))

# entry 91: glitchy 'of of of...' tail — mirror with repeated 의
v91 = SL[91]
head = v91[:v91.index("product")] + "product"
ofn = len([t for t in v91.split(" ") if t == "of"])
KO[91] = ("축적된 평판과 목격담 덕분에, 이 몬스터는 '글리치톱'이라는 별명을 얻었다. "
          "이들은 " + "의 " * ofn + "산물일 수 있다고 추측된다.")
# entry 424: Chinese log line, keep as-is
KO[424] = SL[424]

FIX = {}    # en -> ko for indices already applied via _apply (0-320)
NEW = {}    # en -> ko for indices not yet applied (321-424)
for i, v in enumerate(SL):
    if i <= 320:
        FIX[v] = KO[i]
    else:
        NEW[v] = KO[i]

pk = pak.Pak(TR)
ov = {}
fixed = collections.Counter()
for fn in pk.index:
    if not fn.endswith(".patch"):
        continue
    try:
        d = sbjson.parse_sb(pk.read(fn).decode("utf-8-sig"))
    except Exception:
        continue
    if not isinstance(d, list):
        continue
    changed = False

    def walk(lst):
        global changed
        for i, op in enumerate(lst):
            if isinstance(op, dict):
                if (op.get("op") == "replace" and i > 0
                        and isinstance(lst[i-1], dict)
                        and lst[i-1].get("op") == "test"
                        and isinstance(lst[i-1].get("value"), str)
                        and lst[i-1]["value"] in FIX):
                    nv = FIX[lst[i-1]["value"]]
                    if op["value"] != nv:
                        op["value"] = nv
                        changed = True
                        fixed[fn] += 1
            elif isinstance(op, list):
                walk(op)

    walk(d)
    if changed:
        ov[fn] = json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
del pk

print("files fixed:", len(ov), "ops:", sum(fixed.values()))
if ov:
    pak_writer.write_pak(TR + ".staged", TR, ov)
    for i in range(60):
        try:
            os.replace(TR + ".staged", TR)
            print("replaced")
            break
        except PermissionError:
            time.sleep(5)

# write apply TSV for the new range
w = csv.writer(open("data/_uncov_ko_tx4.tsv", "w", encoding="utf-8", newline=""), delimiter="\t")
w.writerow(["en", "ko"])
for en, k in NEW.items():
    w.writerow([en, k])
print("new tsv:", len(NEW))
