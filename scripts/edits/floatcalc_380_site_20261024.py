# -*- coding: utf-8 -*-
"""FloatCalc+ 3.8.0 사이트 문구 — 앱 페이지(long·features·faq)와 가이드(옵션 2 문단·단계·Free/Pro 문단), 21개 언어 (2026-10-24).

3.7 문구(하루 60분·24시간 패스·연산자 줄·2^10·√144)를 3.8.0 기준으로: 무료 3시간(펼친 시간만)·광고 3시간 전체 잠금 해제,
표준 키패드·입력 중 결과, 텍스트 선택 "FloatCalc+로 계산", ⋮ 메뉴 복사·붙여넣기, 타일·위젯·알림, 자동 접기·다크 모드.
desc·tagline 은 그대로라 하우스 광고 카탈로그는 다시 만들 필요 없다.

    python scripts/edits/floatcalc_380_site_20261024.py <번역 폴더>     # <폴더>/<lang>.json (en 포함 21개)
"""
import json
import os
import sys

SITE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LANGS = "ar de en es fil fr hi id it ja ko ms nl pl pt ru th tr uk vi zh".split()
GUIDE = "floating-calculator-over-other-apps-android"
UPDATED = "2026-10-24"


def load(p):
    raw = open(p, encoding="utf-8", newline="").read()
    return json.loads(raw), "\r\n" if "\r\n" in raw else "\n"


def save(p, data, nl):
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(text.replace("\n", nl))


def main(src):
    tr = {l: json.load(open(os.path.join(src, f"{l}.json"), encoding="utf-8")) for l in LANGS}
    for l, t in tr.items():
        a, g = t["app"], t["guide"]
        assert len(a["features"]) == 6 and len(a["faq"]) == 3 and len(g["steps"]) == 4, l
    for l in LANGS:
        t = tr[l]
        p = os.path.join(SITE, "i18n", f"{l}.json")
        d, nl = load(p)
        app = d["apps"]["floatcalc"]
        app["long"], app["features"], app["faq"] = t["app"]["long"], t["app"]["features"], t["app"]["faq"]
        save(p, d, nl)

        p = os.path.join(SITE, "i18n", "guides", f"{l}.json")
        d, nl = load(p)
        g = d["guides"][GUIDE]
        assert g["app"] == "floatcalc" and len(g["sections"]) == 3, l
        g["updated"] = UPDATED
        g["sections"][1]["p"] = [t["guide"]["sec2_p"]]
        g["sections"][1]["steps"] = t["guide"]["steps"]
        g["sections"][2]["p"] = [t["guide"]["sec3_p"]]
        save(p, d, nl)
    print(f"{len(LANGS)}개 언어 반영")


if __name__ == "__main__":
    main(sys.argv[1])
