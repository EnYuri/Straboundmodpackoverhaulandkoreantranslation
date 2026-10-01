#!/usr/bin/env python3
"""Revert Korean-translated engine tokens back to their literal forms.

Starbound substitutes tokens like <selfname>, <entityname>, <itemName>,
<current>, <required>, <field>, <role>, <questGiver>, <enemy>,
<receivedItems>, <bounty name>, <elementname> at runtime. Translating
them makes the literal Korean text show up instead of the value.

Display-only pseudo-markers (<알 수 없음>, <<케모노 프렌즈>>, codex
redactions, npc subtitles) are intentionally left alone.
"""
import io, json, os, re, sys, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:/My Games/steamapps/common/Starbound")
sys.path.insert(0, "tools")
import pak, sbjson, pak_writer

MODS = r"E:/My Games/steamapps/common/Starbound/mods"
TR = os.path.join(MODS, "zz_translation_female.pak")

TOK = {
    "<현재>": "<current>",
    "<필요>": "<required>",
    "<필수>": "<required>",
    "<아이템 이름>": "<itemName>",
    "<자명>": "<selfname>",
    "<자신 이름>": "<selfname>",
    "<자기이름>": "<selfname>",
    "<실체명>": "<entityname>",
    "<실체이름>": "<entityname>",
    "<엔티티명>": "<entityname>",
    "<엔티티네임>": "<entityname>",
    "<엔터티이름>": "<entityname>",
    "<아이덴티티 이름>": "<entityname>",
    "<필드>": "<field>",
    "<받은아이템>": "<receivedItems>",
    "<현상금 이름>": "<bounty name>",
    "<퀘스트 부여자>": "<questGiver>",
    "<퀘스트 제공자>": "<questGiver>",
    "<적>": "<enemy>",
    "<원소명>": "<elementname>",
}

pk = pak.Pak(TR)
ov = {}
nfix = 0
for fn in sorted(pk.index):
    if not fn.endswith(".patch"):
        continue
    try:
        d = sbjson.parse_sb(pk.read(fn).decode("utf-8"))
    except Exception:
        continue
    n = 0
    def rec(o):
        global n, nfix
        if isinstance(o, list):
            for x in o:
                rec(x)
        elif isinstance(o, dict):
            v = o.get("value")
            if isinstance(v, str) and re.search(r"<[가-힯]", v):
                nv = v
                for a, b in TOK.items():
                    nv = nv.replace(a, b)
                if nv != v:
                    o["value"] = nv
                    n += 1
                    nfix += nv.count("<") - v.count("<") + 1
            for x in o.values():
                if isinstance(x, (list, dict)):
                    rec(x)
    rec(d)
    if n:
        ov[fn] = json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        print(fn[-55:], n)
print("files:", len(ov))
del pk
if "--apply" in sys.argv and ov:
    staged = TR + ".staged"
    pak_writer.write_pak(staged, TR, ov)
    for i in range(60):
        try:
            os.replace(staged, TR)
            print("replaced")
            break
        except PermissionError:
            time.sleep(5)
else:
    print("dry-run")
