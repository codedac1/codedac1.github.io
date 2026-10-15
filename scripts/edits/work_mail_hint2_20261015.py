# -*- coding: utf-8 -*-
"""폼 도입(2026-10-15)으로 버튼이 메일 앱 대신 폼을 연다 → 주소 복사 줄 문구를 바꾼다(work.mail.hint2)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = {
 'en': "Prefer to email us directly? Copy the address.", 'ko': "메일로 직접 보내고 싶으신가요? 주소를 복사하세요.",
 'ja': "メールで直接送りたい場合は、アドレスをコピーしてください。", 'zh': "想直接发邮件？复制邮箱地址。",
 'es': "¿Prefieres escribirnos directamente? Copia la dirección.", 'fr': "Vous préférez nous écrire directement ? Copiez l'adresse.",
 'de': "Lieber direkt eine E-Mail schreiben? Adresse kopieren.", 'pt': "Prefere escrever direto? Copie o endereço.",
 'ru': "Удобнее написать напрямую? Скопируйте адрес.", 'it': "Preferisci scriverci direttamente? Copia l'indirizzo.",
 'ar': "تفضّل مراسلتنا مباشرة؟ انسخ العنوان.", 'hi': "सीधे ईमेल करना चाहते हैं? पता कॉपी करें।",
 'id': "Lebih suka email langsung? Salin alamatnya.", 'th': "อยากส่งอีเมลถึงเราโดยตรง คัดลอกที่อยู่ได้เลย",
 'vi': "Muốn gửi email trực tiếp? Sao chép địa chỉ.", 'tr': "Doğrudan e-posta göndermeyi mi tercih edersiniz? Adresi kopyalayın.",
 'pl': "Wolisz napisać bezpośrednio? Skopiuj adres.", 'nl': "Liever direct mailen? Kopieer het adres.",
 'uk': "Зручніше написати напряму? Скопіюйте адресу.", 'ms': "Lebih suka e-mel terus? Salin alamat.",
 'fil': "Mas gusto mong mag-email nang direkta? Kopyahin ang address.",
}
for code, v in H.items():
    p = os.path.join(ROOT, 'i18n', code + '.json')
    raw = open(p, encoding='utf-8').read(); d = json.loads(raw)
    d['ui']['work.mail.hint2'] = v
    ind = 2 if '\n  "' in raw[:200] else 1
    open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, ensure_ascii=False, indent=ind) + ('\n' if raw.endswith('\n') else ''))
print(len(H), 'langs')
