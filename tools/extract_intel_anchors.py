#!/usr/bin/env python3
"""intel_pages MD 批量锚点提取工具（2026-08-30 建立，P1）。

遍历 knowledge/intel_pages/*.md（353 份历史情报镜像），提取：
  1) 官方阵容表（队伍 x 上单/打野/中单/AD/辅助 -> 选手 x 英雄）
     -> champions.json anchors（英雄 x 队伍 x match）+ players.json anchors
  2) 灰信号段（"无实质灰信号"判定 + 灰信号行）
     -> gray_signals.json 候选计数

用法：
  python3 tools/extract_intel_anchors.py --root /Users/ad/Documents/polymarket
  python3 tools/extract_intel_anchors.py --root . --md knowledge/intel_pages/intel_danmu_NS-BFX_G1_2026-08-27.md
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


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


# 英文英雄 id 常见映射（champions.json 现有 + 补充）
CHAMP_IDS = {
    "jayce": "jayce", "cassiopeia": "cassiopeia", "anivia": "anivia",
    "lucian": "lucian", "aatrox": "aatrox", "yone": "yone",
    "twisted fate": "twisted_fate", "lee sin": "lee_sin", "gnar": "gnar",
    "viktor": "viktor", "ryze": "ryze", "caitlyn": "caitlyn",
    "xin zhao": "xin_zhao", "jhin": "jhin", "ksante": "ksante",
    "locke": "locke", "yunara": "yunara", "ambessa": "ambessa",
    "kalista": "kalista", "drmundo": "drmundo", "mundo": "drmundo",
    "rumble": "rumble", "bard": "bard", "orianna": "orianna",
    "syndra": "syndra", "vi": "vi", "xayah": "xayah", "rakan": "rakan",
    "kaisa": "kaisa", "akali": "akali", "qiyana": "qiyana",
    "karma": "karma", "seraphine": "seraphine", "ashe": "ashe",
    "pantheon": "pantheon", "renekton": "renekton", "jarvan": "jarvan_iv",
    "jarvan iv": "jarvan_iv", "leblanc": "leblanc", "renata": "renata",
    "milio": "milio", "rakan": "rakan", "camille": "camille",
    "ezreal": "ezreal", "thresh": "thresh", "galio": "galio",
    "nocturne": "nocturne", "ornn": "ornn", "zoe": "zoe",
    "sett": "sett", "viego": "viego", "ahri": "ahri",
    "taliyah": "taliyah", "varus": "varus", "corki": "corki",
    "azir": "azir", "lissandra": "lissandra", "tristana": "tristana",
    "jinx": "jinx", "aphelios": "aphelios", "zeri": "zeri",
    "draven": "draven", "sivir": "sivir", "vayne": "vayne",
    "nami": "nami", "lulu": "lulu", "yuumi": "yuumi", "karma": "karma",
}


def parse_roster_table(md: str) -> list[dict]:
    """解析官方阵容表：行含 队伍/上单/打野/中单/AD/辅助。"""
    rows = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if "上单" in line and "打野" in line and "AD" in line and line.strip().startswith("|"):
            # 表头
            j = i + 2  # 跳过分隔行
            while j < len(lines) and lines[j].strip().startswith("|"):
                cells = [c.strip() for c in lines[j].strip("|").split("|")]
                if len(cells) >= 7 and not all(re.fullmatch(r"[-: ]+", c) for c in cells if c):
                    rows.append(cells[:7])
                j += 1
            i = j
        else:
            i += 1
    return rows


def extract_match_id(md: str, fname: str) -> str:
    m = re.search(r"matchId[\s：:]*(\d+)", md)
    if m:
        return m.group(1)
    m = re.search(r"2026[-_]0\d[-_]\d{2}.*?(?:\s|$)", fname)
    return fname.replace(".md", "")


def extract_team_from_cell(cell: str) -> str:
    m = re.search(r"([A-Za-z0-9.]+)", cell)
    return m.group(1).upper() if m else ""


def main() -> int:
    ap = argparse.ArgumentParser(description="intel_pages 锚点批量提取")
    ap.add_argument("--root", default=".")
    ap.add_argument("--md", default="", help="单份 MD；缺省遍历全部")
    args = ap.parse_args()
    root = Path(args.root)
    chs = load(root, "docs/data/intel/champions.json")
    champions = {c["id"]: c for c in chs.get("champions", [])}
    pl = load(root, "docs/data/intel/players.json")
    players = {p["id"]: p for p in pl.get("players", [])}
    gray = load(root, "docs/data/intel/gray_signals.json")
    gray_records = {r.get("id") for r in gray.get("records", [])}

    files = [Path(args.md)] if args.md else sorted((root / "knowledge/intel_pages").glob("*.md"))
    n_roster = n_champ = n_player = n_gray = 0
    gray_counter: dict[str, int] = {}
    for f in files:
        md = f.read_text(encoding="utf-8")
        mid = extract_match_id(md, f.name)
        # 1) 阵容表
        for cells in parse_roster_table(md):
            team = extract_team_from_cell(cells[0])
            if not team:
                continue
            # cells: [队伍, 上单, 打野, 中单, AD, 辅助, 结果?]
            roles = ["top", "jungle", "mid", "adc", "support"]
            for idx, role in enumerate(roles[:5]):
                if idx + 1 >= len(cells):
                    break
                cell = cells[idx + 1]
                # "Kingen 青钢影" / "青钢影" / "Kingen"
                mm = re.match(r"([A-Za-z0-9_.\-]+)?\s*([A-Za-z ]+)?$", cell.strip())
                if not mm:
                    continue
                pname = mm.group(1)
                champ_en = mm.group(2)
                if not champ_en:
                    continue
                cid = CHAMP_IDS.get(champ_en.strip().lower())
                if not cid:
                    continue
                c = champions.setdefault(cid, {"id": cid, "name": champ_en, "game": "lol",
                                               "roles": [role], "anchors": [], "team_fit": [],
                                               "memory_tier": "LONG", "updated_at": "2026-08-30"})
                if "team_fit" not in c:
                    c["team_fit"] = []
                # 队伍 x 英雄锚（去重）
                if not any(x.get("team_id") == team.lower() and x.get("match_id") == mid for x in c["team_fit"]):
                    c["team_fit"].append({"team_id": team.lower(), "note": f"官方阵容 {role} {champ_en}", "match_id": mid})
                c["team_fit"] = c["team_fit"][:30]
                n_champ += 1
                if pname:
                    pid = pname.lower()
                    # 匹配已有选手（前缀归一）
                    entry = players.get(pid)
                    if entry is None:
                        for eid in players:
                            if eid.split("-", 1)[-1] == pid:
                                entry = players[eid]; break
                    if entry is None:
                        entry = {"id": pid, "name": pname, "game": "lol", "team_id": team.lower(),
                                 "danmu": {"mentions_total": 0, "anchors": []}, "updated": "2026-08-30"}
                        players[pid] = entry
                    entry["team_id"] = team.lower()
                    if not entry.get("role"):
                        entry["role"] = role
                    anchors = entry.setdefault("danmu", {}).setdefault("anchors", [])
                    note = f"{mid} {role} {champ_en}（官方阵容）"
                    if note not in anchors:
                        anchors.append(note)
                    entry["danmu"]["anchors"] = anchors[:20]
                    n_player += 1
            n_roster += 1
        # 2) 灰信号计数
        gm = re.search(r"##\s*2灰信号汇总.*?(?=\n##\s*\d)", md, re.S)
        if gm:
            seg = gm.group(0)
            if "无实质灰信号" in seg:
                pass
            else:
                for kw in ["假赛", "剧本", "做任务", "演", "卡盘", "收钱", "送分", "控分"]:
                    if kw in seg:
                        gray_counter[kw] = gray_counter.get(kw, 0) + 1
                        n_gray += 1
                        break
    # 灰信号聚合（按关键词簇）
    for kw, cnt in gray_counter.items():
        gid = f"intel_pages_{kw}"
        if gid in gray_records:
            continue
        gray["records"].append({
            "id": gid, "match": "intel_pages 批量", "league": "多联赛",
            "count": cnt, "time_window": "历史汇总",
            "keywords": [kw], "correlated_markets": [],
            "notes": f"从 {n_gray} 份 intel_pages MD 灰信号段批量提取（P1）",
            "severity": "低（候选）", "verification": "pending",
            "verification_note": "候选待逐场核实", "routes": "待核查",
            "source_doc": "knowledge/intel_pages/*.md",
        })
        gray_records.add(gid)
    chs["champions"] = list(champions.values())
    chs["updated_at"] = "2026-08-30"
    pl["players"] = list(players.values())
    pl["updated_at"] = "2026-08-30"
    gray["updated_at"] = "2026-08-30"
    save(root, "docs/data/intel/champions.json", chs)
    save(root, "docs/data/intel/players.json", pl)
    save(root, "docs/data/intel/gray_signals.json", gray)
    print(f"解析 {len(files)} 份 MD：阵容行 {n_roster} / 英雄锚 {n_champ} / 选手锚 {n_player} / 灰信号命中 {n_gray}（{len(gray_counter)} 簇）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
