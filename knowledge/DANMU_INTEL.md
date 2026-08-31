# 弹幕情报库（虎牙直播间 -> 交易情报）

最后更新：2026-08-24

定位：弹幕是"低可信度、需聚合"的主观情报源；价值不在单条弹幕，而在
**聚合后的共识、分歧与异常**。只作情报参考，不作为交易依据。

> 每场情报 HTML 的全文 MD 镜像见 `knowledge/intel_pages/`（规范：
> `knowledge/INTEL_MD_MIRROR.md`）；本文件为聚合批次账本。

## 数据流与工具

```text
抓取：tools/fetch_huya_danmu.py（实时 WebSocket，JSONL 落盘 docs/data/danmu/<博主>/）
提炼：tools/danmu_intel.py（队伍/选手情绪、盘口、局势、灰信号、弹幕密度峰值）
简报：tools/danmu_report.py（SAP/Apple 风格 HTML，reports/intel_danmu_*.html）
画像：队伍 -> TEAM_PROFILES.md；选手状态 -> 本文记录；盘口 -> 本文记录
```

## 分析维度（对预测市场交易有价值）

```text
1. 队伍情绪：提及数 + 正/负向计数 + 样本（共识与分歧）。
2. 选手状态：选手提及与褒贬（Poby/Hype/Guma 等）。
3. 盘口/数字讨论：让分、人头、数字盘（-6.5 / 48 / 700 等）——观众关注点与市场一致。
4. 局势线索：比分、龙魂、资源、翻盘讨论。
5. 灰信号（仅风险提示）：直播间梗（"小卖部/健身房/接"=接广告/接单暗语），
   不是假赛证据，只标注不引用。
6. 弹幕密度峰值：高活跃分钟 = 比赛关键时刻（团战/翻盘/争议），
   与 Polymarket 价格异动强相关——可作"事件检测"信号。
7. 信息差信号：观众"嘴上看衰" vs 比分/盘面领先的分裂（如 TH 2-0 领先仍被吐槽），
   提示市场情绪与实力判断错位。
```

## 当前批次（2026-08-17 晚，硕硕直播间 323444，窗口 23:42-00:04 UTC）

```text
数据：653+ 条弹幕（持续抓取中）/ 200+ 人；runtime/danmu_intel.json 全量提炼。
比赛识别：TH vs Navi（LEC 系）——观众视角 TH 2:0（"两把速通了"、"零封了"、
  "Navi连控五条龙"）；弹幕提及 FNC/KC/G2 为其他场次讨论，不混入当前场。
队伍：TH 提及高频且负面为主（"th菜得抠"、"究极保枪队然后一波暴毙"），
  但 2:0 领先——**"嘴上看衰、比分领先"的信息差信号**；
  打法特征：放资源换发育、平经济不接龙团（"20 分钟三龙听牌"、"什么都放"）。
  对手 Navi：打野控龙强（"Navi连控五条龙"）、前期能压制 KC（"navi前期可是能压制kc的存在"）。
选手：皇子（TH 打野？）被集中批评（"皇子是人？"、"纯菜逼"、"操作没看懂"）；
  Poby 蛇女褒贬不一；Hype 被质疑；发条中单失误（"发条没学大招"）成为焦点；
  samd 状态被提及（"唯一一个能被samd压的ad"）。
盘口：-6.5 / 人头盘讨论持续（观众核对让分与总人头）；"48"出现为直播间梗/盘口数字，需区分。
局势：**LEC 近期无 1-1、只有 2-0**（观众确认 + 弹幕"最近lec都没有11，都是20"）；
  之前记录"1-1"为其他场次/之前比赛弹幕，已修正；当前场 2-0 速通。
  资源全放（龙/虫/塔）为 TH 场核心议题。
密度峰值：23:57 UTC 45 条/分钟（关键事件时刻，建议与价格序列对照）。
灰信号："接/小卖部/健身房"类为直播间梗（接广告/接单），不构成假赛证据；
  "这版本又开始中路大核刷钱，除了LPL都不咋打架"为版本观察，可作风格参考。
高价值用户：见 knowledge/DANMU_USERS.md（TokyoLll / neoooooo / LuLu13 等）。
```

## 2026-08-18 KC vs GX（LEC BO3，硕硕直播间 323444）

```text
数据：1903 条弹幕 / ~450 人 / 00:43-02:15 UTC；整场复盘
  reports/intel_danmu_KC-GX_full_2026-08-18.html。
结果（弹幕推断，待官方确认）：KC 2:0 GX；两局同剧本——KC 大优势不推进、
  拖到固定时间点终结（第一局约 32-34 分钟、第二局约 26-30 分钟）。
队伍画像更新（TEAM_PROFILES 同步）：
  KC：LEC 独一档，打法"稳到弱队一点希望没有"；核心特征是"卡时间"——
    领先 1 万不推进、到点一波；观众质疑与盘口数字（总时长/总人头）高度重合。
  GX：弱队标签（"LEC 汤圆"），对线即落后、打野被压 3 级、野区被刷爆、
    团战各打各的；唯一正面为 Oscar 奥恩。
选手：少爷（KC 下路）女警五杀+后续四杀=终结位；Yike（GX 打野）被集中批评
  且有"有任务/演戏"质疑；GX 中单安妮/卢锡安被批。
盘口讨论（本场核心）：让分 +9.5 极限收 / -8.5；总时长 小31/大31/大30；
  总人头 两把 23 个。观众结论："四场全卡"、"一个晚上都在卡"。
集体质疑达顶峰（69 条灰信号）："任务联赛/演大时间/这种不是假赛我不信的/
  都计算好的" vs 反方"买中了就是真赛，没中就是假赛"。
  建议沉淀为"LEC 盘口节奏质疑指数"（质疑条数 + 卡盘数字重合度），
  与盘口/价格对照（若未来有对应市场）。
监控经验：页面 5 分钟刷新 + 比赛结束信号（大量 888/88/晚安 + 数据停止增长）
  可作自动停抓判据。
```

## 待办

```text
1. 密度峰值时刻与 Polymarket 价格序列对照（工具后续接入）。
2. 多直播间同场交叉验证（硕硕 + 957 同场比赛弹幕）。
3. 弹幕情绪 -> 价格变化相关性统计（样本累计后）。
4. 选手状态沉淀为独立选手画像（player_profiles.json）。
```

## SOOP 批次（2026-08-18，LCK CL ROUND 4，DNS vs NS）

```text
数据：实时 174 条（G1 尾声 16:35:43-16:40:40，52 人）+
  待 VOD 生成后回捞全量（tools/fetch_soop_vod_chat.py）。
比赛：LCK_CL 频道 [CC] DNS vs NS | 2026 LCK CL ROUND 4。
推断结果（弹幕）：DNS 拿下第一局（"组合出来 DNS 就压胜"、"DNS 大胜"），待官方确认。
队伍：
  DNS —— G1 尾声观众一致看压胜；归因"辅助差距"与 Enosh 卡莎（11-0 生涯记录）。
  NS —— 负面为主（"NS 还是不行"、"阵容后期太差"、"这也叫逆转？"）；
    有逆转苗头但被判定不可能；专业用户归因 BP（拿 Rell 打 Camille）。
英雄/版本观察：Rell 被集中质疑（配 Jhin 不对）、Naafiri 被嘲讽（胜率 10% 梗）、
  Kled 被认 OP、Camille 强度被认可；全场高击杀（分均 1 杀）。
跨局信号（重点）：局间出现"第二局 NS 应该轻松赢？第一局是让的"预判——
  作为 G2 情绪锚点，若 G2 实际走势背离即预期差信号。
灰信号：本窗口 0 条（无假赛/剧本/卡盘质疑），不做风险标注。
高价值用户首批：luckphs1（BP 复盘）、dla0303（战况复核）、kh7135（预测）、
  ph6489（数据/选手）——跨场累计可信度。
报告：reports/intel_soop_DNS-NS_G1_2026-08-18.html。
```

## K杯决赛批次（2026-08-18，DNS vs NS G1，硕硕 + 957 双直播间）

```text
比赛识别：LCK 凯斯帕杯（KeSPA Cup）决赛 DNS vs NS，BO5；硕硕/957 二路解说，
  SOOP LCK_CL 官方流同场（韩文弹幕另存，见上节）。
数据：硕硕 1091 条 + 957 780 条（共 1885 条 / 777 人，窗口 17:08-17:45）。
结果（弹幕推断，待官方确认）：DNS 1:0；人头约 39:5（总 44）。
队伍画像更新：
  DNS —— 打野 shavel（沙伟）盲僧个人秀定局（抢龙/单杀奥拉夫/救 AD）；
    常规赛双杀 NS、此前赢过 GEN；中单蛇女稳定性是隐患；背靠背体力被质疑。
  NS —— 五路被批（打野"龙心"0-5、AD"大菠萝"EZ 整场不交闪、中单"学弟"发条
    没伤害、上单 Kingen 被单杀、辅助"莲子"神经刀）；一队阵容+冠军选手
    （Kingen/学弟）打成这样引发"不该是这成绩"讨论。
盘口讨论：总人头大 36.5/37.5/39.5 方向正确（最终约 44 头）；差盘 12.5/13.5；
  大龙 buff 小 4.5。高击杀局 + 盘口"大" + 观众"刷人头"质疑三者同向。
灰信号（18 条集中爆发，17:38-17:45）："做局/假赛/庄家/资本/演员/明演"指向
  NS 打野/AD 离谱失误；反方"韩国假赛会坐牢"；只作风险标注，不作结论。
后续局观察点：NS 是否换打野/AD 调整；DNS 若拖长盘体能风险；观众"3:0"预期。
报告：reports/intel_danmu_DNS-NS_G1_2026-08-18.html。
```

## K杯决赛 G2 批次（2026-08-18，硕硕 + 957 双直播间）

```text
数据：G2 窗口 18:05-18:31，2346 条 / 919 人。
结果（弹幕推断，待官方确认）：DNS 2:0 领先；第三局后 3:0 横扫夺冠
  （18:44"3:0"、19:04"3-0了"；957 19:00 后切云顶 = 比赛结束）。
核心事件：18:20 暂停潮——DNS 频繁暂停引发灰信号集中爆发（数十条：
  "假赛/打钱/给场外发信号/回溯冠军/奖金少事故多"），盘口玩梗"暂停大2.5"；
  NS 团战连环失误（Kingen 兰博空大、打野潘森迷路、辅助莲子泰坦被批）。
队伍画像更新：
  DNS —— shavel 琪亚娜延续 carry（"世一骑安娜"）；暂停争议成系列赛标签
    （"左边暂停完就开始赢"），需与官方暂停记录对照。
  NS —— "三 FMVP 阵容"（Kingen/学弟/莲子）打成最菜决赛队；资源分配、
    上野强度、教练组被集中质疑；灰信号与实力归因双线并行。
灰信号：G1+G2 连续两局"质疑×盘口"共振（G1 人头大满水 / G2 暂停盘梗），
  建议沉淀"集体质疑指数"（暂停次数×离谱失误×盘口讨论）并与官方数据对照。
报告：reports/intel_danmu_DNS-NS_G2_2026-08-18.html。
```

## LCK CL Gen.GA vs BRO1 批次（2026-08-18，SOOP afchall + 虎牙 323444）

```text
数据：SOOP 5574 条（16:35-21:04，韩语）；虎牙 899 条（20:15-21:04，中文）。
赛况：1:1（G1 BRO1、G2 Gen.GA；G3 未打）——完整复盘见
  knowledge/reviews/2026-08-18_lol-genga-bro1-2026-08-18_genga.md。
核心事件（两路弹幕共识，与赔率同步）：
  G2 20:32 BRO1 压制 Gen.GA 至 91c（Gen.GA 深水 9c）；
  20:40-20:42 BRO1 3 分钟崩到 16c（20:40 虎牙 66 条/分、SOOP 82 条/分峰值）；
  20:47 Gen.GA 99.5c（15 分钟 9c -> 99.5c）。
弹幕共识对象：BRO1 中单瑞兹（+辅助诺提勒斯）被两路观众指"故意送/演"：
  虎牙"瑞兹明牌假赛/从头送到尾/只送大的"；
  SOOP"라이즈가 던지구만 / 고의로 5명 다죽어준 부분".
灰信号处理：两路共识 + 指定选手 + 精确时段 = 强灰信号；仍按纪律只作
  风险标注与复盘素材，不作为假赛证据；用户主观判断 100%（案例 4）。
方法论验证：弹幕密度峰值（20:40-20:47）与价格崩盘窗口精确重叠——
  "弹幕峰值 = 事件检测"第 N 次应验，可作为 G2 类异常事件实时告警信号。
```

## LCK DK vs HLE 批次（2026-08-20，毛毛/硕硕/957/米勒 四直播间）

```text
数据：11294 条（08:14-10:07 UTC），四直播间并发。
结果：HLE 2:0 DK（官方确认）；G1 DK 48.5c->98.5c 峰值->0.5c 归零
  （HLE 16:34 翻盘）；G2 HLE 54.5c->99.95c（DK 两次反扑失败 16-20）。
灰信号（强关键词 54 条，双峰）：G1 翻盘段 16:31-16:44（"中野两个演员/
  按剧本打/dk演戏卖分"）+ G2 段 17:18-17:48（"假赛之王DK/诱盘杀猪/
  lck最假赛区"）——指向 DK 演/送，待核查不作结论（gray_entities 已登记 DK）。
交易联动：用户 G1 买 DK 100U @~63c 浮盈 55% 未止盈，HLE 翻盘归零全亏
  （高位未止盈反样本，对照 NAVI/TH 95c 全卖正样本）。
画像更新：HLE "翻盘能力/领先爱浪"；DK "高位不稳/杰斯体系判负"。
报告：reports/intel_danmu_HLE-DK_2026-08-20.html（弹幕复盘）、
  reports/intel_danmu_dk_hle_2026-08-20.html（含用户交易复盘）。
```

## 2026-08-19 LPL 批次（WBG vs LNG + TES vs AL，官方流 660000 + 米勒 149361 + 记得 528222）

```text
全天监控会话 lpl_lck_2026-08-19（3 路虎牙并发，35,900+ 条弹幕，实时聚合页
  reports/intel_danmu_live_lpl_lck_2026-08-19.html）。

WBG vs LNG（LPL 组内赛，官方确认 2:1，LNG 六连败收官）：
  灰信号 104 条（全场最高）——主线"WBG 不敢赢/杀减号（让分盘）/做任务/庄家指令"，
  15:37-15:55 密集；盘口小28.5/小25.5/+8.5 与灰信号共振；
  小虎被批 360 次（"虎大捞比/大招K完就送"）；
  观众"WBG 基本不可能 2:0"判断部分命中（打到 G3，但 WBG 仍 2:1 胜，
  "不敢赢"未兑现为翻盘）。报告：reports/intel_danmu_WBG-LNG_2026-08-19.html。

TES vs AL（LPL 登峰大战，官方确认 2:1）：
  TES 打野"玉玉"（小天）全程被集火（"赢的局跟玉玉没关系，输的局带崩全队"）；
  AL 巨魔"不控龙"决胜局被批；灰信号 49 条（"TES 放水/演"）未兑现；
  "今天没有一场追二"观察应验（AL 追二失败）；
  官方补充：G1 ZUI 纳尔、G2 Breathe 奎桑提 3/0/7（POG）、G3 TES 拿下。
  报告：reports/intel_danmu_TES-AL_2026-08-19.html。

GEN vs KT（LCK，官方确认 2:1 让一追二）：
  赛前-局中排名博弈"GEN 演"讨论 10+ 条（GEN 赢=晋级+推 T1、KT 输=第五），
  结果未兑现；G1 Kiin 奥拉夫+Ruler 芸阿娜、G2 KT PerfecT 奎桑提扳平
  （弹幕"1-1"判断正确）、G3 Ruler 女警翻盘；GEN 锁定传奇组前二，KT 五连败；
  KT ADC"鸡窝"/BDD 工具人被批；场外 T1 宫斗传闻。
  报告：reports/intel_danmu_GEN-KT_2026-08-19.html。

DNS vs BRO（LCK 二队场，SOOP carrylck 中文流，采集中断）：
  仅捕获 G2 开局 20 条弹幕（20:16-20:49），样本严重不足，结果未确认；
  唯一信息点"史迦納被康爆欸，BRO解題解的真好"；无灰信号；
  待 SOOP VOD 回捞补全（tools/fetch_soop_vod_chat.py）。
  报告：reports/intel_danmu_DNS-BRO_2026-08-19.html。

灰信号纪律：以上"演/放水/庄家指令"均为观众质疑非结论，只作风险标注与盘口对照素材。
```

## WE vs EDG 整场批次（2026-08-19，官方流 + 米勒 + 记得，EDG 2:0）

```text
数据：18,630 条（G1 8,412 + G2 10,218），21:20-23:02。
结果（弹幕口径，官方确认待回填）：EDG 2:0 WE——"赛季首胜""开局就说了必2-0"。
G1：WE 领先约一万被翻（灰信号 462 条，5.5%，峰值 21:55-21:56），MVP 讨论
  （已纠正：Monki 实为 WE 打野，"超雄"是弹幕嘲讽=莽/冲动非外号，"MVP:Monki"是反讽；
   真正候选为 EDG 打野 jiejie）；
G2：BP 永恩焦点（EDG 侧），WE 巨魔/女枪被嘲；EDG 拖后期永恩成型+大龙结束
  （"mvp 给到永恩了"），灰信号 354 条，峰值 23:01（67 条/分，"剧本/内定/没人查"）。
全场灰信号 816 条（4.4%），指向 WE 打野/野辅（"打钱/明演/收米/查赌"），预警等级高。
预测验证：赛前"打满"共识被证伪，"2-0 内定"派命中；"今天没有一场追二"规律 4/4。
交易案例：用户 G2 灰信号出现时买入 EDG 整场 → 2:0 兑现（案例 5，待官方确认归档）。
报告：reports/intel_danmu_WE-EDG_full_2026-08-19.html（+ G1/G2 分页）。
```

## CS2 EWC 批次（2026-08-19，CSBOY官方 123321 + CSBOY-Mo captainmo，爆冷日）

```text
数据：8,700+ 条弹幕（21:45 起），2 路虎牙并发；灰信号 0（无假赛质疑）。
比赛状态（23:38 修正）：Astralis vs G2 与 Magic vs FUT 均进行到第二局、未结束；
  FaZe vs Vitality（23:13 开打）另行关注。
  ⚠️ 误判修正记录：曾把"观众预测/玩梗"（"A队两图晋级了""魔术队赢FUT不意外"）
  当作比赛结果，已回退为"进行中"；结束判定需多信号校验（CAPTURE_RULES 第 12 节）。
已知观察（非结果）：
  G2 新狙击手 rinkle 被批（"不如阳叔一根"）、阳叔离队叙事；
  Magic 双核阿伟/tenzy（阿伟第二局状态被批）；FUT 回合制表现；
  赛前共识 FaZe 图池优势
  （叉车/遗迹至少一张）+ Vitality 沙二 25% 胜率被看衰；反向信号是"爆冷日"
  （当晚 G2 已翻车）与 FaZe 不稳定叙事。
异常：22:17 "真重赛了"信号 + "？？？"刷屏（技术事件，待核查）；非灰信号。
报告：reports/intel_danmu_CS-EWC_2026-08-19.html；实时页
  reports/intel_danmu_live_cs_ewc_2026-08-19.html（60s 刷新）。
```

## CS2 EWC 十六强终局（08-20 晨，4 场全部结束 · 官方已回填 2026-08-23）

```text
1) Astralis vs G2  -> G2 2:1（官方确认；A 队 Ancient 先胜，G2 Dust2/Inferno 连下）
2) Magic vs FUT    -> FUT 2:1（官方确认；magic 图一 Ancient、FUT 后两图逆转）
3) MOUZ vs GL      -> MOUZ 2:1（官方确认；让一追二）
4) Aurora vs FURIA -> FURIA 2:1（官方确认；【修正】原弹幕口径误记欧若拉胜，
   官方赛果为 FURIA 晋级八强，QF 再 2:1 胜 G2）
另：FaZe vs Vitality -> Vitality 2:0（官方确认）；NAVI vs Legacy(菊花) -> Legacy 2:0
（官方确认，图二 Ancient 13-2；菊花=Legacy 巴西队已确认）。
下一轮（官方）：FUT vs MOUZ、FURIA vs G2、Spirit vs Vitality、Legacy vs Falcons。
换血叙事（本轮最有价值情报）：
  小吉米（前 MOUZ 明日之星）→ Aurora，状态低迷被批（"老鼠踢对人了"）；
  K3（前猎鹰指挥）→ GL，枪法硬但指挥被批（"猎鹰踢对人了"为主）；
  魂飞被 MOUZ 踢被质疑"踢错"；fallen/教父（FURIA）老将仍强。
灰信号 0；异常仅"真重赛"与低置信"开子/挂"质疑（非结论）。
报告：reports/intel_danmu_CS-R2_2026-08-20.html + 各场分页。
```

## LCK CL BRO vs KRX 整场批次（2026-08-20，SOOP afchall，KRX 2:1）

```text
结果（弹幕+用户确认，官方待回填）：KRX 2:1 BRO。
G1 KRX 胜（Rich 卡蜜尔；BRO 让 4 龙/奥拉夫死即崩/Deny 被批）；
G2 BRO 胜（瑞兹发力；Rumble 再选被批但 carry，BP 质疑打脸）；
G3 KRX 胜（马拉松局，多次远古龙/男爵难终结；LazyFeel 急于终结失误，
  Rich 远古龙超级操作收尾；BRO"总是占优然后输"）。
灰信号：G3 Naafiri 打野被集中指控故意送（12 条，含"故意不惩戒/故意让龙/
  20+分钟不开大""放水会被开除吗"），severity 中-高，选手 ID 待官方名单；
  已建"KRX Naafiri 打野（待归人）"留痕实体。
BP 验证：G2 Rumble 质疑打脸；G3 BRO 价值阵容部分应验但无法终结。
画像：BRO=终结能力差（长期标签）；KRX=Rich 关键局爆发+无前排隐患。
报告：reports/intel_danmu_LCKCL_BRO-KRX_2026-08-20.html。
```

## LCK HLE vs DK 整场批次（2026-08-20，四路解说流，HLE 2:0）

```text
结果（弹幕多信号，官方待回填）：HLE 2:0 DK。
G1 HLE 翻盘：Delight 牛头 MVP（多次开 DK 核心芸阿娜）；'DK 必赢'共识被打脸。
G2 HLE 再胜：DK 选杰斯被集体判负（'下班杰斯''杰斯这几天全输了'）→ 应验；
  DK 送麻/掉点；'恭喜杰斯又输一局'。
灰信号 4 条（低）：'假赛之王 DK''韩华真的太假了'等，无共识。
盘口：G1 +8.5 讨论；G2 '-6.5 拿下了'兑现。
BP 验证：杰斯=判负（bp_signals 已录，跨场统计项）。
排名博弈：DK 输 KT 抢名额、T1 全赢第二、HLE 锁世界赛。
报告：reports/intel_danmu_HLE-DK_2026-08-20.html。
```

## LCK T1 vs KT 整场批次（2026-08-21，硕硕+957 两路，T1 2:1 让一追二）

```text
结果（弹幕多信号，官方待回填）：T1 2:1 KT（G1 KT、G2/G3 T1）。
G1 KT 胜：BDD 瑞兹偷家终结（'瑞兹偷家赢了'）；'死一次基地爆炸'两路 30 条共振
  （Peyz 阵亡=基地崩）；多兰武器 0-3-0 / 大O 皇子 0-7；'T1 拥有登峰 5 队里最菜的上中野'。
G2 T1 胜：KT 一度领先（'kt2-0很稳'落空）；Peyz 岩雀 9-0 + Keria 牛/游走翻盘；
  多兰 VN 天肥 7.6k 被嘲；20:48-20:52 Oner 定向灰信号（演/收钱/假赛）→ 方向未兑现。
G3 T1 胜：Faker 冰鸟 + Peyz 女警后期接管；KT Perfect 鳄鱼优势送（'鳄鱼收钱了，
  最强的两波他去送了'）；多兰格温送养鳄鱼（21:24 峰值 298 条/分）；KT '充电宝'。
灰信号：G1 实质 3-5（低）；G2 两路约 40（低-中，Oner 未兑现）；G3 两路约 41
  （中，KT 侧弱兑现：'明送/鳄鱼收钱/烬买了/右边中单演'）；新增实体 Oner、Perfect。
盘口：G1 'KT 3.8倍水一波翻盘'兑现（弹幕口径）；G2 '+1.5都快死了''满水t1'；
  G3 终局 '7.5/8.5 卡盘'讨论 2 条（待官方比分核对）。
规律候选：'Peyz 死一次基地爆炸'（G1 应验、G2/G3 未触发）；'资源倾斜多兰=无效'；
  KT '纯不敢赢/充电宝'（连续两局领先被翻）。
排名影响：T1 终结三连败；DK 进季后赛（'赢了dk进了'）；KT 打入围赛。
报告：reports/intel_danmu_T1-KT_2026-08-21.html。
```

## LEC SK vs TH 整场（2026-08-21/22，硕硕单源，TH 2:0 · 含误判修正）

```text
结果（弹幕+用户确认，官方待回填）：TH 2:0 SK（无 G3）。
G1 TH 胜：SK 开局 3-0/5-1 领先被翻（'开局3-0大优势打成这样''5-1打成9-20'），
  TH 后期强度（'右边后期不知道怎么输'）；'sk赚了！/sk今天吃一局'为盘口灰话
  （做局输球获利），非 SK 胜信号。
G2 TH 胜（'恭喜th'00:19）：SK 永恩/皇子/兰博/霞洛团战阵但'小龙团永远不打'，
  TH 剑魔+蔚+炼金龙魂 23 分钟速通（00:25 拿下/速通局，00:32 结束）。
灰信号两局 83 条均指向 SK（输家）：G1 29 条（'狗熊明演/左边收钱/到点就送/
  大优势水位不动'）、G2 54 条（'皇子明着演/wunder是演员/纯假赛/都买了对面赢'）
  ——被质疑方两局均输，方向连续兑现；SK 新实体留痕。
BP 后战绩情报全应验：G1 潘森胜率低/Wunder 纳尔；G2 SK 永恩负锚点
  （'没有纳尔直接输一半'）+ TH 剑魔正锚点（'招牌剑魔 放了就知道输了'）。
盘口：G1 '大优势sk还是水位不动'（灰话）；G2 '都买了对面赢'；跨联赛
  'LPL今天7场AD击杀总和小9.5，6场吃满'作统计素材。
规律：LEC 后期翻盘率高（'30分钟后再猜输赢'）再添样本；TH '放龙剧本'为上周延续。
⚠️ 误判修正（2026-08-22）：初版将 G1 误判为 SK 胜（把灰话当胜负信号），
  已按用户现场确认修正为 TH 2:0；灰话禁用词已入 CAPTURE_RULES 第 12 节。
报告：reports/intel_danmu_SK-TH_2026-08-21.html。
```

## LPL WE vs LGD（2026-08-22，官方流+957，LGD 2:1 让一追二）

```text
结果（弹幕多信号，官方待回填）：LGD 2:1 WE。
G1 WE 胜（弹幕未录制，官方标题口径）；G2 LGD 扳平（'资本告诉你1:1'兑现）；
G3 LGD 碾压（'老干爹虐了21-4''GGWE不像人''恭喜lgd'），系列'史上最毫无悬念的让一追二'。
灰信号：Monki（超雄）三连本场兑现——WE 被疑演→WE 输系列（弱兑现），
  跨场统计 08-19 兑现/08-21 未兑现/08-22 兑现（2/3）；盘口'lgd6倍拿下了'兑现。
BP 后战绩情报：WE 少爷卢锡安负锚点应验；cube 杰斯正锚点 vs 反方分歧。
选手画像：汤圆（LGD 中单）'爆 karis 三把'；WE karis 被口诛；'WE下赛季可以考虑原神'。
规律候选：LGD '每次都打满'再添样本；WE '只会翻盘'本场翻不动。
数据缺口：G1 弹幕缺失（采集 16:05 恢复）、16:28-16:42 中断 14 分钟。
报告：reports/intel_danmu_WE-LGD_2026-08-22.html。
```

## LCK GEN vs DK（2026-08-22 进行中，硕硕+米勒）

```text
进度（弹幕口径）：G1 GEN 胜；G2 进行中（'三星第二把打的真怪'；观众共识'看好GEN 2-0'）。
GEN 已锁常规赛第一（'gen赢不赢都无所谓了'）；T1 vs HLE 决定第二（弹幕口径）。
焦点：Chovy 冰鸟/卡牌、Ruler 女警（'尺狗'）、许秀玩蛇（'许哥这蛇这么厉害'）、DK 上单被批毒瘤。
灰信号低（'geng大哥放一局吧'让局玩梗）。
报告：reports/intel_danmu_GEN-DK_2026-08-22.html。
```

## LPL IG vs NIP（2026-08-22，未开赛，官方流赛前弹幕）

```text
状态：未开赛（17:38 仍等待接档，WE-LGD 已结束）。
赛前共识：IG 热门（'IG太热门了不好整'）；NIP '未尝一败'（观众口径）；结果预测分歧。
观众梗：'糯米鸡七年进不去世界赛了'（NIP）；'LGD竟然赢了'（爆冷日情绪）。
报告：reports/intel_danmu_IG-NIP_2026-08-22.html。
```

## LPL IG vs NIP 整场（2026-08-22，官方流，NIP 2:0）

```text
结果（弹幕多信号+官方标题，待回填）：NIP 2:0 IG（爆冷日第二场）。
G1 NIP 胜（'NIP拿下了'；上单差距刷屏，峰值 1050 条/分）；G2 NIP 胜（'恭喜NIP/2比0了'）。
IG 控分叙事 11+ 条：'IG故意控分，拿涅槃第二，骑士之路对手更菜'——排名博弈灰信号（待官方）。
BP 后战绩情报双负锚点应验：TheShy 奥拉夫（G1）+掘墓（G2）+Meiko 巴德（G2，87 提及）。
NIP 正锚点：佳琪烬（G1）、波比体系（G2，'放波比的代价'）；'严父/克星'叙事。
数据缺口：G1 中段 17:53-18:25 采集中断。
报告：reports/intel_danmu_IG-NIP_2026-08-22.html。
```

## LCK DNS vs KRX（2026-08-22，碎片化数据，结果待确认）

```text
状态：G1 终局（'krx翻了'，DNS 被疑），G2 片段（DNS 疑似换打野），系列结果待确认。
DNS K杯冠军（08-18 3:0 NS）后被集中质疑：'那个杯赛纯纯剧本让他赢得，菜是原罪'
  'DNS这几场把这届K杯含金量打低了'；盘口'场场开低水，场场被虐'。
灰信号高浓度：'好假的比赛啊/假赛之王lck/能跟菠菜合作已经明牌了/韩国打假赛犯法明知故犯'；
  有反方（'这假什么呀后期本来就DNS好打''赌狗把把假的'）。
选手：KRX 打野被赞（'krx玩的好oner啊'）；'下把上rich'待确认；DNS 打野小P被点。
数据缺口：BP/中段未捕获（19:30-19:44 采集中断）。
报告：reports/intel_danmu_DNS-KRX_2026-08-22.html。
```

## LPL JDG vs TES（2026-08-22 进行中，JDG 1:0）

```text
进度：G1 JDG 胜（官方标题'JDG 1:0 TES'），G2 进行中。
TES 状态差：'昨天被BLG打自闭''道心破碎'；小天被批（'不如给小天没他赢不了'反讽）；
  教练 BP 公式化（'谁都知道你选奥拉夫'）；'TES一轮回家打不过LGD'（观众看衰）。
灰信号低；数据断断续续（多处采集中断）。
报告：reports/intel_danmu_JDG-TES_2026-08-22.html。
```

## LPL WE vs AL 整场（2026-08-21，官方流+957，WE 2:1 · 含局次修正）

```text
结果（官方已确认）：WE 2:1 AL（让一追二；G1 AL 赢首局、G2 WE 天崩逆转、
  G3 WE 后期接管）。⚠️ 初版报告局次写反（G1 WE/G2 AL），已按 Polymarket
  结算与官方战报修正为 G1 AL、G2 WE、G3 WE。
灰信号：Monki（WE 打野，超雄）再犯升级——昨日 WE-EDG 816 条灰信号主角，
  今日 G1 再被疑"开演/带着送"；但"WE 送"方向整体未兑现（WE 赢系列），
  与 BRO-BFX 场"质疑兑现"形成对照。塔赞 G1 被批送（AL 仍赢）、
  G3 被批不控龙/送（AL 输），属比赛叙事非结论。
盘口：AL -1.5 讨论（"10 万上车"）-> 未兑现；G3 About 卢锡安三杀收官
  （29 分钟电龙魂）。
规律：WE"劫富济贫/经典剧本"再添样本；LPL 让一追二（对照同日 TES-BLG 零封）。
报告：reports/intel_danmu_WE-AL_2026-08-21.html（结果段已修正）。
```

## LPL TES vs BLG 整场（2026-08-21，官方流，BLG 2:0 零封）

```text
结果（官方已确认）：BLG 2:0 TES（G1 翻盘、G2 回撤 47c 后再锁定 99.5c）。
弹幕：TES 566 / BLG 823 提及；Bin 回归首秀（"世一上 bin"）+ 左手（knight）
  配合被反复点名；TES 侧自嘲为主（"孩子们，我又可以去世界赛出新歌了"），
  小天丝血送人头被调侃——叙事非灰信号，无集中质疑。
形态：G2 为"强势方回撤不破位再锁定"正样本（对照 TES 53c 反抽失败归零）。
快照：docs/data/snapshots/lol-tes-blg-2026-08-21/。
```

## LPL EDG vs TT 整场（2026-08-21，无弹幕，EDG 2:0）

```text
结果（官方已确认）：EDG 2:0 TT（G1 拉锯三波翻盘、G2 龙魂团碾压；MVP BuLLDoG）。
数据缺口：本场 15:00 开赛，早于当日弹幕会话启动（16:56），无弹幕；
  以 Polymarket 结算 + 官方战报双源确认。
快照：docs/data/snapshots/lol-edg-tt-2026-08-21/。
```

## 结果回填批次（2026-08-23 自主执行）

```text
目标：把此前"官方待回填/待确认"的结果一次性补齐，并修正漏记/误记比赛。

【官方确认（本次回填）】
- EWC CS2 R16（08-19/20）：G2 2:1 Astralis；FUT 2:1 magic（Polymarket 快照
  G1 magic/FUT 各 99.95c 一致）；Vitality 2:0 FaZe；MOUZ 2:1 GL；
  FURIA 2:1 Aurora（修正：原弹幕口径误记欧若拉胜）；Legacy(菊花) 2:0 NAVI
  （修正：菊花=Legacy 巴西队，图二 Ancient 13-2，NAVI 9-16 出局）。
- Dota2 TI2026 胜者组首轮（08-20）：Team Spirit 2:0 Iron Wing；新增
  Team Vision 2:1 BoomBoys（BB vs PV，此前有报告未入库）。
- LCK CL（08-18）：GGA 1-2 BRO（官方确认；G2 瑞兹送局为 BRO 唯一败局）。
- LCK 正赛（08-20）：NS 2:0 KRX（Scout 瑞兹/加里奥；KRX 无缘 Play-In 竞争）；
  JDG 2:1 TT（G1 TT、G2 HongQ 阿卡丽、G3 GALA 卡莎 让一追二）。
- KeSPA Cup 2026 决赛：DNS 3:0 NS 夺冠（egamersworld 官方口径）。

【新增比赛记录】
- 2026-08-20_bb_pv：BoomBoys vs Team Vision（VISION 2:1 官方确认）。
- 2026-08-18_lckcl_dns_ns：LCK CL ROUND 4 DNS.C vs NS.EA（G1 DNS 胜弹幕口径；
  系列打满 3 局，完整比分待 VOD 回补；与同日 K 杯决赛 DNS 3:0 NS 为两场）。

【去重合并】
- 2026-08-21_bro_fox -> 2026-08-21_bro_bfx（BFX 2:1 BRO，快照/复盘并入）。
- 2026-08-21_kt_t1 -> 2026-08-21_t1_kt（T1 2:1 KT，快照并入）。

【灰信号验证回填】
- GGA-BRO G2 瑞兹送局：方向兑现（BRO 输该局），官方已确认比分；录像核查中。
- BRO-KRX G3 Naafiri 质疑：方向一致（BRO 输 G3），用户确认系列 KRX 2:1；
  官方 VOD 待回补。
- DNS-KRX：官方确认 DNS 2:0（灰信号"低水方被做局"方向未兑现，refuted 已记）。

【教训固化（一次错误原则）】
- 结果判定禁用单路"观众预测式"弹幕（本次 Aurora/FURIA 误记源）；
  官方回填是唯一终局口径，弹幕只作方向参考。
- 同日同名对决需区分赛事（LCK CL 与 KeSPA 决赛均为 DNS vs NS）。
```

## LPL TT vs LGD（2026-08-23，G1 LGD 1:0 · G2 进行中）

```text
结果（修正留痕）：G1 官方媒体确认 LGD 先下一城（Tangyuan 洛克 15-2-6，25 分钟
  大龙团反手三杀 2 换 5，约 15:44 收尾）；G2 刚进 BP、尚未开局（用户确认 +
  官方 LPL 流 16:10 仍在 BP + Polymarket 未 close：G2 LGD 0.575/TT 0.425，
  系列 LGD 0.825）。
  【曾误报"G2 结束、系列 2:0"——实为 G1 收尾+二路切台，已按 CAPTURE_RULES
  12.13 修正；系列结果以官方市场 close/官方比分源为准】
核心情报（BP 后战绩情报强应验）：
  "洛克=汤圆绝活/拿就有/放必炸"——跨场 08-22 洛克 11/1/5 POG + 本场
  15-2-6，多路共振；TT 教练放洛克+选杰斯体系被集中批评。
版本锚点（LONG）：洛克/永恩类收割型中单成为 ban 位价值标的，BP 词表已加入。
规律：LPL 收官日"无关排名"场次观众共识"输一把直接送 2-0"（G1 兑现，待跨场）。
灰信号：34 条宽口径，多为暂停梗/玩梗，无实质指向，不升级实体。
盘口：Polymarket G2 LGD 0.575 领先（未 close）、Under 2.5 0.575；弹幕让 5.5 讨论。
报告：reports/intel_danmu_TT-LGD_2026-08-23.html；数据：2026-08-23_*.jsonl（3 路，G1 峰值 320/分）。
后续：16:00 T1 vs HLE 抢二；TT 骑士之路 vs IG 以本场 BP 弱项为参照。
```

## LCK T1 vs HLE 整场（2026-08-23，HLE 2:0 抢二成功）

```text
结果：G1 官方战报确认 HLE 胜（Zeus 杰斯 2:51 单杀多兰、Zeka 蛇女+Kanavi 盲僧
  团战完美、Peyz 被针对 0 换 4 一波）；G2 弹幕双路 17:12 终局刷屏（Zeus 凯南
  0 换 4"神王降临"），HLE 2:0 T1（G2 官方待回填）。
核心情报：
  - BP 后战绩情报应验："宙斯的杰斯今年没输过"（16:12:10）→ G1 对位单杀；
  - T1 单核体系验证："Peyz 被针对就 G"（死一次基地爆炸体系再样本）；
  - 多兰连场负锚点（奎桑提被单杀/格温无用）——季后赛隐患；
  - Zeus 杰斯/凯南 = LCK 上单绝活锚点（对照 LPL 杰斯"判负"）；
  - 排名：HLE 第二（直通第二轮）/T1 第三（弹幕口径，官方待回填）。
灰信号：0（"多兰像演员"为情绪玩梗，非灰信号）。
盘口：未检索到 Polymarket 事件（slug 待查）。
报告：reports/intel_danmu_T1-HLE_S0_2026-08-23.html；数据：2026-08-23_shuoshuo/we957 jsonl（双路 1,300+ 条）。
```

## 08-23 晚场批次（LGD-TT 终局 + EDG-JDG + BFX-NS）

```text
1) LGD 2:0 TT（三源确认：Polymarket 结算 LGD 1.0、直播吧"横扫收官"、弹幕）：
   G1 洛克 15-2-6（BP 后战绩情报应验）、G2 汤圆瑞兹+Heng 皇子。
   沉淀：洛克=汤圆绝活锚点（连续 POG 级）；TT 骑士之路 BP 弱项参照。
2) EDG vs JDG：G1 官方确认 JDG 1:0（小徐贾克斯+HongQ 发条，超长暂停 1 小时+）；
   G2 进行中 JDG 大优。跨场情报：BuLLDoG 洛克被教育 vs 汤圆 15-2-6——
   "英雄强度+使用者执行"双因素模型再添样本；jiejie 口碑危机（弹幕 180+ 条批评）。
3) BFX vs NS（18:00 恩怨局）：AD 互换对决（Diable→NS vs Taeyoon→BFX），
   赛前预测 BFX 2-1 打满；硕硕/957 未切台，弹幕待接入（无样本不硬撑）。
4) T1 vs HLE：G2 官方结算待回填（弹幕双路口径 HLE 2:0）；排名 HLE 第二直通/T1 第三。
```

## 08-23 终局回填批次（EDG-JDG / BFX-NS，官方确认）

```text
1) EDG 1:2 JDG（官方三源：直播吧 19:49 战报 + EDG 官博赛后战报 + 弹幕）：
   G1 小徐贾克斯 4/0/1 POG（超长暂停 1h+）/ G2 EDG 大龙团翻盘扳平 /
   G3 锤石钩爆 Leave + GALA 无尽屠戮，JDG 2-1 收官。
   沉淀："京东打满的神"打满样本（08-20 2:1 TT、08-23 2:1 EDG）；
   洛克双因素模型再样本（汤圆 15-2-6 vs BuLLDoG 被教育）；
   jiejie 口碑危机持续（218 条提及多为批评）；灰信号 0 实质。
2) BFX 1:2 NS（官方双源：直播吧 20:27 + 虎扑 19:44）：
   G1 泰永女警 10-0 超神 / G2 大菠萝卢锡安 13 杀爆砍扳平 /
   G3 Scout 辛德拉收官；两队骑士之路第一轮 BO5 生死战再相逢。
   沉淀：AD 互换对决"单局极端表现反转"样本（泰永 10-0 → 大菠萝 13 杀）；
   "大菠萝老了/不行"单局共识易反转；NS 韧性样本（G1 崩后连扳两局）；
   NS 灰信号历史集中（48 条）——骑士之路再遇需重点盯防；灰信号 0 实质。
```

## LEC TH vs GX 整场（2026-08-23/24，GX 2:0 横扫）

```text
结果：GX 2:0 TH（Polymarket 事件 lol-th-gx-2026-08-23 的 game1/game2/BO3/
  让分 GX-1.5/总局数 Under 2.5 全部收敛 GX 99.95% + 弹幕双局 GG 23:56/00:53；
  官方 closed 待回填，gol.gg/loltv.gg 滞后）。
核心情报：
  - BP 后战绩情报双应验：G1 弱队杰斯负锚（"杰斯各大赛区10几连跪/这几天
    杰斯都被翻了"，唯一例外 Zeus）→ TH 输 G1；G2 卢锡安无米利欧负锚
    （"没有米利欧的卢锡安伤害一坨/有米都不选"）→ TH 输 G2；
  - TH 弱队三负锚集齐：杰斯 / 卢锡安无体系 / 剑魔打野（Daglas）——
    "弱队杰斯判负"跨赛区规律再强化（LPL/LCK/LEC 通用观察）；
  - TH 上野负面留痕：Daglas（G1 赵信送/G2 剑魔打野"翡翠水平"）、
    Tracyn 纳尔开团无能（"冒充48/多兰/复活甲/永远不来正面"）；
  - GX 资源团纪律画像（"gx资源团不送永远不可能输"）+ Flakked 老将；
  - 热手叙事反例：TH 刚 2:0 SK 后立即被 GX 横扫——弱队连胜叙事可信度低；
  - MKOI 假赛质疑连续两日被提及（08-22 45 条 + 08-23 5 条跨场）→ 重点跟踪。
灰信号：37 条宽口径（假/演/送/剧本/做任务）集中于 TH"假翻"表演段，
  无实质定向质疑（区别于 SK-TH 83 条指向输家）——本场不升级预警。
盘口：Polymarket 全市场收敛 GX（让分 -1.5、Under 2.5 兑现）；
  弹幕"＋8.5怎么办"G1 让分讨论；G1 总击杀 21.5 临界（局中"20了"）。
报告：reports/intel_danmu_TH-GX_2026-08-23.html；
  数据：2026-08-23/24_shuoshuo_323444.jsonl（比赛窗 973 条）。
```

## EWC CS2 总决赛 Spirit vs FUT（2026-08-23/24，Spirit 3:1 夺冠）

```text
结果：Spirit 3:1 FUT（官方确认：虎扑赛后帖 + 直播吧逐图战报；让一追三）。
核心情报：
  - 图一 Cache FUT 13-10（Spirit 手枪局白送）→ 图二 Anubis Spirit 16-13
    （tN1R 29 杀）→ 图三 Ancient 16-14 加时（zont1x 残局强拆，FUT 两图
    赛点全丢）→ 图四 Nuke 速通（FUT 今年零胜率图，"巴黎图书馆"）；
  - 图池战绩情报双应验：Spirit×Ancient 正锚（"遗迹没输过/世界第一遗迹"）
    → 图三拿下；FUT×Nuke 负锚（"今年零胜率/昨晚被狂虐"+"不搬零胜率的核子
    搬33胜率的沙二吗"）→ 图四速通——CS 版"队伍×地图"模型再样本；
  - FUT 三大软肋实体化：关键局心理波动（两图赛点全丢）、狙击手灾难
    （"fut的狙纯区/换王德发真王朝了"）、图池短板（Ban 沙二不 Ban Nuke）；
  - Spirit：让一追三韧性 + 手枪局弱项（"永远送三分"跨场规律候选）+
    donk 决赛发挥争议；同日 DOTA2 TI15 冠军（一天双冠）；
  - 巴黎客场：全场嘘 Spirit → 夺冠"图书馆"——情绪面对照素材。
灰信号：0 实质（"定制冠军/不敢赢吗FUT"为情绪/浪的调侃）。
盘口：弹幕无数字盘讨论；隐含共识"绿龙3比1"命中；Polymarket 事件未检索到。
报告：reports/intel_danmu_SPIRIT-FUT_2026-08-23.html；
  数据：2026-08-23/24_csboy_123321 + captainmo jsonl（决赛 22,628 条）。
```

## LEC KC vs SHFT G1（2026-08-24，SHFT 爆冷 1:0）

```text
结果：G1 SHFT 胜（弹幕多信号：ACE/一波/1-2梭哈15倍命中/02:00 shift嬴了?；
  官方待回填）。KC 14 分钟领先 5k、天肥女警（近 3k/约 15:13）拖 34 分钟
  被翻，终局"泰坦抢龙 + ACE + 一波"。
核心情报：
  - 灰信号高预警定向 KC（宽口径 ~60 条/定向 24 条）："蛇女明牌假赛/
    蛇女买了收了/女警不放夹子就是明演/KC缺钱非得吃/都是第一了为什么不吃/
    送一小局"——BP 段"KC老师别打假赛"预警兑现，"被质疑方输球"方向兑现，
    KC 08-18 卡时间历史（69 条）再犯升级（凡走过必有痕迹）；
  - 蛇女 BP 正锚未应验（反向）：当日 T1/GENG 放蛇女+盲僧皆败 → 本场 KC
    蛇女被集火送维克托，SHFT 维克托后期接管——版本符号需叠加选手执行
    （对照 HLE Zeka 蛇女赢）；
  - KC 卡时间规律再样本："kc打谁都要30几分钟"应验（34 分钟局）；
    "欧洲自古倒数第一吃第一/周末必有爆冷"——LEC 榜尾爆冷传统；
  - 盘口：人头/让分盘 KC 让 10.5-13.5（1.87-1.88），01:47 盘口"平水"
    翻转；观众高赔押 SHFT"1-2梭哈中了/15倍"G1 命中；
  - 选手级：Canna 朗姆送武器 2 个；Yike 全输出赵信被批；Sheo（SHFT/
    TH 旧将）Vi 把把送但队伍赢；维克托使用者疑似 Puduk（待核）。
灰信号：高（见上），已入 gray_signals 高预警 + KC 实体再犯升级。
报告：reports/intel_danmu_KC-SHFT_G1_2026-08-24.html；
  数据：2026-08-24_shuoshuo_323444.jsonl（G1 窗 867 条）。
```

## LEC KC vs SHFT G2（2026-08-24，KC 马拉松扳平 1:1）

```text
结果：G2 KC 胜（Polymarket game2 结算 99.95% KC + 弹幕"让一追二/赌G死一地"；
  官方交叉确认）。约 49 分钟马拉松局（02:08-02:57），SHFT 卡牌上单/盲僧/EZ
  一度主导（观众喊"早说了2:0"），终局 KC 翻盘。系列 1:1，G3 决胜局
  （Polymarket 总局数 Over 2.5 已定、系列盘 KC 82%）。
核心情报：
  - 灰信号方向混合样本：G1 定向 KC 兑现（KC 输）＋G2 仍高浓度定向 KC 中单
    （瑞兹"控盘假赛杀kc/中单不想赢/这个中路得买多少"）但 KC 赢——G3 决定性；
  - KC 中单双局负锚：G1 蛇女（版本符号失效）→ G2 瑞兹（"补刀都不会"）；
  - SHFT 体系：卡牌上单压纳尔（"死两次经济还领先"）+ 盲僧 4 头（"打破LEC
    弱队无盲僧魔咒"）+ EZ 后期（"少爷ez太尽力了"= 输方尽力）；
  - 盘口：G2 击杀让分 -9.5 结算（"初盘10.5 死活不给"）；SHFT 横扫盘输
    （"这赢了赌G死一地"）。
报告：reports/intel_danmu_KC-SHFT_G2_2026-08-24.html；
  数据：2026-08-24_shuoshuo_323444.jsonl（G2 全窗约 1,100 条）。
```

## LEC KC vs SHFT 整场（2026-08-24，KC 2:1 让一追二）

```text
结果：KC 2:1 SHFT（官方确认：Polymarket lol-shft-kc-2026-08-23 全 settled；
  G1 SHFT / G2 KC / G3 KC）。
核心情报：
  - 灰信号方向整体未兑现（关键反例）：三局高浓度定向 KC（~100 条宽口径，
    中单三局负锚：蛇女/瑞兹/第三选），G1 兑现（KC 输）但 G2/G3 未兑现
    （KC 赢）——"被质疑方必输"不成立，入库 refuted（对照 SK-TH 83 条
    两局兑现：灰信号浓度≠结果方向）；
  - 蛇女 BP 正锚未应验（单局负锚≠系列）：HLE Zeka 蛇女赢 vs KC 蛇女输，
    KC 靠 G2/G3 逆转——版本符号需叠加选手执行；
  - KC 卡时间跨场规律实锤：三局 34/49/27 分钟（08-18 → 08-24 延续）；
  - SHFT：G1 爆冷（0-6 打 7-0）后领先守不住（G2 被翻/G3 未守住），
    首胜未遂（0-7）；"弱队盲僧"正锚候选（盲僧 4 头强打）；
  - 盘口：Polymarket 全 settled（game1 SHFT/game2 KC/BO3 KC/Over2.5）；
    G2 击杀让分 -9.5 结算；"1-2梭哈 15倍" G1 命中但系列未成。
灰信号：~100 条宽口径（高浓度）→ 方向 refuted（官方结算判定）。
报告：reports/intel_danmu_KC-SHFT_full_2026-08-24.html；
  数据：2026-08-24_shuoshuo_323444.jsonl（全窗 3,112 条）。
```

## LCK CL DNS.C vs KRX.C 季后赛（2026-08-24，DNS.C 3:1 晋级）

```text
结果：DNS.C 3:1 KRX.C（Polymarket 多市场结算价 99.95c 锁定：
  G1/G2/G4 DNS.C、G3 KRX.C；O/U3.5 Over、O/U4.5 Under、-1.5 DNS.C、
  -2.5 KRX.C 交叉一致；官方战报待回填）。
核心情报：
  - 残阵规则主线：Rich/LazyFeel 一军出场超额被 CL 季后赛规则禁赛
    （弹幕口径，待官方确认）→ Vincenzo（CL 常规赛 MVP 打野）临时转 ADC；
    弹幕"KRX 是 LazyFeel 单核队/有他早碾压"；
  - BP 锚点三连验证：
    ① Vincenzo×Jhin 排位 7 连败负锚（13:11:43）→ G1 应验方向
      （下路被 Kalista+Renata 压制、Vincenzo 首血+背锅）；
    ② "CL 杰斯必败（제필패）"→ G2 Frog 杰斯应验（后期边带隐形）；
    ③ Lancer×K'Sante 正锚 → G2 翻盘核心、弹幕 MVP（"기인급"）；
  - G3 市场前瞻兑现：G3 进行中时 Polymarket O/U3.5 Over 92.5c、
    -2.5 横扫仅 5c → G3 KRX.C 拿下、系列 4 局——盘中价格信号可操作；
  - 弹幕共识 3-0 未完全兑现（G3 被 KRX.C 上野带走），横扫盘高风险；
  - 灰信号 1 条（轻，G3 15:38 "수상하다"未升级）；"던짐"29 条甄别为
    失误吐槽非假赛指控；
  - 长期沉淀：CL 季后赛 1 军超额禁赛规则、无畏征召（Fearless）、
    Kalista+Renata 下路压制体系、Jhin/K'Sante/Jayce 锚点
    （champions/bp_signals/compositions 已入库）。
报告：reports/intel_danmu_DNS-KRX_2026-08-24.html；
  数据：docs/data/danmu/soop/2026-08-24_soop_afchall.jsonl（10613 条）；
  缺口：15:39-15:47 约 8 分钟（进程中断，已恢复并记录）。
```

## 2026-08-26 · Spirit vs DENDELE CS（BLAST Open Porto Group A · BO3）

```text
结果：Spirit 2:0 DENDELE CS（Polymarket 仲裁：系列 Spirit 99.95c、
  Games Total Under 2.5；G1 遗迹 13-8 弹幕明确、G2 叉车 13-7/13-8 市场推算）。
核心情报：
  - G1 遗迹（Spirit 自选/历史优势图）13-8 拿下，但过程被批
    "送分/经济差"（"绿龙一直在赢但是经济没养好""2打1非要送吗"）；
    12:05-12:11 DENDELE eco 翻回数回合（"被对面eco翻盘了吗？"）；
  - G2 叉车（历史弱图，观众口径"绿龙叉车太差了"）拿下——弱图叙事修正；
    观众"送分"叙事升级（"暂停又送分""看来教练是买了"，0 实锤）；
    13:22 密度峰值 777（"？？？"刷屏）；GG 13:44-13:47 集中出现；
  - 灰信号约 14 条（去重）：G1 开局 4 + 局中 6 + G2 局中 6 + 末段 2，
    集中 Spirit"送分/吃/操控"叙事；两路虎牙房共振；0 实锤、
    无盘口即时重合证据；兑现率统计待回填（"被质疑方输球"模式未出现）；
  - 跨图规律候选：Spirit 领先送分/经济管理差（观众口径，跨场待验证）；
    donk 手枪局正向、sh1ro 残局强、tN1R 被批；
  - 完整性：BLAST 官方房 660729 全程 207 条，G1 前半段（11:55-12:49）未采
    （显式标注缺口，VOD 可回捞）；其余两虎牙房覆盖整场约 19,300 条。
报告：reports/intel_danmu_Spirit-DENDELE_2026-08-26_{g1_bp,g1_mid,g1_end,
  g2_bp,g2_mid,g2_end,full}.html（多节点时间轴：match_cs2-ts7-dendel-2026-08-26.html）；
  数据：docs/data/danmu/huya/2026-08-26_huya_csboy_official.jsonl（33,346 条）+
  2026-08-26_huya_csboy_mo.jsonl（3,270 条）+ 2026-08-26_huya_blast.jsonl（207 条）。
```

> 附注（2026-08-26 作废）：cs2-aur1-g2（Aurora vs G2）因跨联赛混源/分类错误
> （LoL 比赛误放 CS 板块）整场作废（intel_voided），不展示、不统计、不参与队伍沉淀；
> 切片修复：-1800 起点前移已删除 + league_files 联赛源过滤（AGENTS 19）。

## 2026-08-27 · NS vs BFX（LCK 入围赛 R1 · 回家局 BO5）

```text
系列：NS 1:1 BFX（G1 NS 胜、G2 BFX 胜；Riot 官方 API + 虎扑战报双源确认）。
G1 官方阵容：NS Kingen青钢影/Sponge皇子/Scout发条/Diable烬/Lehends慎，
  BFX Clear杰斯/Raptor盲僧/VicLa加里奥/Taeyoon女警/Kellin巴德；
  NS 27 分钟团灭一波；Kingen 青钢影"请神s12"正锚兑现。
G2 官方阵容：NS 安蓓萨(狼母)/梦魇/洛克/芸阿娜/璐璐，
  BFX 兰博/蔚/阿狸/EZ/扇子妈；30 分钟 BFX 0换4 一波；
  VicLa 阿狸 MVP 级（弹幕"无敌狐狸"）、Scout 洛克被批、Sponge 梦魇被批。
灰信号 9 条（IS-001~009，观众质疑·非结论）：Raptor 连两局"送"质疑（实体重点）、
  BFX 赢团不控龙"假赛准备输"簇（IS-007，G2 结果未兑现——BFX 仍赢）、
  Scout "打假赛/演"升级（IS-003/008 待 G3-G5 验证）。
数据：4 路虎牙约 5,669 条（16:09-17:21）+ 持续采集；会话 lck_ns_bfx_2026-08-27。
报告：reports/intel_danmu_LCK-NS-BFX_G{1,2}_2026-08-27.html +
  knowledge/intel_pages/ 同名 MD 镜像（官方阵容已回填）。
方法沉淀：knowledge/OFFICIAL_DATA_SOURCES.md（Riot 官方 API 获取选手×英雄
  权威数据）+ tools/fetch_official_game_data.py（一键拉取，2026-08-27 实测）。
```

## 2026-08-28 · 五场整场复盘补齐（官方终局仲裁）

```text
当日已结束比赛全部补齐整场复盘（12 段决策导向模板，官方源仲裁）：
- CS2 Spirit 2-0 G2（Dust2 13:6 / Cache 13:9 官方；donk 31-23/1.45；
  弹幕 Kick gaules 单源、虎牙缺采；灰信号 1 条候选=观众质疑非结论）。
- CS2 Aurora 2-0 DENDELE（Cache 13:7 / Mirage 16:12 OT 官方；jimpphat 39-21/1.49；
  灰信号 322/pix 4-5 条中预警，指向 DENDELE/Luquetá=观众质疑非结论）。
- CS2 paiN 0-2 NAVI（Nuke 9:13 / Mirage 11:13 官方；剧本论 12+/吃质疑 4-5 未兑现，
  反向修正 NAVI 质疑权重）。
- LPL IG 3-0 TT（Riot gameWins 0/3；三局速通 24:08/24:05/19:45 弹幕口径；
  TheShy 上野体系+下路佳琪；灰信号约 91 条 TT 侧=观众质疑非结论）。
- LPL NIP 3-0 EDG（Riot gameWins 3/0；Guwon 野核三连（大虫子/琪亚娜/龙女）
  + Care 蛇女版本锚；G2 29:59 卡线；灰信号约 8 条 EDG 侧（ZDZ/Leave 实体跟踪）。
另有 LCK BRO 2-3 BFX（BFX 3-2 逆转晋级）与 LEC TH 0-2 SHFT 已同日补齐。
matches.json：合并 LOL-BRO2-FOX1 重复条目为 lck-bro-bfx（BFX 3:2），
  补齐 cs2-aurora-dendele，全部 event_slug 对齐 Polymarket 真实 slug。
时间轴壳修复（vps_intel_pipeline.build_timeline_shell）：支持队伍别名
  （team_names.json）+ 联赛前缀文件名（LCK-/CS2-/LPL-）+ exact 只做优先级
  不丢候选——节点页与整场复盘入口共存（教训：BRO-BFX 全称节点曾丢壳）。
报告：reports/intel_danmu_{CS2-Spirit-G2,CS2-Aurora-DENDELE,LPL-TT-IG,
  LPL-EDG-NIP}_full_2026-08-28.html + knowledge/intel_pages/ 同名 MD 镜像。
数据：官方源=Riot gameWins/window + Liquipedia/HLTV + 中文战报多源交叉；
  弹幕源=虎牙（LPL/LCK）+ Kick（CS2 早场单源）；完整性缺口显式标注。
```

## 2026-08-29 · CS2 LVG vs FUT G1 局中加厚版（败者组生死战）

```text
LVG（#32） vs FUT（#5/#6）· BLAST Open Porto Group B 败者组淘汰 · BO3。
G1 Dust II 半场 FUT 5:7 LVG（HLTV 官方实时），次节进行中。
加厚要点（用户反馈"情报内容度下降"后的样板重建）：
- 背景纵深：两队昨日同病相怜（LVG 1-2 Falcons Dust2 9-3 T→0 CT 崩盘；
  FUT 0-2 Legacy 输自己选图 Ancient，cmtry 26-35/-9）——今日皆生死战。
- 选图解读：LVG 自选 Dust2=FUT 弱图（47.6% 口径）+ 自己 T 侧强；
  FUT 自选 Anubis=低胜率图（40% 口径）——自选弱图分歧点。
- 局内时间线：LVG 5-0 开局（Starry 沙地双杀/z4kr 穿门双杀，Hupu 佐证）
  → FUT 追 5-5 → 半场 7:5 → 次节手枪局 LVG 2v1 白送（z4kr 跳警家 +
  EmiliaQAQ 强出，差 0.6s）——三路虎牙 + HLTV 国际评论同帧共振。
- 选手锚点（带量）：cmtry 空枪负锚（虎牙 10+24 黑称"Jee 青春版" +
  HLTV 国际同频）；z4kr 正→负（开局穿门双杀→2v1 跳警家）；
  EmiliaQAQ 负（"全责"+国际 322 质疑=灰信号候选）；Westmelon 1v3 双杀正；
  dem0n 为 FUT 唯一正锚。
- 盘口背离：Polymarket 图一仍 FUT 73.5c / BO3 84c，与 LVG 半场领先背离
  ——图一结果=盘口重估触发点（22:03 gamma 快照）。
- 灰信号：HLTV 国际"EmiliaQAQ 322 agent"等 4 条=观众质疑·非结论，
  已入 gray_signals（2026-08-29_cs2_lvg_fut）+ gray_entities（lvg_emiliaqaq）。
报告：reports/intel_danmu_CS2-LVG-FUT_G1_2026-08-29.html（加厚版，
  覆盖原薄版）+ knowledge/intel_pages/ 同名 MD 镜像；索引已更新。
数据缺口：21:30-21:55 弹幕未采（战报补证）；次节比分 8:5 弹幕单源待官方；
  HLTV 国际评论为网页快照非结构化采集。
```

## 2026-08-29 · 两场 LoL 整场复盘加厚版（LPL TES-LGD / LCK BFX-T1）

```text
用户要求：今天结束的两场 LoL 按加厚版输出，并沉淀"弹幕共识提炼 + 关键信息"为固定模板。
- LPL TES 1-3 LGD（LGD 3-2 拒绝让二追三，官方 gameWins，LGD 99.95c）：
  G5 秒泽丽 -80c/3min（21:44 81.5c→21:49 0.5c）；让二追三共识 860 条=共识盲区；
  Tian 玉玉 330/天神 94、圆神阿卡丽 140+；灰信号修正（Tian 菠菜 79 + Tangyuan 演员 63）。
- LCK BFX 2-3 T1（T1 3-2 艰难晋级，T1 99.95c）：
  T1 盘口深 V 83.5c→28.5c（BFX 2-1 赛点）→99.95c；让一追三共识 vs 翻盘=共识盲区；
  Doran 杰斯/凯南双正锚、Peyz 韦鲁斯五杀；灰信号修正（剧本论 22 + Raptor 假赛王 7）。
加厚要素：分钟盘口轨迹（minute_csv 并入）、共识提炼表（主题/方向/条数/样本/多源状态）、
  关键信息 TOP、灰信号漏检修正（词表补全后两场均从 0 条修正为实质灰信号）。
模板：INTEL_HTML_TEMPLATE.md §0.3 固化"共识提炼表 + 关键信息 TOP + 灰词全量检查"。
报告：reports/intel_danmu_{LPL-TES-LGD,LCK-BFX-T1}_full_2026-08-29.html（加厚版）
  + knowledge/intel_pages/ 同名 MD 镜像；索引已更新。
结构化库：matches.json 备注更新；gray_signals +2（lpl_tes_lgd/lck_bfx_t1）；
  gray_entities +4（tes_tian/lgd_tangyuan/bfx_raptor/t1）。
```

## 2026-08-29 · CS2 LVG vs FUT 系列 1:1 · G3 局中加厚版

```text
系列 1:1（HLTV 官方）：
- G1 Dust2：LVG 13:10（5-0 开局 → FUT 追 5-5 → 半场 7:5 → 13:10 拿下；
  cmtry 空枪 G1 Rating 0.58；Polymarket Map1 LVG 1.0 结算）。
- G2 Anubis：FUT 13:3（上半场 10:2 碾压；LVG 仅 3 分，弹幕"一分父爱"放水观感；
  z4kr 崩盘被批 + HLTV"Z4kr 322"灰信号；自选图兑现，弱图口径证伪=实为 FUT 强图
  75-0/70-30）。
- G3 Ancient 进行中（23:02 快照）：盘口 BO3 FUT 77.5c + 图三 -3.5 77.5c；
  让一追二共识 34 条与盘口同向；Starry"叶哥哥五杀"图三开局正锚（弹幕口径）。
关键信号：cmtry 黑称系 420+（乌克兰JEE/cmjee）；LVG 图池浅共识（"四张图 0 胜率"）；
  Anubis 中国队伍弱图规律样本；"父爱"送分玩梗=灰信号候选频率上升。
数据缺口：22:45-22:59 采集中断（SIGTERM 自动重启，launchd.log 确认）。
报告：reports/intel_danmu_CS2-LVG-FUT_G3_2026-08-29.html + MD 镜像；索引已更新。
```

## 2026-08-30 · 双场局中更新（LEC NAVI-GX G2 / CS2 Falcons-Legacy G2）

```text
用户要求：输出最新情报。双场并行监控，官方事实层核验后同步更新 HTML+MD 加厚版。
- LEC NAVI vs GIANTX（W6 常规赛，matchId 115548681803406155）：
  G1 官方 gameWins NAVI 1:0（GX 强开阵容全程失灵，NAVI 后期体系约 33 分钟兑现；
  SamD 卢锡安送一血后翻正）；G2 进行中，官方阵容 GX 蒙多/蔚/乐芙兰/霞/洛 vs
  NAVI 鳄鱼/皇子/辛德拉/卡莉丝塔/烈娜塔；弹幕 2-0 共识 15+、GX 蒙多"假肉/充电宝"
  负锚 10+；G1 尾段假赛/做任务质疑 20+（观众质疑·非结论）。
- CS2 Falcons vs Legacy（BLAST Open Porto Group B 胜者组半决赛，HLTV 2396938）：
  G1 Mirage Falcons 13:6（kyousuke 22 杀 1.96 Rating MVP；猎鹰严父共识 114 条
  =共识盲区）；G2 Ancient Legacy 9:8 反超（BLAST 官方实时；半场 Falcons 7:5→
  CT 连追）；Falcons 手枪局硬伤 15+、m0NESY 独木难支；BLAST 官方胜率 Falcons 79.1%。
报告：reports/intel_danmu_{LEC-NAVI-GX,CS2-Falcons-Legacy}_2026-08-30.html + MD 镜像；
  索引（intel_danmu_index.html / intel_pages README）与 matches.json 已同步。
数据缺口：G2 window 击杀/经济延迟；Polymarket 两场 slug 未查到；HLTV Cloudflare
  拦截（以 BLAST 官方页为准）；Liquipedia G2 比分延迟。
```

## 2026-08-30 · 新增"队伍特质/倾向"情报维度（词表 → 输出层 → 画像库）

```text
用户要求：GX"一劣就劣到低"这类弹幕是有价值的队伍特质情报，需要落地。
流程：1) 词表提取 → 2) 情报输出层 → 3) 队伍特质画像库（跨场复利）。

1. 词表（tools/danmu_intel.py TRAIT_KW，8 类）：
   逆风崩盘 / 顺风隐身 / 被翻守不住 / 韧性逆转 / 心态摆烂 /
   慢热手热 / 打法风格 / 选手特质。
   全库扫描（08-19~08-30，130 万+ 条）：逆风崩盘 121 / 顺风隐身 120 /
   被翻守不住 1,130 / 韧性逆转 1,310 / 心态摆烂 2,556 / 慢热手热 242 /
   打法风格 3,737 / 选手特质 2,720。

2. 提炼（danmu_intel.analyze → intel.json team_traits）：
   categories（每类 count+样本） + by_entity（按队伍/选手归属）。
   高价值样本：GX"一劣就劣到低"、TT"一劣势拉的很"、KT"劣势等死/把把被让一追二"、
   AL"一落后就无脑放资源/被翻盘的神"、WE"打野一劣势就乱送"、Legacy"一崩就瞎玩"、
   Falcons"老被翻 K3 背锅/下限低"、donk"逆风没声音只能打顺风"。

3. 输出层：INTEL_HTML_TEMPLATE.md 二.12 固化；情报页 §8 新增
   "队伍特质（弹幕口径·待验证）"子表（对象|特质|样本≤2|多源状态）。
   今晚 NAVI-GX / Falcons-Legacy 两页已加入演示。

4. 画像库：teams.json 全部 52 队登记；42 队已入 traits（类别→count/samples/last_seen），
   工具 tools/accumulate_team_traits.py（--scan 全库刷新 / --merge 单场增量）；
   TEAM_PROFILES.md 新增"队伍特质（弹幕口径）"表；players.json 补 donk/NiKo 特质锚。

5. 防错（一次错误原则）：
   a. 黑豹别名冲突：paiN 曾误挂"黑豹"，已修正回 FURIA（team_names.json）；
   b. id 丢失：vit/teamvision/ironwing 与 teams.json id 不一致，merge 加 id_alias；
   c. 昵称误配：观众昵称 Faker 发言（"Faker:WE 韧性十足"）不得归属选手 Faker，
      实体归属排除"昵称:开头"模式；
   d. 回归：tests/test_team_traits.py（4 用例锁定抓取/分类/归属/昵称防护），全绿。

待办：特质兑现率统计（每场结算回填"逆风崩盘/韧性逆转/顺风隐身"是否应验），
  挂接 result-verification / intel-library-sync 闭环。
```

## 2026-08-30 · 昨晚 4 场整场复盘批量输出（FUT / KC / NAVI / Falcons）

```text
用户要求：弹幕采集结束后，对已结束比赛做完整情报整理输出。
昨晚（08-29 晚 ~ 08-30 凌晨）4 场全部结束，已补/升级整场复盘（HTML+MD 双份）：

1. CS2 LVG vs FUT（FUT 2:1 让一追二，LVG 出局）：
   G1 LVG 13:10 Dust2 / G2 FUT 13:3 Anubis / G3 FUT 13:7 Ancient；
   让一追二共识 34 条 + 盘口 77.5c 双兑现；LVG 图池浅应验；
   Anubis 弱图口径证伪（实为 FUT 强图 75-0/70-30）；cmtry/z4kr 两极=胜负手。
   报告：reports/intel_danmu_CS2-LVG-FUT_full_2026-08-29.html + MD 镜像。

2. LEC KC vs SK（KC 2:0）：Mikyx 巴德"内鬼"114 条负锚方向应验；
   盘口 94.95c/Over2.5 12c/让分 -1.5 79c 全兑现；Canna 双正锚；
   控分质疑 40 条未指向异常。G1 弹幕未采（接入前已结束）为缺口。
   报告：reports/intel_danmu_LEC-KC-SK_full_2026-08-30.html + MD 镜像。

3. LEC NAVI vs GX（NAVI 2:1）：G1/G3 NAVI、G2 GX（Polymarket BO3 NAVI 1.0）；
   G2 SamD 天肥卡莉丝塔 02:45 滑脸送 → 1 万+大龙三分钟被翻；
   "samd会送的"共识应验；NAVI 领先守不住 / GX 韧性特质入库。
   报告：reports/intel_danmu_LEC-NAVI-GX_2026-08-30.html（升级整场版）+ MD。

4. CS2 Falcons vs Legacy（Falcons 2:1 晋级）：13:6/10:13/13:6；
   "猎鹰严父"共识 G1/G3 双盲区；Falcons 手枪局硬伤连续应验靠火力兜底；
   Legacy 韧性 G2 兑现/G3 未续；try Dust2 CT 锚未兑现。
   报告：reports/intel_danmu_CS2-Falcons-Legacy_2026-08-30.html（升级整场版）+ MD。

结构化库：matches.json 4 场全部置"已结束"+结果回填；索引与镜像索引同步。
```

## 2026-08-30 · 情报库丰富（规则固化 + 选手库扩充 + 英雄库扩充）

```text
用户确认：收缩-展开加厚模式为标准，此后所有弹幕情报按此输出；历史页不回补；
继续推进情报库丰富。

1. 规则固化：INTEL_HTML_TEMPLATE.md 二.13"收缩-展开加厚模式"（最高）——
   焦点制（速览卡≤5 焦点）+ <details> 折叠证据层 + 逐局时间线必带 +
   共识≥5 行带量 + 画像带原文证据 + 密度目标（整场≥16KB/局中≥12KB）。

2. 选手库扩充（players.json 21 → 88 人）：
   新工具 tools/accumulate_player_intel.py（全库扫描 + rosters 名册 + 别名表），
   --scan 全库刷新。Top：donk 8157 / niko 4634 / zywoo 3509 / faker 1524 /
   karrigan 1260 / kyousuke 1172 / zeus 1102 / mikyx 788；45 人补规范元数据
   （name/team_id/role/game）。
   防错：①"奥斯卡之夜"梗误配 Oscarinin → 移除 oscar 词条；②"老李家"闲聊
   误配 Faker → faker 词表限 faker/飞科 + 昵称"xxx:"前缀排除。

3. 英雄库扩充（champions.json 18 → 26）：
   回填昨晚 4 场锚点——卡莉丝塔（SamD 天肥送·双刃剑）、蒙多（16 级曲线反转）、
   兰博（犯罪 vs Canna 正锚双面）、巴德（Mikyx 内鬼 114 条）、发条（Poby 团战）、
   辛德拉（斩杀体系）、蔚（Yike 节奏）、霞（执行依赖）——均带 match/player/verified。

待办：赔率/价格轨迹采集（price_snapshots 仅 4 条=最大空白）；CS 地图维度
  （maps.json 独立）；联赛库深化；跨场兑现率聚合页。
```

## 2026-08-30 · 官方基础库 + 对手心理对位库（情报库深化）

```text
用户方向：用官方数据源建立最准确的联赛/队伍/选手基础库（别名/标签/个人情况）；
赔率轨迹已有资产（docs/data/snapshots 分钟级 CSV）复用不重做；
构建联赛/战队/选手/英雄库 + 跨区跨场对手心理聚焦；以情报库方式输出。

1. 官方基础库同步工具 tools/sync_official_base.py（Riot esports-api）：
   - getLeagues -> leagues.json official（lck/lck_cl/lec/lpl 4 个主流，id/slug/region）
   - getTeams   -> teams.json official（38 队：riot_id/code/官方全名；
     DNS->DN SOOPers、T1->T1 修正撞 code 问题：name 精确匹配优先）
   - getSchedule+getEventDetails+window -> players.json official（89 人：
     summoner_name/role/riot_player_id；id 前缀归一化，0 重复）

2. 对手心理对位库 docs/data/intel/matchups.json（跨区跨场，12 条）：
   弹幕共识聚合"克制/严父/血脉压制"叙事 + 官方 H2H 回填：
   - flc-legacy（猎鹰严父 333 条，EWC 2:0 应验/BLAST 被反杀=叙事松动）
   - flc-spirit（绿龙玩具 63）、flc-vit（蜜蜂严父 27）、al-we（血脉压制 14）
   - navi-spirit/g2-spirit（绿龙压制）、furia-fut、legacy-navi、ic-vit 等
   每条带 direction/count/samples/h2h/verified。

3. 选手/英雄库此前已扩充（88 人 / 26 英雄），本轮补 official 字段。

待办：CS 官方基础数据（Liquipedia/HLTV 队伍选手页）同步；对位库随每场结算回填
  H2H；地图维度（maps.json）独立。
```

## 2026-08-30 · CS 官方基础库（Liquipedia 队伍/选手）

```text
用户确认"逐步完成，一步步做"——第一步：CS 侧官方基础数据。
新工具 tools/sync_cs_base.py（Liquipedia CS）：
  18 队 official.liquipedia（title/region/igl/coaches/现役 roster）+ 113 人 CS 选手 official。
准确 roster：Falcons（NiKo/TeSeS/m0NESY/kyousuke/karrigan）、Legacy（arT/try/latto 等）、
  LVG（westmelon/z4kr/Starry/C4LLM3SU3）、FUT（cmtry/Krabeni 等）、Spirit（donk/sh1ro/tN1R）、
  Vitality（ZywOo/ropz）、M80（JBa/slaxz-）、paiN（biguzera）等。
修正：Lynn Vision -> Lynn Vision Gaming 页面标题；FURIA roster 待补（页面结构差异）。

下一步：对位库随结算自动回填 H2H；CS 地图维度 maps.json 独立。
```

## 2026-08-30 · 对位库 H2H 回填 + CS 地图维度（第二、三步）

```text
第二步：matchups.json H2H 回填——从 matches.json 109 场解析队伍 H2H（77 场可解析），
  回填 al-we（WE 1 胜）、g2-spirit（Spirit 1 胜）；bfx-t1 已有手动记录
  （2026-08-29 BFX 2:3 T1=未兑现）。回填逻辑可复用（随结算自动跑）。

第三步：docs/data/intel/maps.json（CS 地图维度，7 张竞技图）：
  - Anubis：FUT 强图（75-0/70-30，应验）；LVG/中国弱图口径证伪
  - Ancient：Legacy 强图（13:10 应验）、FUT 强图（69.2%）、Falcons 心理关口（连续丢图）
  - Dust2：Legacy 历史强图当日未兑现、LVG 自选兑现、Falcons 火力兜底
  - Mirage：Falcons 强图、Legacy 自选未兑现
  - Nuke/Inferno/Overpass：待观察（无锚）
  每条带 match + verified，跨场累计。
```

## 2026-08-30 · 历史数据全量盘点 + 画像文档吸收

```text
用户要求：把之前的数据全部盘一遍，历史复盘数据抓进情报库丰富。

1. 数据资产地图 docs/task/DATA_ASSET_MAP.md（全量盘点）：
   弹幕情报页 238 / MD 镜像 353 / 交易复盘 108 / 交易记录 11 / 赔率轨迹 99（93MB）/
   队伍画像 134 行 / 英雄画像 / 联赛画像 / 经验清单 / 灰信号实锤案例 / 拆解 35 /
   原始弹幕 140 万条 / 结构化库 16 json。含吸收映射表 + 优先级（P0-P3）。

2. 吸收工具 tools/absorb_legacy_intel.py（P0 完成）：
   - LEAGUE_PROFILES.md -> leagues.json：LCK/LPL/LEC/CS2 波动/打满/假赛风险/反转可信
   - CHAMPION_PROFILES.md -> champions.json：卡莎/阿卡丽/奇亚娜 预期情形/交易含义
   - TEAM_PROFILES.md -> teams.json：25 队历史画像（风格/形态倾向/证据/信任）
   - EXPERIENCE_INSIGHTS.md -> leagues.json：联赛级先验结论
   - FIXED_MATCH_SUSPECT_CASES.md -> gray_signals.json：6 个历史假赛疑似案例
     （VIT-GX 08-14、T1-DNS 08-17、NAVI-TH 08-17、GGA-BRO.C 08-18、
       GX-G2 08-24、KRX.C-BFX.Y 08-25，severity 高·待核查）

P1 待办：intel_pages 353 份 MD 批量锚点提取（-> 各库锚点/对位）；
P2：reviews 交易复盘 -> matches.json 盘口/队伍表现；
P3：EWC_CS2_LIBRARY -> CS 队伍地图库；COMMENTERS/DANMU_USERS 画像。
```

## 2026-08-30 · P1-P3 按序完成（历史数据全量吸收）

```text
P1（intel_pages MD 批量提取）：
  工具 tools/extract_intel_anchors.py——353 份 MD 覆盖核对：
  matches.json 已全覆盖（99 场 vs MD 83 场，差异=命名/非比赛页）；
  灰信号段批量提取 53 命中（5 簇候选入库）；官方阵容表锚点提取（标准表格式）。

P2（reviews 交易复盘 -> 盘口轨迹）：
  工具 tools/backfill_review_intel.py——解析 108 份复盘逐局赔率表，
  新建 docs/data/intel/price_paths.json（35 场逐局价格路径，如 DNS.C 3:1 KRX.C
  57.5c->100c、BFX.Y 3:0 HLE.C 深水反超）；matches.json 回填 36 场 price_path_review。

P3（EWC_CS2 + 用户/评论者画像）：
  工具 tools/absorb_p3_profiles.py——
  EWC_CS2_LIBRARY 12 场补进 matches.json（109->121）+ price_paths（47 场）；
  DANMU_USERS 19 人 -> users.json（26 人，专业占比/可信度）；
  COMMENTERS -> commenters.json（EurekaWTI 含地址，评论者画像新建）。

修 bug：absorb_p3 load() 漏 .json 判断（对 md 也 json.loads）；commenters 误提取
  分析章节（只保留含地址块）。
情报库全貌（吸收后）：联赛 8 / 战队 52 / 选手 233 / 英雄 29 / 灰信号 52 /
  对位 12 / 地图 7 / 比赛 121 / 盘口轨迹 47 / 用户 26 / 评论者 1。
```

## 2026-08-30 · 生成端重构：程序固化 + 固定提示词 + 大模型 API（替代 Codex 会话）

```text
用户朋友质疑：迁移到云服务器不该靠云端 Codex 运行；固定流程/材料/方法要用程序固化；
弹幕数据程序拿，定期调大模型接口（固定提示词 + 弹幕 -> 结论）；连固化提示词都没有。
用户认可方向，按此改进：

1. prompts/ 目录（固定提示词，可版本管理、可发给线上对齐）：
   report_full.md（整场复盘）/ report_game.md（局中 bp/mid/end）/
   report_pre.md（赛前）/ report_live.md（局中快照）。
   占位符 {TEAMS}/{DATE}/{SLUG}/{INTEL_JSON}/{SLICE_FILE}/{OFFICIAL_NOTE}/{RESULT_NOTE}/{REPORT_PATH}。
   含：12 段标准标题（写死）、速览卡格式、来源分层纪律、收缩-展开加厚模式、
   共识提炼表、关键信息 TOP、灰信号词表修正、质量标杆。

2. tools/generate_intel_report.py（程序生成端）：
   输入（比赛+弹幕+官方数据）-> 组装固定 prompt -> 调 DeepSeek API（OpenAI 兼容）-> 解析 HTML
   -> 门禁校验（12 段/标准标题/details≥3/无编造胜率）-> 迭代修正（最多 3 次，反馈缺失段重试）-> 写 HTML。
   实测：首次生成缺 8 段 -> 反馈后第 2 次 12 段齐全；标题写死后一次通过门禁。

3. requirements.txt（依赖固化，供云部署）：aiohttp/websockets/pycryptodome/requests/protobuf。

意义：生成端从"Codex 会话（每次输出可能不同）"改为"程序 + 固定 prompt + API"，
  大模型只做文本生成，结构/校验/回填由程序保证——正对朋友提出的架构。
待办：full/game/pre 模板实测；vps_intel_pipeline 切换到本生成端；部署包整理。
```

## 2026-08-30 · 生成端重构三任务全部完成

```text
1. 模板实测（full/game/pre/live 四模板全部跑通）：
   - full（LCK DK vs KT）：29KB，12 段齐全（重试 1 次）
   - game（VIT vs SHFT G1 mid）：18KB，12 段齐全（重试 1 次，details 折叠补强后收敛）
   - pre（TH vs MKOI 赛前）：14KB，12 段齐全（重试 2 次）
   - live（VIT vs SHFT 快照）：一次通过门禁
   实测暴露并修复：模型自编段标题/编造胜率/缺 details -> 门禁逐项拦截 + 迭代反馈收敛。

2. vps_intel_pipeline 切换：run_codex_report 不再调 codex exec，
   改为 subprocess 调 tools/generate_intel_report.py（固定 prompt + DeepSeek API）。
   实测 live 节点 rc=0，生成 reports/intel_danmu_VIT-SHFT_2026-08-30_live_2138.html
   （16KB 12 段齐全）；返回约定保持 (rc, stdout, stderr)。

3. 部署包：tools/make_deploy_package.py -> dist/intel_server_pkg/（272K，22 文件）：
   prompts 4 模板 + generate_intel_report + 规则层/校验/采集工具 + 规范文档 +
   requirements.txt + README（部署步骤/API key/节点参数）。
   云端解压即可跑（不含 Codex，只含 API key 配置）。
```

## 2026-08-31 · 昨晚夜场三场整场复盘补齐（LEC GX-FNC · CS2 FUT-IC · CS2 VIT-Legacy）

```text
1. LEC GX 2:1 FNC（G1/G3 GX、G2 FNC；官方 gameWins + Polymarket 一致）：
   - 页 reports/intel_danmu_LEC-GX-FNC_full_2026-08-31.html（19KB 12 段；硕硕单路 2,079 条，密度 10.0/分）
   - 关键：Oscar（Oscarinin = GX 上单）负面提及 33 次成全场最大槽点但 GX 仍 2:1；
     灰信号 17 条（演/剧本/故意送，多为情绪质疑非结论）；盘口 13 条指向"小人头/不打架"
   - 沉淀：GX 上单突破口 + 中单后期 carry 正锚 + 韧性特质延续
2. CS2 FUT 2:0 IC（G1 Mirage 13:9 / G2 Nuke 13:6；Liquipedia/HLTV + Polymarket 一致）：
   - 页 reports/intel_danmu_CS2-FUT-IC_full_2026-08-31.html（21KB 12 段；CSBOY 三路 15,678 条）
   - 关键：IC 负面提及 92（正1负10）全场最集中；灰信号 41 条多为跨场玩梗
     （绿龙剧本/昨天lvg剧本/mo送人头），不构成本场风险证据；
     donk/Zywoo/Niko 均非本场参赛选手（跨场话题已在页面标注，不进入本场锚点）
   - 沉淀：IC 弹幕负面形象固化；FUT 队伍级正锚（无选手级锚点）
3. CS2 Vitality 2:1 Legacy（G1 Nuke 16:14 OT / G2 Mirage 9:13 / G3 Dust2 13:8；HLTV/战报）：
   - 页 reports/intel_danmu_CS2-VIT-Legacy_full_2026-08-31.html（18KB 12 段；弹幕稀疏 503 条，缺口已标注）
   - 关键：Zywoo 13 提及（正1/负0）本场 Vitality 核心正锚；Legacy 进攻"只会抱团一波"被看衰应验；
     Apex 指挥负面（豆豆/僵尸）；灰信号 0
   - 沉淀：Legacy 战术便秘/心态负面；VIT 韧性（G1 OT 翻盘）
4. 生成端修复（一次错误原则，2026-08-31 固化）：
   - load_data_context 弹幕样本现在带真实北京时间时间戳，禁止模型编造时间线时间
     （教训：首版三页时间线全部偏移 8 小时）
   - report_full.md 固化：时间线必须用样本自带时间戳；小局归属按时间窗近似并标注
   - speedcard_consistency 门禁补识别 4 种生成端卡片结构（intel-item/signal-item/
     evidence/signal-card），回归 tests/test_speedcard_consistency.py 10 项全绿
5. 库同步：matches.json 三场 reports 已回填；teams.json 队伍特质合并
   （GX/FNC/FUT/Vitality/Legacy/IC）；镜像 knowledge/intel_pages/ 三页 MD 已生成
```

## 2026-08-31 · 云端成本对齐（成本基准实测 + 配置检查清单 + 部署包刷新）

```text
背景：用户反馈云端每页"深度版"成本远高于本地实测量级，要求把本地生成端
配置发给线上，核对并更新配置。

1. 成本基准实测（直连 DeepSeek API，读 usage 字段，2026-08-31）：
   - full（整场复盘）：输入≈3,318 / 输出≈7,900 tokens ≈0.057 元/页
   - game（局中 bp/mid/end）：输入≈2,867 / 输出≈6,500 ≈0.048 元/页
   - pre（赛前）：≈1,987/5,000 ≈0.036 元/页；live（快照）：≈1,985/5,700 ≈0.040 元/页
   - 单份 ≈0.04–0.06 元，85% 花在输出；一场 BO3（5–8 页）≈0.25–0.45 元；
     一晚 5–6 场 ≈1.5–2.5 元。

2. 根因结论：成本大头不是模型单次价格，而是"生成路径"——
   本地 = 固定提示词 + 直连 DeepSeek API（程序固化结构，大模型只做文本）；
   云端若仍用 Codex 全量生成（每页读 skill+模板+统计再逐段写），
   成本自然高一个量级以上。

3. 产出：
   - 检查清单 docs/task/CLOUD_COST_CONFIG_CHECKLIST.md
     （成本基准表 + 8 项云端核对项 + 同步步骤 + 降本可选）；
   - 部署包刷新 dist/intel_server_pkg/（2026-08-31 成本对齐版，34 文件），
     并打 zip dist/intel_server_pkg_2026-08-31.zip（128K）直接可发；
   - 同步关键修复：generate_intel_report.py + prompts/report_full.md
     已含"弹幕样本带真实北京时间戳"固化（此前 dist 是旧版，无时间戳规则）。

4. 防错规则（一次错误原则）：
   - 云端成本异常：优先核对 ①生成路径是否仍 Codex 全量 ②模型是否 deepseek-chat
     ③输入样本量是否 ≤60 条 ④重试是否 ≤3 次，再谈模型价格；
   - 生成端代码/提示词每次变更后，必须同步刷新 dist/intel_server_pkg
     （含 prompts/ + tools/generate_intel_report.py），禁止只改本地不发包；
   - 云端对齐验证以 API usage 字段为准：full 输入≈3.3k/输出≈7.9k，
     显著超量即回查上述配置项。
```

## 2026-08-31 · LCK CL 季后赛 R1 KT.C 3:0 KRX.C（SOOP 首采 + 整场复盘）

```text
1. SOOP 采集首次接入（lck_cl_2026-08-31 会话，soop_lck_cl=afchall）：
   - 15:09 接入 SOOP 官方频道 [CC] KT vs KRX | 2026 LCK CL PLAYOFFS ROUND 1，
     WebSocket 弹幕落盘 docs/data/danmu/soop/2026-08-31_soop_lck_cl.jsonl；
   - 同场双源：硕硕虎牙全天在采（旧会话名沿用 08-30，按 ts 过滤），
     切片 docs/data/danmu/slices/2026-08-31_ktc_krxc/（all 2,164 条 / game3 714 条）。
2. 结果：KT.C 3:0 KRX.C（Riot 官方 API 15:22 completed 确认：KT gameWins=3/KRX=0；
   SOOP 弹幕 15:16 已提前多用户"3대0승"/"어제오늘 1군2군다이겼네"、硕硕房
   "说不能3-0的呢"共振——弹幕口径先于官方约 6 分钟验证，matches.json 已回填 official+danmu）。
3. 关键情报：KRX.C 越南 AD 一队超比例禁赛缺席；KRX.C 下路/打野差距集中负锚
   （"ad差距太大"/"3판다 정글 차이"/"빈센조 원딜시키노"）；15:13 KT 推家被守"翻了"密集
   含"翻了哥"玩梗成分（降权）；灰信号 15 条（观众质疑非结论）；"小ck历史上就没 3-0"反共识
   未兑现。
4. 产出：G3 局中页 + 整场复盘页（12 段、速览卡门禁通过、MD 镜像同步、
   reports/intel_danmu_index.html + knowledge/intel_pages/README.md 登记）。
5. 防错规则（一次错误原则）：
   - full 复盘时间线再次出现编造（模型把 15:16 弹幕写成"第1局 15:00/15:50"）：
     根因=DATA_CONTEXT 只喂尾部 400 条样本，模型看不到全窗口时间分布。
     -> 已修复 generate_intel_report.py：full 节点改全窗口等距抽样（spread=True），
     同步 dist/intel_server_pkg；页面时间线已人工用真实时间戳修正。
   - 教训固化：生成端时间线类内容，事后必须与样本时间范围核对（超出样本最大时间戳
     即视为编造）；full 复盘必须覆盖全窗口样本。
```

## 2026-08-31 · CS2 G2 vs Aurora 情报质量事故（NiKo 跨场污染 + 编造阵容）

```text
背景：G2 vs Aurora（BLAST Open 2026 Fall，Aurora 1:0 后图二 Inferno）情报页被用户
指出低价值且错误——"管 Niko 什么事？这队伍现在又没有 Niko 了"。

事故点：
1. 模型编造 G2 阵容表：Niko / huNter- / m0NESY / HooXi / jks（Niko 早已转会 Falcons，
   不在 G2）；Aurora 也编了 r3salt/Lack1/KENSI/Norwi/Patsi。
2. Niko 被当作本场正锚（"Niko 个人状态正向 提及22"）、写进速览卡/方向板/LONG-SHORT/
   画像，实际 22 次提及是弹幕聊 Falcons/NiKo 的跨场话题。
3. §7 时间线把 20:33-20:37 闲聊（翻译软件/养鸡/猎鹰）整段倒出，纯噪声。
4. speedcard --fix 会把 §3 残留的编造阵容再抄回速览卡（修了一次又复发）。

处理（本次已落地）：
- 删除编造阵容表，改为"首发待官方（HLTV）回填，禁止编造选手×队伍对照"；
- 全部 Niko 相关锚点替换为本场真实叙事（阳叔换人/新狙击手 NIP 背景/K3 指挥），
  仅保留 §8 一行标注"Niko（Falcons）·跨场话题·不适用本场"；
- §7 时间线改为精选比赛事件（20:10-20:37 真实时间戳，去闲聊噪声）；
- 速览卡人工重写（每条单→+价值强词），门禁通过（问题页 0）；MD 镜像已同步。

防错规则（一次错误原则，固化）：
- CS2 事实层：选手×队伍对照只信 HLTV/Liquipedia，弹幕提及≠本场选手，禁止编造阵容；
- 跨场选手（NiKo/Falcons、donk/Spirit、Zywoo/VIT 等）出现在弹幕时，一律标注
  "跨场话题·不适用本场"，不得进入本场锚点/画像/速览卡；
- 速览卡门禁修复后必须复核：--fix 可能把正文残留错误抄回速览卡，先清正文再修卡；
- §7 时间线只放比赛相关事件，纯闲聊段（翻译/主播日常/其他比赛）滤除并注明；
- 产出即自检：搜索页面内跨场队名/选手名，确认无"张冠李戴"再交付。
```

## 2026-08-31 · 情报全量盘点 + 最佳模板定稿（196 页四维评分）

```text
1. 盘点：196 个比赛情报页按「完整度 / 价值度 / 沉淀性 / 易读性」四维打分排序：
   - 完整度（12 段齐全/折叠区/大小/MD 镜像/数据完整性/官方回填/时间线）≈40；
   - 价值度（共识/锚点/灰信号/盘口/决策落点/多源/分歧加权，封顶 40）；
   - 沉淀性（队伍画像/选手/长期沉淀/联赛规律/特质/验证回填/兑现，封顶 30）；
   - 易读性（速览卡+折叠，封顶 20）。
2. 排除：非比赛情报页（index/ranking/demo/live 聚合）+ 总分<100 残缺页（63 页）；
   核心集 133 页，最佳参考带 = 前 22 名（12 段齐全+加厚版）。
3. 最佳模板参考集（5 份）：LEC-NAVI-GX（LoL 整场）· CS2-Falcons-Legacy（CS2 整场）·
   LCKCL-NS-DNSC G5（LoL 决胜局节点）· CS2-Aurora-G2 G2（CS2 局中节点）·
   CS2-LVG-FUT full（共识+盘口双兑现）。
4. 产出：
   - 排名页 reports/intel_danmu_template_ranking_v2_2026-08-31.html（含方法论/排除规则/评分表）；
   - 模板文档 knowledge/INTEL_TEMPLATE_BEST_2026-08-31.md（12 段结构 + 速览卡硬格式 +
     加厚版密度 + 来源分层 + 数据完整性三栏 + 沉淀闭环 + 门禁流水线 + LoL/CS2 差异 +
     反面清单），可直发线上情报库工具对齐。
5. 后续：所有新情报页按 INTEL_TEMPLATE_BEST 模板执行；模板迭代先改本文档再同步线上。
```

## 2026-08-31 · 模板回归旧 10 段框架（用户定稿，取代 12 段新版）

```text
背景：用户指出 v2 排名混入新版 12 段结构页面，明确要求回到上周（2026-08-26）
按质量排序的旧框架；以当时排名前两名的 A 型标杆（BFX.Y-HLE.C / DNS-DRX 整场）
和 B 型标杆（NAVI-FNC 局中）为基准重建模板。

产出：
1. 模板文档 knowledge/INTEL_TEMPLATE_OLD_2026-08-31.md：
   - A 型 10 段（比赛信息/结果总览/逐局复盘/队伍画像/人员画像/灰信号/
     联赛规律/预测验证/盘口/情报含义/数据溯源）；
   - B 型局中 11 段（加 状态核验/密度时间线/方向性情报）；
   - 硬性门槛沿用：数据带量/灰信号纪律/结果标"弹幕口径"/BP 后战绩情报/
     MD 镜像/match_state_guard/来源分层/跨场纪律/时间戳纪律/缺口三栏；
   - 明确与 12 段差异：去掉速览卡硬性门槛，回归 10 段骨架。
2. 旧框架样页 reports/intel_danmu_LCKCL-NS-DNSC_full_old_2026-08-31.html
   （LCK CL NS 3:2 DNS 整场复盘：双源 23,230 条 + 官方结算回填 +
   G2/G3 断采缺口显式标注）+ MD 镜像已生成、索引已登记。
3. 线上同步：dist/intel_server_pkg/ 已加入旧模板文档 + 样页（HTML+MD），
   打 zip intel_server_pkg_2026-08-31_oldframework.zip；README 已注明
   "生成端 prompts/ 需按 10 段调整、去掉速览卡硬性门槛"。
4. 结论：旧框架强调 10 段完整骨架 + 数据带量 + 闭环回填，速览卡非硬性；
   后续所有情报页（本地与线上）按 INTEL_TEMPLATE_OLD 执行。
```
