# -*- coding: utf-8 -*-
"""형제 폴더에 있는 앱들의 아이콘/스크린샷을 홈페이지용으로 복사·변환한다."""
import os, glob, sys
from PIL import Image, ImageDraw, ImageFont

# 앱 소스는 이 저장소의 형제 폴더에 있다. 저장소가 옮겨 다녀도 따라가도록
# 저장소 위치에서 거슬러 올라가 잡고, 환경변수로 덮어쓸 수 있게 둔다.
ROOT = os.environ.get("CODEDAC_ROOT") or os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 이 스크립트가 있는 저장소(codedac1.github.io) 자체가 사이트다. 폴더명이 바뀌어도 따라간다.
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = os.path.join(SITE, "images", "icons")
SHOT_DIR = os.path.join(SITE, "images", "shots")
os.makedirs(ICON_DIR, exist_ok=True)
os.makedirs(SHOT_DIR, exist_ok=True)

# 사이트 21개 언어. Windows 판 스크린샷 폴더는 중국어만 zh-Hans 로 되어 있다.
LANGS = "ar de en es fil fr hi id it ja ko ms nl pl pt ru th tr uk vi zh".split()
WIN_LANG = {"zh": "zh-Hans"}

BRAND = (47, 107, 255)
BRAND2 = (31, 79, 208)

# slug -> (icon_source_relpath|GEN:Letter, screenshot_dir_relpath|None, screenshot_glob)
# 안드로이드 앱은 전부 <App>\Resource\PlayStore등록자료\en (2026-09-16 Clipboard 구조로 통일).
APPS = {
    "autostart":     (r"AutoStart\Resource\icon_512.png", r"AutoStart\Resource\PlayStore등록자료\en", "*.png"),
    "clipboard":     (r"Clipboard\Resource\icon_512.png", r"Clipboard\Resource\PlayStore등록자료\en", "*.png"),
    # 스크린샷이 언어별 폴더로 갈라지면서 docs\store-screenshots\en 으로 옮겨 갔다(ReadFocusWin 과 같은 배치).
    "clipboardwin":  (r"ClipboardWin\src\ClipboardPlus\Assets\app.ico", r"ClipboardWin\docs\store-screenshots\en", "store-en-*.png"),
    "floatcalc":     (r"FloatCalc\FloatCalc\app\src\main\res\mipmap-xxhdpi\ic_launcher.webp", r"FloatCalc\Resource\PlayStore등록자료\en", "*.png"),
    "floatcrypto":   (r"FloatCrypto\Resource\icon_512.png", r"FloatCrypto\Resource\PlayStore등록자료\en", "*.png"),
    # 다른 Windows 판과 같은 배치(docs\store-screenshots\en).
    "floatcryptowin": (r"FloatCryptoWin\src\FloatCryptoPlus\Assets\app.ico", r"FloatCryptoWin\docs\store-screenshots\en", "store-en-*.png"),
    "floatnote":     (r"FloatNote\Resource\icon_512.png", r"FloatNote\Resource\PlayStore등록자료\en", "*.png"),
    # 스크린샷이 언어별 폴더로 갈라지면서 docs\store-screenshots\en 으로 옮겨 갔다(ClipboardWin 과 같은 배치).
    "floatnotewin":  (r"FloatNoteWin\src\FloatNotePlus\Assets\app.ico", r"FloatNoteWin\docs\store-screenshots\en", "store-en-*.png"),
    "floattimer":    (r"FloatTimer\FloatTimer\app\src\main\res\mipmap-xxhdpi\ic_launcher.webp", r"FloatTimer\Resource\PlayStore등록자료\en", "*.png"),
    # 스크린샷이 언어별 폴더로 갈라지면서 docs\store-screenshots\en 으로 옮겨 갔다(다른 Windows 판과 같은 배치).
    "floattimerwin": (r"FloatTimerWin\src\FloatTimerPlus\Assets\app.ico", r"FloatTimerWin\docs\store-screenshots\en", "store-en-*.png"),
    "photocleaner":  (r"PhotoCleaner\Resource\icon_512.png", r"PhotoCleaner\Resource\PlayStore등록자료\en", "*.png"),
    # 다른 Windows 판과 같은 배치(docs\store-screenshots\en).
    "photocleanerwin": (r"PhotoCleanerWin\src\PhotoCleanerPlus\Assets\app.ico", r"PhotoCleanerWin\docs\store-screenshots\en", "store-en-*.png"),
    "readfocus":     (r"ReadFocus\Resource\icon_512.png", r"ReadFocus\Resource\PlayStore등록자료\en", "*.png"),
    # 스크린샷이 언어별 폴더로 갈라졌다(en/ko/…). 영어만 쓴다.
    "readfocuswin":  (r"ReadFocusWin\src\ReadFocusPlus\Assets\app.ico", r"ReadFocusWin\docs\store-screenshots\en", "store-en-*.png"),
    "volumebooster": (r"VolumeBooster\Resource\icon_512.png", r"VolumeBooster\Resource\PlayStore등록자료\en", "*.png"),
    # 태블릿 4장(tablet_*)이 같은 폴더에 있어 폰 6장만 고른다.
    "rotate":        (r"Rotate\Resource\icon_512.png", r"Rotate\Resource\PlayStore등록자료\en", "screenshot_*.png"),
    # CallerNote+ (2026-10-08 등록 준비). 아이콘·스토어 스크린샷은 아직 없다 — Resource\icon_512.png 와
    # PlayStore등록자료\en 을 만든 뒤 `python scripts/build_assets.py callernote` 로 돌린다.
    "callernote":    (r"CallerNote\Resource\icon_512.png", r"CallerNote\Resource\PlayStore등록자료\en", "screenshot_*.png"),
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
    # 스크린샷 — 언어별(2026-10-01). 영어는 예전 경로 images/shots/<slug>-N.jpg 그대로,
    # 나머지 20개 언어는 images/shots/<lang>/<slug>-N.jpg. 소스 폴더는 en 자리를 그 언어로 바꾼 곳이다.
    # 태블릿 스크린샷(tablet_*)은 같은 폴더에 있어도 뺀다 — 폰 줄에 섞이면 비율이 깨진다
    # (FloatTimer 6번째 칸에 태블릿이 섞여 있던 것을 이때 고쳤다).
    n = 0
    MAX_SHOTS = 8  # Play Store 폰 스크린샷 상한과 동일. 소스에 있는 만큼 전부 복사.
    if shotdir:
        for lang in LANGS:
            src_lang = WIN_LANG.get(lang, lang) if "store-screenshots" in shotdir else lang
            d = shotdir[:-2] + src_lang if shotdir.endswith(os.sep + "en") else shotdir
            p = pat.replace("-en-", f"-{src_lang}-").replace("_en", f"_{src_lang}")
            files = sorted(f for f in glob.glob(os.path.join(ROOT, d, p))
                           if not os.path.basename(f).startswith("tablet"))[:MAX_SHOTS]
            if not files:
                print(f"  ! {slug} {lang}: 스크린샷 없음 — 영어로 대체됨")
                continue
            out_dir = SHOT_DIR if lang == "en" else os.path.join(SHOT_DIR, lang)
            os.makedirs(out_dir, exist_ok=True)
            for i, f in enumerate(files):
                make_shot(f, os.path.join(out_dir, f"{slug}-{i+1}.jpg"))
            # 소스가 줄었으면 남은 옛 번호를 지운다(PhotoCleaner Windows 4번째가 이렇게 남아 있었다).
            for old in glob.glob(os.path.join(out_dir, f"{slug}-*.jpg")):
                k = os.path.basename(old)[len(slug) + 1:-4]
                if k.isdigit() and int(k) > len(files):
                    os.remove(old)
            if lang == "en":
                n = len(files)
    report[slug] = (icon_ok, n)

for slug, (ic, n) in report.items():
    print(f"{slug:14} icon:{ic:9} shots:{n}")
print("DONE")
