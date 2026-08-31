#!/usr/bin/env python3
"""P3 画像库吸收工具（2026-08-30 建立）。

吸收三份历史画像文档：
  1) knowledge/DANMU_USERS.md            -> users.json（高价值弹幕用户，补全）
  2) knowledge/COMMENTERS.md             -> docs/data/intel/commenters.json（Polymarket 评论者，新建）
  3) knowledge/leagues/EWC_CS2_LIBRARY.md -> matches.json（CS2 EWC 早期比赛补全）+ price_paths.json

用法：
  python3 tools/absorb_p3_profiles.py --root /Users/ad/Documents/polymarket
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


def absorb_danmu_users(root: Path) -> int:
    md = load(root, "knowledge/DANMU_USERS.md")
    d = load(root, "docs/data/intel/users.json")
    users = {u["id"]: u for u in d.get("users", [])}
    n = 0
    for line in md.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 5 or "昵称" in cells[0]:
            continue
        nick, stat, ratio, feature, sample = cells[0], cells[1], cells[2], cells[3], cells[4]
        if not nick:
            continue
        uid = f"huya_{re.sub(r'[^a-z0-9]', '', nick.lower())}"
        u = users.setdefault(uid, {"id": uid, "platform": "huya", "nick": nick,
                                   "type": "专业型", "notes": feature,
                                   "samples": [sample], "first_seen": "2026-08-17",
                                   "credibility": 0.6})
        u["notes"] = feature
        if sample not in u["samples"]:
            u["samples"].append(sample)
        u["samples"] = u["samples"][:5]
        m = re.search(r"(\d+)%", ratio)
        if m:
            u["credibility"] = int(m.group(1)) / 100
        n += 1
    d["users"] = list(users.values())
    d["updated_at"] = "2026-08-30"
    save(root, "docs/data/intel/users.json", d)
    return n


def absorb_commenters(root: Path) -> int:
    md = load(root, "knowledge/COMMENTERS.md")
    d = load(root, "docs/data/intel/commenters.json")
    commenters = {c["id"]: c for c in d.get("commenters", [])}
    n = 0
    # 按 "## 昵称" 分块
    blocks = re.split(r"\n## ", md)
    for b in blocks[1:]:
        name = b.splitlines()[0].strip()
        # 只吸收含"资料/地址"的评论者块，跳过分析章节
        if not name or not any(k in b[:800] for k in ("资料", "baseAddress", "proxyWallet", "评论主地址")):
            continue
        cid = f"pm_{re.sub(r'[^a-z0-9]', '', name.lower())}"
        addr = re.search(r"baseAddress[）)]?[:：]?\s*0x[a-fA-F0-9]{10,}", b)
        proxy = re.search(r"proxyWallet[）)]?[:：]?\s*0x[a-fA-F0-9]{10,}", b)
        style = re.search(r"风格初判：\n(.*?)(?=\n\n|```|\Z)", b, re.S)
        created = re.search(r"账号创建[:：]\s*([\d\-]+)", b)
        c = commenters.setdefault(cid, {"id": cid, "name": name, "source": "COMMENTERS.md",
                                        "base_address": addr.group(0).split(":")[-1].strip() if addr else "",
                                        "proxy_wallet": proxy.group(0).split(":")[-1].strip() if proxy else "",
                                        "created": created.group(1) if created else "",
                                        "style": "", "updated": "2026-08-30"})
        if style:
            c["style"] = style.group(1).strip()[:500]
        c["updated"] = "2026-08-30"
        n += 1
    d["commenters"] = list(commenters.values())
    d["updated_at"] = "2026-08-30"
    save(root, "docs/data/intel/commenters.json", d)
    return n


def absorb_ewc_cs2(root: Path) -> int:
    md = load(root, "knowledge/leagues/EWC_CS2_LIBRARY.md")
    m = load(root, "docs/data/intel/matches.json")
    pp = load(root, "docs/data/intel/price_paths.json")
    paths = pp.get("paths", [])
    path_slugs = {p["slug"] for p in paths}
    matches = m["matches"]
    match_ids = {x.get("id") for x in matches}
    n = 0
    for line in md.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 6 or "比赛（slug）" in cells[0]:
            continue
        slug, date, tag, result, shape, status = cells[0], cells[1], cells[2], cells[3], cells[4], cells[5]
        if not slug.startswith("cs2-"):
            continue
        if slug in match_ids:
            continue
        teams = []
        mm = re.match(r"cs2-([a-z0-9]+)-([a-z0-9]+)-", slug)
        if mm:
            teams = [mm.group(1).upper(), mm.group(2).upper()]
        matches.append({
            "id": slug, "slug": slug, "event_slug": slug, "date": "2026-08-" + date.split("-")[-1],
            "teams": teams, "league": f"CS2 · {tag}", "status": "已结束",
            "result_inferred": result, "price_shape": shape,
            "notes": f"EWC CS2 台账（EWC_CS2_LIBRARY.md）：{status}；赔率形态 {shape}",
            "memory_tier": "LONG", "updated_at": "2026-08-30",
        })
        match_ids.add(slug)
        if slug not in path_slugs:
            paths.append({"slug": slug, "source": "knowledge/leagues/EWC_CS2_LIBRARY.md",
                          "result": result, "price_shape": shape,
                          "key_points": [], "updated": "2026-08-30"})
            path_slugs.add(slug)
        n += 1
    m["matches"] = matches
    m["updated_at"] = "2026-08-30"
    pp = {"schema_version": "1.0", "updated_at": "2026-08-30",
          "description": "交易复盘/EWC CS2 盘口轨迹库（P2+P3），按比赛 slug 索引。",
          "paths": paths}
    save(root, "docs/data/intel/matches.json", m)
    save(root, "docs/data/intel/price_paths.json", pp)
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description="P3 画像吸收")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root)
    nu = absorb_danmu_users(root)
    nc = absorb_commenters(root)
    ne = absorb_ewc_cs2(root)
    print(f"弹幕用户 {nu} | 评论者 {nc} | EWC CS2 比赛 {ne}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
