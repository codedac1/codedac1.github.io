# -*- coding: utf-8 -*-
"""개인정보처리방침: 익명 사용 통계(2026-11-11) — 21개 언어.

새 7항(usage)을 6항(payments) 뒤에 끼우고 뒤 항목 번호를 하나씩 미룬다. 1항 원칙·요약 첫 줄·데이터 표 라벨(usageStats)·
변경 이력·최종 개정일을 바꾼다. 문안: privacy_usage_20261111/<lang>.json. 한 번만 반영(이미 usage 가 있으면 건너뜀).

    python scripts/edits/privacy_usage_20261111.py   → node scripts/scan_app_privacy.js → node scripts/gen_site.js
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PRIV = os.path.join(HERE, "..", "..", "i18n", "privacy")
SRC = os.path.join(HERE, "privacy_usage_20261111")
KEYS = {"updated", "summary0", "principle", "usage_title", "usage_html", "data_label", "history"}
done = 0
for f in sorted(os.listdir(PRIV)):
    lang = f[:-5]
    t = json.load(open(os.path.join(SRC, f), encoding="utf-8"))
    assert set(t) == KEYS, lang
    path = os.path.join(PRIV, f)
    d = json.load(open(path, encoding="utf-8"))
    ids = [s["id"] for s in d["sections"]]
    if "usage" in ids:
        continue
    at = ids.index("payments") + 1
    for s in d["sections"][at:]:
        if s["id"] == "history":
            continue
        m = re.match(r"^(\D*?)(\d+)", s["title"])
        assert m, (lang, s["title"])
        s["title"] = s["title"][:m.start(2)] + str(int(m.group(2)) + 1) + s["title"][m.end(2):]
    d["sections"].insert(at, {"id": "usage", "title": t["usage_title"], "html": t["usage_html"]})
    sec = {s["id"]: s for s in d["sections"]}
    sec["principle"]["html"] = t["principle"]
    h = sec["history"]["html"]
    tag = '<ul class="legal-history">'
    assert h.startswith(tag), lang
    sec["history"]["html"] = tag + t["history"] + h[len(tag):]
    d["summary"][0] = t["summary0"]
    d["data"]["usageStats"] = t["data_label"]
    d["updated"] = t["updated"]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    done += 1
print("반영", done)
