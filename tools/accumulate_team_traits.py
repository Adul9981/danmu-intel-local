#!/usr/bin/env python3
"""队伍特质/倾向自动沉淀工具（2026-08-30 建立）。

从弹幕情报中提取"队伍特质/倾向"（逆风崩盘/顺风隐身/被翻守不住/韧性逆转/
心态摆烂/慢热手热/打法风格/选手特质，词表见 tools/danmu_intel.py TRAIT_KW），
按规范队伍 id（docs/data/intel/team_names.json）累计进 teams.json traits 字段，
实现"每场 -> 队伍特质画像"跨场复利闭环。

两种模式：
  1) scan：直接扫描弹幕 JSONL 库（全库或指定文件），聚合特质；
  2) merge：把某场 intel.json 的 team_traits.by_entity 合并进 teams.json
     （供比赛结算自动流水线使用，accumulate_team_intel 可调用）。

用法：
  python3 tools/accumulate_team_traits.py --root /Users/ad/Documents/polymarket --scan
  python3 tools/accumulate_team_traits.py --root /Users/ad/Documents/polymarket \
      --merge runtime/danmu_sessions/lec_2026-08-29/intel.json
  python3 tools/accumulate_team_traits.py --root /Users/ad/Documents/polymarket \
      --scan --files docs/data/danmu/huya/2026-08-30_huya_shuoshuo.jsonl
"""

from __future__ import annotations

import argparse
import glob
import json
import re
from collections import defaultdict
from pathlib import Path

import danmu_intel


def load(root: Path, rel: str):
    p = root / rel
    if not p.exists():
        return {} if rel.endswith(".json") else ""
    if rel.endswith(".json"):
        return json.loads(p.read_text(encoding="utf-8"))
    return p.read_text(encoding="utf-8")


def save(root: Path, rel: str, data) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def _hit(text: str, kw: str) -> bool:
    low = text.lower()
    k = kw.lower()
    if not k:
        return False
    if k.isascii() and k.isalnum() and len(k) <= 4:
        return bool(re.search(rf"(?<![a-z0-9]){re.escape(k)}(?![a-z0-9])", low))
    return k in low


def entity_matcher(team_names: dict, player_names: dict) -> tuple[dict, dict]:
    """构建 规范队伍id -> 关键词 与 选手名 -> 关键词 匹配器。"""
    team_kws: dict[str, list[str]] = {}
    for t in team_names.get("teams", []):
        kws = [str(t.get("abbr", ""))] + [a for a in t.get("aliases", []) if a]
        team_kws[str(t["id"])] = kws
    player_kws: dict[str, list[str]] = {}
    for p in player_names.get("players", []):
        name = str(p.get("name", ""))
        # 弹幕常用英文 ID/昵称：选手 name 形如 "donk" / "Niko（尼公子）"
        en = re.sub(r"[（(].*$", "", name).strip()
        player_kws[str(p.get("id", en))] = [en] if en else []
    return team_kws, player_kws


def scan_files(files: list[Path], team_kws: dict, player_kws: dict) -> dict:
    """扫描弹幕文件，返回 {entity: {cat: {count, samples}}}。"""
    agg: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for f in files:
        for line in f.open(encoding="utf-8"):
            try:
                o = json.loads(line)
            except Exception:  # noqa: BLE001
                continue
            text = o.get("text") or o.get("message", "")
            if not text:
                continue
            for cat, kws in danmu_intel.TRAIT_KW.items():
                if not any(k in text for k in kws):
                    continue
                for ent, ent_kws in team_kws.items():
                    if any(_hit(text, k) and not re.search(rf"(?i){re.escape(k)}\s*[:：]", text) for k in ent_kws if k):
                        agg[ent][cat].append(text)
                for ent, ent_kws in player_kws.items():
                    if any(_hit(text, k) and not re.search(rf"(?i){re.escape(k)}\s*[:：]", text) for k in ent_kws if k):
                        agg[ent][cat].append(text)
                break
    return {ent: {c: {"count": len(v), "samples": list(dict.fromkeys(v))[:3]} for c, v in cats.items()} for ent, cats in agg.items()}


def merge_into_teams(teams_lib: dict, traits_by_entity: dict, today: str, replace: bool = False) -> int:
    """把特质聚合合并进 teams.json（按 id 匹配；选手特质另行提示）。

    replace=True（全库扫描）：用新聚合替换既有 traits（ground truth）；
    replace=False（单场 intel 合并）：按 count 增量累计。
    """
    merged = 0
    team_by_id = {t["id"]: t for t in teams_lib.get("teams", [])}
    # id 变体映射（team_names.json id 与 teams.json id 的差异）
    id_alias = {
        "vit": "vitality",
        "teamvision": "team_vision",
        "ironwing": "iron_wing",
    }
    for ent, cats in traits_by_entity.items():
        team = team_by_id.get(ent) or team_by_id.get(id_alias.get(ent, ""))
        if team is None:
            continue  # 选手或未登记队伍：由选手库/登记流程处理
        if replace:
            team["traits"] = {}
        traits = team.setdefault("traits", {})
        for cat, d in cats.items():
            slot = traits.setdefault(cat, {"count": 0, "samples": [], "last_seen": ""})
            slot["count"] = int(d["count"]) if replace else int(slot.get("count", 0)) + int(d["count"])
            for s in d.get("samples", []):
                if s not in slot["samples"]:
                    slot["samples"].append(s)
            slot["samples"] = slot["samples"][:3]
            slot["last_seen"] = today
        merged += 1
    return merged


def main() -> int:
    ap = argparse.ArgumentParser(description="队伍特质沉淀工具")
    ap.add_argument("--root", default=".", help="项目根目录")
    ap.add_argument("--scan", action="store_true", help="扫描弹幕库模式")
    ap.add_argument("--merge", metavar="INTEL_JSON", help="合并单场 intel.json 的 team_traits")
    ap.add_argument("--files", nargs="*", default=[], help="指定弹幕文件（scan 模式）")
    args = ap.parse_args()
    root = Path(args.root)

    team_names = load(root, "docs/data/intel/team_names.json")
    player_names = load(root, "docs/data/intel/players.json")
    teams_lib = load(root, "docs/data/intel/teams.json")
    today = __import__("datetime").date.today().isoformat()
    team_kws, player_kws = entity_matcher(team_names, player_names)

    traits = {}
    if args.merge:
        intel = json.loads((root / args.merge).read_text(encoding="utf-8"))
        by_entity = intel.get("team_traits", {}).get("by_entity", {})
        # intel.json 用 danmu_intel.TEAMS/PLAYERS 的英文键，先归一化到规范 id
        alias = {
            "navi": "navi", "Navi": "navi", "NAVI": "navi",
            "Spirit": "spirit", "Vitality": "vitality", "MOUZ": "mouz",
            "FURIA": "furia", "G2": "g2", "T1": "t1", "KT": "kt",
            "HLE": "hle", "GEN": "gen", "KC": "kc", "GX": "gx",
            "TH": "th", "WBG": "wbg", "LNG": "lng", "WE": "we",
            "EDG": "edg", "BLG": "blg", "TES": "tes", "IG": "ig",
            "DNS": "dns", "BFX": "bfx", "LGD": "lgd", "NIP": "nip",
            "JDG": "jdg", "DK": "dk", "FaZe": "faze", "Liquid": "liquid",
            "MongolZ": "mongolz", "EF": "ef", "Astra": "astra",
        }
        norm = {}
        for ent, cats in by_entity.items():
            norm[alias.get(ent, ent)] = cats
        traits = norm
    elif args.scan:
        files = [Path(f) for f in args.files] if args.files else [
            Path(f)
            for pat in ("docs/data/danmu/huya/*.jsonl", "docs/data/danmu/soop/*.jsonl",
                        "docs/data/danmu/twitch/*.jsonl", "docs/data/danmu/kick/*.jsonl")
            for f in sorted(glob.glob(str(root / pat)))
        ]
        traits = scan_files(files, team_kws, player_kws)
    else:
        ap.error("请指定 --scan 或 --merge")

    n = merge_into_teams(teams_lib, traits, today, replace=args.scan)
    save(root, "docs/data/intel/teams.json", teams_lib)
    print(f"merged traits into {n} teams -> docs/data/intel/teams.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
