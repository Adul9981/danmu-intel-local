# 弹幕情报服务部署包（2026-08-31 · 旧框架回归版）

> 架构：程序固化流程 + 固定提示词（prompts/）+ 大模型 API（DeepSeek）。
> 云端不运行 Codex 会话，只跑程序 + 调 API——输出结构/校验由程序保证。
>
> **模板变更（2026-08-31 用户定稿）：回归旧 10 段框架**，不再用 12 段速览卡/方向板。
> 规范见 `INTEL_TEMPLATE_OLD_2026-08-31.md`；样页（可直接对照生成）：
> `reports/template_samples/intel_danmu_LCKCL-NS-DNSC_full_old_2026-08-31.html`。
> 生成端 prompts/ 需按 10 段骨架调整（去掉速览卡硬性门槛，保留数据带量/
> 灰信号纪律/结果标"弹幕口径" / MD 镜像 / match_state_guard 四道闸）。
>
> **成本基准（2026-08-31 实测）**：单页 ≈0.04–0.06 元（full≈3.3k in / 7.9k out
> tokens），一场 BO3 ≈0.25–0.45 元，一晚 5–6 场 ≈1.5–2.5 元。
> 若云端成本远高于此，先读 `COST_CONFIG_CHECKLIST.md` 逐项核对
> （重点：生成路径是否仍是 Codex 全量、模型是否 deepseek-chat、
> 输入样本量是否控制在 ≤60 条）。

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
COST_CONFIG_CHECKLIST.md  成本与配置检查清单（云端对齐用）
INTEL_TEMPLATE_OLD_2026-08-31.md  旧框架 10 段模板（当前标准）
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
python3 tools/generate_intel_report.py \
  --teams VIT,SHFT --date 2026-08-30 --node full \
  --intel-json <规则层情报.json> --slice-file <弹幕切片.jsonl> \
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
