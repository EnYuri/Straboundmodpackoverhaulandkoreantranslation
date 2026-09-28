"""Fourth glossary-consistency batch fix (2026-09-28 item-name/description
priority QA pass, continued after batch2/3). Sourced from a re-run of
qa_pak_glossary.py against the pak_pairs.tsv extracted post-batch3.

Several entries here are deliberately scoped to full-phrase or asset-specific
substrings rather than bare terms, because the bare Korean form legitimately
overlaps with an accepted alternative elsewhere in the same glossary term
(e.g. "프로텍터레이트" is an accepted alternative for the Terrene Protectorate
row and must not be touched when it appears in that context) or because the
bare form is dangerously short/common (e.g. bare "텔" collides with
텔레포터/텔레비전/etc.).

Terms surveyed but intentionally left unchanged (false positives or
judgment calls, not touched by this batch):
- Old One: all report hits are either generic "an old one" / "the old one"
  English phrases (unrelated to the Centens deity), or the codex's own
  "고대인" contextual variant, which the glossary note explicitly allows
  ("문맥에 따라 조정 가능").
- Floran (floranDescription fields): the vanilla-style third-person
  Floran-speak flavor text is deliberately rewritten as normal narration
  without needing the literal race-name word present; not a bug.
- Trink (MEGA-TRINK): a stylized ALL-CAPS in-universe model/brand name,
  same convention as other preserved weapon model names; not the race noun.
- Spooked: both hits are natural conjugations/negations of the correct
  겁먹- stem ("안 놀랐다", "겁먹었다"), not the banned "추격당함" alternate;
  acceptable variation of the status-effect term in flavor dialogue.
- One-Handed: the "~: 한 손으로 사용." tag phrasing is a consistent,
  deliberate convention shared identically across all matching items (verb
  phrase, not the attributive-before-noun case the glossary note describes).
- Fuel Hatch (연료 주입구 vs glossary's 연료 해치): confined to Sexbound-adjacent
  interface titles (aphroditesbow/sexbound_reassembler/sexbound_runicassembler)
  where "주입구" reads as a probable intentional innuendo pun; left alone
  pending explicit confirmation rather than silently overwritten.
- Alliance (generic "alliance"/"동맹"/"연합" as a common English noun): the
  qa script matches the word case-insensitively, so most of the 30 hits are
  ordinary lowercase "alliance" in Saturnian/Miniknog/Grineer/GIC/Youkai
  contexts unrelated to the Elithian faction proper noun. Only instances
  whose asset path or surrounding context unambiguously names the Elithian
  Alliance faction are fixed below; the rest are left as natural Korean.
- Miniknog Stronghold ("지식부 요새", 57 hits): still an open judgment call
  from batch2/3, deferred.
"""
import json
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

SRC_PAK = STAR / "mods" / "female_translation.pak"
OUT_PAK = STAR / "translation" / "translation-baseline-20260921" / "female_translation.pak.NEW8"

REPLACEMENTS = [
    # Thelean -> 텔레안 (targeted; bare "텔" is too short/common to touch globally)
    ("텔레아 베소메이어", "텔레안 베소메이어"),
    ("텔레아", "텔레안"),
    ("텔의 무기와 일치한다", "텔레안 무기와 일치한다"),
    ("텔의 함선", "텔레안 함선"),
    # Protectorate -> 보호국 (targeted; bare "프로텍터레이트" also appears as an
    # accepted Terrene Protectorate alternative elsewhere in this same asset
    # and must not be touched there)
    ("프로텍터레이트만이 아니야", "보호국만이 아니야"),
    ("프로텍터레이트 네트워크에 연결할 수 없음", "보호국 네트워크에 연결할 수 없음"),
    # Elithian Alliance -> 엘리시안 얼라이언스 (additional wrong variants found
    # in this batch beyond batch2's list)
    ("엘리시아 연합", "엘리시안 얼라이언스"),
    ("얼라이언스의 문장이 새겨진 깃발.", "엘리시안 얼라이언스의 문장이 새겨진 깃발."),
    # Alliance (Elithian, fixed rule) -> 얼라이언스; scoped to unambiguous
    # Elithian-faction-namespace strings only, not generic "alliance" prose
    ("언젠가는 그들도 연합에 가입하면 좋겠어.", "언젠가는 그들도 얼라이언스에 가입하면 좋겠어."),
    ("연합에서 승무원 모집", "얼라이언스에서 승무원 모집"),
    ("계약서로 연합 승무원 모집", "계약서로 얼라이언스 승무원 모집"),
    ("연합 전자기기에 사용되는", "얼라이언스 전자기기에 사용되는"),
    ("통합 연합 제작대", "통합 얼라이언스 제작대"),
    ("연합과 보호국 사이의 무역로", "얼라이언스와 보호국 사이의 무역로"),
    # Relic Seeker -> 유물 탐구자 (렐릭 시커 explicitly banned by glossary;
    # majority usage already 유물 탐구자, this fixes the minority)
    ("렐릭 시커", "유물 탐구자"),
    # Aegisalt -> 에지솔트
    ("이지설트", "에지솔트"),
    # Magilock -> 매지락 (two distinct wrong forms)
    ("마지록", "매지락"),
    ("마기록", "매지락"),
    # Magishot -> 매지샷 (two distinct wrong forms)
    ("매직샷", "매지샷"),
    ("마법탄", "매지샷"),
    # gheatsyn -> 기트신 (superseded ad-hoc guess predating the 2026-09-23 term decision)
    ("게아신", "기트신"),
    # Kel'chis -> 켈치스
    ("켈키스", "켈치스"),
    # Jorgasian -> 조가시안
    ("조르가시아", "조가시안"),
    # Notician Federation -> 노틱스 연방
    ("노티시안 연방", "노틱스 연방"),
    # Mehros Avan -> 메로스 아반
    ("메흐로스 아반", "메로스 아반"),
    # Grand Protector -> 대보호자 (three distinct wrong forms; majority is
    # already 대보호자, 79 vs these minorities)
    ("대호보자", "대보호자"),
    ("대수호자", "대보호자"),
    ("대프로텍터", "대보호자"),
    # Trink Circuit -> 트링크 서킷 (longer "중앙" form first)
    ("트링크 중앙 회로", "트링크 중앙 서킷"),
    ("트링크 회로", "트링크 서킷"),
    # Crafting Station -> 제작대
    ("제작 스테이션", "제작대"),
    # Sniper Rifle -> 저격소총 (no space)
    ("저격 소총", "저격소총"),
    # Quietus -> 콰이어투스
    ("쿠에투스", "콰이어투스"),
]


def _vlqr(d, p):
    r = 0
    while True:
        b = d[p]; p += 1
        r = (r << 7) | (b & 0x7F)
        if not b & 0x80:
            return r, p


def _key(d, p):
    l, p = _vlqr(d, p)
    return p + l


def _val(d, p):
    t = d[p]; p += 1
    if t == 0x05:
        l, p = _vlqr(d, p); return p + l
    if t == 0x04:
        _, p = _vlqr(d, p); return p
    if t == 0x06:
        c, p = _vlqr(d, p)
        for _ in range(c):
            p = _val(d, p)
        return p
    if t == 0x01:
        c, p = _vlqr(d, p)
        for _ in range(c):
            p = _key(d, p); p = _val(d, p)
        return p
    if t == 0x00:
        return p
    if t == 0x02:
        return p + 1
    if t == 0x03:
        return p + 8
    raise ValueError(f"dynval type {t:#x} at {p - 1}")


def vlq(n):
    parts = []
    while True:
        parts.append(n & 0x7F)
        n >>= 7
        if not n:
            break
    out = bytearray()
    for i, b in enumerate(reversed(parts)):
        out.append(b | (0x80 if i < len(parts) - 1 else 0))
    return bytes(out)


def replace_in_value(v):
    if isinstance(v, str):
        changed = False
        for old, new in REPLACEMENTS:
            if old in v:
                v = v.replace(old, new)
                changed = True
        return v, changed
    if isinstance(v, list):
        changed = False
        out = []
        for item in v:
            nv, c = replace_in_value(item)
            out.append(nv)
            changed = changed or c
        return out, changed
    if isinstance(v, dict):
        changed = False
        out = {}
        for k, item in v.items():
            nv, c = replace_in_value(item)
            out[k] = nv
            changed = changed or c
        return out, changed
    return v, False


def main():
    d0 = SRC_PAK.read_bytes()
    off0 = struct.unpack(">Q", d0[8:16])[0]
    assert d0[off0:off0 + 5] == b"INDEX"
    p = off0 + 5
    pairs, p = _vlqr(d0, p)
    for _ in range(pairs):
        p = _key(d0, p)
        p = _val(d0, p)
    meta_blob = d0[off0:p]

    src = Pak(str(SRC_PAK))
    files = {name: src.read(name) for name in src.index}
    print("base pak entries:", len(files))

    needles = [old.encode("utf-8") for old, _ in REPLACEMENTS]
    assets_changed = 0
    for name in sorted(files):
        if not name.endswith(".patch"):
            continue
        data = files[name]
        if not any(n in data for n in needles):
            continue
        try:
            doc = json.loads(data)
        except Exception:
            continue
        new_doc, changed = replace_in_value(doc)
        if changed:
            files[name] = json.dumps(new_doc, ensure_ascii=False).encode("utf-8")
            assets_changed += 1
            print("fixed", name)

    buf = bytearray(b"SBAsset6" + b"\x00" * 8)
    index_entries = []
    for name in sorted(files):
        data = files[name]
        off = len(buf)
        buf += data
        index_entries.append((name.encode("utf-8"), off, len(data)))

    index_off = len(buf)
    buf += meta_blob
    buf += vlq(len(index_entries))
    for name, off, n in index_entries:
        buf += vlq(len(name)) + name + struct.pack(">QQ", off, n)
    buf[8:16] = struct.pack(">Q", index_off)

    OUT_PAK.write_bytes(bytes(buf))
    print("assets changed:", assets_changed)
    print("wrote", OUT_PAK, len(buf), "bytes,", len(index_entries), "entries")


if __name__ == "__main__":
    main()
