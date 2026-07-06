# -*- coding: utf-8 -*-
"""소셜 공유용 OG 이미지(1200x630) 생성."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BRAND = (47, 107, 255)
BRAND2 = (31, 79, 208)
img = Image.new("RGB", (W, H), BRAND)
d = ImageDraw.Draw(img)
# 대각 그라데이션
for y in range(H):
    t = y / H
    c = tuple(int(BRAND[i] * (1 - t) + BRAND2[i] * t) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)

def font(sz, bold=True):
    path = r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"
    try:
        return ImageFont.truetype(path, sz)
    except Exception:
        return ImageFont.load_default()

# 로고 텍스트 CodeDAC (DAC 흰색 강조는 단색이라 전체 흰색)
brand_f = font(120)
d.text((80, 180), "CodeDAC", font=brand_f, fill=(255, 255, 255))
# 태그라인
tag_f = font(46, bold=True)
d.text((84, 330), "Code-based Development And Consulting", font=tag_f, fill=(226, 234, 255))
sub_f = font(34, bold=False)
d.text((86, 405), "Smartphone Utility Apps  ·  App / Web Dev  ·  Consulting", font=sub_f, fill=(198, 214, 255))

# 하단 강조 바
d.rectangle([80, 470, 200, 478], fill=(255, 255, 255))

img.save(r"C:\CodeDAC\codedac\images\og-image.png", "PNG")
print("og-image.png 생성 완료:", img.size)
