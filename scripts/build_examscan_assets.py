"""ExamScan 전용 페이지(/examscan.html) 이미지 — 2026-11-25.

ExamScan 저장소의 스토어 스크린샷(21개 언어, 1080x1920 PNG)에서 페이지에 쓰는 5장(1 한눈에·2 경고·4 찾기·7 기록·8 한계,
gen_site.js EXS_SHOTS 와 같은 번호)을 골라 폭 540 WebP 로 줄여 images/examscan/<lang>/<n>.webp 에 쓴다.
언어 폴더 이름이 사이트 코드와 같다(ar … zh, id). 없는 언어는 gen_site.js 가 en 으로 대신 쓴다.

    python scripts/build_examscan_assets.py
"""
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SRC = os.path.join(os.path.dirname(SITE), 'ExamScan', 'store', 'screenshots', 'PlayStore등록자료')
OUT = os.path.join(SITE, 'images', 'examscan')
SHOTS = [1, 2, 4, 7, 8]
WIDTH = 540


def main():
    if not os.path.isdir(SRC):
        sys.exit(f'스크린샷 폴더 없음: {SRC}')
    n = 0
    for lang in sorted(os.listdir(SRC)):
        d = os.path.join(SRC, lang)
        if not os.path.isdir(d):
            continue
        for i in SHOTS:
            src = os.path.join(d, f'screenshot_{i:02d}_{lang}.png')
            if not os.path.exists(src):
                print(f'  (없음) {lang} {i}')
                continue
            im = Image.open(src).convert('RGB')
            im = im.resize((WIDTH, round(im.height * WIDTH / im.width)), Image.LANCZOS)
            os.makedirs(os.path.join(OUT, lang), exist_ok=True)
            im.save(os.path.join(OUT, lang, f'{i}.webp'), 'WEBP', quality=82, method=6)
            n += 1
    print(f'ok {n}장 -> {OUT}')


if __name__ == '__main__':
    main()
