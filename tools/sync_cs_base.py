#!/usr/bin/env python3
"""CS2 官方基础数据同步工具（2026-08-30 建立）。

从 Liquipedia CS 拉取关注队伍的官方基础数据（现役 roster/IGL/教练/区域），
更新 teams.json（official.liquipedia）与 players.json（CS 选手 official）。

用法：
  python3 tools/sync_cs_base.py --root /Users/ad/Documents/polymarket
  python3 tools/sync_cs_base.py --root . --teams flc,legacy,lvg
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_cs2_liquipedia import page_wikitext, field, search_pages  # noqa: E402


def load(root: Path, rel: str):
    p = root / rel
    if not p.exists():
        return {} if rel.endswith(".json") else ""
    return json.loads(p.read_text(encoding="utf-8"))


def save(root: Path, rel: str, data) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


# team_names id -> Liquipedia 页面标题（CS 队伍）
CS_PAGES = {
    "flc": "Team Falcons", "legacy": "Legacy", "lvg": "Lynn Vision Gaming",
    "fut": "FUT Esports", "m80": "M80", "pain": "paiN Gaming",
    "9z": "9z Team", "spirit": "Team Spirit", "vitality": "Team Vitality",
    "g2": "G2 Esports", "navi": "Natus Vincere", "faze": "FaZe Clan",
    "mouz": "MOUZ", "furia": "FURIA Esports", "liquid": "Team Liquid",
    "mongolz": "The MongolZ", "ef": "Eternal Fire", "aurora": "Aurora Gaming",
    "ic": "Inner Circle Esports", "gl": "GamerLegion", "astralis": "Astralis",
    "magic": "Magic", "ag": "AG", "astra": "Astra",
}


def parse_roster(wt: str) -> tuple[list[dict], str, str, str]:
    """从队伍页提取现役 roster + igl + coaches + region。"""
    players: list[dict] = []
    # 现役段：{{Squad|status=active|...{{Person|flag=xx|id=NiKo|name=...|...}}...}}
    m = re.search(r"===Active===\s*(\{\{Squad\|status=active.*?)\}\}\s*===Former===", wt, re.S)
    block = m.group(1) if m else ""
    for pm in re.finditer(r"\{\{Person\|([^}]*)\}\}", block):
        body = pm.group(1)
        def fld(key: str) -> str:
            fm = re.search(rf"\|\s*{key}\s*=([^|}}]*)", body)
            return fm.group(1).strip() if fm else ""
        pid = fld("id").strip("[]")
        name = fld("name").strip("[]")
        flag = fld("flag")
        role = fld("role")
        if pid:
            players.append({"id": pid, "name": name or pid, "flag": flag, "role": role or "rifler"})
    igl = field(wt, "igl") or ""
    igl = re.sub(r"\{\{flag\|[^}]*\}\}|\[\[|\]\]", "", igl).strip()
    coaches = field(wt, "coaches") or ""
    region = field(wt, "region") or ""
    return players, igl, coaches, region


def sync(root: Path, team_ids: list[str]) -> tuple[int, int]:
    teams_lib = load(root, "docs/data/intel/teams.json")
    players_lib = load(root, "docs/data/intel/players.json")
    team_by_id = {t["id"]: t for t in teams_lib.get("teams", [])}
    players = {p["id"]: p for p in players_lib.get("players", [])}
    nt = np_ = 0
    for tid in team_ids:
        page = CS_PAGES.get(tid)
        if not page:
            continue
        try:
            wt = page_wikitext(page)
        except Exception:  # noqa: BLE001
            # 尝试搜索兜底
            try:
                cands = search_pages(page, 3)
                if not cands:
                    print(f"  {tid}: 页面不可达")
                    continue
                wt = page_wikitext(cands[0])
            except Exception:  # noqa: BLE001
                print(f"  {tid}: 页面不可达")
                continue
        players_list, igl, coaches, region = parse_roster(wt)
        team = team_by_id.get(tid)
        if team is None:
            continue
        team["official"] = team.get("official", {})
        team["official"]["liquipedia"] = {
            "title": page, "region": region, "igl": igl,
            "coaches": coaches[:120],
            "roster": [{"id": p["id"], "name": p["name"], "flag": p["flag"], "role": p["role"]} for p in players_list],
        }
        nt += 1
        for p in players_list:
            pid = f"cs2-{p['id'].lower()}"
            entry = players.get(pid)
            if entry is None:
                entry = {"id": pid, "name": p["name"] or p["id"], "game": "cs2", "team_id": tid,
                         "danmu": {"mentions_total": 0, "anchors": []}, "updated": "2026-08-30"}
                players[pid] = entry
            entry["official"] = {
                "liquipedia_id": p["id"], "name": p["name"] or p["id"],
                "flag": p["flag"], "role": p["role"], "team": team.get("name", tid),
            }
            if not entry.get("role"):
                entry["role"] = p["role"]
            entry["team_id"] = tid
            np_ += 1
    teams_lib["updated_at"] = "2026-08-30"
    players_lib["updated_at"] = "2026-08-30"
    players_lib["players"] = list(players.values())  # 写回新增条目
    save(root, "docs/data/intel/teams.json", teams_lib)
    save(root, "docs/data/intel/players.json", players_lib)
    return nt, np_


def main() -> int:
    ap = argparse.ArgumentParser(description="CS 官方基础库同步")
    ap.add_argument("--root", default=".")
    ap.add_argument("--teams", default="", help="逗号分隔的 team_names id；缺省全部 CS 队")
    args = ap.parse_args()
    root = Path(args.root)
    ids = [x.strip() for x in args.teams.split(",") if x.strip()] if args.teams else list(CS_PAGES)
    nt, np_ = sync(root, ids)
    print(f"teams official.liquipedia 同步 {nt} 队；players CS official 同步 {np_} 人")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
