# -*- coding: utf-8 -*-
"""폼 도입(2026-10-15): work.lead 끝 문장 '둘 다 메일 한 통으로 시작' -> '짧은 양식 하나로 시작'."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
R = {
 'ar': ("فكلاهما يبدأ برسالة بريد إلكتروني واحدة.", "فكلاهما يبدأ بنموذج قصير واحد."),
 'de': ("Beide beginnen mit einer einzigen E-Mail.", "Beide beginnen mit einem kurzen Formular."),
 'en': ("both start with a single email.", "both start with one short form."),
 'es': ("ambos empiezan con un simple correo.", "ambos empiezan con un breve formulario."),
 'fil': ("parehong nagsisimula sa isang email.", "parehong nagsisimula sa isang maikling form."),
 'fr': ("dans les deux cas, tout commence par un simple e-mail.", "dans les deux cas, tout commence par un court formulaire."),
 'hi': ("दोनों की शुरुआत बस एक ईमेल से होती है।", "दोनों की शुरुआत बस एक छोटे फ़ॉर्म से होती है।"),
 'id': ("keduanya cukup dimulai dengan satu email.", "keduanya cukup dimulai dengan satu formulir singkat."),
 'it': ("in entrambi i casi basta un'email per iniziare.", "in entrambi i casi basta un breve modulo per iniziare."),
 'ja': ("どちらもメール一通から始まります。", "どちらも短いフォームひとつから始まります。"),
 'ko': ("둘 다 메일 한 통으로 시작합니다.", "둘 다 짧은 양식 하나로 시작합니다."),
 'ms': ("kedua-duanya bermula dengan hanya satu e-mel.", "kedua-duanya bermula dengan hanya satu borang ringkas."),
 'nl': ("allebei beginnen ze met één e-mail.", "allebei beginnen ze met één kort formulier."),
 'pl': ("obie zaczynają się od jednego maila.", "obie zaczynają się od krótkiego formularza."),
 'pt': ("os dois começam com um simples e-mail.", "os dois começam com um formulário curto."),
 'ru': ("оба начинаются с одного письма.", "оба начинаются с короткой формы."),
 'th': ("ทั้งสองทางเริ่มต้นได้ด้วยอีเมลเพียงฉบับเดียว", "ทั้งสองทางเริ่มต้นได้ด้วยแบบฟอร์มสั้น ๆ เพียงชุดเดียว"),
 'tr': ("ikisi de tek bir e-postayla başlar.", "ikisi de kısa bir formla başlar."),
 'uk': ("обидва починаються з одного листа.", "обидва починаються з короткої форми."),
 'vi': ("cả hai đều bắt đầu chỉ với một email.", "cả hai đều bắt đầu chỉ với một biểu mẫu ngắn."),
 'zh': ("两种方式都只需一封邮件就能开始。", "两种方式都只需填一张简短的表单就能开始。"),
}
for code, (old, new) in R.items():
    p = os.path.join(ROOT, 'i18n', code + '.json')
    raw = open(p, encoding='utf-8').read(); d = json.loads(raw)
    s = d['ui']['work.lead']
    if s.count(old) != 1:
        raise SystemExit(f'{code}: 원문 불일치')
    d['ui']['work.lead'] = s.replace(old, new)
    ind = 2 if '\n  "' in raw[:200] else 1
    open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, ensure_ascii=False, indent=ind) + ('\n' if raw.endswith('\n') else ''))
print('ok', len(R))
