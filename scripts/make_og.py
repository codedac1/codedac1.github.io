# -*- coding: utf-8 -*-
"""소셜 공유용 OG 이미지(1200x630) 생성.

1) images/og-image.png — 홈·개인정보처리방침용. 브랜드 배너(16:9)의 가운데를 OG 비율(1.905:1)로
   잘라 줄인다. 배너는 로고·태그라인·앱 아이콘이 가운데 모여 있어 위아래 띠만 조금 잘려 나간다.
2) images/og/<slug>.png — 앱 상세용. 예전엔 첫 스크린샷(세로 506x900)을 그대로 썼는데,
   가로형 미리보기 카드(summary_large_image)에서는 가운데 한 토막만 잘려 무슨 앱인지 알 수 없었다.
   배너와 같은 그라디언트 위에 아이콘·앱 이름·플랫폼, 오른쪽에 스크린샷을 얹는다.
   앱 이름은 모든 언어에서 같은 고유명사라 언어별로 만들지 않는다.

배너나 스크린샷이 바뀌면 이 스크립트를 다시 돌리고 `node scripts/gen_site.js` 로 재생성한다.
(gen_site.js 는 images/og/<slug>.png 가 있을 때만 그 이미지를 쓰고, 없으면 첫 스크린샷으로 돌아간다.)
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(r"D:\CodeDAC\Data\CodeDAC 배경2_4096.png")
OUT = ROOT / "images" / "og-image.png"
APP_OUT = ROOT / "images" / "og"

W, H = 1200, 630
TEAL = (77, 182, 172)
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"


def banner_og():
    src = Image.open(SRC).convert("RGB")
    sw, sh = src.size
    crop_h = round(sw * H / W)
    top = (sh - crop_h) // 2
    img = src.crop((0, top, sw, top + crop_h)).resize((W, H), Image.LANCZOS)
    img.save(OUT, "PNG", optimize=True)
    print("og-image.png 생성 완료:", img.size)


def background():
    """css/style.css 의 .hero 와 같은 135° 그라디언트 + 원 윤곽."""
    stops = [0, .42, .74, 1.2]
    colors = np.array([(62, 78, 118), (47, 59, 89), (51, 86, 106), TEAL], dtype=float)
    x = np.arange(W)[None, :]
    y = np.arange(H)[:, None]
    t = (x + y) / (W + H)
    rgb = np.stack([np.interp(t, stops, colors[:, c]) for c in range(3)], axis=-1)
    img = Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")
    rings = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(rings)
    for cx, cy, r in [(120, 80, 330), (620, -330, 520), (1130, 120, 300), (190, 700, 250), (1080, 690, 400)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255, 30), width=3)
    return Image.alpha_composite(img, rings)


def rounded(im, radius):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1], radius, fill=255)
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


def paste_with_shadow(base, im, xy, radius, blur=18, offset=10, alpha=110):
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sx, sy = xy[0], xy[1] + offset
    ImageDraw.Draw(shadow).rounded_rectangle([sx, sy, sx + im.size[0], sy + im.size[1]], radius, fill=(8, 12, 26, alpha))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(shadow)
    base.alpha_composite(im, dest=xy)


def fit_font(draw, text, path, size, max_w, min_size=34):
    while size > min_size:
        f = ImageFont.truetype(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(path, min_size)


def app_og(app):
    slug, name = app["slug"], app["name"]
    windows = app.get("platform") == "windows"
    img = background()

    # 오른쪽: 스크린샷 두 장을 엇갈려 겹친다(뒤 장은 살짝 위·오른쪽).
    if windows:
        sw = 580
        text_max = 1200 - sw - 60 - 80 - 40
        shots = []
        for i in (2, 1):
            p = ROOT / "images" / "shots" / f"{slug}-{i}.jpg"
            if p.exists():
                s = Image.open(p).convert("RGB")
                shots.append(rounded(s.resize((sw, round(s.size[1] * sw / s.size[0])), Image.LANCZOS), 16))
        x0 = 1200 - sw - 60
        if len(shots) == 2:
            paste_with_shadow(img, shots[0], (x0 + 40, 130), 16, alpha=80)
            paste_with_shadow(img, shots[1], (x0 - 10, 210), 16)
        elif shots:
            paste_with_shadow(img, shots[0], (x0, 150), 16)
    else:
        sh = 470
        shots = []
        for i in (1, 2):
            p = ROOT / "images" / "shots" / f"{slug}-{i}.jpg"
            if p.exists():
                s = Image.open(p).convert("RGB")
                shots.append(rounded(s.resize((round(s.size[0] * sh / s.size[1]), sh), Image.LANCZOS), 22))
        sw = shots[0].size[0] if shots else 0
        x0 = 1200 - 70 - sw * 2 - 26
        text_max = x0 - 80 - 36
        for i, s in enumerate(shots):
            paste_with_shadow(img, s, (x0 + i * (sw + 26), 58 + i * 44), 22)

    d = ImageDraw.Draw(img)

    # 왼쪽: 아이콘 → 앱 이름(+ for Windows) → 플랫폼 · 스토어 → 워드마크
    icon = Image.open(ROOT / "images" / "icons" / f"{slug}.png").convert("RGBA").resize((168, 168), Image.LANCZOS)
    paste_with_shadow(img, icon, (80, 96), 36, blur=16, offset=12, alpha=120)

    base, suffix = (name[: -len(" for Windows")], "for Windows") if name.endswith(" for Windows") else (name, "")
    f_name = fit_font(d, base, FONT_BOLD, 68, text_max)
    y = 300
    d.text((80, y), base, font=f_name, fill=(255, 255, 255))
    y += f_name.size + 14
    if suffix:
        f_suf = ImageFont.truetype(FONT_BOLD, 38)
        d.text((82, y), suffix, font=f_suf, fill=TEAL)
        y += 52
    f_plat = ImageFont.truetype(FONT_REG, 30)
    plat = "Windows · Microsoft Store" if windows else "Android · Google Play"
    d.text((82, y + 4), plat, font=f_plat, fill=(255, 255, 255, 190))

    f_brand = ImageFont.truetype(FONT_BOLD, 40)
    d.text((80, 522), "Code", font=f_brand, fill=(255, 255, 255))
    d.text((80 + d.textlength("Code", font=f_brand), 522), "DAC", font=f_brand, fill=TEAL)

    APP_OUT.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(APP_OUT / f"{slug}.png", "PNG", optimize=True)
    print(f"og/{slug}.png 생성 완료")


if __name__ == "__main__":
    banner_og()
    for app in json.loads((ROOT / "scripts" / "apps_base.json").read_text(encoding="utf-8")):
        app_og(app)
