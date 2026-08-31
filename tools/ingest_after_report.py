#!/usr/bin/env python3
"""赛后自动入库脚本（2026-08-31 建立）。

在情报页生成（generate_intel_report --node full）后自动沉淀到情报库：
  1) matches.json 结果回填（若提供 --result）
  2) 选手提及/锚点 -> players.json（accumulate_player_intel）
  3) 队伍特质 -> teams.json（accumulate_team_traits --merge）
  4) 队伍画像 -> teams.json（accumulate_team_intel --match，容错）
  5) 报告索引（可选，发布时由 vps_publish 处理）

用法：
  python3 tools/ingest_after_report.py --root . --teams GX,FNC --date 2026-08-31 \
      --slug lol-gx-fnc-2026-08-31 --slice-file <弹幕文件> --intel-json <intel.json> \
      [--result "GX 2:0 FNC（官方）" --winner GX --score 2-0]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], root: Path) -> int:
    print(f"[ingest] $ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=str(root), capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        print(f"[ingest] 步骤失败 rc={r.returncode}: {r.stderr[-400:]}")
    else:
        print(f"[ingest] OK: {r.stdout.strip()[-200:]}")
    return r.returncode


def update_matches(root: Path, slug: str, result: str, winner: str, score: str) -> bool:
    p = root / "docs/data/intel/matches.json"
    if not p.exists():
        print("[ingest] matches.json 不存在，跳过结果回填")
        return False
    d = json.loads(p.read_text(encoding="utf-8"))
    for m in d.get("matches", []):
        if m.get("slug") == slug or m.get("id") == slug or m.get("event_slug") == slug:
            m["status"] = "已结束"
            m["result_inferred"] = result
            if winner:
                m["winner"] = winner
            if score:
                m["score"] = score
            m["source"] = "official+danmu"
            m["updated_at"] = "2026-08-31"
            p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"[ingest] matches.json 已回填: {slug} -> {result}")
            return True
    # 找不到则创建新条目（新框架生成的比赛可能未在库中）
    teams_raw = [t for t in slug.replace("lol-", "").replace("cs2-", "").split("-") if t]
    league = "CS2" if slug.startswith("cs2") else "LOL"
    d["matches"].append({
        "id": slug, "slug": slug, "event_slug": slug,
        "date": slug.split("-")[-1] if len(slug.split("-")) >= 3 else "",
        "teams": teams_raw[:2], "league": league, "status": "已结束",
        "result_inferred": result,
        "winner": winner or "", "score": score or "",
        "source": "official+danmu", "memory_tier": "LONG",
        "updated_at": "2026-08-31",
    })
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[ingest] matches.json 新建条目: {slug} -> {result}")
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description="赛后自动入库")
    ap.add_argument("--root", default=".")
    ap.add_argument("--teams", required=True, help="逗号分隔，如 GX,FNC")
    ap.add_argument("--date", required=True)
    ap.add_argument("--slug", default="")
    ap.add_argument("--slice-file", default="", help="本场弹幕文件（选手沉淀用）")
    ap.add_argument("--intel-json", default="", help="本场规则层 intel.json（队伍特质用）")
    ap.add_argument("--result", default="", help="如 GX 2:0 FNC（官方）")
    ap.add_argument("--winner", default="")
    ap.add_argument("--score", default="")
    args = ap.parse_args()
    root = Path(args.root)
    teams = [t.strip() for t in args.teams.split(",")]
    slug = args.slug or f"lol-{teams[0].lower()}-{teams[1].lower()}-{args.date}"

    # 1) 结果回填
    if args.result:
        update_matches(root, slug, args.result, args.winner, args.score)

    # 2) 选手沉淀（按场弹幕）
    if args.slice_file and Path(args.slice_file).exists():
        run(["python3", "tools/accumulate_player_intel.py", "--root", ".", "--files", args.slice_file], root)
    else:
        print("[ingest] 无 slice-file，跳过选手沉淀")

    # 3) 队伍特质（按场 intel.json 合并）
    if args.intel_json and Path(args.intel_json).exists():
        run(["python3", "tools/accumulate_team_traits.py", "--root", ".", "--merge", args.intel_json], root)
    else:
        print("[ingest] 无 intel-json，跳过队伍特质沉淀")

    # 4) 队伍画像（容错）
    run(["python3", "tools/accumulate_team_intel.py", "--root", ".", "--match", slug, "--stats"], root)

    print(f"[ingest] 完成：{slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
