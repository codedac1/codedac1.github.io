# -*- coding: utf-8 -*-
"""사이트에서 시간 제한·광고 패스 문구 빼기 — 11개 앱 앱 페이지·가이드, 21개 언어 (2026-10-24).

Play 등록정보와 같은 원칙: 무료/Pro 는 기능 차이로만 쓴다(앱 1개·하루 내보내기 3회·183% 같은 기능 한도는 둔다).
빼는 것: 하루/세션 사용 시간(3시간·60분), 광고로 여는 패스(24시간·3시간·Free Pass). 숫자가 자주 바뀌어
사이트에 틀린 정보가 남기 쉽고(FloatCalc 60분 → 3시간), 설치 전 사람에게 먼저 보일 내용이 아니다.

    python scripts/edits/no_time_limits_site_20261024.py <폴더>
      <폴더>/spec.json  [{id, file: app|guide, path, en}]
      <폴더>/<lang>.json {id: 새 값}  (en 은 spec 의 en 값)
"""
import json
import os
import sys

SITE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LANGS = "ar de en es fil fr hi id it ja ko ms nl pl pt ru th tr uk vi zh".split()


def load(p):
    raw = open(p, encoding="utf-8", newline="").read()
    return json.loads(raw), "\r\n" if "\r\n" in raw else "\n"


def save(p, data, nl):
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(text.replace("\n", nl))


def put(root, path, value):
    for k in path[:-1]:
        root = root[k]
    old = root[path[-1]]
    if type(old) is not type(value):
        raise TypeError(f"{path}: {type(old).__name__} → {type(value).__name__}")
    root[path[-1]] = value


def main(src):
    spec = json.load(open(os.path.join(src, "spec.json"), encoding="utf-8"))
    ids = {s["id"] for s in spec}
    for l in LANGS:
        vals = {s["id"]: s["en"] for s in spec} if l == "en" else \
            json.load(open(os.path.join(src, f"{l}.json"), encoding="utf-8"))
        assert set(vals) == ids, (l, set(vals) ^ ids)
        files = {"app": os.path.join(SITE, "i18n", f"{l}.json"),
                 "guide": os.path.join(SITE, "i18n", "guides", f"{l}.json")}
        loaded = {k: load(p) for k, p in files.items()}
        for s in spec:
            put(loaded[s["file"]][0], s["path"], vals[s["id"]])
        for k, (d, nl) in loaded.items():
            save(files[k], d, nl)
    print(f"{len(LANGS)}개 언어 × {len(spec)}개 항목 반영")


if __name__ == "__main__":
    main(sys.argv[1])
