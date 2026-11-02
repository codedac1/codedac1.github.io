# -*- coding: utf-8 -*-
"""Windows Pro 재개 반영(2026-11-02) — 21개 언어.

FloatNote+ Win(1.0.27~, 게시됨)·Clipboard+ Win(1.0.35, 제출)이 선택형 평생 Pro 를 다시 판다. 동기화는 Windows 에서 무료,
그 전부터 쓰던 사람은 Pro 기능이 계속 무료(LegacyGrant). 사이트의 "Windows 판은 전부 무료·인앱 결제 없음"이 틀려졌다:
- apps.floatnotewin.features[5] 끝 문장, apps.floatnotewin.faq[2].a
- apps.clipboardwin.faq[2].a (10/30 clipboardwin_free_faq_20261030.py 가 넣은 '전부 무료' 답을 대체)
- guides sticky-notes-always-on-top-windows / clipboard-history-windows 의 sections[2].p[0] 끝 문장
번역 원본: win_pro_returns_20261102.json (언어별 교체 문자열). 검사: 바꾸지 않을 앞부분이 그대로인지, Pro 가 들어갔는지.

    python scripts/edits/win_pro_returns_20261102.py   → node scripts/gen_site.js
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
I18N = os.path.join(HERE, "..", "..", "i18n")
NEW = json.load(open(os.path.join(HERE, "win_pro_returns_20261102.json"), encoding="utf-8"))


def load(p):
    raw = open(p, encoding="utf-8").read()
    return raw, json.loads(raw)


def save(p, raw, d):
    indent = 2 if raw.startswith("{\n  ") else None
    out = json.dumps(d, ensure_ascii=False, indent=indent)
    if raw.endswith("\n"):
        out += "\n"
    open(p, "w", encoding="utf-8", newline="").write(out)


def keep_head(old, new, frac, what, lang, bad):
    """old 의 앞부분(frac 비율)이 new 에 그대로 남아 있어야 한다 — 마지막 문장만 바꾸는 칸."""
    n = int(len(old) * frac)
    if not new.startswith(old[:n]):
        bad.append(f"{lang}:{what} head changed")


bad = []
for lang, v in sorted(NEW.items()):
    pa, pg = os.path.join(I18N, f"{lang}.json"), os.path.join(I18N, "guides", f"{lang}.json")
    ra, a = load(pa)
    rg, g = load(pg)
    fn, cb = a["apps"]["floatnotewin"], a["apps"]["clipboardwin"]
    gs = g["guides"]["sticky-notes-always-on-top-windows"]["sections"][2]["p"]
    gc = g["guides"]["clipboard-history-windows"]["sections"][2]["p"]

    keep_head(fn["features"][5], v["fn_feat5"], 0.5, "fn_feat5", lang, bad)
    keep_head(gs[0], v["g_sticky"], 0.6, "g_sticky", lang, bad)
    keep_head(gc[0], v["g_clip"], 0.5, "g_clip", lang, bad)   # 바꾸는 마지막 문장이 문단의 절반 가까이 되는 언어가 있다
    if v["fn_faq2"]["q"] != fn["faq"][2]["q"]: bad.append(f"{lang}:fn q changed")
    if v["cb_faq2"]["q"] != cb["faq"][2]["q"]: bad.append(f"{lang}:cb q changed")
    for k in ("fn_feat5", "g_sticky", "g_clip"):
        if "Pro" not in v[k]: bad.append(f"{lang}:{k} no Pro")
    for k in ("fn_faq2", "cb_faq2"):
        if "Pro" not in v[k]["a"]: bad.append(f"{lang}:{k} no Pro")

    fn["features"][5] = v["fn_feat5"]
    fn["faq"][2] = dict(v["fn_faq2"])
    cb["faq"][2] = dict(v["cb_faq2"])
    gs[0] = v["g_sticky"]
    gc[0] = v["g_clip"]
    if "--check" not in sys.argv:
        save(pa, ra, a)
        save(pg, rg, g)

print("languages", len(NEW), "| problems:", bad or "none")
