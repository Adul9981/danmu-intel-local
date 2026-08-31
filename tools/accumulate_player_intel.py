#!/usr/bin/env python3
"""选手情报库自动沉淀工具（2026-08-30 建立）。

从弹幕库批量提取选手提及/正负情绪/锚点，更新 docs/data/intel/players.json，
实现"每场 -> 选手画像"跨场复利闭环（选手库原仅 21 人，2026-08-30 扩充）。

词表来源：
  1) tools/danmu_intel.py PLAYERS（通用词条：Canna/Niko/donk/Faker 等）；
  2) docs/data/intel/rosters.json 官方名册 player_id（oscarinin/isma 等）；
  3) 补充别名表 PLAYER_ALIASES（昨晚新增首发/社区黑话）。

用法：
  python3 tools/accumulate_player_intel.py --root /Users/ad/Documents/polymarket --scan
  python3 tools/accumulate_player_intel.py --root /Users/ad/Documents/polymarket \
      --files docs/data/danmu/huya/2026-08-30_huya_shuoshuo.jsonl
"""

from __future__ import annotations

import argparse
import glob
import json
import re
from collections import Counter, defaultdict
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


# 补充别名表（2026-08-30）：昨晚新增首发/社区黑话，key=player_id
PLAYER_ALIASES: dict[str, list[str]] = {
    # LEC NAVI-GX / KC-SK 首发
    "samd": ["samd", "三亩地", "小礼物"],
    "maynter": ["maynter"],
    "rhilech": ["rhilech"],
    "parus": ["parus"],
    # "奥斯卡"是社区"奥斯卡之夜"（演/假赛梗），不是选手名——禁止误配
    "oscarinin": ["oscarinin"],
    "isma": ["isma"],
    "jackies": ["jackies", "jackies?"],
    "flakked": ["flakked"],
    "jun": ["jun"],
    "canna": ["canna", "金东河"],
    "yike": ["yike", "yike"],
    "caliste": ["caliste", "卡莉"],
    "busio": ["busio"],
    "wunder": ["wunder", "温德"],
    "skeanz": ["skeanz"],
    "slowq": ["slowq"],
    "jopa": ["jopa"],
    "mikyx": ["mikyx", "米人"],
    # CS2 Falcons/Legacy 首发
    "karrigan": ["karrigan", "大表哥"],
    "kyousuke": ["kyousuke", "京介", "荆芥", "荆"],
    "teses": ["teses", "特赛斯"],
    "art": ["art", "arT"],
    "dumau": ["dumau"],
    "latto": ["latto"],
    "n1ssim": ["n1ssim", "nissim"],
    # LVG/FUT 首发
    "cmtry": ["cmtry", "厘米try"],
    "z4kr": ["z4kr"],
    "starry": ["starry", "叶哥哥"],
    "jee": ["jee"],
}


def build_player_kws(rosters: dict, extra: dict | None = None) -> dict:
    """玩家 id -> 关键词（danmu_intel.PLAYERS + rosters + extra）。"""
    kws: dict[str, list[str]] = {}
    for pid, vals in danmu_intel.PLAYERS.items():
        kws[pid.lower()] = list(vals)
    for t in rosters.get("teams", []):
        for p in t.get("roster", []):
            pid = str(p.get("player_id", "")).lower()
            if pid and pid not in kws:
                kws[pid] = [pid]
    for pid, vals in (extra or {}).items():
        kws[pid.lower()] = list(vals)
    # 多义词清洗：faker 去掉"老李"（"老李家/老李粉丝"闲聊误配），保留英文+飞科
    if "faker" in kws:
        kws["faker"] = ["faker", "飞科"]
    # "奥斯卡之夜"是社区演/假赛梗，不是选手——整条移除
    kws.pop("oscar", None)
    return kws


def scan_files(files: list[Path], kws: dict) -> dict:
    """返回 {player_id: {mentions, pos, neg, samples, tone}}。"""
    agg: dict[str, dict] = {}
    for f in files:
        for line in f.open(encoding="utf-8"):
            try:
                o = json.loads(line)
            except Exception:  # noqa: BLE001
                continue
            text = o.get("text") or o.get("message", "")
            if not text:
                continue
            for pid, vals in kws.items():
                # 排除"昵称:开头"误配（如观众昵称 Faker 发言"Faker:WE 韧性十足"）
                if not any(_hit(text, k) and not re.search(rf"(?i){re.escape(k)}\s*[:：]", text) for k in vals):
                    continue
                a = agg.setdefault(pid, {"mentions": 0, "pos": 0, "neg": 0, "samples": []})
                a["mentions"] += 1
                if danmu_intel.sentiment(text) == "pos":
                    a["pos"] += 1
                elif danmu_intel.sentiment(text) == "neg":
                    a["neg"] += 1
                if len(a["samples"]) < 6:
                    a["samples"].append(text[:90])
                break
    # 补 tone
    for a in agg.values():
        a["tone"] = "正" if a["pos"] > a["neg"] else ("负" if a["neg"] > a["pos"] else "中性")
        a["samples"] = list(dict.fromkeys(a["samples"]))
    return agg


def merge_into_players(players_lib: dict, agg: dict, team_names: dict, replace: bool = False) -> int:
    """合并进 players.json。

    replace=True（全库扫描）：mentions/pos/neg 用扫描值覆盖（ground truth）；
    replace=False（单场增量）：按值累加。
    """
    by_id = {p["id"]: p for p in players_lib.get("players", [])}
    # player_id -> team_id 推断（rosets 无队名时留空）
    n = 0
    for pid, a in agg.items():
        if a["mentions"] < 3:
            continue  # 样本不足不建画像
        existing = by_id.get(pid)
        if existing:
            d = existing.setdefault("danmu", {})
            d["mentions_total"] = a["mentions"] if replace else int(d.get("mentions_total") or 0) + a["mentions"]
            d["pos"] = a["pos"] if replace else int(d.get("pos", 0)) + a["pos"]
            d["neg"] = a["neg"] if replace else int(d.get("neg", 0)) + a["neg"]
            for s in a["samples"]:
                if s not in d.setdefault("anchors", []):
                    d["anchors"].append(s)
            d["anchors"] = d["anchors"][:12]
            existing["updated"] = "2026-08-30"
        else:
            players_lib["players"].append({
                "id": pid, "name": pid, "game": "unknown", "team_id": None,
                "danmu": {"mentions_total": a["mentions"], "pos": a["pos"], "neg": a["neg"],
                          "anchors": a["samples"][:6], "tone": a["tone"]},
                "updated": "2026-08-30",
            })
            by_id[pid] = players_lib["players"][-1]
        n += 1
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description="选手情报沉淀")
    ap.add_argument("--root", default=".", help="项目根目录")
    ap.add_argument("--files", nargs="*", default=[], help="指定弹幕文件；缺省全库扫描")
    args = ap.parse_args()
    root = Path(args.root)
    rosters = load(root, "docs/data/intel/rosters.json")
    players_lib = load(root, "docs/data/intel/players.json")
    team_names = load(root, "docs/data/intel/team_names.json")
    kws = build_player_kws(rosters, PLAYER_ALIASES)
    files = [Path(f) for f in args.files] if args.files else [
        Path(f)
        for pat in ("docs/data/danmu/huya/*.jsonl", "docs/data/danmu/soop/*.jsonl",
                    "docs/data/danmu/twitch/*.jsonl", "docs/data/danmu/kick/*.jsonl")
        for f in sorted(glob.glob(str(root / pat)))
    ]
    agg = scan_files(files, kws)
    n = merge_into_players(players_lib, agg, team_names, replace=True)
    players_lib["updated_at"] = "2026-08-30"
    save(root, "docs/data/intel/players.json", players_lib)
    print(f"merged {n} players -> docs/data/intel/players.json (total {len(players_lib['players'])})")
    for pid, a in sorted(agg.items(), key=lambda kv: -kv[1]["mentions"])[:15]:
        print(f"  {pid}: {a['mentions']} 正{a['pos']}/负{a['neg']} tone={a['tone']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
