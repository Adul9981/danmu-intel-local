#!/usr/bin/env python3
"""交易复盘 -> matches.json 盘口轨迹回填工具（2026-08-30 建立，P2）。

遍历 knowledge/reviews/*.md（108 份交易复盘），提取：
  1) 比赛 slug / 对阵 / 日期（从文件名 + 标题）
  2) 逐局赔率表（每局价格路径摘要）
  3) 整局 Moneyline 表（关键价格点）
回填 matches.json 的 price_path_review 字段（盘口轨迹摘要 + 复盘引用）。

用法：
  python3 tools/backfill_review_intel.py --root /Users/ad/Documents/polymarket
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def load(root: Path, rel: str):
    p = root / rel
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def save(root: Path, rel: str, data) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def normalize_slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def extract_slug(fname: str, md: str) -> str:
    """从文件名/正文提取比赛 slug（去日期前缀/后缀）。"""
    m = re.search(r"(?:lol|cs2|dota2)[a-z0-9_.\-]*20\d{2}-\d{2}-\d{2}", fname)
    if m:
        return m.group(0).replace(".md", "")
    m = re.search(r"(?:lol|cs2|dota2)[a-z0-9_.\-]+", fname)
    if m:
        return m.group(0).replace(".md", "")
    return fname.replace(".md", "")


def parse_price_tables(md: str) -> list[str]:
    """提取含价格数字（如 56.5c / 0.05c / 99.95c）的表格行。"""
    out = []
    lines = md.splitlines()
    in_table = False
    for ln in lines:
        s = ln.strip()
        if s.startswith("|") and re.search(r"\d+(\.\d+)?\s*c", s):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) >= 3:
                out.append(" | ".join(cells[:6]))
                in_table = True
        elif in_table and s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) >= 3 and re.search(r"\d+(\.\d+)?c|^\d+$", " ".join(cells)):
                out.append(" | ".join(cells[:6]))
        else:
            in_table = False
    return out[:20]


def main() -> int:
    ap = argparse.ArgumentParser(description="交易复盘回填")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root)
    m = load(root, "docs/data/intel/matches.json")
    matches = m["matches"]
    pp = load(root, "docs/data/intel/price_paths.json")
    paths = pp.get("paths", []) if isinstance(pp, dict) else pp
    path_ids = {p.get("slug") for p in paths}
    # 队伍缩写集合（用于对阵匹配）
    team_set = {
        "TES", "LGD", "BLG", "AL", "WE", "TT", "IG", "NIP", "EDG", "JDG", "WBG", "LNG",
        "T1", "GEN", "HLE", "KT", "DK", "NS", "BFX", "BRO", "DNS", "DRX", "FOX",
        "KC", "GX", "SK", "TH", "FNC", "VIT", "NAVI", "G2", "SHFT",
        "FLC", "LEGACY", "LVG", "FUT", "M80", "PAIN", "9Z", "SPIRIT", "VITALITY",
        "FAZE", "MOUZ", "FURIA", "LIQUID", "MONGOLZ", "EF", "AURORA", "IC", "GL",
        "BB", "PV", "IW", "TS", "ACE", "VAN", "FOKUS", "PHA", "NRG", "OG", "SHU",
        "K27", "B8", "PRV", "WC1", "LONE", "VAE", "MGC", "FAL2", "TS7", "MGLZ", "PR1", "AUR1",
    }
    # 建立归一化 slug -> match 索引
    by_slug = {}
    for x in matches:
        for key in (x.get("id"), x.get("slug"), x.get("event_slug")):
            if key:
                by_slug.setdefault(normalize_slug(str(key)), x)
    n_fill = 0
    for f in sorted((root / "knowledge/reviews").glob("*.md")):
        if f.name in ("index.md", "day_review.md", "ewc_cs2_batch.md"):
            continue
        md = f.read_text(encoding="utf-8")
        slug = extract_slug(f.name, md)
        nslug = normalize_slug(slug)
        match = by_slug.get(nslug)
        # 对阵匹配：文件名里的两个队名 + 日期
        if match is None:
            fname_teams = [t for t in team_set if t.lower() in f.name.lower()]
            date = re.search(r"20\d{2}-\d{2}-\d{2}", f.name)
            date = date.group(0) if date else ""
            for x in matches:
                ts = x.get("teams", [])
                if len(ts) != 2:
                    continue
                if len(fname_teams) >= 2 and all(
                    any(t.lower() in str(y).lower() for y in ts) for t in fname_teams[:2]
                ):
                    match = x; break
        if match is None:
            continue
        rows = parse_price_tables(md)
        # 提取结果：只匹配"队伍 比分 队伍"且排除日期（yyyy-mm-dd / yyyy-mm-dd hh:mm）
        res = re.search(r"([A-Za-z]{2,}[A-Za-z0-9. ]*?)\s+(\d+)\s*:\s*(\d+)\s+([A-Za-z]{2,}[A-Za-z0-9.]*)", md[:1000])
        result = ""
        if res and not re.match(r"20\d{2}", res.group(1)):
            result = f"{res.group(1)} {res.group(2)}:{res.group(3)} {res.group(4)}"
        # 独立盘口轨迹库（不依赖 matches.json 覆盖）
        ps = normalize_slug(slug)
        if ps not in path_ids and rows:
            paths.append({
                "slug": ps, "source": f"knowledge/reviews/{f.name}",
                "result": result, "key_points": rows[:20], "updated": "2026-08-30",
            })
            path_ids.add(ps)
        if not rows:
            continue
        match["price_path_review"] = {
            "source": f"knowledge/reviews/{f.name}",
            "result": result,
            "key_points": rows,
            "updated": "2026-08-30",
        }
        n_fill += 1
    m["updated_at"] = "2026-08-30"
    pp = {"schema_version": "1.0", "updated_at": "2026-08-30",
          "description": "交易复盘盘口轨迹库（P2，2026-08-30）：从 knowledge/reviews 提取逐局赔率路径，按比赛 slug 索引。",
          "paths": paths}
    save(root, "docs/data/intel/matches.json", m)
    save(root, "docs/data/intel/price_paths.json", pp)
    print(f"盘口轨迹库 {len(paths)} 场；回填 matches.json {n_fill} 场")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
