# -*- coding: utf-8 -*-
"""가이드 2개 추가(2026-10-30) — 21개 언어.

- floating-stopwatch-windows (floattimerwin): Bing Copilot 인용 1위 질의 "floating stopwatch for pc" 용.
- choose-clipboard-manager-android (clipboard): "무료 클립보드 관리자 고르는 법" 비교형 질의 용.

원문: scripts/edits/new_guides_20261030_en.json, 번역: 같은 폴더 new_guides_20261030/<lang>.json

    python scripts/edits/new_guides_20261030.py   → node scripts/gen_site.js
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GUIDES = os.path.join(HERE, "..", "..", "i18n", "guides")
SRC = os.path.join(HERE, "new_guides_20261030")
EN = os.path.join(HERE, "new_guides_20261030_en.json")


def shape(g):
    return [len(s["p"]) * 10 + len(s.get("steps", [])) for s in g["sections"]] + [len(g["faq"])]


en = json.load(open(EN, encoding="utf-8"))
n = 0
for f in sorted(os.listdir(GUIDES)):
    lang = f[:-5]
    new = en if lang == "en" else json.load(open(os.path.join(SRC, f), encoding="utf-8"))
    assert set(new) == set(en), lang
    for slug, g in new.items():
        assert shape(g) == shape(en[slug]), (lang, slug)
        assert g["app"] == en[slug]["app"] and g["updated"] == en[slug]["updated"], (lang, slug)
    p = os.path.join(GUIDES, f)
    raw = open(p, encoding="utf-8").read()
    d = json.loads(raw)
    d["guides"].update(new)
    indent = 2 if raw.startswith("{\n  ") else None
    out = json.dumps(d, ensure_ascii=False, indent=indent)
    if raw.endswith("\n"):
        out += "\n"
    open(p, "w", encoding="utf-8", newline="").write(out)
    n += 1
print("updated", n)
