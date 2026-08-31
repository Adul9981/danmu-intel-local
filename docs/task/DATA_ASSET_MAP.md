# 情报库数据资产地图（2026-08-30 盘点）

> 目的：把项目历史积累的完整数据全部盘清，识别可吸收进结构化情报库的资产，
> 实现"历史复盘 -> 情报库"复利闭环。本文件为盘点基准，随资产变化更新。

## 一、资产清单（全量）

| 资产 | 位置 | 数量/规模 | 内容 | 可吸收性 |
| --- | --- | --- | --- | --- |
| 弹幕情报页 | reports/intel_danmu_*.html | 238 页（08-17~08-30） | 局中/BP/整场/画像情报，26 个 full | ★★★（锚点/灰信号/对位） |
| MD 情报镜像 | knowledge/intel_pages/ | 353 个 .md | 每场情报全文（可解析） | ★★★（批量提取） |
| 交易复盘 | knowledge/reviews/ | 108 份 | 每笔交易复盘（08-04 起） | ★★（盘口/队伍表现） |
| 交易记录 | knowledge/trades/ | 11 份 | 成交记录 | ★（matches 关联） |
| 赔率轨迹 | docs/data/snapshots/ | 99 个（93MB） | 分钟级价格 CSV | ★★★（盘口维度） |
| 队伍画像 | knowledge/TEAM_PROFILES.md | 134 行 | 08-08 前历史队伍画像/形态倾向 | ★★★（→ teams.json） |
| 英雄画像 | knowledge/CHAMPION_PROFILES.md | 17 行 | 卡莎/阿卡丽/奇亚娜预期情形 | ★★★（→ champions.json） |
| 联赛画像 | knowledge/LEAGUE_PROFILES.md | 30 行 | 波动/打满/假赛风险/反转可信 | ★★★（→ leagues.json） |
| 经验清单 | knowledge/EXPERIENCE_INSIGHTS.md | 90 行 | 已确认/待验证经验 | ★★（联赛级先验） |
| 边缘日志 | knowledge/EDGE_LOG.md | 87 行 | 信号/规律留痕 | ★★（沉淀层） |
| 解说画像 | knowledge/COMMENTERS.md | 85 行 | 解说/主播倾向 | ★★（streamer_profiles） |
| 用户画像 | knowledge/DANMU_USERS.md | 65 行 | 高价值弹幕用户 | ★★（users.json） |
| 信号库 | knowledge/INTEL_SIGNALS.md + intel_signals.json | 296 行 + json | 信号定义/示例 | ★★（信号字典） |
| 灰信号实锤 | knowledge/leagues/FIXED_MATCH_SUSPECT_CASES.md | 案例 1+ | 假赛疑似案例（VIT vs GX） | ★★★（→ gray_signals） |
| CS 历史库 | knowledge/leagues/EWC_CS2_LIBRARY.md 等 | 多份 | EWC/CS2 队伍地图库 | ★★★（→ teams/maps） |
| 拆解案例 | docs/forensics/ | 35 份 md + 8 案例 | 交易者拆解 | ★（独立域） |
| 弹幕原始库 | docs/data/danmu/ | 177 文件 140 万条 | 原始弹幕 | ★★★（回溯提取） |
| 历史会话 | runtime/danmu_sessions/ | 30 个 | 采集会话状态 | ★（完整性） |
| 结构化库 | docs/data/intel/ | 16 个 json | 已结构化情报 | 基准 |

## 二、吸收映射（源 -> 目标库）

| 源 | 目标库 | 吸收内容 | 状态 |
| --- | --- | --- | --- |
| LEAGUE_PROFILES.md | leagues.json | 波动等级/打满倾向/假赛风险/反转可信/仓位修正/依据 | ✅ 2026-08-30（4 联赛） |
| CHAMPION_PROFILES.md | champions.json | 英雄预期情形/交易含义/信任等级 | ✅ 2026-08-30（3 英雄） |
| TEAM_PROFILES.md | teams.json | 历史画像（风格/形态倾向/证据/信任） | ✅ 2026-08-30（25 队） |
| EXPERIENCE_INSIGHTS.md | leagues.json + knowledge | 联赛级先验结论 | ✅ 2026-08-30 |
| FIXED_MATCH_SUSPECT_CASES.md | gray_signals.json | 假赛疑似案例（高 severity） | ✅ 2026-08-30（6 案例） |
| EDGE_LOG.md | knowledge（沉淀） | 信号/规律留痕 | 🔄 待办 |
| COMMENTERS.md | commenters.json | Polymarket 评论者画像 | ✅ 2026-08-30（1 人） |
| DANMU_USERS.md | users.json | 高价值弹幕用户 | ✅ 2026-08-30（19 人） |
| intel_pages/*.md | 各库 | 历史情报锚点批量提取（覆盖已确认） | ✅ 2026-08-30（matches 全覆盖确认） |
| EWC_CS2_LIBRARY.md | matches.json/price_paths.json | CS 历史比赛/赔率形态 | ✅ 2026-08-30（12 场） |
| reviews/*.md | price_paths.json + matches.json | 盘口轨迹/逐局赔率 | ✅ 2026-08-30（35 场） |

## 三、优先级

```text
P0（已完成 2026-08-30）：画像文档吸收（TEAM/CHAMPION/LEAGUE/EXPERIENCE/灰信号实锤）
P1（已完成 2026-08-30）：intel_pages MD 覆盖确认（matches.json 全覆盖）+ 灰信号候选提取
P2（已完成 2026-08-30）：reviews 交易复盘 -> price_paths.json 盘口轨迹库（35 场）+ matches 回填
P3（已完成 2026-08-30）：EWC_CS2_LIBRARY -> matches/price_paths（12 场）；COMMENTERS/DANMU_USERS 画像
待办：EDGE_LOG 沉淀吸收；CS 队伍地图库（maps 队伍×图锚继续累计）
```
