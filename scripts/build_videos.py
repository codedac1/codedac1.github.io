# -*- coding: utf-8 -*-
"""앱 상세 페이지에 붙일 유튜브 쇼츠 목록과 포스터 이미지를 만든다 (2026-10-01).

입력: 아래 VIDEOS(앱 slug → (한국어판 ID, 영어판 ID)). 쇼츠를 새로 올리면 여기에 추가하고 다시 돌린다.
출력:
  · scripts/app_videos.json — slug → {ko|en: {id, title, uploadDate}}. gen_site.js 가 읽는다.
  · images/videos/<id>.webp — 360x640 포스터. 유튜브 세로 썸네일(oar2.jpg, 1080x1920)을 줄여 사이트에 둔다.
    페이지를 열 때 i.ytimg.com 에 요청하지 않으려는 것 — 영상을 누르기 전까지 유튜브와 아무 통신이 없다.

한국어 페이지는 한국어판, 나머지 20개 언어 페이지는 영어판을 쓴다(Play 등록정보 홍보 영상과 같은 규칙).
ID 는 Data/listings/edits/promo_video_*.py(안드로이드)와 채널 쇼츠 목록+oEmbed 제목(Windows)으로 맞췄다.
"""
import io
import json
import os
import re
import sys
import urllib.request

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(ROOT, "scripts", "app_videos.json")
OUT_DIR = os.path.join(ROOT, "images", "videos")

VIDEOS = {  # slug: (ko, en)
    "clipboard":       ("2jBLO5JoAYM", "lC7cGE3l92c"),
    "autostart":       ("ySxWGsEQV-w", "p_SvWytI9XE"),
    "floatcalc":       ("xd1wHPFps94", "VUotC13tT2s"),
    "floatcrypto":     ("uJpcUPhG9WU", "p9HNe6wyZvs"),
    "floattimer":      ("60x7xsddvy4", "nilyCJ3ucU8"),
    "volumebooster":   ("muO0OBEcfvY", "tg7VE35Gl5A"),
    "photocleaner":    ("BKXChOHWuLk", "iz9pLdzQ6_c"),
    "readfocus":       ("zXhzIH93dGQ", "g0qwDRuU8KQ"),
    "floatnote":       ("ZVhsLvSHsKk", "qwf5qDbbxpI"),
    "clipboardwin":    ("qfrufRJjO_U", "gWCUZczp-cc"),
    "readfocuswin":    ("t_qBkuezvYg", "MXzvWDgTMZA"),
    "floatnotewin":    ("WR9tsuQ_RJ4", "wbzu1wshVCg"),
    "floattimerwin":   ("SNlZBVOPeU4", "BxPXhH2sJMA"),
    "photocleanerwin": ("ROpTUp_fCWQ", "nT_0vUEYAHQ"),
    "floatcryptowin":  ("VKsTULFaRjE", "md2rOxowuEw"),
}

UA = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en"}


def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()


def info(vid):
    # oEmbed 200 = 퍼가기 허용. 막혀 있으면 사이트에서 재생이 안 되므로 여기서 멈춘다.
    title = json.loads(fetch(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"))["title"]
    page = fetch(f"https://www.youtube.com/shorts/{vid}").decode("utf-8", "replace")
    m = re.search(r'itemprop="uploadDate" content="([^"]+)"', page) or re.search(r'"uploadDate":"([^"]+)"', page)
    if not m:
        sys.exit(f"{vid}: uploadDate 를 찾지 못함")
    return title, m.group(1)


def poster(vid):
    out = os.path.join(OUT_DIR, vid + ".webp")
    if os.path.exists(out):
        return
    im = Image.open(io.BytesIO(fetch(f"https://i.ytimg.com/vi/{vid}/oar2.jpg"))).convert("RGB")
    if im.size != (1080, 1920):
        sys.exit(f"{vid}: 세로 썸네일이 아님 {im.size}")
    im.resize((360, 640), Image.LANCZOS).save(out, "WEBP", quality=80, method=6)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    data = {}
    for slug, (ko, en) in VIDEOS.items():
        data[slug] = {}
        for lang, vid in (("ko", ko), ("en", en)):
            title, date = info(vid)
            poster(vid)
            data[slug][lang] = {"id": vid, "title": title, "uploadDate": date}
            print(f"{slug:16} {lang} {vid} {date[:10]} {title[:50]}")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"저장: scripts/app_videos.json ({len(data)}개 앱)")


if __name__ == "__main__":
    main()
