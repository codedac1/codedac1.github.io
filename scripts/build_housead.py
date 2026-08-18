# -*- coding: utf-8 -*-
"""하우스 광고(패밀리 앱 크로스 프로모션) 엔드포인트를 생성한다.

앱들이 예전엔 형제 앱 아이콘과 소개 문구를 각자 res/ 에 번들로 들고 있었다.
같은 아이콘이 앱마다 다른 해상도/다른 파일명으로 존재해 합계 2.06MB 였고(SecretAlbum
혼자 1.18MB, AutoStart 571KB), 형제 앱 문구는 로케일 파일에 흩어져 2,048개 항목이 됐다.
무엇보다 신규 앱을 홍보하려면 형제 앱 저장소를 전부 고쳐 재출시해야 했고, 실제로
FloatNote/PhotoCleaner/SecretAlbum은 아무 앱에서도 홍보되지 못한 채 남았다.

이제 누구를 홍보할지는 EXCLUDED/WEIGHTS 를 고쳐 이 스크립트를 다시 돌리고 사이트를
올리면 끝난다 — 앱 출시가 필요 없다.

여기서 만드는 것:

    /housead/v1/catalog.<locale>.json   로케일별 카탈로그 (앱 목록 + 문구 + 아이콘 해시)
    /housead/v1/icon/<slug>.webp        192x192 아이콘

앱은 카탈로그 1개를 받아 캐시하고, 거기서 무작위로 고른 **한 개**의 아이콘만
추가로 받는다. 아이콘을 통째로 받는 경로는 없다.

문구와 아이콘의 출처는 이미 사이트가 갖고 있는 것을 그대로 쓴다 — 새로 쓰는
콘텐츠가 없어야 사이트와 앱의 문구가 어긋나지 않는다:

    scripts/apps_base.json   슬러그 -> 스토어 URL (안드로이드 여부와 패키지명이 여기서 나온다)
    i18n/<locale>.json       apps.<slug>.name / .desc / .tag
    images/icons/<slug>.png  256x256 (build_assets.py 가 각 앱 저장소에서 생성)

실행:
    python scripts/build_housead.py
"""
import glob
import hashlib
import io
import json
import os
import re

from PIL import Image

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_JSON = os.path.join(SITE, "scripts", "apps_base.json")
I18N_DIR = os.path.join(SITE, "i18n")
SRC_ICON_DIR = os.path.join(SITE, "images", "icons")
OUT_DIR = os.path.join(SITE, "housead", "v1")
OUT_ICON_DIR = os.path.join(OUT_DIR, "icon")

# 앱이 카드에 48~64dp 로 그리므로 192 면 xxxhdpi(4x) 에서도 여유가 있다. 256 원본을
# 그대로 내리면 트래픽만 늘고 화면에서 달라지는 것이 없다.
ICON_PX = 192

# 홍보 대상에서 뺄 앱.
#
# 안드로이드 앱이어도 여기 있으면 카탈로그에 넣지 않는다 — 아이콘도 만들지 않고,
# 이미 있던 것은 지운다. 형제 앱들이 이 앱을 광고하지 않게 될 뿐, 이 앱 자신은
# 그대로 다른 형제 앱을 광고한다(양쪽은 별개다).
EXCLUDED = {
    "secretalbum",
    "floatcrypto",
}

# 가중 무작위 추첨의 가중치. 기본 10.
#
# 이 값을 올리는 것으로 "어떤 앱을 얼마나 밀 것인가"를 앱 재출시 없이 조정한다 —
# 원격 카탈로그로 옮긴 가장 큰 실익이다. 아래 둘은 번들 시절 어느 앱의 카탈로그에도
# 들어가지 못해 크로스 프로모션을 한 건도 받지 못했으므로 당분간 두 배로 둔다.
WEIGHTS = {
    "floatnote": 20,
    "photocleaner": 20,
}
DEFAULT_WEIGHT = 10

# 카드 부제로 쓸 i18n 필드. `desc` 는 앱마다 톤이 고른 설명문이고, `tagline` 은
# 길이가 들쭉날쭉한 마케팅 문구라 카드에서 잘린다. 바꾸려면 여기만 고치면 된다.
SUBTITLE_FIELD = "desc"

PLAY_ID = re.compile(r"[?&]id=([A-Za-z0-9_.]+)")


def android_apps():
    """apps_base.json 에서 홍보할 안드로이드 앱만 (slug, package) 로 뽑는다.

    Windows 카운터파트(Microsoft Store) 는 안드로이드 기기에 설치할 수 없으므로
    홍보 대상이 아니다 — 스토어 URL 로 갈라낸다. {EXCLUDED} 에 넣은 앱도 뺀다.
    """
    with io.open(BASE_JSON, encoding="utf-8") as f:
        base = json.load(f)
    out = []
    for app in base:
        if app["slug"] in EXCLUDED:
            continue
        m = PLAY_ID.search(app.get("store") or "")
        if m:
            out.append((app["slug"], m.group(1)))
    return out


def build_icon(slug):
    """256x256 사이트 아이콘에서 192x192 webp 를 만들고 (파일명, 내용해시) 를 준다."""
    src = os.path.join(SRC_ICON_DIR, slug + ".png")
    if not os.path.exists(src):
        return None
    im = Image.open(src).convert("RGBA")
    im = im.resize((ICON_PX, ICON_PX), Image.LANCZOS)
    buf = io.BytesIO()
    # method=6 은 가장 느리지만 가장 작다. 14개짜리 배치라 시간은 문제가 안 된다.
    im.save(buf, "WEBP", quality=88, method=6)
    data = buf.getvalue()

    os.makedirs(OUT_ICON_DIR, exist_ok=True)
    out = os.path.join(OUT_ICON_DIR, slug + ".webp")
    # 내용이 같으면 쓰지 않는다 — 매 빌드마다 mtime 만 바뀌어 git 이 더럽혀지는 걸 막는다.
    if not (os.path.exists(out) and open(out, "rb").read() == data):
        with open(out, "wb") as f:
            f.write(data)
    return slug + ".webp", hashlib.sha256(data).hexdigest()[:12], len(data)


def locales():
    """i18n/ 에 있는 로케일 코드. privacy/ 같은 하위 폴더는 제외."""
    out = []
    for p in sorted(glob.glob(os.path.join(I18N_DIR, "*.json"))):
        out.append(os.path.splitext(os.path.basename(p))[0])
    return out


def prune_icons(keep):
    """카탈로그에 없는 아이콘 파일을 지운다.

    홍보 대상에서 뺀 앱({EXCLUDED})의 아이콘이 남아 있으면 어느 카탈로그도 가리키지
    않는 채로 사이트에 계속 올라간다. 앱이 받아 가지는 않지만, 지우지 않으면 왜 있는지
    설명할 수 없는 파일이 된다.
    """
    if not os.path.isdir(OUT_ICON_DIR):
        return
    live = {name for name, _digest in keep.values()}
    for f in sorted(os.listdir(OUT_ICON_DIR)):
        if f.endswith(".webp") and f not in live:
            os.remove(os.path.join(OUT_ICON_DIR, f))
            print("  아이콘 제거: %s (홍보 대상 아님)" % f)


def main():
    apps = android_apps()
    if not apps:
        raise SystemExit("apps_base.json 에서 안드로이드 앱을 찾지 못했다")

    icons = {}
    total = 0
    for slug, _pkg in apps:
        built = build_icon(slug)
        if built is None:
            print("  (경고) images/icons/%s.png 없음 - 이 앱은 카탈로그에서 빠진다" % slug)
            continue
        name, digest, size = built
        icons[slug] = (name, digest)
        total += size
    print("아이콘 %d개 / %d bytes (%dx%d webp)" % (len(icons), total, ICON_PX, ICON_PX))

    prune_icons(icons)

    os.makedirs(OUT_DIR, exist_ok=True)
    written = 0
    for loc in locales():
        with io.open(os.path.join(I18N_DIR, loc + ".json"), encoding="utf-8") as f:
            copy = json.load(f).get("apps") or {}

        entries = []
        for slug, pkg in apps:
            if slug not in icons:
                continue
            c = copy.get(slug)
            if not c or not c.get("name"):
                # 이 로케일에 문구가 없는 앱은 넣지 않는다. 영어로 섞어 내보내면
                # 카드 하나만 언어가 다른, 번역 누락처럼 보이는 화면이 된다.
                continue
            icon, digest = icons[slug]
            entries.append({
                "pkg": pkg,
                "name": c["name"],
                "sub": c.get(SUBTITLE_FIELD) or "",
                "tag": c.get("tag") or "",
                "icon": icon,
                "h": digest,
                "w": WEIGHTS.get(slug, DEFAULT_WEIGHT),
            })

        out = os.path.join(OUT_DIR, "catalog.%s.json" % loc)
        # 앱이 파싱하는 파일이다. 사람이 읽을 일은 드물고 매 요청 트래픽이 되므로
        # 들여쓰기 없이 쓴다.
        body = json.dumps({"v": 1, "apps": entries}, ensure_ascii=False,
                          separators=(",", ":"))
        prev = None
        if os.path.exists(out):
            with io.open(out, encoding="utf-8") as f:
                prev = f.read()
        if prev != body:
            with io.open(out, "w", encoding="utf-8") as f:
                f.write(body)
        written += 1
        print("  catalog.%-3s %d apps / %d bytes" % (loc, len(entries), len(body.encode("utf-8"))))

    print("카탈로그 %d개 생성 -> %s" % (written, os.path.relpath(OUT_DIR, SITE)))


if __name__ == "__main__":
    main()
