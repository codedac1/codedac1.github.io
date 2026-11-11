# -*- coding: utf-8 -*-
"""가이드 3편 보강(2026-11-11) — 네이버 블로그 글에만 있던 '설치 없이' 방법을 21개 언어 가이드로.

- floating-notes-over-other-apps-android: 갤럭시 팝업 화면(+분할 화면) 섹션·FAQ 1개
- floating-timer-over-other-apps-android: 시계 앱 타이머+알림창·팝업 화면 섹션(맨 앞)·FAQ 1개
- open-app-automatically-after-reboot-android: 갤럭시 자동 다시 시작·Android Auto 섹션·FAQ 1개

원문: guide_galaxy_20261111/en.json(ko 는 직접 작성), 나머지 19개는 번역. insert_at 위치에 섹션을 끼우고
FAQ 는 뒤에 붙인다. 이미 같은 제목의 섹션이 있으면 건너뛴다(한 번만 반영).

    python scripts/edits/guide_galaxy_20261111.py   → node scripts/gen_site.js
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GUIDES = os.path.join(HERE, "..", "..", "i18n", "guides")
SRC = os.path.join(HERE, "guide_galaxy_20261111")
DATE = "2026-11-11"


def shape(patch):
    return {k: ([len(s["p"]) * 10 + len(s.get("steps", [])) for s in v["sections"]], len(v["faq"]), v["insert_at"])
            for k, v in patch.items()}


en = json.load(open(os.path.join(SRC, "en.json"), encoding="utf-8"))
want = shape(en)
done = skipped = 0
for f in sorted(os.listdir(GUIDES)):
    lang = f[:-5]
    pf = os.path.join(SRC, f)
    if not os.path.exists(pf):
        raise SystemExit(f"번역 없음: {lang}")
    patch = json.load(open(pf, encoding="utf-8"))
    if shape(patch) != want:
        raise SystemExit(f"구조 다름: {lang}")
    path = os.path.join(GUIDES, f)
    doc = json.load(open(path, encoding="utf-8"))
    for slug, p in patch.items():
        g = doc["guides"][slug]
        heads = {s["h"] for s in g["sections"]}
        if all(s["h"] in heads for s in p["sections"]):
            skipped += 1
            continue
        at = p["insert_at"]
        g["sections"][at:at] = p["sections"]
        g["faq"].extend(p["faq"])
        g["updated"] = DATE
        done += 1
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
print(f"반영 {done} · 건너뜀 {skipped}")
