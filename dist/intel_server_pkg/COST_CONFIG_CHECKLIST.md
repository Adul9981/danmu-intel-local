# 弹幕情报生成端 · 成本与配置检查清单（2026-08-31）

> 用途：云端情报生成若成本远高于本地基准，先按本清单逐项核对配置。
> 核心结论：**成本大头不在模型单次价格，而在"生成路径"**——本地用
> 固定提示词 + 直连 DeepSeek API（程序固化结构），云端若仍用 Codex
> 全量生成（每页读 skill+模板+统计再逐段写），成本自然高一个量级以上。

---

## 一、本地实测成本基准（直连 DeepSeek API，2026-08-31 实测 usage 字段）

| 节点 | 输入 prompt tokens | 输出 HTML tokens | 估算成本（deepseek-chat：输入 3 元/百万、输出 6 元/百万） |
| --- | --- | --- | --- |
| full（整场复盘） | ≈3,318 | ≈7,900 | ≈0.057 元/页 |
| game（局中 bp/mid/end） | ≈2,867 | ≈6,500 | ≈0.048 元/页 |
| pre（赛前） | ≈1,987 | ≈5,000 | ≈0.036 元/页 |
| live（局中快照） | ≈1,985 | ≈5,700 | ≈0.040 元/页 |

汇总：
- 单份情报约 **0.04–0.06 元**，85% 花在输出 token；
- 一场 BO3（5–8 页）约 **0.25–0.45 元**；
- 一晚 5–6 场全节点约 **1.5–2.5 元**。

主要变量：
1. **门禁重试**：本地最多重试 3 次（仅缺段/结构不过时重试），重试一次约翻倍；
2. **高峰期价格**：DeepSeek V4 高峰时段输出价可能 6→12 元/百万，成本翻倍；
3. **模型选择**：最大杠杆——换 reasoner/高级模型单页成本可涨 10–100 倍。

---

## 二、本地权威生成配置（以本仓库为准）

| 文件 | 作用 |
| --- | --- |
| `tools/generate_intel_report.py` | 程序化生成端：组装 prompt → DeepSeek API → 校验 → 写 HTML/MD |
| `prompts/report_full.md` | 整场复盘固定提示词（12 段模板 + 时间戳固化 + 来源分层） |
| `prompts/report_game.md` | 局中节点提示词（bp/mid/end） |
| `prompts/report_pre.md` | 赛前提示词 |
| `prompts/report_live.md` | 局中快照提示词 |
| `knowledge/INTEL_HTML_TEMPLATE.md` | 12 段模板规格 + 速览卡 + 收缩-展开加厚模式 |
| `tools/speedcard_consistency.py` | 速览卡一致性审计门禁 |
| `tools/match_state_guard.py` | 结果/状态四道闸门禁 |
| `knowledge/OFFICIAL_DATA_SOURCES.md` | 官方数据源清单（LoL Riot / CS2 Liquipedia→HLTV） |
| `reports/template_samples/` | 最终成品蓝本（整场 + 局中页各一份） |

### 模型参数（本地固化，云端必须一致）

```text
model:       deepseek-chat
temperature: 0.3
max_tokens:  首调 8000；门禁重试 16000
重试：       最多 3 次，仅当 12 段/标准标题/details≥3 门禁不过时触发
输入：       规则层统计摘要 + 本场弹幕代表样本（≤60 条、每条≤50 字、带北京时间戳）
输出：       正文约 700–1000 字、完整 HTML（SAP/Apple 内联样式）
```

> ⚠️ 2026-08-31 关键修复：`generate_intel_report.py` 与 `prompts/report_full.md`
> 已加入"弹幕样本必须带真实北京时间戳"的固化规则（此前纯 API 模型会幻觉
> 时间线偏移 8 小时）。**云端必须同步这两个文件**，否则即使成本对齐，
> 时间线数据也会出错。

---

## 三、云端检查项（按对成本的影响从大到小）

1. **生成路径（最大头）**：是否还在用 Codex/Agent 全量生成每页？
   → 必须换成 `tools/generate_intel_report.py` 直连 DeepSeek API，
   结构/校验由程序保证，大模型只做"弹幕/官方数据 → 中文情报文本"。
2. **模型**：确认是 `deepseek-chat`，不是 reasoner 或其他高级模型。
3. **max_tokens / temperature**：对齐 8000 / 0.3（重试 16000）。
4. **重试逻辑**：门禁不过最多 3 次；不要"每页无限重试"或"人工反复重生成"。
5. **输入样本量**：只喂规则层统计 + 代表样本（≤60 条），
   不裸喂整场 1.5 万条弹幕（会线性放大输入成本且模型吸收不了）。
6. **节点/页数**：默认 3 节点节奏（BP / 局中 / 局末），关键局按需拆；
   不要每个时间点都开一页。
7. **提示词版本**：`prompts/` 四份固定提示词必须与本地最新版一致，
   禁止让模型"每次自己读模板再写"（重复读长模板=反复花输入 token）。
8. **门禁后置**：生成后程序化过 `speedcard_consistency.py --check` +
   `match_state_guard.py`，用程序校验替代"人工/模型重读返工"。

---

## 四、同步动作（发完配置后云端照做）

```text
1. 用最新 dist/intel_server_pkg 覆盖云端 /opt/danmu-intel 同名文件：
   prompts/、tools/generate_intel_report.py、knowledge/INTEL_HTML_TEMPLATE.md、
   knowledge/INTEL_MD_MIRROR.md、reports/template_samples/
2. 确认 DEEPSEEK_API_KEY 已配置（环境变量或 ~/.codex/config.toml）。
3. 重启生成流水线（systemd / launchd）。
4. 跑一页 full 验证：
   python3 tools/generate_intel_report.py --teams X,Y --date 2026-08-31 \
     --node full --intel-json <intel.json> --slice-file <切片.jsonl> \
     --out reports/intel_danmu_X-Y_full_2026-08-31.html
5. 用 API usage 字段核对：full 输入≈3.3k、输出≈7.9k tokens，成本≈0.05 元；
   若显著超量，回查上面第 2/5/7 项。
```

---

## 五、降本可选（按需开启）

- **分层输出**：节点一结束先用规则层速览摘要版（模板直出、秒级），
  完整 12 段后台补全——"第一眼能看到"压到分钟级以内，同时保留完整版质量；
- **深度版开关**：只对关键场次/决赛场开深度版，其余规则版
  （云端已提出此方案，本地认可）；
- **错峰**：DeepSeek V4 高峰时段（国内晚高峰）输出价翻倍，可考虑错峰生成非紧急页。
