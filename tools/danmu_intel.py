#!/usr/bin/env python3
"""Extract trade-relevant intel from Huya danmaku JSONL.

Reads ts/nick/text JSONL (from tools/fetch_huya_danmu.py) and outputs a
structured intel JSON + Chinese summary covering:
  - teams / players sentiment (pos/neg counts + samples)
  - odds & numbers discussion (让分/人头/盘口 digits)
  - match situation clues (score, resources, comeback talk)
  - gray signals (直播间灰话：接单/假赛/买 etc., flagged as risk only)
  - danmaku density bursts (high-activity minutes = likely key game moments;
    trade-relevant: correlated with price moves)

Usage:
  python3 tools/danmu_intel.py --input docs/data/danmu/shuoshuo/2026-08-17_323444.jsonl \
      --out runtime/danmu_intel.json
"""

from __future__ import annotations

import argparse
import datetime
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path


TEAMS = {
    "KC": ["kc", "karmine"],
    "GX": ["gx", "giantx"],
    "TH": ["th", "heratics"],
    "Navi": ["navi", "natus"],
    "T1": ["t1"],
    "DNS": ["dns", "dnsoop"],
    "KT": ["kt"],
    "HLE": ["hle", "hanwha"],
    "GEN": ["gen", "geng"],
    "WBG": ["wbg", "微博"],
    "LNG": ["lng", "李宁"],
    "WE": ["we", "西安we"],
    "EDG": ["edg"],
    "BLG": ["blg"],
    "TES": ["tes"],
    "IG": ["ig", "invictus"],
    # CS2 (EWC/IEM/BLAST/Major) — 2026-08-19 新增
    "Vitality": ["vitality", "小蜜蜂"],
    "Spirit": ["spirit", "绿龙"],
    "G2": ["g2"],
    "NAVI": ["navi", "natus"],
    "FaZe": ["faze", "法泽"],
    "MOUZ": ["mouz", "老鼠"],
    "Liquid": ["liquid", "液体"],
    "FURIA": ["furia", "黑豹"],
    "MongolZ": ["mongolz", "蒙古"],
    "EF": ["eternal fire", "永恒之火"],
    "Astra": ["astra"],
    "AG": ["ag"],
    "白鲨": ["白鲨"],
    "情久": ["情久"],
    "EP": ["ep"],
    # Dota2 (TI2026) — 2026-08-20 新增
    "Iron Wing": ["iron wing", "ironwing", "1w", "铁翼"],
    # Team Spirit shares an English tag with the CS2 roster; Chinese Dota2
    # audiences commonly use “雪碧”, which is unambiguous in this feed.
    "Spirit": ["spirit", "绿龙", "雪碧", "team spirit"],
    # LoL/LCK/LPL/LEC 补充 + CS2/BLAST + Dota2（2026-08-30 补齐 team_names 全量，
    # 保证队伍特质/画像归属不漏；关键词与 docs/data/intel/team_names.json 对齐）
    "TT": ["tt", "thundertalk"],
    "AL": ["al", "anyones legend"],
    "LGD": ["lgd"],
    "JDG": ["jdg", "jd gaming"],
    "SK": ["sk", "sk gaming"],
    "DK": ["dk", "dplus"],
    "BRO": ["bro", "bro2", "brion"],
    "NS": ["ns", "nongshim"],
    "KRX": ["krx", "kiwoom"],
    "BFX": ["bfx", "fearx"],
    "NIP": ["nip", "ninjas in pyjamas"],
    "FNC": ["fnc", "fnatic"],
    "SHFT": ["shft", "shifters"],
    "FLC": ["flc", "falcons", "team falcons", "猎鹰"],
    "Legacy": ["legacy", "菊花"],
    "M80": ["m80"],
    "LVG": ["lvg", "lynn vision"],
    "paiN": ["pain", "pain gaming"],
    "9z": ["9z", "9z team"],
    "IC": ["ic", "inner circle"],
    "Team Vision": ["team vision", "parivision", "pv"],
    "BoomBoys": ["boomboys", "boombos", "bb"],
}

PLAYERS = {
    "Canna": ["canna", "金东河"],
    "Oscar": ["奥斯卡", "oscar"],
    "Poby": ["poby"],
    "Hype": ["hype"],
    "Guma": ["姑妈", "guma", "gumayusi"],
    "Mithy": ["mithy"],
    "Faker": ["faker", "飞科", "老李"],
    "Chovy": ["chovy", "超威"],
    "Zeus": ["zeus", "宙斯"],
    # CS2 — 2026-08-19 新增
    "Niko": ["niko", "尼公子"],
    "Apex": ["apex", "apex"],
    "Zywoo": ["zywoo", "载物"],
    "donk": ["donk"],
    "m0NESY": ["m0nesy", "小孩哥"],
    "Twistzz": ["twistzz"],
    "ropz": ["ropz"],
    "sh1ro": ["sh1ro", "西若"],
    # Dota2 TI2026: Iron Wing vs Team Spirit
    "Pure": ["pure", "普洱"],
    "bzm": ["bzm", "泽马"],
    "33": ["33"],
    "Ari": ["ari"],
    "Whitemon": ["whitemon"],
    "Yatoro": ["yatoro", "亚托罗", "雨神"],
    "Larl": ["larl", "拉尔"],
    "Collapse": ["collapse", "崩溃哥", "崩溃"],
    "not me": ["not me", "notme"],
    "rue": ["rue"],
}

POSITIVE = ["无敌", "强", "猛", "好强", "厉害", "nb", "牛逼", "可以", "稳", "有希望", "相信", "顶"]
NEGATIVE = ["菜", "怂", "懦夫", "垃圾", "拉胯", "发瘟", "废物", "送", "放", "坑", "不行", "离谱", "被压"]
ODDS_KW = ["人头", "让分", "盘口", "赔率", "水位", "6.5", "7.5", "48", "700", "-6.5", "+6.5"]
GRAY_KW = [
    "假赛", "剧本", "菠菜", "买了", "卡盘", "送分", "故意", "操控", "收钱", "演了", "在演",
    # 韩文（SOOP/LCK CL 主体，2026-08-26 补：G4 曾 44 条韩文灰信号规则层报 0）
    "고의", "던지노", "던짐", "던졌", "던지네", "던지고", "지령", "조작", "대리",
    # 英文（Twitch）
    "throw", "rigged", "match fix", "selling", "int",
]
SITUATION_KW = [
    "龙魂", "大龙", "小龙", "经济", "翻盘", "一波", "2-0", "1-1", "2-1",
    "比分", "听牌", "推塔", "开龙", "团战", "优势", "落后", "gg",
    # Dota2
    "肉山", "打盾", "拿盾", "买活", "高地", "守高", "破路", "超级兵", "兵线",
    "塔防", "三路", "bkb", "圣剑",
]

# ---- team traits (队伍特质/倾向, 2026-08-30 新增) ----
# 弹幕对队伍/选手"特定情形下表现倾向"的描述，属于画像层高价值信号：
# 逆风崩盘 / 顺风隐身 / 被翻守不住 / 韧性逆转 / 心态摆烂 / 慢热手热 /
# 打法风格 / 选手特质。词表来源于 2026-08-30 全量弹幕库扫描归纳
# （样本见 knowledge/TEAM_PROFILES.md "队伍特质（弹幕口径）" 与
# knowledge/DANMU_INTEL.md 2026-08-30 记录）。单条命中可能是事件而非特质，
# 须按实体聚合跨场累计后再进画像；情报页呈现须标"弹幕口径·待验证"。
TRAIT_KW = {
    "逆风崩盘": [
        "一劣", "一劣势", "一逆风", "逆风就", "逆风不", "逆风送", "逆风没",
        "逆风不行", "逆风没声音", "逆风局就", "崩盘就", "一崩", "崩到底",
        "劣到", "一崩盘", "劣势就", "劣势拉", "劣势打不过", "劣势不会",
        "一劣势就", "落后就", "一落后", "落后不会", "落后崩",
    ],
    "顺风隐身": [
        "顺风隐身", "顺风没声音", "一顺风", "顺风就", "顺风才", "顺风不",
        "领先不会", "优势不会", "优势就浪", "领先就浪", "浪输", "大优残局",
        "优势守不住", "经济领先不会", "优势送", "优势乱送", "大优势浪", "领先送",
    ],
    "被翻守不住": [
        "被翻", "被翻盘", "被逆转", "翻车", "守不住", "被让一追", "领先被翻",
        "大优被", "大优势被", "被追", "守不住优势",
    ],
    "韧性逆转": [
        "韧性", "翻盘能力", "翻盘基因", "让一追", "逆转", "落后能", "落后翻",
        "硬翻", "追分", "抗压", "落后追", "逆转能力", "翻盘执行力", "绝地翻盘",
        "落后稳住",
    ],
    "心态摆烂": [
        "摆烂", "开摆", "上头", "急了", "心态崩", "心态炸", "不想赢", "放弃",
        "不想打", "摆完", "瞎玩", "乱玩", "心态",
    ],
    "慢热手热": [
        "慢热", "手热", "越打越强", "越打越拉", "越打越屎", "越打越软",
        "梦幻开局", "拖后期", "越拖", "后程发力", "前期强", "后期强", "中后期",
        "前期猛", "前期弱", "后期猛", "越打越猛", "越打越菜",
    ],
    "打法风格": [
        "打法", "运营", "控图", "纪律性", "战术", "体系", "强开", "铁桶",
        "拉扯", "纯天梯", "乱来打法", "打架队", "快攻", "慢节奏", "怂队",
        "风格", "滚雪球",
    ],
    "选手特质": [
        "隐身", "站不出来", "关键局", "软脚", "大赛型", "关键先生", "单核",
        "独木难支", "带不动", "混子", "上限", "下限", "carry不动", "靠不住",
        "大赛软脚", "神经刀", "代练", "拖后腿", "短板",
    ],
}

# ---- deep theme analysis (detailed, opinion-oriented) ----
THEMES = {
    "比赛局势": ["2-0", "1-1", "2-1", "gg", "一波", "翻盘", "龙魂", "暂停", "结束", "零封", "速通", "拿下", "赢了", "输了", "肉山", "打盾", "拿盾", "买活", "高地", "守高", "破路", "超级兵", "兵线", "塔防", "三路", "bkb", "圣剑"],
    "队伍打法/实力": ["阵容", "打法", "保枪", "放资源", "放龙", "控龙", "运营", "强开", "打架", "送分", "首败", "碾压", "菜", "强", "怂", "懦", "无敌", "四保一", "带线", "拉扯"],
    "选手表现": ["皇子", "发条", "蛇女", "打野", "中单", "上单", "下路", "辅助", "canna", "oscar", "奥斯卡", "samd", "姑妈", "guma", "poby", "hype", "pure", "bzm", "泽马", "whitemon", "yatoro", "亚托罗", "雨神", "larl", "拉尔", "collapse", "崩溃", "not me", "rue"],
    "BP/阵容": ["bp", "ban", "pick", "选", "英雄", "体系", "counter", "克制", "一号位", "二号位", "三号位", "四号位", "五号位"],
    "盘口/数字": ["盘", "人头", "让分", "6.5", "7.5", "48", "700", "收", "赔", "水位"],
    "集体质疑": ["假赛", "剧本", "菠菜", "买了", "卡盘", "送分", "故意", "操控", "收钱"],
}

VERDICT_POS = ["强", "猛", "无敌", "厉害", "稳", "有希望", "牛逼", "nb", "可以", "顶", "好"]
VERDICT_NEG = ["菜", "怂", "懦", "垃圾", "废物", "送", "放", "坑", "离谱", "不行", "假", "演", "搞"]


def esc(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def sentiment(text: str) -> str | None:
    if any(k in text for k in POSITIVE):
        return "pos"
    if any(k in text for k in NEGATIVE):
        return "neg"
    return None


def keyword_hit(text: str, keyword: str) -> bool:
    """Avoid matching short ASCII team codes inside unrelated words."""
    lowered = text.lower()
    kw = keyword.lower()
    if kw.isascii() and kw.isalnum() and len(kw) <= 3:
        return bool(re.search(rf"(?<![a-z0-9]){re.escape(kw)}(?![a-z0-9])", lowered))
    return kw in lowered


def _ts_value(row: dict) -> float:
    """Normalize row timestamp to epoch seconds (huya numeric ts / soop string ts+unixtime)."""
    if row.get("unixtime"):
        return float(row["unixtime"])
    ts = row.get("ts")
    if isinstance(ts, (int, float)):
        return float(ts)
    try:
        return datetime.datetime.fromisoformat(str(ts).replace("+0800", "+08:00")).timestamp()
    except (TypeError, ValueError):
        return 0.0


def analyze(rows: list[dict]) -> dict:
    # normalize platform fields: SOOP uses "message", huya uses "text"
    rows = [dict(r, text=r.get("text", r.get("message", ""))) for r in rows]

    def clean(text: str) -> str:
        """样本清洗（2026-08-26 精细度优化）：去 emote 标记/URL，压缩空白。
        避免 Twitch 表情符号与广告刷屏污染情报样本。"""
        t = re.sub(r"\[emote:[^\]]*\]", "", text)
        t = re.sub(r"https?://\S+", "", t)
        t = re.sub(r"\s+", " ", t).strip()
        return t[:120]

    if not rows:
        return {
            "meta": {
                "total": 0,
                "active_users": 0,
                "window_utc": ["等待首条弹幕", "等待首条弹幕"],
                "density_per_min": 0.0,
                "sample_status": "insufficient",
            },
            "teams": {},
            "players": {},
            "odds_discussion": {"count": 0, "samples": []},
            "situation": {"count": 0, "samples": []},
            "gray_signals": {"count": 0, "samples": []},
            "team_traits": {},
            "density_bursts": [],
            "top_users": [],
        }
    ts = [_ts_value(r) for r in rows]
    t0, t1 = min(ts), max(ts)
    minutes = max((t1 - t0) / 60, 1)

    # density bursts by minute
    buckets: dict[int, list[dict]] = defaultdict(list)
    for r in rows:
        buckets[int(_ts_value(r) // 60)].append(r)
    counts = {k: len(v) for k, v in buckets.items()}
    if counts:
        vals = list(counts.values())
        mean = sum(vals) / len(vals)
        std = math.sqrt(sum((v - mean) ** 2 for v in vals) / len(vals)) if len(vals) > 1 else 0
        bursts = [
            {
                "minute_utc": datetime.datetime.fromtimestamp(k * 60, datetime.timezone.utc).strftime("%H:%M"),
                "count": c,
                "samples": [clean(x["text"]) for x in buckets[k][:4] if clean(x["text"])],
            }
            for k, c in sorted(counts.items(), key=lambda kv: -kv[1])
            if c >= max(mean + 2 * std, 6)
        ][:8]
    else:
        bursts = []

    # teams / players sentiment
    team_agg: dict[str, dict] = {}
    for name, kws in TEAMS.items():
        hits = [r for r in rows if any(keyword_hit(r["text"], k) for k in kws)]
        if not hits:
            continue
        pos = sum(1 for r in hits if sentiment(r["text"]) == "pos")
        neg = sum(1 for r in hits if sentiment(r["text"]) == "neg")
        team_agg[name] = {
            "mentions": len(hits),
            "pos": pos,
            "neg": neg,
            "samples": [clean(r["text"]) for r in hits[:5] if clean(r["text"])],
        }

    player_agg: dict[str, dict] = {}
    for name, kws in PLAYERS.items():
        hits = [r for r in rows if any(keyword_hit(r["text"], k) for k in kws)]
        if not hits:
            continue
        pos = sum(1 for r in hits if sentiment(r["text"]) == "pos")
        neg = sum(1 for r in hits if sentiment(r["text"]) == "neg")
        player_agg[name] = {
            "mentions": len(hits),
            "pos": pos,
            "neg": neg,
            "samples": [clean(r["text"]) for r in hits[:5] if clean(r["text"])],
        }

    odds = [r for r in rows if any(k in r["text"] for k in ODDS_KW)]
    gray = [r for r in rows if any(k in r["text"] for k in GRAY_KW)]
    situation = [r for r in rows if any(k in r["text"] for k in SITUATION_KW)]
    users = Counter(r.get("nick") or r.get("nickname") or r.get("user_id") or "?" for r in rows)

    # team traits (队伍特质/倾向, 2026-08-30): 按类别聚合 + 归属实体
    trait_rows: list[tuple[str, str]] = []  # (category, text)
    trait_by_entity: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for r in rows:
        t = r["text"]
        for cat, kws in TRAIT_KW.items():
            if not any(k in t for k in kws):
                continue
            trait_rows.append((cat, t))
            for ent, ent_kws in TEAMS.items():
                # 排除"昵称:开头"误配（如观众昵称 Faker 发言"Faker:WE 韧性十足"）
                if any(keyword_hit(t, k) and not re.search(rf"(?i){re.escape(k)}\s*[:：]", t) for k in ent_kws):
                    trait_by_entity[ent][cat].append(t)
            for ent, ent_kws in PLAYERS.items():
                if any(keyword_hit(t, k) and not re.search(rf"(?i){re.escape(k)}\s*[:：]", t) for k in ent_kws):
                    trait_by_entity[ent][cat].append(t)
            break

    def _dedup(items: list[str], limit: int) -> list[str]:
        seen: list[str] = []
        for x in items:
            x2 = x.strip()
            if not x2 or x2 in seen or any(x2 in s or s in x2 for s in seen):
                continue
            seen.append(x2)
            if len(seen) >= limit:
                break
        return seen

    team_traits = {
        "categories": {
            cat: {
                "count": sum(1 for c, _ in trait_rows if c == cat),
                "samples": _dedup([t for c, t in trait_rows if c == cat], 5),
            }
            for cat in TRAIT_KW
        },
        "by_entity": {
            ent: {
                cat: {"count": len(v), "samples": _dedup(v, 3)}
                for cat, v in cats.items() if v
            }
            for ent, cats in trait_by_entity.items() if cats
        },
    }

    return {
        "meta": {
            "total": len(rows),
            "active_users": len(users),
            "window_utc": [
                datetime.datetime.fromtimestamp(t0, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M"),
                datetime.datetime.fromtimestamp(t1, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M"),
            ],
            "density_per_min": round(len(rows) / minutes, 1),
            "sample_status": "ready",
        },
        "teams": team_agg,
        "players": player_agg,
        "odds_discussion": {"count": len(odds), "samples": [clean(r["text"]) for r in odds[:8] if clean(r["text"])]},
        "situation": {"count": len(situation), "samples": [clean(r["text"]) for r in situation[:8] if clean(r["text"])]},
        "gray_signals": {"count": len(gray), "samples": [clean(r["text"]) for r in gray[:8] if clean(r["text"])]},
        "team_traits": team_traits,
        "density_bursts": bursts,
        "top_users": users.most_common(8),
    }


def print_summary(intel: dict) -> None:
    m = intel["meta"]
    print(f"弹幕情报（{m['window_utc'][0]} ~ {m['window_utc'][1]}，{m['total']} 条，{m['active_users']} 人，{m['density_per_min']} 条/分）\n")
    print("== 队伍情绪 ==")
    for name, d in sorted(intel["teams"].items(), key=lambda kv: -kv[1]["mentions"]):
        _s = d["samples"][0][:40] if d.get("samples") else "（无样本）"
        print(f"  {name}: 提及{d['mentions']} 正{d['pos']}/负{d['neg']} | 例: {_s}")
    print("\n== 选手状态 ==")
    for name, d in sorted(intel["players"].items(), key=lambda kv: -kv[1]["mentions"]):
        _s = d["samples"][0][:40] if d.get("samples") else "（无样本）"
        print(f"  {name}: 提及{d['mentions']} 正{d['pos']}/负{d['neg']} | 例: {_s}")
    print(f"\n== 盘口/数字讨论（{intel['odds_discussion']['count']} 条）==")
    for s in intel["odds_discussion"]["samples"][:5]:
        print(f"  - {s[:50]}")
    print(f"\n== 局势线索（{intel['situation']['count']} 条）==")
    for s in intel["situation"]["samples"][:5]:
        print(f"  - {s[:50]}")
    print(f"\n== 灰信号（{intel['gray_signals']['count']} 条，仅风险提示）==")
    for s in intel["gray_signals"]["samples"][:5]:
        print(f"  - {s[:50]}")
    if intel.get("team_traits", {}).get("categories"):
        print("\n== 队伍特质/倾向（弹幕口径 · 待验证）==")
        for cat, d in intel["team_traits"]["categories"].items():
            if not d["count"]:
                continue
            sample = d["samples"][0][:44] if d["samples"] else ""
            print(f"  {cat}: {d['count']} 条 | 例: {sample}")
        for ent, cats in intel["team_traits"].get("by_entity", {}).items():
            parts = [f"{cat} {d['count']}" for cat, d in cats.items()]
            if parts:
                print(f"  ↳ {ent}: " + " / ".join(parts))
    if intel["density_bursts"]:
        print(f"\n== 弹幕密度峰值（比赛关键时刻，与价格异动相关）==")
        for b in intel["density_bursts"][:5]:
            print(f"  {b['minute_utc']} UTC：{b['count']} 条 | {b['samples'][0][:40]}")


def analyze_deep(rows: list[dict]) -> dict:
    """Theme-grouped, assertion-oriented deep analysis (no raw danmaku stream)."""
    rows = [dict(r, text=r.get("text", r.get("message", ""))) for r in rows]
    themed: dict[str, list[str]] = {t: [] for t in THEMES}
    for r in rows:
        t = r["text"]
        for theme, kws in THEMES.items():
            if any(k.lower() in t.lower() for k in kws):
                themed[theme].append(t)
                break

    def dedup(items: list[str], limit: int = 8) -> list[str]:
        seen: list[str] = []
        for x in items:
            x2 = x.strip()
            if not x2 or x2 in seen or any(x2 in s or s in x2 for s in seen):
                continue
            seen.append(x2)
            if len(seen) >= limit:
                break
        return seen

    themes_out = {t: {"count": len(v), "samples": dedup(v)} for t, v in themed.items()}

    # assertion extraction: object + verdict
    objs = ["KC", "GX", "TH", "Navi", "T1", "皇子", "发条", "打野", "中单", "上单", "下路",
            "Canna", "Oscar", "奥斯卡", "samd", "姑妈", "Poby", "Hype", "阵容", "LEC",
            "Iron Wing", "IW", "Spirit", "雪碧", "Pure", "bzm", "泽马", "33", "Ari", "Whitemon",
            "Yatoro", "亚托罗", "雨神", "Larl", "拉尔", "Collapse", "崩溃", "not me", "rue"]
    assertions: list[tuple[str, str, int]] = []
    counter: dict[tuple[str, str], int] = {}
    for r in rows:
        t = r["text"]
        for o in objs:
            if o.lower() not in t.lower():
                continue
            for v in VERDICT_NEG:
                if v in t:
                    key = (o, "负面:" + v)
                    counter[key] = counter.get(key, 0) + 1
                    break
            else:
                for v in VERDICT_POS:
                    if v in t:
                        key = (o, "正面:" + v)
                        counter[key] = counter.get(key, 0) + 1
                        break
    for (o, v), c in sorted(counter.items(), key=lambda kv: -kv[1]):
        assertions.append((o, v, c))

    # key event timeline: burst minutes with dominant theme
    buckets: dict[int, list[str]] = {}
    for r in rows:
        buckets.setdefault(int(r["ts"] // 60), []).append(r["text"])
    events = []
    for minute, texts in sorted(buckets.items()):
        if len(texts) < 6:
            continue
        theme_count = {}
        for t in texts:
            for theme, kws in THEMES.items():
                if any(k.lower() in t.lower() for k in kws):
                    theme_count[theme] = theme_count.get(theme, 0) + 1
                    break
        top = max(theme_count, key=theme_count.get) if theme_count else "其他"
        import datetime as _dt
        events.append({
            "minute_utc": _dt.datetime.fromtimestamp(minute * 60, _dt.timezone.utc).strftime("%H:%M"),
            "count": len(texts),
            "theme": top,
            "sample": texts[0][:40],
        })

    return {"themes": themes_out, "assertions": assertions[:16], "events": events[-10:]}


def main() -> int:
    parser = argparse.ArgumentParser(description="弹幕 -> 交易情报提炼")
    parser.add_argument("--input", required=True, help="JSONL 弹幕文件")
    parser.add_argument("--out", default=None, help="情报 JSON 输出路径（可选）")
    args = parser.parse_args()
    rows = [
        json.loads(line)
        for line in Path(args.input).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    intel = analyze(rows)
    if args.out:
        Path(args.out).write_text(json.dumps(intel, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n已保存：{args.out}")
    # 2026-08-30：先保存再打印（打印崩溃不再丢 JSON）——
    # 教训：8-29 回填复盘时 print_summary 因空样本 IndexError，
    # 情报 JSON 未保存导致 Codex 生成失败/超时。
    try:
        print_summary(intel)
    except Exception:  # noqa: BLE001
        print("[danmu_intel] print_summary 失败（不影响已保存 JSON）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
