# 弹幕情报库 · 本地采集版（danmu-intel-local）

> 把电竞直播弹幕，变成可溯源、可支持决策的情报，并且越攒越值钱。

本仓库是弹幕情报系统的**本地采集与分析版**：多路直播间（虎牙为主）弹幕采集 →
按比赛×节点时间窗切片 → 规则层统计（词表/提及量/密度/灰信号）→ LLM 提炼 →
门禁校验 → HTML + MD 双格式情报输出 → 结构化情报库沉淀 → 验证回填。
事实层（时间/队伍/比分/选手×英雄·地图/结算）一律以官方/权威公开源校准
（Riot esports-api / Liquipedia / HLTV / Polymarket 结算），弹幕只负责提供
"观众怎么看、有什么信号、有什么质疑"。

云端 Python 工程版的设计文档见 `docs/task/DANMU_INTEL_CLOUD_PYTHON_PROJECT_PRD.md`
（PRD v2.0，可直接照此开发部署）。

## 仓库结构

```text
knowledge/            弹幕情报知识库与规则（SOP / 模板 / 验证方法论 / 防错规则）
tools/                采集 / 切片 / 规则统计 / 情报生成 / 发布工具（Python）
reports/              情报输出页（HTML + MD，含认可样页与实战样例）
prompts/              固定提示词（report_full / game / pre / live）
docs/task/            产品与设计文档（含 PRD v2.0）
docs/data/intel/      结构化情报库（matches/teams/players/gray/bp/leagues）
docs/framework/       项目框架文档
config/               配置（队伍命名 / 联赛 / 直播间注册 / 同步）
schemas/              JSON 契约
vendor/               real-url 弹幕库（vendor 化，防平台改版）
deploy/               部署脚本与 systemd 单元
deliverables/ dist/   历史云端部署包
```

## 认可的情报模板与样例

| 内容 | 路径 |
| --- | --- |
| 情报模板（唯一标准 · 旧 10 段框架） | `knowledge/INTEL_TEMPLATE_OLD_2026-08-31.md` |
| 模板样页（LCK CL NS 3:2 DNS 整场复盘） | `reports/intel_danmu_LCKCL-NS-DNSC_full_old_2026-08-31.html` |
| 实战样例（CS2 Aurora vs G2 · 图二三加时 19:16 · 弹幕防误实战） | `reports/intel_danmu_CS2-Aurora-G2_G2_ot_2026-08-31.html` |
| 决胜图局中样例 | `reports/intel_danmu_CS2-Aurora-G2_G3_mid_2026-08-31.html` |
| 云端项目 PRD v2.0 | `docs/task/DANMU_INTEL_CLOUD_PYTHON_PROJECT_PRD.md` |

## 平台边界（2026-08-26 起用户定稿）

- 虎牙：主源（官方流 / 957 / 毛毛 / 米勒 / 记得 / 硕硕 / CSBOY×2 / BLAST 等）；
- SOOP：LCK CL 韩语官方流（可选，韩文弹幕需中文化后聚合）；
- Twitch：**明确不采集**（数据源质量问题）；
- KICK：预留（结构保留，默认关闭）。

## 本仓库不含

- 任何密钥 / 私钥 / API Token；
- 原始弹幕大数据（仅保留结构化情报库与脱敏统计）；
- 交易执行代码与交易者拆解（属独立项目域）；
- runtime 运行状态与日志。

## 快速开始

```bash
# 采集（多直播间同场会话）
python3 tools/run_danmu_session.py --session <name> --room <source>=<url> ...

# 切片（比赛×节点时间窗）
python3 tools/slice_danmu_by_match.py --manifest <manifest.json>

# 规则层情报提炼
python3 tools/danmu_intel.py --input <slice.jsonl> --out intel.json

# 生成情报页（A 型整场 / B 型局中 / 赛前）
python3 tools/danmu_report.py --input intel.json --template full
```

完整工作流见 `knowledge/DANMU_WORKFLOW.md`（五阶段 SOP）。

## 防错纪律（最高优先级）

- 终局判定四信号齐备才允许发布"已结束"：官方比分 + 官方系列状态 + 弹幕多信号共振 + 流量骤降；
- CS2 加时制参数化（4 回合加时块 / 无限 / 领先 2 分），弹幕"回家 / 图三了 / 比分喊话"
  一律只作候选信号，以官方源仲裁；
- 事实层只信官方，弹幕结论可溯源，缺数据显式标「无」；
- 灰信号只作风险标注，对外永远写「观众质疑 · 非结论」；
- 弹幕引用脱敏，不展示用户身份。
