# 云端弹幕情报部署手册（2026-08-31 · 照此配置即可）

> 目标：把本地这套「采集 → 切片 → 生成 → 发布」完整链路部署到云服务器。
> 架构：**程序固化流程 + 固定提示词（prompts/）+ 大模型 API（DeepSeek）**，
> 不依赖 Codex 会话；大模型只做"弹幕数据 → 中文情报文本"，结构/校验由程序保证。
> 云端路径约定：`/opt/danmu-intel`（本地对应 `/Users/ad/Documents/polymarket`）。

---

## 0. 环境准备（一次性）

```bash
cd /opt/danmu-intel
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # aiohttp/websockets/pycryptodome/requests/protobuf

# API Key（生成端用，二选一）
export DEEPSEEK_API_KEY="sk-你的key"    # 推荐：写进 ~/.bashrc 或 systemd 环境
# 或写入 ~/.codex/config.toml: experimental_bearer_token = "sk-你的key"
```

需要同步到服务器的目录/文件（部署包 dist/intel_server_pkg 已含）：

```text
prompts/                          固定提示词（report_full/game/pre/live）
tools/                            全部工具脚本
knowledge/                        模板与规范（INTEL_HTML_TEMPLATE 等）
requirements.txt                  Python 依赖
docs/data/danmu/                  弹幕原始数据（采集落盘目录，需可写）
runtime/danmu_sessions/           采集会话状态目录（需可写）
reports/                          情报输出目录（需可写）
```

---

## 1. 采集（弹幕抓取）

### 1.1 启动多直播间采集会话

```bash
cd /opt/danmu-intel
nohup python3 tools/run_danmu_session.py \
  --session lec_2026-08-31 \
  --title "LEC 08-31 场次（硕硕等）" \
  --room huya_shuoshuo=https://www.huya.com/323444 \
  --room huya_maomao=https://www.huya.com/149346 \
  --seconds 0 \
  > runtime/danmu_sessions/lec_2026-08-31_launch.log 2>&1 &
```

规则：
- **同场同会话**：同一场比赛的所有直播间放同一 `--session`（避免跨联赛混源）；
- **跨联赛必须分会话**（LCK/LPL/LEC/CS2 各自独立 session）；
- 每房独立落盘 `docs/data/danmu/huya/<日期>_<源>.jsonl`；
- 会话健康状态在 `runtime/danmu_sessions/<session>/session.json`；
- 进程死了自动重启由会话托管；**建议用 launchd/systemd 托管**保证常驻。

### 1.2 launchd 托管（macOS 本地）示例

```xml
<!-- ~/Library/LaunchAgents/com.ad.danmu-lec-2026-08-31.plist -->
<dict>
  <key>Label</key><string>com.ad.danmu-lec-2026-08-31</string>
  <key>ProgramArguments</key>
  <array>
    <string>/opt/danmu-intel/.venv/bin/python</string>
    <string>/opt/danmu-intel/tools/run_danmu_session.py</string>
    <string>--session</string><string>lec_2026-08-31</string>
    <string>--room</string><string>huya_shuoshuo=https://www.huya.com/323444</string>
    <string>--seconds</string><string>0</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key>
  <dict><key>SuccessfulExit</key><false/></dict>
</dict>
```

```bash
launchctl load ~/Library/LaunchAgents/com.ad.danmu-lec-2026-08-31.plist
# Linux 用 systemd unit，KeepAlive=true 等价
```

### 1.3 采集健康检查

```bash
# 会话状态
python3 -c "import json; s=json.load(open('runtime/danmu_sessions/<session>/session.json')); print([(r['source'],r.get('state'),r.get('message_count')) for r in s['rooms']])"

# 数据 0 条/长时间无新数据 = 先怀疑工具（进程死/断线），告警排查，禁止报"无弹幕"
# 房间直播内容核验
curl -s https://www.huya.com/<room> | grep -o '"introduction":"[^"]*'
```

---

## 2. 切片（按比赛/节点切弹幕）

用 `tools/slice_danmu_by_match.py`，manifest 定义比赛窗口：

```bash
python3 tools/slice_danmu_by_match.py \
  --manifest docs/data/danmu/slices/manifest.json \
  --out-dir docs/data/danmu/slices
```

manifest.json 模板（每场比赛一条）：

```json
{
  "matches": [
    {
      "id": "2026-08-31_lec_gx_fnc",
      "teams": ["GX", "FNC"],
      "league": "LEC",
      "streams": [
        {"file": "docs/data/danmu/huya/2026-08-31_huya_shuoshuo.jsonl", "source": "huya_shuoshuo"}
      ],
      "window": {"start": "2026-08-31T00:15:00+08:00", "end": "2026-08-31T02:30:00+08:00"},
      "games": [
        {"game_no": 1, "window": {"start": "2026-08-31T00:15:00+08:00", "end": "2026-08-31T01:00:00+08:00"}},
        {"game_no": 2, "window": {"start": "2026-08-31T01:05:00+08:00", "end": "2026-08-31T02:00:00+08:00"}}
      ]
    }
  ]
}
```

纪律（防混源）：
- **每个比赛的切片只能用该联赛默认采集集**（leagues.json），禁止混入其他联赛直播间；
- 节点切片窗口精确：只取本节点阶段时间窗（如 G2 BP 从 G2 选人开始，不含 G1 尾段/局间闲聊）；
- 切完先 `wc -l` 核对条数，0 条先查采集再切片。

---

## 3. 生成（固定提示词 + DeepSeek API）

核心：`tools/generate_intel_report.py`（程序固化流程，自带校验/迭代修正闭环）。

```bash
export DEEPSEEK_API_KEY="sk-你的key"

# 整场复盘（full）
python3 tools/generate_intel_report.py \
  --teams GX,FNC --date 2026-08-31 --node full \
  --intel-json runtime/danmu_sessions/lec_2026-08-31/intel.json \
  --slice-file docs/data/danmu/slices/2026-08-31_lec_gx_fnc/G1.jsonl \
  --official-note "LEC 常规赛 BO3；官方阵容/结果见溯源" \
  --result-note "GX 2:0 FNC（官方 gameWins）" \
  --out reports/intel_danmu_LEC-GX-FNC_full_2026-08-31.html

# 局中节点（game，bp/mid/end）
python3 tools/generate_intel_report.py \
  --teams GX,FNC --date 2026-08-31 --node game --game 2 --gphase bp \
  --intel-json ... --slice-file ... --out reports/intel_danmu_..._G2_bp_2026-08-31.html

# 赛前（pre）
python3 tools/generate_intel_report.py \
  --teams GX,FNC --date 2026-08-31 --node pre \
  --intel-json ... --slice-file ... --out reports/intel_danmu_..._pre_2026-08-31.html
```

节点说明：

| 节点 | 参数 | 页面标注 |
| --- | --- | --- |
| full 整场 | `--node full` | 整场复盘（≥16KB） |
| game 局中 | `--node game --game N --gphase bp/mid/end` | 局中·非终局 |
| pre 赛前 | `--node pre` | 赛前·未开赛 |
| live 快照 | `--node live` | 局中·非终局 |

门禁（程序自动，不过则反馈模型重试最多 3 次）：

```text
- 12 段结构齐全（0 速览→11 溯源，缺一不可）
- 段标题符合标准（模型自编标题会被拦）
- <details> 折叠区 ≥3（收缩-展开加厚模式）
- 无编造胜率/无源数字
- HTML 完整（含 </html>）
```

### 3.1 生成后自动入库（--ingest，2026-08-31 新增）

`full`（整场复盘）生成成功后，加 `--ingest` 自动沉淀到情报库：

```bash
python3 tools/generate_intel_report.py \
  --teams GX,FNC --date 2026-08-31 --node full --ingest \
  --intel-json runtime/danmu_sessions/lec_2026-08-31/intel.json \
  --slice-file <整场切片.jsonl> \
  --result-note "GX 2:0 FNC（官方 gameWins）" \
  --out reports/intel_danmu_LEC-GX-FNC_full_2026-08-31.html
```

`--ingest` 自动执行（tools/ingest_after_report.py，幂等）：

```text
1) matches.json 结果回填（找不到自动新建条目）；
2) 选手提及/锚点 -> players.json（accumulate_player_intel --files 本场弹幕）；
3) 队伍特质 -> teams.json（accumulate_team_traits --merge intel.json）；
4) 队伍画像 -> teams.json（accumulate_team_intel --match，容错）；
5) 索引/发布由 vps_publish 下一步处理。
```

也可单独跑：

```bash
python3 tools/ingest_after_report.py --root . --teams GX,FNC --date 2026-08-31 \
  --slug lol-gx-fnc-2026-08-31 \
  --slice-file <弹幕文件> --intel-json <intel.json> \
  --result "GX 2:0 FNC（官方）" --winner GX --score 2-0
```

`intel.json`（规则层）由 `tools/danmu_intel.py` 从弹幕产出：

```bash
python3 tools/danmu_intel.py \
  --input docs/data/danmu/slices/<match>/<窗口>.jsonl \
  --out runtime/danmu_sessions/<session>/intel.json
```

---

## 4. 发布（服务器 → 网站）

用 `tools/vps_publish.py`（VPS → GitHub Pages 自动同步 + 付费墙 + 速览卡审计）。

### 4.1 一次性配置（GitHub Deploy Key）

```bash
# 服务器生成 deploy key
ssh-keygen -t ed25519 -f ~/.ssh/github_deploy -N ""
# 公钥加到 GitHub 仓库 Settings -> Deploy keys（勾选写权限）
cat ~/.ssh/github_deploy.pub
```

### 4.2 发布脚本（systemd timer 每 5 分钟触发）

```bash
python3 tools/vps_publish.py
# 幂等：无新文件不提交；自动做：
#   speedcard 速览卡审计 -> favicon/nav/统计注入 -> 付费墙（已结束场次开放）-> push
```

systemd timer 示例：

```ini
# /etc/systemd/system/intel-publish.service
[Unit]
Description=Intel publish
[Service]
ExecStart=/opt/danmu-intel/.venv/bin/python /opt/danmu-intel/tools/vps_publish.py
WorkingDirectory=/opt/danmu-intel
Environment=DEEPSEEK_API_KEY=sk-你的key

# /etc/systemd/system/intel-publish.timer
[Timer]
OnBootSec=60
OnUnitActiveSec=300
[Install]
WantedBy=timers.target
```

```bash
systemctl daemon-reload && systemctl enable --now intel-publish.timer
```

---

## 5. 端到端示例（一场比赛全流程）

```bash
# ① 采集（LEC GX vs FNC，硕硕+毛毛）
python3 tools/run_danmu_session.py --session lec_2026-08-31 \
  --title "LEC 08-31 GX vs FNC" \
  --room huya_shuoshuo=https://www.huya.com/323444 \
  --room huya_maomao=https://www.huya.com/149346 --seconds 0 &

# ② 赛前切片 + 赛前情报
python3 tools/slice_danmu_by_match.py --manifest docs/data/danmu/slices/manifest.json
python3 tools/danmu_intel.py --input <赛前切片> --out runtime/danmu_sessions/lec_2026-08-31/intel.json
python3 tools/generate_intel_report.py --teams GX,FNC --date 2026-08-31 --node pre \
  --intel-json runtime/danmu_sessions/lec_2026-08-31/intel.json --slice-file <赛前切片> \
  --out reports/intel_danmu_LEC-GX-FNC_pre_2026-08-31.html

# ③ 局中节点（G1 mid / G2 bp / G2 end 等，循环）
python3 tools/generate_intel_report.py --teams GX,FNC --date 2026-08-31 --node game \
  --game 1 --gphase mid --intel-json ... --slice-file <G1中切片> \
  --out reports/intel_danmu_LEC-GX-FNC_G1_mid_2026-08-31.html

# ④ 比赛结束 → 整场复盘 + 自动入库
python3 tools/generate_intel_report.py --teams GX,FNC --date 2026-08-31 --node full \
  --intel-json ... --slice-file <整场切片> --result-note "GX 2:0 FNC（官方）" --ingest \
  --out reports/intel_danmu_LEC-GX-FNC_full_2026-08-31.html

# ⑤ 发布
python3 tools/vps_publish.py
```

---

## 6. 关键纪律（照此配置，防止线上质量崩）

```text
1. 事实层只信官方（Riot API / Liquipedia / Polymarket 结算），弹幕只做佐证；
2. 跨联赛分会话，禁止混源；切片用联赛默认采集集过滤；
3. 生成端门禁不过 = 情报未交付（不许人工放行跳过）；
4. 灰信号只标"观众质疑·非结论"，不升格；
5. 每场结束后做整场复盘 + 同步结构化库（matches/teams/players/gray）；
6. 所有时间用北京时间展示；缺口显式标注（不硬凑）。
```

## 7. 故障排查速查

| 现象 | 排查 |
| --- | --- |
| 采集 0 条/断流 | 查 session.json 心跳 + launchd/systemd 状态 + 房间是否在播 |
| 生成门禁不过 | 看输出缺哪段/标题是否自编，检查 intel.json 与切片是否对应本场 |
| API 401 | DEEPSEEK_API_KEY 未配置或失效 |
| 发布无新文件 | 确认 reports 有新 HTML + deploy key 权限 + timer 运行 |
| 情报内容明显错 | 先查输入（切片是否混源/窗口是否错），再查生成 |
