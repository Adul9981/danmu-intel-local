#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T1 vs BNK FEARX G2 BP 后情报（2026-08-29 · LCK 季后赛 BO5）。

系列 T1 1-0（官方 gameWins）；G2 进行中。官方 window 阵容回填。
"""

from pathlib import Path

from gen_fut_legacy_g1_end import page  # noqa: E402

REPORTS = Path("/Users/ad/Documents/polymarket/reports")

SPEED = """
  <div class="top">
    <span class="score-big">G2 BP 后 · 系列 T1 1-0 BFX（官方）· 局中·非终局</span>
    <span class="badge b-ok">官方 gameWins + 阵容确认</span>
    <span class="badge b-anchor">Faker 阿卡丽兑现弹幕预测</span>
    <span class="badge b-risk">灰信号 40 条早现 · 观众质疑非结论</span>
  </div>
  <div style="margin-top:8px">
    <div class="sig"><span class="tag" style="color:var(--accent)">锚点</span><span><b>Faker 阿卡丽（官方确认）兑现 BP 讨论</b>："faker跟我学的akl""李哥阿卡丽还一坨？？"——G2 中单对位 Faker 阿卡丽 vs VicLa 阿狸成为胜负手，<b>说明</b> T1 主动提速、BFX 需处理阿卡丽进场（官方：T1 Faker 阿卡丽 / BFX VicLa 阿狸） <span class="meta">→ 详 §3</span></span></div>
    <div class="sig"><span class="tag" style="color:var(--bad)">风险</span><span><b>灰信号 40 条在 G2 开局即出现</b>（"第二把假赛开始了""故意装糖""又是这个剧本？"，观众质疑·非结论）——<b>需警惕</b> G2 若出现异常节奏（配合"买了"类词），须盘口/价格验证，不裸赌 <span class="meta">→ 详 §2</span></span></div>
    <div class="sig"><span class="tag" style="color:var(--purple)">共识</span><span><b>观众"2-0 了/1-1 了"分歧 + T1 提速预期</b>："科目四走一波"（2-0 速通梗）vs "打gg和hle老李不敢这样出的"（嘲讽 Faker 激进选角）——<b>意味着</b> G2 若 T1 速胜则系列天平倾斜，若被 BFX 扳平则进入拉锯 <span class="meta">→ 详 §5</span></span></div>
    <div class="sig"><span class="tag" style="color:var(--sub)">盘口</span><span><b>本窗口无有效数字盘讨论</b>（119 条命中均为"48"管泽元梗）——<b>样本不足</b>，G2 盘口以官方结算为准 <span class="meta">→ 详 §4</span></span></div>
  </div>
  <div class="errbox"><b>数据说明：</b>本页为本地快速生成（管线 Codex 全量生成排队中）；弹幕窗口 17:00–17:18 CST（4083 条/1760 活跃/226.4 条分）；五路虎牙采集正常。</div>
"""


SECTIONS = [
    ("1", "比赛信息与结果总览（官方源）", """<table>
    <tr><td>对阵</td><td>T1 vs BNK FEARX（BFX）· LCK 季后赛（世界赛名额关键战）· BO5 · slug=lol-t1-fox1-2026-08-29</td></tr>
    <tr><td>官方时间</td><td>2026-08-29 16:00 CST 开赛 · Riot matchId 117030752644841589 · 状态 inProgress</td></tr>
    <tr><td>系列状态（官方）</td><td><b>T1 1 - 0 BFX</b>（Riot gameWins）：G1 T1 胜；<b>G2 BP 已锁、开局进行中</b></td></tr>
    <tr><td>弹幕规模（G2 BP）</td><td>17:00–17:18 CST 窗口 <b>4,083 条 / 1,760 活跃 / 226.4 条/分</b>；密度峰值 17:00（1152 条/分，G1 结束/G2 BP 密集）</td></tr>
    <tr><td>完整性</td><td><span class="badge b-ok">五路齐采</span>硕硕 + 957 + 毛毛 + 米勒 + Remember；无新增缺口（G1 开赛段缺口已修复）</td></tr>
  </table>
  <p class="meta">系列 = Riot gameWins；阵容 = Riot window 回填（2026-08-29 17:20 CST）；弹幕仅作过程佐证。</p>"""),
    ("2", "灰信号汇总（风险 · 观众质疑非结论）", """<p><b>G2 BP 窗口有效 40 条</b>（早现 · 五路共振 · 观众质疑非结论）：</p>
  <ul>
    <li><b>G2 假赛叙事开局即现</b>："第二把假赛开始了，看看韩国棒子怎么演戏，""故意装糖""又是这个剧本？""你小子怎么每次都故意快一点"</li>
    <li><b>"买了"类</b>："我买了lgd+1.5"（他场，剔除）· "k神昨天买了"（他场，剔除）——本场直接"买了"类以"故意装糖/剧本"为主</li>
    <li>延续 G1 的 BFX 打野质疑语境（观众口径），未点名新对象</li>
  </ul>
  <div class="warnbox"><b>纪律声明：</b>以上均为观众质疑/玩梗，<b>非假赛证据</b>；灰信号只作风险标注与跨场实体跟踪，不上升结论。G2 开局质疑早现，配合"故意装糖"语境按低置信处理。</div>"""),
    ("3", "BP 与阵容情报（官方 window + 弹幕）", """<p><b>✅ 官方阵容（Riot window 回填）：</b></p>
  <table>
    <tr><th>队</th><th>G2 阵容</th><th>弹幕口径（BP 讨论）</th></tr>
    <tr><td>BFX（蓝）</td><td>Clear 兰博 · Raptor 潘森 · VicLa 阿狸 · Taeyoon 泽丽 · Kellin 悠米</td><td>阿狸对位阿卡丽；"超威的狐狸？"（阿狸讨论）；潘森+悠米组合</td></tr>
    <tr><td>T1（红）</td><td>Doran 奥恩 · Oner 梦魇 · Faker <b>阿卡丽</b> · Peyz EZ · Keria 萨勒芬妮</td><td><b>"faker跟我学的akl"（阿卡丽预测兑现）</b>；"放羊就行了，老李别放兔子""老李的兔子还不如兰子的"（兔子=阿狸，Faker 未选）；"李哥阿卡丽还一坨？？泉水杀超威"</td></tr>
  </table>
  <p class="meta">BP 后战绩情报：无"选手×英雄历史战绩"类弹幕；"打gg和hle老李不敢这样出的"为对 Faker 激进选角（阿卡丽）的版本评价。</p>"""),
    ("4", "盘口与市场讨论", """<ul>
    <li><b>本窗口无有效数字盘讨论：</b>规则层 odds_discussion=119 条，人工复核均为"48"管泽元梗（"48bin/力挺管哥"）——<b>样本不足</b>，不硬造。</li>
    <li><b>官方结算：</b>系列 T1 1-0（gameWins）；G2 进行中，G2 Winner 待官方/结算回填。</li>
  </ul>"""),
    ("5", "方向性情报板（锚点 × 共识 × 风险）", """<table>
    <tr><th>维度</th><th>BFX</th><th>T1</th></tr>
    <tr><td>BP 层</td><td>VicLa 阿狸 vs Faker 阿卡丽（对位焦点）；潘森+悠米 vs 梦魇+萨勒芬妮</td><td>Faker 阿卡丽激进选角（弹幕预测兑现）；Oner 梦魇大招进场体系</td></tr>
    <tr><td>本场信号（官方）</td><td>G1 告负（0-1）；G2 蓝色方</td><td>G1 胜（1-0）；G2 红色方</td></tr>
    <tr><td>反方声音</td><td>"1-1了"（观众预测 BFX 扳平）</td><td>"打gg和hle老李不敢这样出的"（质疑 Faker 激进）· "老李的兔子还不如兰子的"</td></tr>
    <tr><td>共识</td><td colspan="2">"2-0了/科目四走一波"（T1 速通预期）vs "1-1"（BFX 扳平）分歧；G2 阿卡丽 vs 阿狸为最大变量</td></tr>
  </table>"""),
    ("6", "情报含义与决策落点", """<ul>
    <li><b>系列结论（截至 G2 BP）：</b>T1 <b>1-0</b> BFX（官方），G2 进行中——T1 手握先手，G2 BP 主动提速（Faker 阿卡丽）。</li>
    <li><b>核心看点：</b>Faker 阿卡丽 vs VicLa 阿狸对位（弹幕 BP 讨论已兑现选角）；Oner 梦魇 vs Raptor 潘森节奏；BFX 若再输则赛点局压力巨大。</li>
    <li><b>风险提示：</b>灰信号 40 条 G2 开局早现（观众质疑·非结论）；"48"梗污染盘口统计（已剔除）；G2 Winner 待官方回填。</li>
    <li><b>G2 局中关注：</b>阿卡丽进场节奏、梦魇大招配合、BFX 是否延续放龙质疑；灰信号实体（BFX 打野）跨场跟踪。</li>
  </ul>"""),
    ("7", "逐局复盘（G1 已复盘 + G2 BP）", """<table>
    <tr><th>局</th><th>状态</th><th>要点</th></tr>
    <tr><td>G1</td><td>T1 胜（官方 1-0）</td><td>详见 G1 结束情报页：BFX 皇子威胁未兑现、T1 韧性、33 杀线盘口兑现</td></tr>
    <tr><td>G2 BP</td><td>BP 已锁 · 开局</td><td>Faker 阿卡丽（弹幕预测兑现）；BFX 阿狸+潘森+悠米；密度峰值 17:00（1152 条/分）；"2-0/1-1"分歧</td></tr>
  </table>
  <p class="meta">G2 局中/局末情报将在节点数据就绪后补发。</p>"""),
    ("8", "队伍 / 人员画像（证据层 · 官方 + 弹幕口径）", """<p><b>T1：</b>G1 韧性取胜后 G2 主动提速——<b>Faker</b> 阿卡丽（47 条提及，BP 预测兑现；"阿卡丽还一坨/泉水杀超威"为强度讨论）；Oner 梦魇（大招进场体系）；Doran 奥恩、Peyz EZ、Keria 萨勒芬妮。</p>
  <p><b>BFX（BNK FEARX）：</b>0-1 落后背水一战——VicLa 阿狸（对位焦点）、Raptor 潘森（G1 皇子被顶住后换角）、Clear 兰博、Taeyoon 泽丽、Kellin 悠米；打野灰信号实体跨场跟踪。</p>
  <p><b>周边叙事：</b>"科目四走一波"（2-0 速通梗）；"48"管泽元梗（他场事件）；"打gg和hle老李不敢这样出的"（LCK 强队对位评价）。</p>"""),
    ("9", "联赛规律与版本（沉淀层）", """<ul>
    <li><b>LCK 季后赛 BP 信号：</b>Faker 阿卡丽/阿狸类刺客对位在强强对话中成为弹幕核心讨论——"谁拿阿狸/阿卡丽"版本锚延续（Care 蛇女之后的新对位焦点）。</li>
    <li><b>灰信号早现模式：</b>大比分领先/背水一战局开局即现"剧本/故意装糖"质疑——需结合后续赛果级事件甄别（本场按低置信处理）。</li>
    <li><b>数据完备性：</b>五路同采后 BP 窗口密度 226 条/分，规则层可及时产出（本页即基于规则层 4083 条快速生成）。</li>
  </ul>"""),
    ("10", "预测验证回填（沉淀层）", """<table>
    <tr><th>预测/锚点</th><th>时间</th><th>状态</th></tr>
    <tr><td>"faker跟我学的akl / 想看他阿卡丽"（Faker 阿卡丽预测）</td><td>17:00-17:18</td><td><b>兑现</b>（官方 window：T1 Faker 阿卡丽）</td></tr>
    <tr><td>"2-0了/科目四走一波"（T1 速通预期）</td><td>17:0x</td><td>待 G2 结果验证</td></tr>
    <tr><td>"1-1了"（BFX 扳平预期）</td><td>17:0x</td><td>待 G2 结果验证</td></tr>
    <tr><td>灰信号 40 条（G2 开局假赛质疑）</td><td>17:00-17:18</td><td>观众质疑·非结论；待 G2 结果与盘口验证</td></tr>
  </table>"""),
    ("11", "数据与溯源", """<p><b>官方源：</b>Riot API getSchedule（matchId 117030752644841589，inProgress，gameWins T1 1-0）+ getEventDetails/window（G2 阵容回填，2026-08-29 17:20 CST 抓取）。</p>
  <p class="meta"><b>弹幕数据窗口</b>：17:00–17:18 CST（09:00–09:18 UTC）· 4,083 条 / 1,760 活跃 / 226.4 条分；密度峰值 17:00（1152 条/分）。</p>
  <p class="meta"><b>数据源</b>：虎牙五路——硕硕 323444 / 957 890001 / 毛毛 149346 / 米勒 149361 / Remember rememberlol；无新增缺口。</p>
  <p class="meta"><b>结果仲裁</b>：Riot gameWins（官方）；G2 Winner 待结算回填；"48"梗已从盘口统计剔除。</p>
  <p class="meta"><b>情报输出时间</b>：2026-08-29 17:25 CST（北京时间）· 本地快速生成（管线 Codex 全量版排队中，同 URL 稍后覆盖为完整版）。</p>"""),
]


HTML = page(
    "LCK 季后赛 · T1 vs BNK FEARX · G2 BP 后情报（系列 T1 1-0）· 2026-08-29",
    "LCK 季后赛 BO5 · G2 BP 已锁 · 系列 T1 1-0 BFX（官方 gameWins）· 局中·非终局",
    SPEED,
    SECTIONS,
    "弹幕情报 · 观众质疑非结论 · 结果以官方源为准 · Polymarket 电竞情报项目",
)


def main() -> None:
    out = REPORTS / "intel_danmu_T1-BNK FEARX_2026-08-29_g2_bp.html"
    out.write_text(HTML, encoding="utf-8")
    print(f"written: {out}")


if __name__ == "__main__":
    main()
