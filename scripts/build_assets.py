# -*- coding: utf-8 -*-
"""C:\\CodeDAC 하위 앱들의 아이콘/스크린샷을 홈페이지용으로 복사·변환한다."""
import os, glob, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\CodeDAC"
# 이 스크립트가 있는 저장소(codedac1.github.io) 자체가 사이트다. 폴더명이 바뀌어도 따라간다.
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = os.path.join(SITE, "images", "icons")
SHOT_DIR = os.path.join(SITE, "images", "shots")
os.makedirs(ICON_DIR, exist_ok=True)
os.makedirs(SHOT_DIR, exist_ok=True)

BRAND = (47, 107, 255)
BRAND2 = (31, 79, 208)

# slug -> (icon_source_relpath|GEN:Letter, screenshot_dir_relpath|None, screenshot_glob)
APPS = {
    "autostart":     (r"AutoStart\Resource\icon_512.jpg", r"AutoStart\Resource\screenshots\en", "*.png"),
    "clipboard":     (r"Clipboard\Resource\icon_512.png", r"Clipboard\Resource\PlayStore등록자료\en", "*.png"),
    "clipboardwin":  (r"ClipboardWin\src\ClipboardPlus\Assets\app.ico", r"ClipboardWin\Resource\shots", "store-en-*.png"),
    "floatcalc":     (r"FloatCalc\FloatCalc\app\src\main\res\mipmap-xxhdpi\ic_launcher.webp", r"FloatCalc\Resource\PlayStore등록자료\screenshots_v3\en", "*.png"),
    "floatcrypto":   (r"FloatCrypto\Resource\PlayStore_template\images\app_icon.png", r"FloatCrypto\Resource\PlayStore_등록자료\en", "*.png"),
    "floatnote":     (r"FloatNote\Resource\icon_512.png", r"FloatNote\Resource\PlayStore등록자료\en", "*.png"),
    # 한국어 스크린샷은 store-ko-* 라 영어만 고른다.
    "floatnotewin":  (r"FloatNoteWin\src\FloatNotePlus\Assets\app.ico", r"FloatNoteWin\Resource\shots", "store-en-*.png"),
    "floattimer":    (r"FloatTimer\FloatTimer\app\src\main\res\mipmap-xxhdpi\ic_launcher.webp", r"FloatTimer\Resource\screenshots_en", "*.png"),
    # 한국어 스크린샷은 store-ko-* 라 영어만 고른다.
    "floattimerwin": (r"FloatTimerWin\src\FloatTimerPlus\Assets\app.ico", r"FloatTimerWin\Resource\shots", "store-en-*.png"),
    "photocleaner":  (r"PhotoCleaner\Resource\icon_512.png", r"PhotoCleaner\Resource\PlayStore\screenshots\en", "*.png"),
    "readfocus":     (r"ReadFocus\Resource\icon_512.png", r"ReadFocus\Resource\screenshots\en", "*.png"),
    # "0*.png" 는 영어 스크린샷만 고른다(한국어는 ko- 접두사).
    "readfocuswin":  (r"ReadFocusWin\src\ReadFocusPlus\Assets\app.ico", r"ReadFocusWin\docs\store-screenshots", "0*.png"),
    "secretalbum":   (r"SecretAlbum\SecretAlbum\app\src\main\res\mipmap-xxhdpi\ic_launcher.webp", r"SecretAlbum\Resource", "screenshot_en_*.png"),
    # "0*.png" 는 번호 붙은 폰 스크린샷만 고른다(feature_graphic_1024x500.png 제외).
    "volumebooster": (r"VolumeBooster\Resource\icon_512.png", r"VolumeBooster\Resource\play_store\en", "0*.png"),
}

def rounded_mask(size, radius):
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
    return m

def make_icon(src, out):
    size = 256
    im = Image.open(src)
    if hasattr(im, "n_frames") and im.format == "ICO":
        im = max([f.copy() for f in [im]], key=lambda x: x.size[0])
        im = Image.open(src)  # PIL picks largest by default on load
    im = im.convert("RGBA")
    # 정사각형 크롭
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
    im = im.resize((size, size), Image.LANCZOS)
    # 투명 여백을 흰색으로 채운다(런처 아이콘은 가운데 도형만 있고 주변이 투명한 경우가 많음)
    bg = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    bg.alpha_composite(im)
    # 둥근 모서리 적용
    bg.putalpha(rounded_mask(size, 56))
    bg.save(out)

def make_generated_icon(letter, out):
    size = 256
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # 세로 그라데이션
    for y in range(size):
        t = y / size
        c = tuple(int(BRAND[i] * (1 - t) + BRAND2[i] * t) for i in range(3))
        d.line([(0, y), (size, y)], fill=c + (255,))
    im.putalpha(rounded_mask(size, 56))
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 150)
    except Exception:
        font = ImageFont.load_default()
    d2 = ImageDraw.Draw(im)
    bb = d2.textbbox((0, 0), letter, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d2.text(((size - tw) / 2 - bb[0], (size - th) / 2 - bb[1]), letter, font=font, fill=(255, 255, 255, 255))
    im.save(out)

def make_shot(src, out):
    im = Image.open(src).convert("RGB")
    target_h = 900
    w, h = im.size
    if h > target_h:
        im = im.resize((int(w * target_h / h), target_h), Image.LANCZOS)
    im.save(out, "JPEG", quality=82, optimize=True)

# 인자로 slug 를 주면 그 앱만 다시 만든다(전체 재생성은 기존 파일을 모두 덮어쓴다).
only = set(sys.argv[1:])
if only - set(APPS):
    sys.exit(f"알 수 없는 slug: {', '.join(sorted(only - set(APPS)))}")

report = {}
for slug, (icon, shotdir, pat) in APPS.items():
    if only and slug not in only:
        continue
    # 아이콘
    icon_out = os.path.join(ICON_DIR, slug + ".png")
    if icon.startswith("GEN:"):
        make_generated_icon(icon.split(":", 1)[1], icon_out)
        icon_ok = "generated"
    else:
        make_icon(os.path.join(ROOT, icon), icon_out)
        icon_ok = "copied"
    # 스크린샷
    n = 0
    MAX_SHOTS = 8  # Play Store 폰 스크린샷 상한과 동일. 소스에 있는 만큼 전부 복사.
    if shotdir:
        files = sorted(glob.glob(os.path.join(ROOT, shotdir, pat)))
        for i, f in enumerate(files[:MAX_SHOTS]):
            make_shot(f, os.path.join(SHOT_DIR, f"{slug}-{i+1}.jpg"))
            n += 1
    report[slug] = (icon_ok, n)

for slug, (ic, n) in report.items():
    print(f"{slug:14} icon:{ic:9} shots:{n}")
print("DONE")
