#!/usr/bin/env python3
"""历史画像/经验数据吸收工具（2026-08-30 建立）。

把 knowledge/ 下历史画像文档吸收进结构化情报库，实现"历史复盘 -> 情报库"复利：
  LEAGUE_PROFILES.md        -> leagues.json   （波动/打满/假赛风险/反转可信）
  CHAMPION_PROFILES.md      -> champions.json （英雄预期情形/交易含义/信任）
  TEAM_PROFILES.md          -> teams.json     （历史画像：风格/形态倾向/证据/信任）
  EXPERIENCE_INSIGHTS.md    -> leagues.json   （联赛级先验结论备注）
  leagues/FIXED_MATCH_SUSPECT_CASES.md -> gray_signals.json（假赛疑似案例）

用法：
  python3 tools/absorb_legacy_intel.py --root /Users/ad/Documents/polymarket
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


def md_table_rows(md: str) -> list[list[str]]:
    """解析 Markdown 表格，返回行列表（去分隔行/空行）。"""
    rows = []
    for line in md.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r"[-: ]+", c) for c in cells if c):
            continue  # 分隔行
        rows.append(cells)
    return rows


def absorb_leagues(root: Path) -> int:
    md = load(root, "knowledge/LEAGUE_PROFILES.md")
    rows = md_table_rows(md)
    d = load(root, "docs/data/intel/leagues.json")
    leagues = {l["id"]: l for l in d.get("leagues", [])}
    # 联赛名 -> 现有 id
    id_map = {"LCK": "lck", "LPL": "lpl", "LEC": "lec", "LCP": "lcp",
              "CS2": "cs2", "Valorant": "valorant"}
    n = 0
    for r in rows[1:]:
        if len(r) < 6:
            continue
        name = r[0].strip("*")
        lid = id_map.get(name)
        if not lid or lid not in leagues:
            continue
        e = leagues[lid]
        e["profile"] = {
            "波动等级": r[1], "打满倾向": r[2], "假赛风险": r[3],
            "反转可信": r[4], "仓位修正": r[5], "依据样本": r[6] if len(r) > 6 else "",
            "source": "LEAGUE_PROFILES.md(2026-08-09)",
        }
        n += 1
    # EXPERIENCE_INSIGHTS 联赛级先验并入 notes
    exp = load(root, "knowledge/EXPERIENCE_INSIGHTS.md")
    for lid, tag in [("lec", "LEC"), ("lck", "LCK"), ("lpl", "LPL"), ("cs2", "CS2")]:
        if lid not in leagues:
            continue
        notes = []
        for line in exp.splitlines():
            if line.strip().startswith("|") and tag in line and "|" in line:
                cells = [c.strip() for c in line.strip("|").split("|")]
                if len(cells) >= 3:
                    notes.append(f"[经验] {cells[1]}（{cells[2]}）")
        if notes:
            leagues[lid]["experience_insights"] = notes[:8]
    d["leagues"] = list(leagues.values())
    d["updated_at"] = "2026-08-30"
    save(root, "docs/data/intel/leagues.json", d)
    return n


def absorb_champions(root: Path) -> int:
    md = load(root, "knowledge/CHAMPION_PROFILES.md")
    rows = md_table_rows(md)
    d = load(root, "docs/data/intel/champions.json")
    chs = {c["id"]: c for c in d.get("champions", [])}
    # 英雄中文名 -> id
    name_map = {"卡莎": "kaisa", "阿卡丽": "akali", "奇亚娜": "qiyana"}
    n = 0
    for r in rows[1:]:
        if len(r) < 6:
            continue
        cn = r[0].split("（")[0].strip("*")
        hid = name_map.get(cn)
        if not hid:
            continue
        c = chs.setdefault(hid, {"id": hid, "name": r[0].strip("*"), "game": "lol",
                                 "roles": [r[1]], "anchors": [], "team_fit": [],
                                 "memory_tier": "LONG", "updated_at": "2026-08-30"})
        c["profile"] = {
            "位置": r[1], "风格标签": r[2], "预期情形": r[3],
            "交易含义": r[4], "证据样本": r[5], "信任": r[6] if len(r) > 6 else "",
            "source": "CHAMPION_PROFILES.md(2026-08-09/10)",
        }
        n += 1
    d["champions"] = list(chs.values())
    d["updated_at"] = "2026-08-30"
    save(root, "docs/data/intel/champions.json", d)
    return n


def absorb_teams(root: Path) -> int:
    md = load(root, "knowledge/TEAM_PROFILES.md")
    rows = md_table_rows(md)
    d = load(root, "docs/data/intel/teams.json")
    by_id = {t["id"]: t for t in d.get("teams", [])}
    id_map = {"BLG": "blg", "JDG": "jdg", "TES": "tes", "WE": "we", "TT": "tt",
              "BRO": "bro", "T1": "t1", "HLE": "hle", "NS": "ns", "DNS": "dns",
              "KT": "kt", "DRX": "krx", "NIP": "nip", "WBG": "wbg", "LGD": "lgd",
              "Gen.G": "gen", "TH": "th", "KC": "kc", "GX": "gx"}
    n = 0
    for r in rows[1:]:
        if len(r) < 5:
            continue
        name = r[0].split("（")[0].strip("*")
        tid = id_map.get(name)
        if not tid or tid not in by_id:
            continue
        t = by_id[tid]
        t.setdefault("market", {})
        t["market"]["style"] = r[1]
        t["market"]["tendency"] = r[2]
        t["market"]["evidence"] = r[3]
        t["market"]["trust"] = r[4]
        t["market"]["source"] = "TEAM_PROFILES.md(历史画像)"
        n += 1
    d["updated_at"] = "2026-08-30"
    save(root, "docs/data/intel/teams.json", d)
    return n


def absorb_gray_suspects(root: Path) -> int:
    md = load(root, "knowledge/leagues/FIXED_MATCH_SUSPECT_CASES.md")
    d = load(root, "docs/data/intel/gray_signals.json")
    records = d.get("records", [])
    ids = {r.get("id") for r in records}
    # 提取案例块（## 案例 N：标题）
    blocks = re.split(r"\n## ", md)
    n = 0
    for b in blocks[1:]:
        title_line = b.splitlines()[0].strip()
        m = re.match(r"案例\s*\d+：(.+)", title_line)
        if not m:
            continue
        title = m.group(1).strip()
        rid = "suspect_" + re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
        if rid in ids:
            continue
        # 提取关键字段
        status = re.search(r"状态：(.+)", b)
        odds = re.search(r"赔率证据：(.+)", b)
        behavior = re.search(r"行为证据（用户观察 \+ 解说提示）：(.+)", b, re.S)
        verdict = re.search(r"结论：(.+)", b)
        records.append({
            "id": rid, "match": title, "league": "LEC",
            "count": 1, "time_window": "整场",
            "keywords": ["疑似假赛", "怪装备", "领先不打团"],
            "correlated_markets": ["整场", "G2"],
            "notes": (behavior.group(1)[:200] if behavior else "") + "；" + (verdict.group(1) if verdict else ""),
            "severity": "高（疑似，未证实）",
            "verification": "pending",
            "verification_note": "来自 FIXED_MATCH_SUSPECT_CASES.md；待外部证据核查",
            "routes": "待核查",
            "source_doc": "knowledge/leagues/FIXED_MATCH_SUSPECT_CASES.md",
        })
        ids.add(rid)
        n += 1
    d["records"] = records
    d["updated_at"] = "2026-08-30"
    save(root, "docs/data/intel/gray_signals.json", d)
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description="历史画像吸收")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root)
    nl = absorb_leagues(root)
    nc = absorb_champions(root)
    nt = absorb_teams(root)
    ng = absorb_gray_suspects(root)
    print(f"leagues 吸收 {nl} | champions 吸收 {nc} | teams 吸收 {nt} | gray 疑似案例 {ng}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
