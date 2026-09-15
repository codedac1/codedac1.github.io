# -*- coding: utf-8 -*-
"""소셜 공유용 OG 이미지(1200x630) 생성.

브랜드 배너(16:9)의 가운데를 OG 비율(1.905:1)로 잘라 줄인다. 배너는 로고·태그라인·앱 아이콘이
가운데 모여 있어 위아래 띠만 조금 잘려 나간다. 배너가 바뀌면 이 스크립트만 다시 돌리면 된다.
"""
from pathlib import Path

from PIL import Image

SRC = Path(r"D:\CodeDAC\Data\CodeDAC 배경2_4096.png")
OUT = Path(__file__).resolve().parent.parent / "images" / "og-image.png"

W, H = 1200, 630

src = Image.open(SRC).convert("RGB")
sw, sh = src.size
crop_h = round(sw * H / W)
top = (sh - crop_h) // 2
img = src.crop((0, top, sw, top + crop_h)).resize((W, H), Image.LANCZOS)

img.save(OUT, "PNG", optimize=True)
print("og-image.png 생성 완료:", img.size)
