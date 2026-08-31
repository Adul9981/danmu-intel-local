# tools/ 工具索引（自动生成 · 2026-08-30）

> 本项目全部 Python 工具。通用工具带 argparse 参数（--root 指定项目根，缺省当前目录）；
> 一次性工具为历史场次生成脚本，仅参考不复用。
> **生成端**：prompts/ 固定提示词 + tools/generate_intel_report.py（程序调大模型 API，替代 Codex 会话）。
> **部署**：tools/make_deploy_package.py -> dist/intel_server_pkg/（云端一键跑）。

## 通用工具（可复用）

| 工具 | 用途 | 用法 |
| --- | --- | --- |
| absorb_legacy_intel.py | 历史画像/经验数据吸收工具（2026-08-30 建立）。 | `python3 tools/absorb_legacy_intel.py --root /Users/ad/Documents/polymarket` |
| absorb_p3_profiles.py | P3 画像库吸收工具（2026-08-30 建立）。 | `python3 tools/absorb_p3_profiles.py --root /Users/ad/Documents/polymarket` |
| accumulate_player_intel.py | 选手情报库自动沉淀工具（2026-08-30 建立）。 | `python3 tools/accumulate_player_intel.py --root /Users/ad/Documents/polymarket --scan` |
| accumulate_team_intel.py | 队伍情报库自动沉淀闭环（2026-08-26 用户定稿）。 | `python3 tools/accumulate_team_intel.py --root /opt/danmu-intel` |
| accumulate_team_traits.py | 队伍特质/倾向自动沉淀工具（2026-08-30 建立）。 | `python3 tools/accumulate_team_traits.py --root /Users/ad/Documents/polymarket --scan` |
| add_favicon.py | Add favicon <link> to every site HTML page (idempotent). | `` |
| add_paywall.py | Inject Pro paywall into premium intel pages (idempotent). | `` |
| add_site_nav.py | Idempotent unified top nav + simple breadcrumb for every site page. | `` |
| add_stats_track.py | Inject page-view tracking snippet into every site page (idempotent). | `` |
| append_knowledge_review.py | Append a completed grid trade review into the knowledge base and update the inde | `` |
| backfill_predictions.py | Backfill predictions from existing intel report HTML into matches.json. | `python3 tools/backfill_predictions.py [--reports reports] [--matches-json docs/data/intel/matches.json]` |
| backfill_results.py | Auto-backfill match results from Polymarket settlement (local daily). | `` |
| backfill_review_intel.py | 交易复盘 -> matches.json 盘口轨迹回填工具（2026-08-30 建立，P2）。 | `python3 tools/backfill_review_intel.py --root /Users/ad/Documents/polymarket` |
| bar_monitor_runner.py | 1-minute bar monitor + strategy state engine (execution layer). | `python3 tools/bar_monitor_runner.py --slug <event-slug> --strategy B_FAVORITE_DIP` |
| batch_counterfactual.py | Batch counterfactual review across all snapshot series (发现回测链, 只读). | `python3 tools/batch_counterfactual.py` |
| build_backtest_visual.py | Build visual backtest pages from compact backtest JSON files. | `` |
| build_closed_loop.py | Build a closed-loop evidence HTML page for a finished danmaku-intel match. | `python3 tools/build_closed_loop.py \` |
| build_gray_stats.py | Build the gray-signal verification stats page from structured data. | `python3 tools/build_gray_stats.py [--out .danmu_intel_site/intel/intel_gray_verification_stats.html]` |
| build_history_index.py | Build the historical danmaku intel library page with league/team/date filters. | `python3 tools/build_history_index.py [--site-dir .danmu_intel_site]` |
| build_home_stats.py | Update homepage "#intel" stats block with live asset counts. | `` |
| build_home_today.py | Update homepage "#today" block with today's key LoL matches. | `` |
| build_intel_bp_stats.py | Build BP 信号兑现率统计页（reports/intel_bp_verification_stats.html）。 | `` |
| build_intel_champion_lookup.py | Build 选手 × 英雄 锚点速查表（reports/intel_champion_anchor_lookup.html）。 | `` |
| build_intel_graph.py | 构建弹幕情报库关系图谱（graph.json）：从各实体文件推导关联边。 | `` |
| build_intel_pregame.py | 生成「赛前速览」情报页：结合已有情报库，比赛前快速查询一页看全。 | `python3 tools/build_intel_pregame.py --teams KC,SHFT --league LEC --date 2026-08-24` |
| build_intel_profiles.py | Build C-type profile pages (teams/players/leagues) + gray verification stats. | `` |
| build_intel_quick_lookup.py | 生成情报速查台（静态 HTML，浏览器内搜索队伍/英雄/选手/昵称/比赛）。 | `` |
| build_intel_relational.py | 生成情报库「关联浏览台」（静态 HTML）：从任意实体出发，浏览其关联网络。 | `` |
| build_match_page.py | Build a match-detail page with the unified two-level selector shell. | `python3 tools/build_match_page.py --match-id 2026-08-22_we_lgd [--push]` |
| build_morphology_html.py | Regenerate the morphology census HTML with SVG charts (read-only data). | `` |
| build_node_page.py | Build a node intel page following the 10-section INTEL_HTML_TEMPLATE. | `python3 tools/build_node_page.py --match-id 2026-08-18_dns_ns --game g1 --node bp \` |
| build_profiles_page.py | Build the teams/players/leagues profile quick-reference page. | `` |
| cancel_grid_orders.py | Cancel live orders tracked by a grid runner state file. | `` |
| check_gray_escalation.py | 灰信号实体"再犯升级"自动检查 + 报告页。 | `` |
| check_grid_status.py | Read-only status check for a grid runner state file. | `` |
| check_lpl_gamewins.py | Print official gameWins for LPL matches on a date (read-only). | `` |
| check_open_orders.py | List open orders with loud failure on API errors. | `` |
| check_stream_match.py | 直播内容匹配校验（2026-08-26 用户定稿，切赛识别主信号）。 | `python3 tools/check_stream_match.py --match lol-drxc-foxy-2026-08-25 \` |
| classify_pattern.py | Classify 1-minute/5-minute price series into reversal-pattern-library labels. | `python3 tools/classify_pattern.py --snapshot docs/data/snapshots/2026-08-07_lol-fox1-bro2` |
| cleanup_intel_artifacts.py | 情报中间产物清理 + 核心情报库保护备份（2026-08-26 建立）。 | `python3 tools/cleanup_intel_artifacts.py --dry-run   # 只看会删什么` |
| comment_intel.py | Pre-match / in-play comment intel for the task-2 scan pipeline. | `python3 tools/comment_intel.py --events-json runtime/watchlist_events.json` |
| counterfactual_review.py | 反事实复盘：给定价格序列 + 交易参数，计算"若按 D2 锁盈 / D3 止损规则执行"的结果。 | `python3 tools/counterfactual_review.py --snapshot-file <jsonl> --side <方向> \` |
| create_trade_launcher.py | Create a one-click macOS launcher for a prepared grid trade plan. | `` |
| create_trade_review.py | Create a standard post-trade review document from a grid state file. | `` |
| daily_intel_check.py | Daily Polymarket esports match check for the danmu-intel product. | `` |
| daily_pattern_review.py | Daily pattern review + inactivity/content warnings (automation entry point). | `` |
| danmu_intel.py | Extract trade-relevant intel from Huya danmaku JSONL. | `python3 tools/danmu_intel.py --input docs/data/danmu/shuoshuo/2026-08-17_323444.jsonl \` |
| danmu_live_monitor.py | Live danmaku monitor: analyze a growing JSONL every N seconds and refresh an HTM | `python3 tools/danmu_live_monitor.py \` |
| danmu_report.py | Generate a lightweight SAP/Apple-style HTML briefing from a Huya danmaku JSONL. | `` |
| edge_stats.py | EDGE LOG statistics: group recorded edges by info type / edge vs conviction. | `` |
| event_marker.py | Event marker tool v1: record match window markers for later data slicing. | `` |
| export_golden_set.py | Export a classifier golden set from all snapshot classification.jsonl files. | `python3 tools/export_golden_set.py` |
| export_today_matches.py | Export today's esports matches from watchlist_events.json -> matches_today.json. | `python3 tools/export_today_matches.py [--input runtime/watchlist_events.json]` |
| extract_intel_anchors.py | intel_pages MD 批量锚点提取工具（2026-08-30 建立，P1）。 | `python3 tools/extract_intel_anchors.py --root /Users/ad/Documents/polymarket` |
| fetch_cs2_liquipedia.py | Fetch CS2 match facts (time, teams, maps, scores) from Liquipedia CS wiki. | `python3 tools/fetch_cs2_liquipedia.py --event "BLAST/Open/2026/Fall"` |
| fetch_danmu_multi.py | Concurrent live-danmaku capture for multiple rooms (Huya + SOOP). | `` |
| fetch_game_status.py | Fetch game/map winner market status for watchlist matches -> runtime/game_status | `python3 tools/fetch_game_status.py` |
| fetch_huya_danmu.py | Fetch live danmaku from a Huya room via the real-url WebSocket client. | `` |
| fetch_huya_replay.py | Download a Huya live replay (直播录像) audio for the intel pipeline. | `python3 tools/fetch_huya_replay.py --id 1121405272` |
| fetch_kick_danmu.py | Fetch live chat (danmaku) from a Kick.com channel via public APIs. | `` |
| fetch_official_game_data.py | Fetch official LoL esports lineup / result data from Riot APIs. | `python3 tools/fetch_official_game_data.py --league lck --date 2026-08-27 --teams NS,BFX` |
| fetch_price_snapshot.py | Fetch 1-minute Polymarket price snapshots for an esports event into docs/data/sn | `python3 tools/fetch_price_snapshot.py --slug lol-blg-tes-2026-08-07` |
| fetch_series_comments.py | Fetch and slice Polymarket series comments into the intel knowledge base. | `python3 tools/fetch_series_comments.py fetch --series lol --days 5` |
| fetch_soop_danmu.py | Fetch live chat (danmaku) from a SOOP (ex-AfreecaTV) broadcast room. | `` |
| fetch_soop_vod_chat.py | Backfill SOOP (ex-AfreecaTV) VOD chat history as JSONL. | `` |
| fetch_twitch_danmu.py | Fetch live chat (danmaku) from a Twitch channel via anonymous IRC. | `python3 tools/fetch_twitch_danmu.py \` |
| follow_winner_accounts.py | Long-term tracking of winning/profitable esports accounts (read-only). | `` |
| forensics_arb_backtester.py | Backtester for S-F1 complete-set arbitrage (SigmaP mispricing). | `` |
| forensics_arb_scanner.py | S-F1 完整集定价套利只读扫描器 v0 (forensics_arb_scanner.py) | `python3 tools/forensics_arb_scanner.py` |
| forensics_price_path_analysis.py | Unified price-path analysis for esports winner markets (read-only). | `` |
| forensics_sigma_scan.py | Sigma-p mispricing scanner for Polymarket neg-risk groups (read-only). | `` |
| generate_intel_report.py | 程序化情报生成端（2026-08-30 建立，替代"Codex 会话生成"）。 | `python3 tools/generate_intel_report.py --teams VIT,SHFT --date 2026-08-30 \` |
| grid_config_generator.py | Generate trade_config JSON for prediction-market grid strategies. | `` |
| grid_plan_runner.py | Run a fixed-USD grid trade plan through the existing Polymarket bot code. | `` |
| grid_status_summary.py | Human-friendly status summary for a grid runner state file. | `` |
| html_to_intel_md.py | Convert an intel HTML page to a full-fidelity Markdown mirror. | `python3 tools/html_to_intel_md.py \` |
| intel_query.py | 弹幕情报库检索工具（英雄×队伍×选手×比赛×锚点）。 | `python3 tools/intel_query.py 杰斯            # 全库关键词检索` |
| intel_stats.py | Intel signal credibility statistics: source type x signal tag x verification. | `` |
| label_esports_users.py | Label esports users by on-chain behavior for a BO3 moneyline event. | `python3 tools/label_esports_users.py label <event_slug> [--data-dir DIR] [--db PATH]` |
| llm_client.py | 大模型直连客户端（极简架构 · 固定提示词 + 数据 -> 结论）。 | `` |
| lottery_machine_backtest.py | Lottery machine backtest: layer-1 deep-lottery ladders + layer-2 rebound confirm | `` |
| make_deploy_package.py | 情报服务部署包制作工具（2026-08-30 建立，任务 3）。 | `python3 tools/make_deploy_package.py --out dist/intel_server_pkg` |
| mapread_wallet_tracker.py | Mapread wallet tracker - ingest mapread.gg public JSON APIs into the forensics l | `python3 tools/mapread_wallet_tracker.py board [--segment all|lol|cs2|dota2|valorant] [--out DIR]` |
| market_scanner.py | Opportunity scanner for discovery patterns. | `` |
| match_manager.py | Match management records: per-match status cards (series progress + order flags) | `python3 tools/match_manager.py init --slug <slug> --title "..." --league LPL --bo 3` |
| match_state_guard.py | Match result declaration guard (结果判定门禁 · 2026-08-25). | `python3 tools/match_state_guard.py --teams "GX,G2" \` |
| match_status.py | Match status resolution (shared by today page & homepage generators). | `` |
| morphology_census.py | Definitive price-morphology census across all snapshot matches (read-only). | `` |
| morphology_comparison.py | Complete base-morphology comparison with REAL match minutes (read-only). | `` |
| observe_esports_match.py | Read-only live observer for an esports match's market prices. | `python3 tools/observe_esports_match.py --slug lol-navi-th-2026-08-17` |
| opinion_cluster.py | 弹幕意见聚类与归因（2026-08-26 用户定稿，情报加工层）。 | `python3 tools/opinion_cluster.py --match lol-drxc-foxy-2026-08-25 \` |
| path_morphology_live.py | Forward-looking morphology classification signals (read-only). | `` |
| pattern_audit.py | Pattern library audit: re-validation counts + new-pattern discovery. | `python3 tools/pattern_audit.py` |
| polymarket_strategy_backtester.py | Backtest A/B grid strategy shape on a Polymarket event. | `` |
| prematch_predictor.py | V2-S2 pre-match pattern prediction + pre-match resting order plan (执行准备链). | `python3 tools/prematch_predictor.py --slug <event-slug>` |
| prepare_grid_trade.py | Prepare a fixed-USD grid trade from a Polymarket URL. | `` |
| price_path_taxonomy.py | Full price-path taxonomy across every snapshot match (read-only). | `` |
| publish_closed_loop.py | Build and optionally publish a closed-loop page to the danmu-intel site. | `python3 tools/publish_closed_loop.py --match-id 2026-08-22_we_lgd --push` |
| publish_intel_pages.py | Publish danmaku intel pages to the danmu-intel site + regenerate index. | `python3 tools/publish_intel_pages.py [--site-dir .danmu_intel_site] [--push]` |
| quick_signal_monitor.py | One-minute lightweight signal monitor (read-only). | `` |
| rebuild_shells.py | Rebuild all match timeline shells in REPORTS (server side). | `python3 tools/rebuild_shells.py [--reports DIR]` |
| rebuild_shells_0828.py | Rebuild match timeline shells for 2026-08-28 finished matches in the pub dir. | `` |
| record_intel_signal.py | Record and verify subjective intel signals (Huya casters / streamers / danmaku). | `python3 tools/record_intel_signal.py add --date 2026-08-08 --match lol-... \` |
| record_prediction.py | Record / verify an audience prediction into docs/data/intel/matches.json. | `python3 tools/record_prediction.py --match-id 2026-08-22_we_lgd \` |
| reformat_intel_template.py | Reformat legacy intel HTML pages into the decision-first 12-section template. | `python3 tools/reformat_intel_template.py --html reports/intel_danmu_DNS-DRX_2026-08-24.html` |
| register_match.py | 比赛日程登记：往 docs/data/danmu/schedule.json 增改一条比赛窗口。 | `python3 tools/register_match.py --match-id 2026-08-23_blg_al \` |
| render_fast_intel.py | 规则直出情报页（极简极省 · 零 LLM Token）。 | `` |
| replay_bar_monitor.py | Historical validation: replay snapshot series through the bar monitor engine. | `python3 tools/replay_bar_monitor.py` |
| resource_watchdog.py | 服务器资源预警（2026-08-26 建立）：内存 / 磁盘 / 情报中间产物监控。 | `` |
| route_resonance.py | 多路直播间共振检测：判断某关键词/事件在几路弹幕中同时出现。 | `python3 tools/route_resonance.py 蛇女 --date 2026-08-24 --routes shuoshuo_323444,official_660000` |
| run_danmu_session.py | Run a resilient multi-room danmaku intelligence session. | `` |
| run_speed_fix.py | 服务器端速览卡批量修复入口（2026-08-26）。 | `` |
| run_speed_fix_local.py | 本地速览卡批量修复入口（2026-08-26，独立于 ssh 场景）。 | `` |
| slice_danmu_by_match.py | Slice raw danmaku JSONL by MATCH dimension (a BO series with optional games). | `python3 tools/slice_danmu_by_match.py --manifest docs/data/danmu/slices/manifest.json` |
| soop_live_monitor.py | Live monitor for SOOP danmaku: refresh an SAP-style HTML page every N seconds. | `python3 tools/soop_live_monitor.py \` |
| speedcard_consistency.py | 速览卡 ↔ 正文一致性检查与自动修复（2026-08-26 用户定稿，最高）。 | `` |
| stats_server.py | Minimal site traffic stats server for danmu-intel (VPS side). | `` |
| summarize_scan_diagnostics.py | Summarize task 2 live scan outputs in Chinese. | `` |
| sync_cs_base.py | CS2 官方基础数据同步工具（2026-08-30 建立）。 | `python3 tools/sync_cs_base.py --root /Users/ad/Documents/polymarket` |
| sync_danmu_from_server.py | 从线上采集服务器同步弹幕数据到本地（rsync 增量）。 | `python3 tools/sync_danmu_from_server.py            # 按配置同步` |
| sync_official_base.py | 官方基础数据库同步工具（2026-08-30 建立）。 | `python3 tools/sync_official_base.py --root /Users/ad/Documents/polymarket` |
| task2_pipeline.py | Task 2 automation pipeline: scan -> action queue -> bar monitor wiring. | `python3 tools/task2_pipeline.py --once` |
| transcribe_audio.py | Transcribe recorded live-stream audio to Chinese text (intel pipeline stage 2). | `` |
| update_site_today.py | Generate the danmu-intel site's auto "today matches" page. | `python3 tools/update_site_today.py --date 2026-08-23` |
| verify_match_end.py | Verify whether a danmaku window really signals a match END (防误判). | `python3 tools/verify_match_end.py --input docs/data/danmu/huya/xxx.jsonl \` |
| verify_match_result.py | 比赛结果官方结算快速校验（Polymarket 结算优先，零网页搜索）。 | `python3 tools/verify_match_result.py                  # 扫描全部待确认且带 slug 的比赛` |
| void_match_intel.py | 作废某场比赛的情报数据（2026-08-26 用户定稿：数据错误/混源即整场作废）。 | `` |
| vps_backfill_nodes.py | Backfill pre/live node pages for finished matches missing nodes. | `python3 tools/vps_backfill_nodes.py --match lol-gx-g2-2026-08-24` |
| vps_capture.py | VPS 7x24 弹幕采集守护（临时过渡方案：VPS 只抓弹幕，本地做分析）。 | `python3 tools/vps_capture.py                # 常驻守护` |
| vps_intel_pipeline.py | VPS intel pipeline: match end detection -> slice -> rule intel -> Codex report. | `python3 tools/vps_intel_pipeline.py --once        # 定时触发（每 5 分钟）` |
| vps_publish.py | VPS -> GitHub Pages auto-publish: sync generated intel pages to danmu-intel repo | `` |
| vps_self_check.py | VPS self-check: auto-detect and repair data-integrity issues. | `` |

## 一次性/历史脚本（不复用，仅参考）

| 工具 | 用途 |
| --- | --- |
| cleanup_g3.py | 应急：彻底下架 KT vs BRO G3 全部节点（bp/mid/end），并重建时间轴。 |
| gen_aurora_dendele_full_2026-08-28.py | Aurora Gaming vs DENDELE CS 整场复盘（2026-08-28 · BLAST Open Porto Group A 败者组 R1）。 |
| gen_bro_bfx_g3.py | HANJIN BRION vs BNK FEARX G3 BP 后/局中情报（2026-08-28，LCK 入围赛 BO5）。 |
| gen_bro_bfx_g4.py | HANJIN BRION vs BNK FEARX G4 BP 后/局中情报（2026-08-28，LCK 入围赛 BO5）。 |
| gen_deep_intel.py | 深度情报页生成器（固定提示词 + 数据 -> API -> 结论填入骨架）。 |
| gen_edg_nip_full_2026-08-28.py | EDward Gaming vs Ninjas in Pyjamas 整场复盘（2026-08-28 · LPL 骑士之路 BO5）。 |
| gen_fut_legacy_full.py | FUT vs Legacy G2 结束 + 整场复盘（2026-08-27，BLAST Open Porto Group B）。 |
| gen_fut_legacy_g1.py | FUT vs Legacy G1 节点（2026-08-27，22:30 CST 开赛，图一 Ancient）。 |
| gen_fut_legacy_g1_end.py | FUT vs Legacy G1 结束情报（2026-08-27，22:30 CST 开赛，图一 Ancient）。 |
| gen_fut_legacy_g2_bp.py | FUT vs Legacy G2 BP/开局情报（2026-08-27，图二 Dust II 沙二）。 |
| gen_fut_legacy_g2_mid.py | FUT vs Legacy G2 局中情报（2026-08-27，图二 Dust II 沙二）。 |
| gen_mouz_9z_g1.py | MOUZ vs 9z G1 三节点修正页（2026-08-27，官方 20:00 CST 开赛）。 |
| gen_mouz_full.py | MOUZ vs 9z G2 结束 + 整场复盘（2026-08-27，MOUZ 2-0，官方窗口）。 |
| gen_navi_m80_pages.py | 生成 NAVI vs M80（BLAST Open Porto · 2026-08-26）G1 局后复盘页。 |
| gen_ns_fox1_g1_end.py | 生成 NS vs BFX（LCK 骑士之路 R1）G1 局末情报页（2026-08-27）。 |
| gen_ns_full.py | NS vs BFX 整场复盘（2026-08-27，BFX 3-1 NS，Polymarket 仲裁）。 |
| gen_ns_g3_bp_clean.py | NS vs BFX G3 BP 后/开局情报（干净窗口版，2026-08-27）。 |
| gen_spirit_dendele_pages.py | 生成 Spirit vs DENDELE CS（BLAST Open Porto · 2026-08-26）情报页。 |
| gen_spirit_g2_full_2026-08-28.py | Spirit vs G2 整场复盘（2026-08-28 · BLAST Open Porto Group A UB 半决赛1）。 |
| gen_t1_bfx_g1_end_2026-08-29.py | T1 vs BNK FEARX G1 结束情报（2026-08-29 · LCK 季后赛 BO5）。 |
| gen_t1_bfx_g2_bp_2026-08-29.py | T1 vs BNK FEARX G2 BP 后情报（2026-08-29 · LCK 季后赛 BO5）。 |
| gen_tt_ig_full_2026-08-28.py | ThunderTalk Gaming vs Invictus Gaming 整场复盘（2026-08-28 · LPL 骑士之路 BO5）。 |
| gen_yesterday_backfill.py | 批量补齐 2026-08-26 缺失节点情报页（事后回补，标注来源）。 |
| lock_removed_nodes.py | 锁定已下架节点：G1/G2/G3 全部相位写状态文件（流水线跳过），并清理残留报告。 |
| regen_g34.py | 应急：生成 KT vs BRO G3 局末 + G4 BP（Codex 全量，用户标准格式）。 |
| regen_kt_nodes.py | 应急：重新生成 lol-kt-bro2-2026-08-26 G1 节点（BP/MID/END，BO5，虎牙源已修复）。 |