#!/usr/bin/env python3
# Apply translations for all remaining mods (scan_remaining.py output).
#   regular-asset rows -> grouped overlay ops  -> mods/localeko_rest.pak
#   .patch-asset rows  -> per-source span-edit repack TSVs
#
# Phases:
#   (default)   resolve Koreans, write overlay source tree + repack TSVs, print stats
#   --pack      pack the overlay tree into mods/localeko_rest.pak
#   --repack    run every pending span-edit repack (backs up originals)
import csv, json, re, shutil, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from pak import Pak
from align_merged_translations import parse_json
from jsonc_spans import parse_spans, navigate, _unescape
from pick_tm_multi import pick

MODS = ROOT / "mods"
WORK = ROOT / "translation" / "translation-rest-20260922"
OVERLAY_SRC = WORK / "source" / "female_translation"
OVERLAY_PAK = MODS / "female_translation.pak"
REPACK_DIR = WORK / "repack"
BACKUP = Path(r"E:\Desktop\mods\replaced-installed-20260922\rest-repacks")
STAGE = ROOT / "translation" / "rest-stage"

MANUAL_EXTRA = {
    "Assault Rifle": "돌격소총",
    "MATERIALS AVAILABLE": "사용 가능한 재료",
    "50% of Pixels Lost": "픽셀의 50% 손실",
    "Detail colour": "세부 색상",
}

# glitch-style "<Emotion>. <sentence>" composition: reuse translated bodies
PREFIX_KO = {
    "Demanding": "요구", "Lustful": "음란", "Observant": "관찰", "Horny": "욕정",
    "Needy": "갈망", "Shocked": "충격", "Lecherous": "음란", "Greedy": "욕심",
    "Arrogant": "오만", "Questioning": "질문", "Ticklish": "간지러움",
    "Pleased": "기쁨", "Unsure": "불안", "Naughty": "음란", "Stunned": "기절",
    "Gluttonus": "탐욕", "Mixed": "혼합", "Curious": "호기심",
    "Cautious": "조심", "Worried": "걱정", "Amazed": "놀람", "Excited": "흥분",
    "Confused": "혼란", "Thoughtful": "심사숙고", "Annoyed": "짜증",
    "Happy": "기쁨", "Sad": "슬픔", "Angry": "분노", "Calm": "차분",
    "Panicked": "당황", "Relieved": "안도", "Surprised": "놀람",
    "Analytical": "분석", "Informative": "정보", "Interested": "흥미",
    "Jealous": "질투", "Fearful": "공포", "Bored": "지루",
    "Affirmative": "확인", "Regretful": "후회", "Nostalgic": "감상적",
    "Emotional": "감정적", "Doubtful": "의심", "Terrified": "공포",
    "Neutral": "중립", "Analyse": "분석 중", "Analyze": "분석 중",
    "Descriptive": "묘사", "Observation": "관찰", "Observed": "관찰",
    "Hopeful": "희망", "Amused": "흥미", "Delighted": "기쁨",
    "Frustrated": "좌절", "Sarcastic": "빈정", "Sincere": "진심",
    "Impressed": "감탄", "Disappointed": "실망", "Warning": "경고",
    "Statement": "진술", "Disgust": "혐오", "Regret": "후회",
    "Sly": "교활", "Eager": "열정", "Proud": "자랑", "Sleepy": "졸림",
    "Determined": "결의", "Grateful": "감사", "Nervous": "긴장",
    "Suspicious": "의심", "Wistful": "아쉬움", "Insistent": "고집",
    "Playful": "장난", "Impatient": "조급", "Resigned": "체념",
    "Smug": "의기양양", "Cold": "냉담", "Gentle": "온화",
    "Alert": "경고", "Alarmed": "경계", "Affectionate": "애정",
    "Amicable": "우호", "Anticipating": "기대", "Aroused": "흥분",
    "Assertive": "단호", "Authoritative": "위엄", "Blasphemous": "신성모독",
    "Blastphemus": "신성모독", "Boastful": "자랑", "Brash": "거침",
    "Carnal": "육욕", "Charmed": "매혹", "Chilled": "냉기",
    "Climaxing": "절정", "Commanding": "지배", "Compliment": "칭찬",
    "Complimenting": "칭찬", "Confessing": "고백", "Conflicted": "갈등",
    "Convivial": "친근", "Coy": "수줍", "Crass": "천박", "Dazed": "멍함",
    "Desperate": "절박", "Dominant": "지배", "Dominating": "지배",
    "Domineering": "오만", "Enamoured": "매료", "Energized": "활기",
    "Extactic": "황홀", "Frightened": "공포", "Heated": "달아오름",
    "Helpful": "도움", "Humorus": "익살", "Inquisitive": "호기심",
    "Intrigued": "호기심", "Intoxicated": "취함", "Joyous": "환희",
    "Kindly": "친절", "Lascivious": "음탕", "Lewd": "음란",
    "Loving": "애정", "Offering": "헌납", "Overheating": "과열",
    "Overheated": "과열", "Perplexed": "당혹", "Pleasured": "쾌락",
    "Preparing": "준비", "Prideful": "자랑", "Punny": "말장난",
    "Randy": "흥분", "Ravished": "도취", "Satisfied": "만족",
    "Serious": "진지", "Stern": "엄격", "Teasing": "도발",
    "Urgent": "긴급", "Admiration": "감탄", "Praise": "찬양",
    "Concerned": "걱정", "Saturated": "포화", "Double Climax": "동시 절정",
    "Proud demeanor": "자랑스러운 태도", "Hungrily mating": "굶주린 교미",
}
PREFIX_RE = re.compile(r"^([A-Z][a-z]+(?:\s+[a-z]+)*)\.\s+(.+)$", re.S)
DNA_RE = re.compile(r"^(.+?) DNA acquired!$", re.S)

RACE_KO = {
    "Apex": "에이펙스", "Avian": "에이비언", "Floran": "플로란", "Human": "인간",
    "Hylotl": "힐로틀", "Glitch": "글리치", "Novakid": "노바키드",
    "Neki": "네키", "Neko": "네코", "Felin": "페린", "Fenerox": "페네록스",
    "Kitsune": "키츠네", "Deerkin": "디어킨", "Bunnykin": "버니킨",
    "Mauskin": "마우스킨", "Penguin": "펭귄", "Argonian": "아르고니안",
    "Braxien": "브락시엔", "Demonic": "악마", "Eevee": "이브이",
    "Everis": "에베리스", "Familiar": "패밀리어", "Gardevan": "가데반",
    "Kemono": "케모노", "Ruin": "루인", "Unknown": "미상",
    "Avali": "아발리", "Slimeperson": "슬라임인", "Viera": "비에라",
    "Lucario": "루카리오", "Lamia": "라미아", "Saturn": "새턴",
    "Elithian": "엘리시안", "Alta": "알타", "Shellguard": "셸가드",
    "Aegi": "아에기", "Akkimari": "아키마리", "Annelisk": "아넬리스크",
    "Centens": "센텐스", "Draunaar": "드라우나르", "Droden": "드로덴",
    "Hyvon": "하이본", "Juux": "주우크스", "Noolith": "눌리스",
    "Notix": "노틱스", "Satkyterran": "새트키테란", "Trink": "트링크",
    "Lustling": "러스틀링", "Nekololis": "네코롤리스", "Woofie": "우피",
}


def derive_korean(eng, en2ko, depth=0):
    """try to compose a translation from known parts"""
    key = norm_key(eng)
    if key in en2ko:
        return en2ko[key]
    m = DNA_RE.match(key)
    if m and m.group(1).strip() in RACE_KO:
        return f"{RACE_KO[m.group(1).strip()]} DNA 확보!"
    if depth < 2:
        m = PREFIX_RE.match(key)
        if m and m.group(1) in PREFIX_KO:
            rest = derive_korean(m.group(2), en2ko, depth + 1)
            if rest:
                return f"{PREFIX_KO[m.group(1)]}. {rest}"
    for sep in (" »", " ..."):
        if key.endswith(sep):
            base = en2ko.get(norm_key(key[:-len(sep)]))
            if base:
                return base + sep
    return ""


def norm_key(s):
    return s.strip().replace("\r\n", "\n")


def load_en2ko():
    en2ko = {}
    def add(eng, kor):
        k = norm_key(eng)
        if k and kor and k not in en2ko:
            en2ko[k] = kor
    for fn, ec, kc in (("legacy_translation_memory.tsv", "currentOriginal", "legacyKorean"),
                       ("translation_memory.tsv", "currentOriginal", "existingKorean")):
        for r in csv.DictReader(open(HERE / fn, encoding="utf-8-sig", newline=""), delimiter="\t"):
            add(r[ec], r[kc])
    # earlier applied batches
    wl = [r["englishText"] for r in csv.DictReader(
        open(HERE / "worklist_new.tsv", encoding="utf-8-sig", newline=""), delimiter="\t")]
    for bf in sorted((HERE / "translations").glob("batch_*.tsv")):
        for r in csv.reader(open(bf, encoding="utf-8-sig", newline=""), delimiter="\t"):
            if len(r) >= 2 and r[0].isdigit() and int(r[0]) < len(wl):
                add(wl[int(r[0])], r[1])
    id2eng = {r["id"]: r["englishText"] for r in csv.DictReader(
        open(HERE / "missed_worklist.tsv", encoding="utf-8-sig", newline=""), delimiter="\t")}
    for bf in sorted((HERE / "translations").glob("missed_*.tsv")):
        for r in csv.reader(open(bf, encoding="utf-8-sig", newline=""), delimiter="\t"):
            if len(r) >= 2 and r[0] != "id":
                add(id2eng.get(r[0], ""), r[1])
    p = HERE / "tm_multi_chosen.tsv"
    if p.exists():
        for r in csv.DictReader(open(p, encoding="utf-8-sig", newline=""), delimiter="\t"):
            add(r["english"], r["chosen"])
    # rest worklist batches (id -> row in rest_worklist.tsv)
    id2eng = {}
    with open(HERE / "rest_worklist.tsv", encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            id2eng[r["id"]] = r["englishText"]
    for bf in sorted((HERE / "translations").glob("rest_*.tsv")):
        for r in csv.reader(open(bf, encoding="utf-8-sig", newline=""), delimiter="\t"):
            if len(r) >= 2 and r[0] != "id":
                add(id2eng.get(r[0], ""), r[1])
    return en2ko


def resolve_targets(en2ko):
    """returns overlay_ops{asset:[ops]}, repack{source:[(asset,ptr,eng,kor)]}, stats"""
    overlay_ops = defaultdict(list)
    repack = defaultdict(list)
    conflicts = []
    stats = Counter()
    seen = {}
    for r in csv.DictReader(open(HERE / "rest_targets.tsv", encoding="utf-8-sig", newline=""), delimiter="\t"):
        src, asset, ptr, eng = r["sourceMod"], r["assetPath"], r["jsonPointer"], r["englishText"]
        cat = r["tmCategory"]
        man = MANUAL_EXTRA.get(norm_key(eng))
        if cat == "tm-single":
            kor = man or r["suggestedKorean"]
        elif cat == "tm-multi":
            cands = [c.strip() for c in r["suggestedKorean"].split(" || ") if c.strip()]
            kor = man or (pick(cands, ptr, eng) if cands else "")
        else:
            kor = man or derive_korean(eng, en2ko)
        if not kor:
            stats[f"missing:{cat}"] += 1
            continue
        if r["inPatchAsset"] == "1":
            repack[src].append((asset, ptr, eng, kor))
            stats["repack-target"] += 1
            continue
        key = (asset, ptr)
        if key in seen:
            if seen[key] != kor:
                conflicts.append((src, asset, ptr, eng, seen[key], kor))
                stats["conflict"] += 1
            continue
        seen[key] = kor
        overlay_ops[asset].append([
            {"op": "test", "path": ptr, "value": eng},
            {"op": "replace", "path": ptr, "value": kor},
        ])
        stats["overlay-op"] += 1
    return overlay_ops, repack, conflicts, stats


def collect_mod_names():
    """every installed mod's metadata name (for the includes load-order list)"""
    names = []
    for d in MODS.iterdir():
        if d.is_dir():
            mf = d / "_metadata"
            if mf.exists():
                try:
                    names.append(json.loads(mf.read_text(encoding="utf-8-sig")).get("name"))
                except Exception:
                    pass
        elif d.suffix == ".pak" and d.name != OVERLAY_PAK.name:
            try:
                names.append(Pak(str(d)).meta.get("name"))
            except Exception:
                pass
    return sorted({n for n in names if n and n not in ("localeko_rest", "female_translation")})


def write_outputs(overlay_ops, repack):
    n_files = 0
    for asset, groups in overlay_ops.items():
        pf = OVERLAY_SRC / (asset.lstrip("/") + ".patch")
        pf.parent.mkdir(parents=True, exist_ok=True)
        pf.write_text(json.dumps(groups, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        n_files += 1
    meta = OVERLAY_SRC / "_metadata"
    meta.write_text(json.dumps({
        "name": "female_translation",
        "friendlyName": "Korean Overhaul Translation",
        "version": "2026-09-27.1",
        "author": "local maintenance",
        "description": "Auto-generated Korean translation overlay covering remaining content mods.",
        "includes": collect_mod_names(),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPACK_DIR.mkdir(parents=True, exist_ok=True)
    for src, rows in repack.items():
        safe = re.sub(r"[^A-Za-z0-9_.-]", "_", src)
        with open(REPACK_DIR / f"{safe}.tsv", "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh, delimiter="\t", lineterminator="\n")
            w.writerow(("assetPath", "jsonPointer", "englishText", "koreanText"))
            w.writerows(rows)
    return n_files


def pack_overlay():
    if OVERLAY_PAK.exists():
        OVERLAY_PAK.unlink()
    subprocess.run([str(ROOT / "win" / "asset_packer.exe"),
                    str(OVERLAY_SRC), str(OVERLAY_PAK), "-s"], check=True)
    print("packed", OVERLAY_PAK)


def span_edit_text(text, edits):
    """edits: [(pointer, orig, kor)] -> (new_text, counts)"""
    counts = Counter()
    root = parse_spans(text)
    spans = []
    for pointer, orig, kor in edits:
        try:
            node = navigate(root, pointer)
        except (KeyError, IndexError, ValueError):
            counts["pointer-missing"] += 1
            continue
        if node.kind != "string":
            counts["not-a-string"] += 1
            continue
        plain = _unescape(text[node.start + 1:node.end - 1])
        if norm_key(plain) != norm_key(orig):
            counts["text-mismatch"] += 1
            continue
        if "\r\n" in plain:
            kor = kor.replace("\n", "\r\n")
        spans.append((node.start, node.end, kor))
    for start, end, kor in sorted(spans, key=lambda s: -s[0]):
        text = text[:start] + json.dumps(kor, ensure_ascii=False) + text[end:]
        counts["applied"] += 1
    return text, counts


def run_repacks():
    totals = Counter()
    STAGE.mkdir(parents=True, exist_ok=True)
    for tsv in sorted(REPACK_DIR.glob("*.tsv")):
        rows = [r for r in csv.DictReader(open(tsv, encoding="utf-8-sig", newline=""), delimiter="\t")]
        if not rows:
            continue
        # source name was sanitized; find matching source in mods/
        safe = tsv.stem
        src = None
        for d in MODS.iterdir():
            tag = d.name + "/" if d.is_dir() else d.name
            if re.sub(r"[^A-Za-z0-9_.-]", "_", tag) == safe:
                src = d
                break
        if src is None:
            totals[f"missing-source:{safe}"] += len(rows)
            continue
        by_asset = defaultdict(list)
        for r in rows:
            by_asset[r["assetPath"]].append((r["jsonPointer"], r["englishText"], r["koreanText"]))
        if src.is_dir():
            # unpacked mod: edit files in place
            for asset, edits in by_asset.items():
                f = src / asset.lstrip("/")
                if not f.exists():
                    totals["dir-asset-missing"] += len(edits)
                    continue
                text = f.read_text(encoding="utf-8")
                try:
                    text2, c = span_edit_text(text, edits)
                except ValueError:
                    totals["dir-parse-failed"] += len(edits)
                    continue
                if c["applied"]:
                    f.write_text(text2, encoding="utf-8", newline="")
                totals.update({f"dir-{k}": v for k, v in c.items()})
            continue
        # pak: backup once, always unpack from the pristine backup so
        # incremental translation updates never text-mismatch
        BACKUP.mkdir(parents=True, exist_ok=True)
        bkp = BACKUP / src.name
        if not bkp.exists():
            shutil.copy2(src, bkp)
        stage = STAGE / safe
        if stage.exists():
            shutil.rmtree(stage)
        r = subprocess.run([str(ROOT / "win" / "asset_unpacker.exe"), str(bkp), str(stage)],
                           capture_output=True)
        if r.returncode != 0:
            print("UNPACK FAILED", src.name,
                  (r.stderr or r.stdout).decode(errors="replace")[-1500:])
            totals["unpack-failed"] += len(rows)
            continue
        for asset, edits in by_asset.items():
            f = stage / asset.lstrip("/")
            if not f.exists():
                totals["asset-missing"] += len(edits)
                continue
            text = f.read_text(encoding="utf-8")
            try:
                text2, c = span_edit_text(text, edits)
            except ValueError:
                totals[f"parse-failed:{asset}"] += len(edits)
                continue
            if c["applied"]:
                f.write_text(text2, encoding="utf-8", newline="")
            totals.update(c)
        out = stage.parent / (safe + ".pak")
        r = subprocess.run([str(ROOT / "win" / "asset_packer.exe"), str(stage), str(out), "-s"],
                           capture_output=True)
        if r.returncode != 0:
            print("PACK FAILED", src.name,
                  (r.stderr or r.stdout).decode(errors="replace")[-1500:])
            totals["pack-failed"] += len(rows)
            continue
        shutil.copy2(out, src)
        totals[f"repacked:{src.name}"] += 1
        shutil.rmtree(stage)
        out.unlink()
    print(json.dumps(dict(totals), ensure_ascii=False, indent=2))


def main():
    en2ko = load_en2ko()
    overlay_ops, repack, conflicts, stats = resolve_targets(en2ko)
    if "--write" in sys.argv or not any(a.startswith("--") for a in sys.argv[1:]) or "--dry" in sys.argv:
        if "--dry" not in sys.argv:
            n = write_outputs(overlay_ops, repack)
            print("overlay patch files:", n)
        if conflicts:
            WORK.mkdir(parents=True, exist_ok=True)
            with open(WORK / "conflicts.tsv", "w", encoding="utf-8-sig", newline="") as fh:
                w = csv.writer(fh, delimiter="\t", lineterminator="\n")
                w.writerow(("sourceMod", "assetPath", "jsonPointer", "englishText",
                            "keptKorean", "droppedKorean"))
                w.writerows(conflicts)
    if "--pack" in sys.argv:
        pack_overlay()
    if "--repack" in sys.argv:
        run_repacks()
    print(json.dumps(dict(stats), ensure_ascii=False))


if __name__ == "__main__":
    main()
