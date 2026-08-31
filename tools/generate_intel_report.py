#!/usr/bin/env python3
"""程序化情报生成端（2026-08-30 建立，替代"Codex 会话生成"）。

架构：程序固化流程/模板/校验，大模型只做"弹幕/官方数据 -> 中文情报文本"。
  prompts/ 目录 = 固定提示词（可版本管理、可发给线上对齐）；
  本程序 = 组装 prompt -> 调大模型 API -> 解析 -> 校验 -> 写 HTML/MD。

用法：
  python3 tools/generate_intel_report.py --teams VIT,SHFT --date 2026-08-30 \
      --node full --intel-json runtime/danmu_sessions/lec_2026-08-30/intel.json \
      --slice-file docs/data/danmu/huya/2026-08-30_huya_shuoshuo.jsonl \
      --out reports/intel_danmu_LEC-VIT-SHFT_full_2026-08-30.html
  python3 tools/generate_intel_report.py --teams VIT,SHFT --date 2026-08-30 \
      --node game --game 1 --gphase mid ...（局中节点）
  python3 tools/generate_intel_report.py --teams VIT,SHFT --date 2026-08-30 --node pre ...

环境：DEEPSEEK_API_KEY 或 ~/.codex/config.toml experimental_bearer_token。
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"


def deepseek_key() -> str:
    key = os.environ.get("DEEPSEEK_API_KEY", "")
    if key:
        return key
    try:
        cfg = Path.home() / ".codex" / "config.toml"
        if cfg.exists():
            m = re.search(
                r'experimental_bearer_token\s*=\s*"([^"]+)"',
                cfg.read_text(encoding="utf-8"),
            )
            if m:
                return m.group(1)
    except Exception:  # noqa: BLE001
        pass
    return ""


def call_llm(prompt: str, max_tokens: int = 8000) -> str:
    key = deepseek_key()
    if not key:
        raise RuntimeError("未找到 DeepSeek API Key（DEEPSEEK_API_KEY 或 ~/.codex/config.toml）")
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL, data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=900) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def extract_html(content: str) -> str:
    """从 LLM 输出中提取 HTML（处理 ```html 包裹 / 前后噪音）。"""
    content = content.strip()
    m = re.search(r"```(?:html)?\s*(.*?)```", content, re.S)
    if m:
        content = m.group(1).strip()
    i = content.find("<!DOCTYPE html")
    if i < 0:
        i = content.find("<html")
    j = content.rfind("</html>")
    if i >= 0 and j > i:
        content = content[i:j + len("</html>")]
    return content


def validate_html(html: str) -> list[str]:
    """基本门禁：非空、完整、12 段编号存在。返回问题列表（空=通过）。"""
    issues = []
    if not html or len(html) < 3000:
        issues.append("HTML 过短或为空")
    if "</html>" not in html.lower() or "<html" not in html.lower():
        issues.append("HTML 不完整（缺 <html>/</html>）")
    if html.count("<details") < 3:
        issues.append(f"收缩-展开加厚模式：<details> 折叠区仅 {html.count('<details')} 个（应 ≥3：原文摘录/长画像/时间线）")
    section_keywords = {
        0: ["速览", "核心"], 1: ["比赛信息", "结果总览", "状态核验"],
        2: ["灰信号"], 3: ["BP", "选人", "阵容"],
        4: ["盘口", "市场"], 5: ["方向", "共识", "锚点"],
        6: ["决策", "LONG", "SHORT", "含义"], 7: ["逐局", "复盘"],
        8: ["画像", "队伍", "人员"], 9: ["规律", "版本", "联赛"],
        10: ["验证", "回填", "预测"], 11: ["溯源", "数据"],
    }
    for n in range(0, 12):
        if f'class="no">{n}</span>' not in html:
            issues.append(f"缺少第 {n} 段（速览卡/结果/灰信号/BP/盘口/方向板/决策/逐局/画像/规律/回填/溯源）")
            continue
        m = re.search(rf'<h2[^>]*><span class="no">{n}</span>([^<]*)</h2>', html)
        if m:
            title = m.group(1)
            if not any(k.lower() in title.lower() for k in section_keywords[n]):
                issues.append(f"第 {n} 段标题「{title}」不符合标准")
    # 只拦无源推测胜率（预测/弹幕/估算）；允许官方源（HLTV/BLAST/Polymarket）
    for mm in re.finditer(r"(预测胜率|弹幕胜率|观众胜率|估算胜率|看好的?胜率)\s*[：: ]?\s*(\d{1,3})%", html):
        issues.append(f"疑似无源编造胜率数字：{mm.group(0)}（需带证据来源，禁止硬造）")
    return issues


def fill(template: str, params: dict) -> str:
    for k, v in params.items():
        template = template.replace("{" + k + "}", str(v))
    return template


def load_data_context(intel_json: str, slice_file: str, max_sample: int = 60,
                      spread: bool = False) -> str:
    """把规则层统计 + 弹幕样本真正嵌入 prompt（替代路径字符串）。

    2026-08-31 修复：此前 prompt 只给文件路径，纯 API 模型读不到弹幕，
    导致"带量"内容可能编造。现在嵌入 intel.json 统计摘要 + 本场弹幕样本。
    2026-08-31 二次修复：样本必须带真实时间戳（北京时间），否则模型会
    幻觉时间线时间（教训：三页 full 复盘时间线全部偏移 8 小时）。
    """
    parts: list[str] = []
    # 1) 规则层统计（danmu_intel.py 产出）
    if intel_json and Path(intel_json).exists():
        try:
            d = json.loads(Path(intel_json).read_text(encoding="utf-8"))
            meta = d.get("meta", {})
            parts.append(
                f"【规则层统计（真实）】弹幕总数={meta.get('total')}，"
                f"活跃用户={meta.get('active_users')}，密度={meta.get('density_per_min')}条/分"
            )
            for grp, key in (("队伍", "teams"), ("选手", "players")):
                items = d.get(key, {})
                if items:
                    top = sorted(items.items(), key=lambda kv: -kv[1].get("mentions", 0))[:8]
                    line = "；".join(f"{k}:提及{v.get('mentions',0)}(正{v.get('pos',0)}/负{v.get('neg',0)})" for k, v in top)
                    parts.append(f"【{grp}提及 TOP（真实）】{line}")
            for grp, key in (("灰信号", "gray_signals"), ("盘口", "odds_discussion"), ("局势", "situation")):
                v = d.get(key, {})
                if isinstance(v, dict) and v.get("count"):
                    samples = "；".join(str(s)[:40] for s in v.get("samples", [])[:4])
                    parts.append(f"【{grp}（真实）】{v.get('count')}条：{samples}")
            traits = d.get("team_traits", {}).get("categories", {})
            if traits:
                tl = "；".join(f"{k}:{v.get('count',0)}" for k, v in traits.items() if v.get("count"))
                parts.append(f"【队伍特质统计（真实）】{tl}")
        except Exception as e:  # noqa: BLE001
            parts.append(f"【规则层读取失败】{e}")
    # 2) 本场弹幕样本（去重、截断、带时间）
    if slice_file and Path(slice_file).exists():
        try:
            rows = []
            for line in Path(slice_file).open(encoding="utf-8"):
                try:
                    o = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                rows.append(o)
            rows.sort(key=lambda x: x.get("ts", 0))
            seen = set()
            samples: list[str] = []
            # full（整场复盘）用全窗口等距抽样，避免模型只看到尾部、
            # 把 15:16 的弹幕当成"第1局 15:00"来编造时间线
            # （2026-08-31 教训：full 复盘时间线整体偏移 +1h，见 DANMU_INTEL.md）；
            # game/live/pre 仍取尾部近窗口（局中/赛末更相关）。
            pool = rows if spread else rows[-400:]
            step = max(1, len(pool) // max_sample)
            for o in pool[::step]:
                t = (o.get("text") or o.get("message") or "").strip()
                if not t or t in seen:
                    continue
                seen.add(t)
                # 真实北京时间时间戳，禁止模型自行换算/编造
                try:
                    bj = datetime.datetime.fromtimestamp(o.get("ts", 0), datetime.timezone(datetime.timedelta(hours=8)))
                    ts_label = bj.strftime("%m-%d %H:%M:%S")
                except Exception:  # noqa: BLE001
                    ts_label = "时间未知"
                samples.append(f"[{ts_label}北京] {t[:50]}")
                if len(samples) >= max_sample:
                    break
            if samples:
                parts.append(f"【本场弹幕样本 {len(samples)} 条（真实，用于提炼，勿照抄）】" + "｜".join(samples))
        except Exception as e:  # noqa: BLE001
            parts.append(f"【弹幕样本读取失败】{e}")
    return "\n".join(parts)


SECTION_NAMES = {
    0: "核心情报速览", 1: "比赛信息与结果总览", 2: "灰信号汇总", 3: "BP 锚点与选人情报",
    4: "盘口与市场讨论", 5: "方向性情报板", 6: "情报含义与决策落点",
    7: "逐局复盘", 8: "队伍/人员画像", 9: "联赛规律与版本",
    10: "预测验证回填", 11: "数据与溯源",
}


def main() -> int:
    ap = argparse.ArgumentParser(description="程序化情报生成端")
    ap.add_argument("--teams", required=True, help="逗号分隔，如 VIT,SHFT")
    ap.add_argument("--date", required=True, help="2026-08-30")
    ap.add_argument("--slug", default="", help="slug（缺省自动拼）")
    ap.add_argument("--node", required=True, choices=["full", "game", "pre", "live"])
    ap.add_argument("--game", type=int, default=0, help="局号（game 节点）")
    ap.add_argument("--gphase", default="mid", choices=["bp", "mid", "end"], help="局中相位")
    ap.add_argument("--intel-json", default="", help="规则层情报 JSON 路径")
    ap.add_argument("--slice-file", default="", help="弹幕切片路径")
    ap.add_argument("--official-note", default="", help="官方数据说明（如 G1 阵容已确认）")
    ap.add_argument("--result-note", default="", help="已确认结果（full 节点）")
    ap.add_argument("--out", required=True, help="输出 HTML 路径")
    ap.add_argument("--ingest", action="store_true", help="生成成功后自动入库（full 节点，调 ingest_after_report）")
    args = ap.parse_args()

    teams = [t.strip() for t in args.teams.split(",")]
    slug = args.slug or f"lol-{teams[0].lower()}-{teams[1].lower()}-{args.date}"
    template_name = {
        "full": "report_full.md", "game": "report_game.md",
        "pre": "report_pre.md", "live": "report_live.md",
    }[args.node]
    template = (PROMPTS / template_name).read_text(encoding="utf-8")
    if not template.strip():
        print(f"缺模板 {template_name}"); return 1

    gphase_label = {"bp": "BP 后/开局（EARLY-GAME）", "mid": "局中（MID-GAME）",
                    "end": "局末/局间（GAME-REVIEW）"}.get(args.gphase, args.gphase)
    end_note = ""
    if args.node == "game" and args.gphase == "end":
        end_note = "第 {GAME} 小局按时间窗估计已结束（局末·待结算校准），结果待官方核对。" \
                   "本页为该小局唯一页面，必须完整覆盖本局 BP/选人、对线、关键团战、结局。"
    params = {
        "TEAMS": " vs ".join(teams), "DATE": args.date, "SLUG": slug,
        "GAME": args.game, "GPHASE_LABEL": gphase_label, "END_NOTE": end_note,
        "INTEL_JSON": args.intel_json or "（无规则层 JSON）",
        "SLICE_FILE": args.slice_file or "（未指定切片）",
        "DATA_CONTEXT": load_data_context(args.intel_json, args.slice_file,
                                          spread=(args.node == "full")) or "（无弹幕数据，写「样本不足」）",
        "OFFICIAL_NOTE": args.official_note or "（未提供，见页面溯源）",
        "RESULT_NOTE": ("本场已确认结果：" + args.result_note + "，页面结果总览直接采用并标注来源「Polymarket 结算」。") if args.result_note else "",
        "REPORT_PATH": args.out,
    }
    prompt = fill(template, params)

    # 迭代修正闭环：生成 -> 校验 -> 不过则反馈缺失段重试（最多 3 次）
    html = ""
    issues: list[str] = []
    for attempt in range(1, 4):
        print(f"[generate] 节点={args.node} slug={slug} 尝试 {attempt}/3 -> 调 {MODEL} ...")
        cur_prompt = prompt
        if attempt > 1 and issues:
            missing = "、".join(SECTION_NAMES[int(x[0])] for x in issues if x and x[0].isdigit() and int(x[0]) in SECTION_NAMES)
            cur_prompt = (
                f"{prompt}\n\n【修正要求】你上一版输出缺少以下段落：{missing or '；且 HTML 不完整'}。"
                f"请严格按 12 段模板完整重写整页（<h2><span class=\"no\">N</span>标题</h2> 编号 0-11，"
                f"一段都不能少），保留上一版正确内容与数据，补齐缺失段落，并加入 <details> 折叠区。"
                f"12 段标题必须原样使用："
                f"0 核心情报速览｜1 比赛信息与结果总览｜2 灰信号汇总｜3 BP 锚点与选人情报｜"
                f"4 盘口与市场讨论｜5 方向性情报板｜6 情报含义与决策落点｜7 逐局复盘｜"
                f"8 队伍/人员画像｜9 联赛规律与版本｜10 预测验证回填｜11 数据与溯源。"
                f"当前缺失/标题不符项：{missing or 'HTML 不完整'}。"
                f"【收缩-展开硬性要求】全页必须包含至少 3 个 <details><summary>…</summary>…</details> "
                f"折叠区（建议：弹幕原文摘录放 §2/§3、完整弹幕时间线放 §7、长画像放 §8），"
                f"每个折叠区 summary 写明内容（如「G2 完整弹幕时间线（折叠）」）。"
            )
        try:
            content = call_llm(cur_prompt, max_tokens=16000)
        except Exception as e:  # noqa: BLE001
            print(f"[generate] LLM 调用失败: {e}")
            return 1
        html = extract_html(content)
        issues = validate_html(html)
        if not issues:
            break
        print(f"[generate] 门禁未过（缺 {len(issues)} 项），重试...")
    else:
        print(f"[generate] 3 次尝试后门禁仍未过：{issues}")
        (Path(args.out)).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(html, encoding="utf-8")
        return 2

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"[generate] OK -> {out_path}（{len(html)} 字节，12 段齐全）")
    # 自动入库：full 节点且 --ingest 时触发赛后沉淀
    if args.ingest and args.node == "full":
        import subprocess as _sp
        ingest_cmd = [
            sys.executable, str(ROOT / "tools" / "ingest_after_report.py"),
            "--root", str(ROOT), "--teams", ",".join(teams), "--date", args.date,
            "--slug", slug, "--slice-file", args.slice_file, "--intel-json", args.intel_json,
        ]
        if args.result_note:
            ingest_cmd += ["--result", args.result_note]
        print(f"[generate] 自动入库触发：{' '.join(ingest_cmd[-8:])} ...")
        try:
            r = _sp.run(ingest_cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=700)
            print(f"[generate] 入库 rc={r.returncode}：{r.stdout.strip()[-200:]}")
        except Exception as e:  # noqa: BLE001
            print(f"[generate] 自动入库失败（不影响页面已生成）: {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
