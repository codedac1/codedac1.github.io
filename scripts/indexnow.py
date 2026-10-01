#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""indexnow.py — sitemap.xml 의 URL 을 IndexNow 로 네이버(와 IndexNow 참여 엔진)에 알린다.

    py scripts/indexnow.py                 # sitemap 전체 제출
    py scripts/indexnow.py --changed       # page_lastmod.json 에서 오늘 바뀐 페이지만
    py scripts/indexnow.py URL [URL ...]   # 지정한 URL 만
    py scripts/indexnow.py --dry-run       # 보낼 목록만 출력

키: 사이트 루트의 <키>.txt (내용 = 키). 이 파일을 지우거나 이름을 바꾸면 제출이 403 이 된다.
엔드포인트는 네이버(searchadvisor.naver.com/indexnow). IndexNow 프로토콜상 한 곳에 보낸 URL 은
Bing 등 다른 참여 엔진에도 공유된다. 한 번에 최대 10,000개.

응답: 200 = 접수, 202 = 접수(키 확인 대기), 400 = 형식 오류, 403 = 키 파일 불일치,
422 = URL 이 host 와 다름, 429 = 너무 잦은 제출. 접수가 곧 색인 보장은 아니다.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "codedac.com"
ENDPOINT = "https://searchadvisor.naver.com/indexnow"


def key():
    for p in glob.glob(os.path.join(ROOT, "*.txt")):
        name = os.path.splitext(os.path.basename(p))[0]
        if re.fullmatch(r"[0-9a-f]{32}", name) and open(p, encoding="utf-8").read().strip() == name:
            return name
    sys.exit("사이트 루트에 IndexNow 키 파일(<32자리 hex>.txt)이 없습니다.")


def sitemap_urls():
    return re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())


def changed_today():
    lm = json.load(open(os.path.join(ROOT, "scripts", "page_lastmod.json"), encoding="utf-8"))
    today = dt.date.today().isoformat()
    return [u for u, v in lm.items() if isinstance(v, dict) and v.get("d") == today]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--changed", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    urls = a.urls or (changed_today() if a.changed else sitemap_urls())
    urls = [u for u in dict.fromkeys(urls) if u.startswith(f"https://{HOST}/")]
    if not urls:
        sys.exit("보낼 URL 이 없습니다.")
    k = key()
    print(f"{len(urls)}개 URL, 키 {k[:6]}…, → {ENDPOINT}")
    if a.dry_run:
        print("\n".join(urls))
        return

    body = json.dumps({"host": HOST, "key": k, "keyLocation": f"https://{HOST}/{k}.txt",
                       "urlList": urls[:10000]}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            print("응답", r.status, r.read().decode(errors="replace")[:300])
    except urllib.error.HTTPError as e:
        print("응답", e.code, e.read().decode(errors="replace")[:300])
        sys.exit(1)


if __name__ == "__main__":
    main()
