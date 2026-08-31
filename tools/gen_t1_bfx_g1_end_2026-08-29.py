#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T1 vs BNK FEARX G1 结束情报（2026-08-29 · LCK 季后赛 BO5）。

官方：G1 T1 胜（Riot gameWins 1-0，matchId 117030752644841589）；
G2 进行中。弹幕五路（硕硕/957/毛毛/米勒/Remember）采集。
"""

from pathlib import Path

from gen_fut_legacy_g1_end import page  # noqa: E402

REPORTS = Path("/Users/ad/Documents/polymarket/reports")

SPEED = """
  <div class="top">
    <span class="score-big">G1 T1 胜（官方 gameWins 1-0）· 系列 T1 1-0 BFX</span>
    <span class="badge b-ok">官方 gameWins 确认</span>
    <span class="badge b-anchor">G2 进行中</span>
    <span class="badge b-risk">灰信号 50 条 · 观众质疑非结论</span>
  </div>
  <div style="margin-top:8px">
    <div class="sig"><span class="tag" style="color:var(--accent)">锚点</span><span><b>BFX 打野 Raptor 皇子是 G1 最大威胁点但未兑现</b>："皇子不失误t1炸了""eq中了t1是不是炸了"——T1 靠团队韧性顶住皇子节奏拿下 G1，<b>说明</b> G1 胜负手在皇子节奏对位，G2 需继续盯 BFX 打野（官方：Raptor 皇子 / T1 Oner 蔚） <span class="meta">→ 详 §3/§7</span></span></div>
    <div class="sig"><span class="tag" style="color:var(--bad)">风险</span><span><b>灰信号 50 条集中指向 BFX 打野</b>（"假赛王/买了/明演了/故意送"刷屏，观众质疑·非结论）——被质疑方 G1 输球，<b>需警惕</b> G2 若 BFX 打野再现异常节奏，须配合盘口/价格验证，不裸赌 <span class="meta">→ 详 §2</span></span></div>
    <div class="sig"><span class="tag" style="color:var(--sub)">盘口</span><span><b>"大33"杀数盘观众口径兑现</b>（"33到了 可以结束了"）——<b>表明</b> 33 杀线为 G1 关键收尾线，可作 G2 盘口观察锚；"48"梗（573 条命中）为管泽元事件玩梗，非本场盘口 <span class="meta">→ 详 §4</span></span></div>
    <div class="sig"><span class="tag" style="color:var(--purple)">共识</span><span><b>T1 强度被认可 + Faker 状态成讨论焦点（246 条）</b>："为什么T1这么变态"；"感觉老李今天状态不好啊"（负向）vs 皮肤梗——G2 关注 Faker 燕雀/对位与 BFX 打野节奏 <span class="meta">→ 详 §5/§8</span></span></div>
  </div>
  <div class="errbox"><b>数据说明：</b>本页为补发（管线 Codex 全量生成超时未出，本地快速生成）；弹幕窗口 16:09–16:58 CST（12943 条/2914 活跃）；开赛段 16:00–16:09 因采集器故障缺采（已修复，G2 起完整）。结果以官方 gameWins 为准。</div>
"""


SECTIONS = [
    ("1", "比赛信息与结果总览（官方源）", """<table>
    <tr><td>对阵</td><td>T1 vs BNK FEARX（BFX）· LCK 季后赛（世界赛名额关键战）· BO5 · slug=lol-t1-fox1-2026-08-29</td></tr>
    <tr><td>官方时间</td><td>2026-08-29 16:00 CST 开赛（08:00 UTC）· Riot matchId 117030752644841589 · 状态 inProgress</td></tr>
    <tr><td>系列状态（官方）</td><td><b>T1 1 - 0 BFX</b>（Riot gameWins 1-0）：G1 T1 胜；G2 进行中</td></tr>
    <tr><td>弹幕规模（G1）</td><td>16:09–16:58 CST 窗口 <b>12,943 条 / 2,914 活跃 / 268.9 条/分</b>；密度峰值 16:45（1230 条/分）</td></tr>
    <tr><td>完整性</td><td><span class="badge b-ok">五路齐采</span>硕硕 323444 + 957 890001 + 毛毛 149346 + 米勒 149361 + Remember rememberlol；<b>缺口：16:00–16:09 开赛段未采</b>（采集器故障，已修复）</td></tr>
  </table>
  <p class="meta">系列/比分 = Riot API gameWins（官方）；阵容 = Riot window 回填；弹幕仅作过程佐证。</p>"""),
    ("2", "灰信号汇总（风险 · 观众质疑非结论）", """<p><b>G1 窗口有效 50 条</b>（中预警 · 五路共振 · 观众质疑非结论），集中指向 <b>BFX 打野 Raptor</b>：</p>
  <ul>
    <li><b>"假赛王"叙事反复</b>："bfx打野出了名的假赛王，先锋赛打G2就唐了3吧"（多次刷屏，指向 BFX 打野历史表现）</li>
    <li><b>当场质疑</b>："买了""假赛离谱""明演了""故意送耶稣来了也没用呀""队友人都死了，这他妈买了吧？"</li>
    <li>盘口联动："大33已经放里边了""33到了 可以结束了"（33 杀线口径，与"买了"质疑同现）</li>
  </ul>
  <div class="warnbox"><b>纪律声明：</b>以上均为观众质疑/玩梗，<b>非假赛证据</b>；灰信号只作风险标注与跨场实体跟踪（BFX 打野进入 gray-tracking），不上升结论。G1 被质疑方（BFX）输球，但按"灰信号只作统计不推因果"纪律处理。</div>"""),
    ("3", "BP 与阵容情报（官方 window + 弹幕）", """<p><b>✅ 官方阵容（Riot window 回填，2026-08-29 17:10 CST）：</b></p>
  <table>
    <tr><th>队</th><th>G1 阵容</th><th>弹幕口径</th></tr>
    <tr><td>BFX（蓝）</td><td>Clear 奎桑提 · Raptor <b>皇子</b> · VicLa 瑞兹 · Taeyoon 卢锡安 · Kellin 米利欧</td><td>"皇子不失误t1炸了""eq中了t1是不是炸了"——皇子节奏是 BFX 最大威胁点；"bfx优势，你敢信？"（前期领先）</td></tr>
    <tr><td>T1（红）</td><td>Doran 杰斯 · Oner 蔚 · Faker <b>燕雀</b> · Peyz 芸阿娜 · Keria 璐璐</td><td>"这皇子不比tes的强？"（T1 侧视角）；Faker 燕雀 246 条提及（"状态不好/又送了"负向 vs 皮肤梗）；"打FAKER就行了"</td></tr>
  </table>
  <p class="meta">BP 后战绩情报：无"选手×英雄历史战绩"类弹幕；BFX 打野"先锋赛打 G2 唐 3 把"为观众历史叙事（灰信号语境，非确认）。</p>"""),
    ("4", "盘口与市场讨论", """<ul>
    <li><b>"大33"杀数盘（观众口径兑现）：</b>"大33已经放里边了""33到了 可以结束了"——观众确认 33 杀线达成，比赛随之结束；本场唯一有效盘口信号（单源弹幕口径，待平台回填）。</li>
    <li><b>"48"梗 573 条命中：</b>"48bin/力挺管哥/4848448"为管泽元相关事件玩梗，<b>非本场盘口</b>，已剔除。</li>
    <li><b>官方结算：</b>G1 Winner 官方 gameWins T1 胜（1-0）；G2 进行中。</li>
  </ul>"""),
    ("5", "方向性情报板（锚点 × 共识 × 风险）", """<table>
    <tr><th>维度</th><th>BFX</th><th>T1</th></tr>
    <tr><td>强度层</td><td>黑马挑战者；Raptor 皇子节奏强但被质疑（灰信号实体）；前期能拿到优势（"bfx优势你敢信"）</td><td>夺冠热门；团队韧性（顶住皇子节奏拿下 G1）；Faker 状态成焦点</td></tr>
    <tr><td>本场信号（官方）</td><td>G1 告负（0-1）；放龙质疑（"左边优势放龙不知道怎么想的"）</td><td>G1 胜（1-0）；"为什么T1这么变态"</td></tr>
    <tr><td>反方声音</td><td>"现在的t1真不一定打的过ig"（嘲讽 T1 强度）</td><td>"感觉老李今天状态不好啊""老李又送了"（Faker 负向）</td></tr>
    <tr><td>共识</td><td colspan="2">T1 强度被认可；"和昨天ig一样，纯人机/保送右边"（T1 晋级叙事）；Faker 状态讨论 246 条为 G2 最大变量</td></tr>
  </table>"""),
    ("6", "情报含义与决策落点", """<ul>
    <li><b>系列结论（G1）：</b>T1 <b>1-0</b> BFX（官方）——G2 进行中，T1 先手。</li>
    <li><b>核心胜负手：</b>BFX 皇子节奏（Raptor）被 T1 团队韧性顶住；Faker 燕雀对位 VicLa 瑞兹成系列焦点；"大33"杀数盘口径兑现说明 G1 为高击杀局。</li>
    <li><b>风险提示：</b>灰信号 50 条指向 BFX 打野（观众质疑·非结论，跨场跟踪）；开赛段 16:00-16:09 数据缺口（采集器故障已修复）；盘口"大33"为单源弹幕口径待平台回填。</li>
    <li><b>G2 关注：</b>BFX 是否继续放皇子/换打野节奏、Faker 状态与燕雀对位、T1 是否延续速通；灰信号实体（BFX 打野）进入长期跟踪。</li>
  </ul>"""),
    ("7", "逐局复盘（G1 · 官方结果 + 弹幕过程）", """<table>
    <tr><th>阶段</th><th>过程（弹幕口径 · 北京时间）</th></tr>
    <tr><td>BP/开局（16:00–16:09）</td><td>官方阵容确认（BFX 蓝皇子/瑞兹/卢锡安 vs T1 红杰斯/蔚/燕雀/芸阿娜/璐璐）；<b>开赛段因采集器故障缺采</b>（缺口显式标注）</td></tr>
    <tr><td>对线/节奏（16:09–16:40）</td><td>"bfx优势，你敢信？"（BFX 前期领先）；"小龙不要吗/左边优势放龙不知道怎么想的"（BFX 放龙质疑）；"皇子不失误t1炸了""eq中了t1是不是炸了"（皇子威胁点）</td></tr>
    <tr><td>关键团/收尾（16:40–16:58）</td><td>密度峰值 16:45（1230 条/分）；"大33到了 可以结束了"（33 杀线兑现）；T1 拿下 G1；"为什么T1这么变态"刷屏</td></tr>
  </table>
  <p class="meta">G2 进行中（官方 gameWins 1-0）。</p>"""),
    ("8", "队伍 / 人员画像（证据层 · 官方 + 弹幕口径）", """<p><b>T1：</b>LCK 夺冠热门、世界赛名额关键战；G1 顶住 BFX 皇子节奏拿下——<b>Faker</b> 燕雀 246 条提及（"状态不好/又送了"负向 vs "皮肤梗"支持，G2 最大变量）；Oner 蔚、"这皇子不比tes的强"（T1 侧）；Doran 杰斯、Peyz 芸阿娜、Keria 璐璐。</p>
  <p><b>BFX（BNK FEARX）：</b>黑马挑战者（前日 3-2 逆转 BRO 晋级）；<b>Raptor</b> 皇子为 G1 最大威胁点，但被观众"假赛王/买了"集中质疑（灰信号实体，跨场跟踪）；Clear 奎桑提、VicLa 瑞兹、Taeyoon 卢锡安、Kellin 米利欧；"bfx优势你敢信"（前期能拿优势）。</p>
  <p><b>周边叙事：</b>"保送右边/纯人机"（T1 晋级预期）；"48"管泽元梗（LPL 事件，非本场）；Guma 粉丝 ID 刷屏（Gumayusi#98891）。</p>"""),
    ("9", "联赛规律与版本（沉淀层）", """<ul>
    <li><b>LCK 季后赛 BO5：</b>高击杀局（33 杀线口径）下强队韧性更关键——T1 顶住皇子节奏说明"节奏型打野"在 BO5 的克制关系。</li>
    <li><b>灰信号触发模式：</b>打野"假赛王"历史叙事 + 当场"买了/明演"——集中指向打野位，需跨场验证（BFX 打野实体跟踪）。</li>
    <li><b>数据完备性：</b>五路虎牙同采后 LCK 信号量级显著提升（G1 12,943 条）；开赛段缺口已通过采集器修复避免再犯。</li>
  </ul>"""),
    ("10", "预测验证回填（沉淀层）", """<table>
    <tr><th>预测/锚点</th><th>时间</th><th>状态</th></tr>
    <tr><td>"bfx优势，你敢信？"（BFX 前期领先）</td><td>16:1x</td><td>BFX 前期优势存在但<b>未兑现胜局</b>（T1 赢 G1）</td></tr>
    <tr><td>"皇子不失误t1炸了 / eq中了t1是不是炸了"（BFX 皇子威胁）</td><td>16:1x-16:3x</td><td><b>未兑现</b>（皇子节奏被 T1 顶住）——威胁点确认但未能终结</td></tr>
    <tr><td>"大33到了 可以结束了"（33 杀线）</td><td>16:4x</td><td><b>兑现</b>（33 杀线达成，比赛收尾）</td></tr>
    <tr><td>"感觉老李今天状态不好啊"（Faker 负向）</td><td>16:1x-16:4x</td><td>G1 结果 T1 胜；Faker 状态作为 G2 观察项（待验证）</td></tr>
    <tr><td>灰信号 50 条（BFX 打野假赛王/买了）</td><td>16:09-16:58</td><td>被质疑方 BFX 输球——按纪律只作统计不推因果（观众质疑·非结论）</td></tr>
  </table>"""),
    ("11", "数据与溯源", """<p><b>官方源：</b>Riot API getSchedule（matchId 117030752644841589，inProgress，gameWins T1 1-0）+ getEventDetails/window（G1 官方阵容回填，2026-08-29 17:10 CST 抓取）。</p>
  <p class="meta"><b>弹幕数据窗口</b>：16:09–16:58 CST（08:09–08:58 UTC）· 12,943 条 / 2,914 活跃 / 268.9 条分；密度峰值 16:45（1230 条/分）。</p>
  <p class="meta"><b>数据源</b>：虎牙五路同会话——硕硕 323444 / 957 890001 / 毛毛 149346 / 米勒 149361 / Remember rememberlol；<b>缺口：16:00–16:09 开赛段未采</b>（采集器 08:00 UTC 检测离线后未复查，已修复为 60s 复查自动连接）。</p>
  <p class="meta"><b>结果仲裁</b>：Riot gameWins（官方）；弹幕仅过程佐证；"大33"盘口为单源弹幕口径待平台回填。</p>
  <p class="meta"><b>情报输出时间</b>：2026-08-29 17:15 CST（北京时间）· 本页为管线超时补发，本地快速生成；情报原则：核心=本场弹幕，事实层=官方源仲裁。</p>"""),
]


HTML = page(
    "LCK 季后赛 · T1 vs BNK FEARX · G1 结束情报（T1 1-0）· 2026-08-29",
    "LCK 季后赛 BO5 · G1 T1 胜（官方 gameWins 1-0）· G2 进行中 · 2026-08-29",
    SPEED,
    SECTIONS,
    "弹幕情报 · 观众质疑非结论 · 结果以官方源为准 · Polymarket 电竞情报项目",
)


def main() -> None:
    out = REPORTS / "intel_danmu_T1-BNK FEARX_2026-08-29_g1_end.html"
    out.write_text(HTML, encoding="utf-8")
    print(f"written: {out}")


if __name__ == "__main__":
    main()
