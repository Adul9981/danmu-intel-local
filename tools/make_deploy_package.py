#!/usr/bin/env python3
"""情报服务部署包制作工具（2026-08-30 建立，任务 3）。

把"程序固化流程 + 固定提示词 + 大模型 API"的最小可运行集打成一个部署包，
云端解压即可跑（不含 Codex，只含 API key 配置）。

用法：
  python3 tools/make_deploy_package.py --out dist/intel_server_pkg
  # 打包后 scp/rsync 到云服务器，按 README.md 部署
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 部署包文件清单（相对项目根）
FILES = [
    # 生成端（核心）
    "prompts/report_full.md", "prompts/report_game.md",
    "prompts/report_pre.md", "prompts/report_live.md",
    "tools/generate_intel_report.py",
    # 规则层 / 校验
    "tools/danmu_intel.py",
    "tools/verify_match_result.py",
    "tools/match_state_guard.py",
    "tools/speedcard_consistency.py",
    "tools/ingest_after_report.py",
    # 采集（可选，云端如需自采）
    "tools/fetch_huya_danmu.py",
    "tools/fetch_soop_danmu.py",
    "tools/run_danmu_session.py",
    # 官方数据
    "tools/fetch_official_game_data.py",
    "tools/fetch_cs2_liquipedia.py",
    # 依赖 / 规范
    "requirements.txt",
    "knowledge/INTEL_HTML_TEMPLATE.md",
    "knowledge/DANMU_CAPTURE_RULES.md",
    "knowledge/INTEL_MD_MIRROR.md",
    "knowledge/MEMORY_TIERS.md",
    "AGENTS.md",
]


README = """# 弹幕情报服务部署包（2026-08-30）

> 架构：程序固化流程 + 固定提示词（prompts/）+ 大模型 API（DeepSeek）。
> 云端不运行 Codex 会话，只跑程序 + 调 API——输出结构/校验由程序保证。

## 目录

```
prompts/                固定提示词（report_full/game/pre/live，可版本管理）
tools/generate_intel_report.py   程序生成端（组装 prompt -> DeepSeek API -> 校验 -> HTML）
tools/danmu_intel.py    规则层提炼（词表/情绪/灰信号/队伍特质）
tools/verify_match_result.py / match_state_guard.py   结果与状态门禁
tools/speedcard_consistency.py   速览卡一致性校验
tools/fetch_huya_danmu.py 等     弹幕采集（可选）
knowledge/              模板/规范（INTEL_HTML_TEMPLATE 等）
reports/template_samples/  最终情报成品蓝本（整场复盘 + 局中页各一份，生成结果对照此结构/密度/样式）
requirements.txt        Python 依赖
```

## 最终产物蓝本（reports/template_samples/）

生成出的情报 HTML 应**对照蓝本的结构、密度与样式**：

```text
intel_danmu_LEC-VIT-SHFT_full_2026-08-30.html   整场复盘蓝本（12 段、速览卡、details 折叠）
intel_danmu_CS2-FUT-IC_G2_mid_2026-08-31.html  局中页蓝本（局中·非终局标注）
```

对照要点：
- 12 段结构 + 标准标题（0 核心情报速览 → 11 数据与溯源）；
- 速览卡 = 比分/进度一行 + TOP 信号 3-5 条（风险→锚点→盘口→共识）+ 决策落点；
- 证据层用 <details> 折叠（原文摘录/时间线/长画像），整场 ≥3 个；
- 灰信号带"观众质疑·非结论"；时间全部北京时间；数据完整性三栏。

## 部署步骤

```bash
# 1. 安装依赖
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. 配置 API Key（二选一）
export DEEPSEEK_API_KEY="sk-xxx"        # 推荐环境变量
# 或写入 ~/.codex/config.toml: experimental_bearer_token = "sk-xxx"

# 3. 生成情报（示例：整场复盘）
python3 tools/generate_intel_report.py \\
  --teams VIT,SHFT --date 2026-08-30 --node full \\
  --intel-json <规则层情报.json> --slice-file <弹幕切片.jsonl> \\
  --official-note "G1 官方阵容已确认..." --out reports/intel_danmu_xxx.html

# 4. 校验/发布
python3 tools/speedcard_consistency.py --check <页面>   # 速览卡审计
```

## 节点参数

- `--node full`（整场复盘）/ `game`（局中 bp/mid/end，需 `--game 1 --gphase bp`）/
  `pre`（赛前）/ `live`（局中快照）
- 生成端自带迭代修正闭环：门禁不过（12 段/标准标题/details≥3/无编造数字）
  自动反馈模型重试（最多 3 次）。

## 说明

- 大模型只做"弹幕/官方数据 -> 中文情报文本"；结构、校验、回填由程序保证。
- 事实层（官方 API/Polymarket 结算）在 vps_intel_pipeline / verify 脚本中程序化处理。
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="部署包制作")
    ap.add_argument("--out", default="dist/intel_server_pkg")
    args = ap.parse_args()
    out = ROOT / args.out
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    copied = 0
    for rel in FILES:
        src = ROOT / rel
        if not src.exists():
            print(f"  跳过（缺失）: {rel}")
            continue
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1
    (out / "README.md").write_text(README, encoding="utf-8")
    # 技能文件（供参考，提示词已内化到 prompts/）
    skill_src = Path.home() / ".codex/skills/intel-report/SKILL.md"
    if skill_src.exists():
        (out / "skills/intel-report/SKILL.md").parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_src, out / "skills/intel-report/SKILL.md")
    # 最终产物蓝本（整场 + 局中各一份）
    for sample in [
        "reports/intel_danmu_LEC-VIT-SHFT_full_2026-08-30.html",
        "reports/intel_danmu_CS2-FUT-IC_G2_mid_2026-08-31.html",
    ]:
        src = ROOT / sample
        if src.exists():
            dst = out / "reports/template_samples" / src.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1
    print(f"部署包已生成：{out}（{copied} 文件 + README + skill）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
