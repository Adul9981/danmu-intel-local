---
name: intel-report
description: 按标准模板输出弹幕情报 HTML 页面（局中/整场复盘/画像三类，SAP 样式）。Use when generating danmaku intel HTML reports (in-game / full review / profile) in the Polymarket intel project.
---

# 情报 HTML 输出 (Intel Report Generation)

项目根目录：/Users/ad/Documents/polymarket。**模板为最高规范**：knowledge/INTEL_HTML_TEMPLATE.md（A/B/C 三类 + 硬性门槛）。样式规范：SAP/Apple（#f5f5f7 浅底、白卡、单一强调色、系统字体栈）。

## 核心结构 (Core Structure)
- **A 整场复盘页**：10 段（结果总览/逐局/队伍画像/人员画像带量/灰信号/规律/预测验证/盘口/含义/溯源）。
- **B 局中情报页** = A 的进行中快照：必须覆盖 A 全部关键段，未知段写"待观察/样本不足"，禁止删段。
- **C 画像页**：队伍/选手长期画像（组织/风格/核心/盘口定位）。
- 标杆样例：reports/intel_danmu_WE-EDG_full_2026-08-19.html、HLE-DK_2026-08-20.html、DOTA-BB-PV_2026-08-20.html。

## 硬性门槛 (Quality Gates)
1. 数据带量（条数/提及量/密度）；2. 灰信号显著展示+纪律；3. 结果标"弹幕口径·未确认"；4. 每页至少 1 条可跨场长期沉淀；5. 无样本不硬撑、无信号不硬造。
6. **BP 后战绩情报必抓**（2026-08-21 固化）：pick 锁定后窗口内"选手×英雄"
   历史战绩/胜率提及（CS：图三转换窗口"队伍×地图"强图/历史战绩），
   无则写"无战绩情报提及"；规则见 INTEL_HTML_TEMPLATE.md 二.7。
7. **MD 镜像必出**（2026-08-24 固化）：每个 HTML 情报页必须同步生成同名 MD
   镜像到 `knowledge/intel_pages/`（规范见 knowledge/INTEL_MD_MIRROR.md），
   覆盖 HTML 10 段骨架全文，缺失即视为情报未交付；
   并在 `knowledge/intel_pages/README.md` 索引表登记。
8. **收缩-展开加厚模式**（2026-08-30 用户定稿，最高）：所有情报页按"加厚版"标准
   ——速览卡焦点制（≤5 焦点）+ 证据层 `<details>` 折叠（原文/长画像/时间线）+
   逐局必带弹幕时间线（真实时间戳带量）+ 共识≥5 行 + 密度目标整场≥16KB；
   规则详见 knowledge/INTEL_HTML_TEMPLATE.md 二.13；历史页不回补。

## 语言 (Language)
HTML 内容以中文为主；技能说明中英双语。
