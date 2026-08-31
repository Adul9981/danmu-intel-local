#!/usr/bin/env python3
"""官方基础数据库同步工具（2026-08-30 建立）。

从 Riot 官方赛事 API 同步最准确的联赛/队伍/选手基础数据：
  - getLeagues  -> leagues.json  official（riot_id/slug/region/name）
  - getTeams    -> teams.json    official（riot_id/code/name/record 战绩）
  - getSchedule + window -> players.json official（summoner_name/role/team）

用法：
  python3 tools/sync_official_base.py --root /Users/ad/Documents/polymarket
  python3 tools/sync_official_base.py --root . --leagues-only
  python3 tools/sync_official_base.py --root . --recent-games 8
"""

from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from pathlib import Path

API_KEY = "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"
BASE = "https://esports-api.lolesports.com/persisted/gw"
FEED = "https://feed.lolesports.com/livestats/v1"

LEAGUE_IDS = {
    "lck": "98767991310872058",
    "lck_cl": "98767991335774713",
    "lpl": "98767991314006698",
    "lec": "98767991302996019",
    "lcs": "98767991299243165",
    "lcp": "113476371197627891",
}


def api(path: str, params: dict) -> dict:
    url = f"{BASE}/{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        "x-api-key": API_KEY, "accept": "application/json",
        "user-agent": "polymarket-intel/sync_official_base",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def feed(game_id: str) -> dict | None:
    try:
        req = urllib.request.Request(f"{FEED}/window/{game_id}",
                                     headers={"user-agent": "polymarket-intel/sync_official_base"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode())
    except Exception:  # noqa: BLE001
        return None


def load(root: Path, rel: str):
    p = root / rel
    if not p.exists():
        return {} if rel.endswith(".json") else ""
    return json.loads(p.read_text(encoding="utf-8"))


def save(root: Path, rel: str, data) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def sync_leagues(root: Path) -> int:
    d = load(root, "docs/data/intel/leagues.json")
    leagues = {l["id"]: l for l in d.get("leagues", [])}
    n = 0
    # 按现有自定义 id -> Riot 官方映射补 official
    for lid, riot in LEAGUE_IDS.items():
        if lid not in leagues:
            continue
        entry = leagues[lid]
        ol = api("getLeagues", {"hl": "zh-CN"}).get("data", {}).get("leagues", [])
        info = next((x for x in ol if x.get("id") == riot), {})
        entry["official"] = {
            "riot_id": riot, "slug": info.get("slug", ""), "name": info.get("name", ""),
            "region": info.get("region", ""),
        }
        n += 1
    d["leagues"] = list(leagues.values())
    d["updated_at"] = "2026-08-30"
    save(root, "docs/data/intel/leagues.json", d)
    return n


def sync_teams(root: Path) -> int:
    d = load(root, "docs/data/intel/teams.json")
    team_names = load(root, "docs/data/intel/team_names.json")
    full_by_id = {str(t["id"]): t.get("full", "") for t in team_names.get("teams", [])}
    teams = d.get("teams", [])
    # 全量队伍池（getTeams 返回全联赛共享池）
    pool = api("getTeams", {"hl": "zh-CN"}).get("data", {}).get("teams", [])
    by_code: dict[str, dict] = {}
    by_name: dict[str, dict] = {}
    for t in pool:
        code = t.get("code", "")
        if code:
            by_code.setdefault(code, t)
        nm = t.get("name", "")
        if nm:
            by_name.setdefault(nm.lower(), t)
    n = 0
    for t in teams:
        # 优先 team_names.full 精确匹配（避免 DNS/T1 撞 code：Challengers 同 code）
        full = full_by_id.get(t.get("id"), "") or t["name"].split("（")[0]
        ot = by_name.get(full.lower())
        if ot is None:
            code = t.get("abbr") or t["name"].split("（")[0]
            base = code.split(".")[0].split(" ")[0]
            ot = by_code.get(code) or by_code.get(base)
        if not ot:
            continue
        t["official"] = {
            "riot_id": ot.get("id"), "code": ot.get("code"), "name": ot.get("name"),
        }
        n += 1
    d["updated_at"] = "2026-08-30"
    save(root, "docs/data/intel/teams.json", d)
    return n


def sync_players(root: Path, recent_games: int = 10) -> int:
    """从近期已结束比赛的 window 提取实际参赛选手官方数据。"""
    d = load(root, "docs/data/intel/players.json")
    players = {p["id"]: p for p in d.get("players", [])}
    n = 0
    # 1) getSchedule -> matchId；2) getEventDetails -> gameId；3) window -> 选手
    game_ids: list[str] = []
    for lid in LEAGUE_IDS.values():
        try:
            sched = api("getSchedule", {"hl": "zh-CN", "leagueId": lid}).get("data", {}).get("schedule", {}).get("events", [])
        except Exception:  # noqa: BLE001
            continue
        for ev in sched[-recent_games:]:
            m = ev.get("match") or {}
            mid = m.get("id")
            if not mid:
                continue
            try:
                det = api("getEventDetails", {"hl": "zh-CN", "id": mid})
                games = (det.get("data", {}).get("event", {}).get("match") or {}).get("games", [])
            except Exception:  # noqa: BLE001
                continue
            for g in games:
                if g.get("state") == "completed":
                    game_ids.append(g["id"])
    for gid in game_ids[:recent_games * 3]:
        w = feed(gid)
        if not w:
            continue
        gm = w.get("gameMetadata", {})
        for side in ("blueTeamMetadata", "redTeamMetadata"):
            meta = gm.get(side, {})
            team_code = ""
            for p in meta.get("participantMetadata", []):
                sn = p.get("summonerName", "")
                role = p.get("role", "")
                # summonerName 形如 "NS Kingen" -> 提取名字
                name = sn.split(" ", 1)[-1] if " " in sn else sn
                pid = name.lower().replace(" ", "")
                # 匹配已有条目：id == pid 或 id 去掉游戏前缀后 == pid
                entry = players.get(pid)
                if entry is None:
                    for existing_id in players:
                        if existing_id.split("-", 1)[-1] == pid:
                            entry = players[existing_id]
                            break
                if entry is None:
                    entry = {"id": f"lol-{pid}", "name": name, "game": "lol",
                             "danmu": {"mentions_total": 0, "anchors": []}, "updated": "2026-08-30"}
                    players[entry["id"]] = entry
                entry["official"] = {
                    "summoner_name": sn, "role": role, "riot_player_id": p.get("esportsPlayerId"),
                }
                entry["role"] = role
                entry["game"] = "lol"
                n += 1
    d["players"] = list(players.values())
    d["updated_at"] = "2026-08-30"
    save(root, "docs/data/intel/players.json", d)
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description="官方基础库同步")
    ap.add_argument("--root", default=".")
    ap.add_argument("--leagues-only", action="store_true")
    ap.add_argument("--recent-games", type=int, default=10)
    args = ap.parse_args()
    root = Path(args.root)
    nl = sync_leagues(root)
    print(f"leagues official 同步 {nl}")
    if args.leagues_only:
        return 0
    nt = sync_teams(root)
    print(f"teams official 同步 {nt}")
    np_ = sync_players(root, args.recent_games)
    print(f"players official 同步 {np_}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
