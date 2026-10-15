# -*- coding: utf-8 -*-
"""개인정보처리방침 9항에 웹사이트 입력 폼 안내 추가 (2026-10-15).

사실 근거 — Data/site-contact/main.py:
  받는 것: 이메일 주소, 입력한 내용(국가 등 선택 항목 포함). IP 는 시간당 횟수 제한에 메모리로만 쓰고 저장하지 않는다.
  처리: Google Cloud Run · Firestore (asia-northeast3 = 서울), 메일함으로 전달.
  보관: Firestore TTL 로 1년 뒤 자동 삭제. 자동 답장 메일 없음. 마케팅에 쓰지 않음.
'updated' 날짜(10/8 -> 10/15)와 변경 이력 한 줄도 함께 넣는다.
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR = os.path.join(ROOT, 'i18n', 'privacy')

P = {
'en': ("If you use the contact form on our website, we receive what you enter: your email address, your message and any optional details such as your country. The form is processed on Google Cloud (Cloud Run and Firestore in Seoul, South Korea) and forwarded to our inbox. We use it only to reply to you, never for marketing, and we do not send automatic emails to the address you enter. Form entries are deleted automatically after one year; email us if you want yours deleted sooner. Your IP address is used only briefly to limit repeated submissions and is not stored.",
       "Added the contact form on our website (Section 9)."),
'ko': ("웹사이트의 문의 입력 폼을 이용하면 회사는 입력하신 내용(이메일 주소, 문의 내용, 국가 등 선택 항목)을 받습니다. 폼은 Google Cloud(대한민국 서울 리전의 Cloud Run·Firestore)에서 처리되어 회사 메일함으로 전달됩니다. 이 정보는 문의에 답하는 데에만 쓰며 마케팅에는 쓰지 않고, 입력하신 주소로 자동 메일을 보내지 않습니다. 폼 입력 내용은 1년이 지나면 자동으로 삭제되며, 그 전에 삭제를 원하시면 이메일로 알려 주세요. IP 주소는 반복 전송을 막기 위해 잠시 사용할 뿐 저장하지 않습니다.",
       "웹사이트 문의 입력 폼 안내를 추가했습니다(9항)."),
'ja': ("当社ウェブサイトのお問い合わせフォームをご利用の場合、入力された内容（メールアドレス、お問い合わせ内容、国などの任意項目）を受け取ります。フォームは Google Cloud（韓国・ソウルの Cloud Run と Firestore）で処理され、当社のメールボックスに転送されます。この情報は返信のためにのみ使用し、マーケティングには使用せず、入力されたアドレスへ自動メールを送ることもありません。フォームの入力内容は1年後に自動的に削除されます。それより前の削除をご希望の場合はメールでお知らせください。IP アドレスは連続送信を防ぐために一時的に使うだけで、保存しません。",
       "ウェブサイトのお問い合わせフォームについての説明を追加しました（9）。"),
'zh': ("如果您使用我们网站上的联系表单，我们会收到您填写的内容：电子邮件地址、留言以及国家等可选信息。表单在 Google Cloud（韩国首尔的 Cloud Run 和 Firestore）上处理，并转发到我们的邮箱。这些信息仅用于回复您，不用于营销，我们也不会向您填写的地址发送自动邮件。表单内容会在一年后自动删除；如需提前删除，请发邮件告诉我们。您的 IP 地址只会被短暂用于限制重复提交，不会被存储。",
       "新增网站联系表单的说明（第 9 条）。"),
'es': ("Si usas el formulario de contacto de nuestro sitio web, recibimos lo que escribes: tu dirección de correo, tu mensaje y los datos opcionales que añadas, como tu país. El formulario se procesa en Google Cloud (Cloud Run y Firestore en Seúl, Corea del Sur) y se reenvía a nuestro buzón. Lo usamos solo para responderte, nunca con fines de marketing, y no enviamos correos automáticos a la dirección que indicas. Los envíos del formulario se eliminan automáticamente al cabo de un año; escríbenos si quieres que borremos el tuyo antes. Tu dirección IP solo se usa brevemente para limitar envíos repetidos y no se guarda.",
       "Se añadió el formulario de contacto del sitio web (sección 9)."),
'fr': ("Si vous utilisez le formulaire de contact de notre site, nous recevons ce que vous saisissez : votre adresse e-mail, votre message et les informations facultatives comme votre pays. Le formulaire est traité sur Google Cloud (Cloud Run et Firestore à Séoul, Corée du Sud) puis transmis à notre boîte de réception. Nous l'utilisons uniquement pour vous répondre, jamais à des fins marketing, et nous n'envoyons pas d'e-mails automatiques à l'adresse saisie. Les envois du formulaire sont supprimés automatiquement au bout d'un an ; écrivez-nous si vous souhaitez une suppression plus tôt. Votre adresse IP sert seulement brièvement à limiter les envois répétés et n'est pas conservée.",
       "Ajout du formulaire de contact du site web (section 9)."),
'de': ("Wenn Sie das Kontaktformular auf unserer Website nutzen, erhalten wir Ihre Eingaben: Ihre E-Mail-Adresse, Ihre Nachricht und freiwillige Angaben wie Ihr Land. Das Formular wird auf Google Cloud (Cloud Run und Firestore in Seoul, Südkorea) verarbeitet und an unser Postfach weitergeleitet. Wir nutzen die Angaben nur, um Ihnen zu antworten, nie für Marketing, und senden keine automatischen E-Mails an die angegebene Adresse. Formulareingaben werden nach einem Jahr automatisch gelöscht; schreiben Sie uns, wenn Ihre Angaben früher gelöscht werden sollen. Ihre IP-Adresse wird nur kurz genutzt, um wiederholte Einsendungen zu begrenzen, und nicht gespeichert.",
       "Kontaktformular auf der Website ergänzt (Abschnitt 9)."),
'pt': ("Se você usar o formulário de contato do nosso site, recebemos o que você preencher: seu e-mail, sua mensagem e informações opcionais como seu país. O formulário é processado no Google Cloud (Cloud Run e Firestore em Seul, Coreia do Sul) e encaminhado para a nossa caixa de entrada. Usamos essas informações só para responder a você, nunca para marketing, e não enviamos e-mails automáticos para o endereço informado. Os envios do formulário são apagados automaticamente após um ano; escreva para nós se quiser que o seu seja apagado antes. Seu endereço IP é usado só por pouco tempo para limitar envios repetidos e não é armazenado.",
       "Incluímos o formulário de contato do site (seção 9)."),
'ru': ("Если вы пользуетесь формой обратной связи на нашем сайте, мы получаем то, что вы ввели: адрес электронной почты, сообщение и необязательные сведения, например страну. Форма обрабатывается в Google Cloud (Cloud Run и Firestore в Сеуле, Южная Корея) и пересылается в наш почтовый ящик. Мы используем эти данные только для ответа вам, не для маркетинга, и не отправляем автоматических писем на указанный адрес. Данные из формы автоматически удаляются через год; напишите нам, если хотите удалить их раньше. IP-адрес используется лишь ненадолго, чтобы ограничить повторные отправки, и не сохраняется.",
       "Добавлены сведения о форме обратной связи на сайте (раздел 9)."),
'it': ("Se usi il modulo di contatto del nostro sito, riceviamo ciò che inserisci: il tuo indirizzo email, il messaggio e i dati facoltativi come il tuo paese. Il modulo viene elaborato su Google Cloud (Cloud Run e Firestore a Seul, Corea del Sud) e inoltrato alla nostra casella di posta. Lo usiamo solo per risponderti, mai per marketing, e non inviamo email automatiche all'indirizzo indicato. I dati del modulo vengono cancellati automaticamente dopo un anno; scrivici se vuoi che i tuoi vengano cancellati prima. Il tuo indirizzo IP viene usato solo brevemente per limitare gli invii ripetuti e non viene conservato.",
       "Aggiunto il modulo di contatto del sito (sezione 9)."),
'ar': ("إذا استخدمت نموذج التواصل على موقعنا، فإننا نتلقى ما تُدخله: عنوان بريدك الإلكتروني ورسالتك وأي بيانات اختيارية مثل بلدك. تتم معالجة النموذج على Google Cloud (Cloud Run وFirestore في سيول، كوريا الجنوبية) ثم يُحوَّل إلى بريدنا. نستخدمه فقط للرد عليك، ولا نستخدمه للتسويق أبدًا، ولا نرسل رسائل تلقائية إلى العنوان الذي تُدخله. تُحذف بيانات النموذج تلقائيًا بعد سنة واحدة؛ راسلنا إن أردت حذف بياناتك قبل ذلك. يُستخدم عنوان IP الخاص بك لفترة وجيزة فقط للحد من الإرسال المتكرر ولا يُخزَّن.",
       "أضفنا معلومات عن نموذج التواصل على الموقع (القسم 9)."),
'hi': ("अगर आप हमारी वेबसाइट के संपर्क फ़ॉर्म का इस्तेमाल करते हैं, तो हमें वह जानकारी मिलती है जो आप भरते हैं: आपका ईमेल पता, आपका संदेश और देश जैसी वैकल्पिक जानकारी। फ़ॉर्म Google Cloud (सियोल, दक्षिण कोरिया में Cloud Run और Firestore) पर प्रोसेस होकर हमारे इनबॉक्स में भेजा जाता है। हम इसका इस्तेमाल सिर्फ़ आपको जवाब देने के लिए करते हैं, मार्केटिंग के लिए कभी नहीं, और आपके दिए पते पर कोई अपने-आप ईमेल नहीं भेजते। फ़ॉर्म की जानकारी एक साल बाद अपने-आप मिटा दी जाती है; अगर आप पहले मिटवाना चाहें तो हमें ईमेल करें। आपका IP पता सिर्फ़ बार-बार भेजे जाने को रोकने के लिए थोड़ी देर इस्तेमाल होता है और सहेजा नहीं जाता।",
       "वेबसाइट के संपर्क फ़ॉर्म की जानकारी जोड़ी गई (खंड 9)।"),
'id': ("Jika Anda memakai formulir kontak di situs kami, kami menerima apa yang Anda isi: alamat email, pesan, dan data opsional seperti negara Anda. Formulir diproses di Google Cloud (Cloud Run dan Firestore di Seoul, Korea Selatan) lalu diteruskan ke kotak masuk kami. Kami memakainya hanya untuk membalas Anda, tidak pernah untuk pemasaran, dan kami tidak mengirim email otomatis ke alamat yang Anda isi. Isian formulir dihapus otomatis setelah satu tahun; kirim email kepada kami jika ingin dihapus lebih awal. Alamat IP Anda hanya dipakai sebentar untuk membatasi pengiriman berulang dan tidak disimpan.",
       "Menambahkan formulir kontak di situs web (Bagian 9)."),
'th': ("หากคุณใช้แบบฟอร์มติดต่อบนเว็บไซต์ของเรา เราจะได้รับข้อมูลที่คุณกรอก ได้แก่ อีเมล ข้อความ และข้อมูลที่ไม่บังคับ เช่น ประเทศ แบบฟอร์มจะถูกประมวลผลบน Google Cloud (Cloud Run และ Firestore ที่โซล เกาหลีใต้) แล้วส่งต่อมายังกล่องจดหมายของเรา เราใช้ข้อมูลนี้เพื่อตอบกลับคุณเท่านั้น ไม่ใช้เพื่อการตลาด และไม่ส่งอีเมลอัตโนมัติไปยังที่อยู่ที่คุณกรอก ข้อมูลในแบบฟอร์มจะถูกลบอัตโนมัติหลังจากหนึ่งปี หากต้องการให้ลบก่อนนั้นโปรดส่งอีเมลถึงเรา ที่อยู่ IP ของคุณถูกใช้ชั่วคราวเพื่อจำกัดการส่งซ้ำเท่านั้นและจะไม่ถูกจัดเก็บ",
       "เพิ่มข้อมูลเกี่ยวกับแบบฟอร์มติดต่อบนเว็บไซต์ (ข้อ 9)"),
'vi': ("Nếu bạn dùng biểu mẫu liên hệ trên trang web của chúng tôi, chúng tôi nhận được những gì bạn nhập: địa chỉ email, nội dung và các thông tin tùy chọn như quốc gia. Biểu mẫu được xử lý trên Google Cloud (Cloud Run và Firestore tại Seoul, Hàn Quốc) rồi chuyển tới hộp thư của chúng tôi. Chúng tôi chỉ dùng thông tin này để trả lời bạn, không bao giờ dùng cho tiếp thị, và không gửi email tự động tới địa chỉ bạn nhập. Dữ liệu biểu mẫu tự động bị xóa sau một năm; hãy email cho chúng tôi nếu bạn muốn xóa sớm hơn. Địa chỉ IP của bạn chỉ được dùng trong thời gian ngắn để hạn chế gửi lặp lại và không được lưu.",
       "Bổ sung thông tin về biểu mẫu liên hệ trên trang web (Mục 9)."),
'tr': ("Web sitemizdeki iletişim formunu kullanırsanız girdiğiniz bilgileri alırız: e-posta adresiniz, mesajınız ve ülkeniz gibi isteğe bağlı bilgiler. Form Google Cloud'da (Güney Kore, Seul'deki Cloud Run ve Firestore) işlenir ve gelen kutumuza iletilir. Bu bilgileri yalnızca size yanıt vermek için kullanırız, asla pazarlama için kullanmayız ve girdiğiniz adrese otomatik e-posta göndermeyiz. Form kayıtları bir yıl sonra otomatik olarak silinir; daha önce silinmesini isterseniz bize e-posta gönderin. IP adresiniz yalnızca tekrarlanan gönderimleri sınırlamak için kısa süreliğine kullanılır ve saklanmaz.",
       "Web sitesindeki iletişim formu eklendi (Bölüm 9)."),
'pl': ("Jeśli korzystasz z formularza kontaktowego na naszej stronie, otrzymujemy to, co wpiszesz: adres e-mail, wiadomość i dane opcjonalne, takie jak kraj. Formularz jest przetwarzany w Google Cloud (Cloud Run i Firestore w Seulu, Korea Południowa) i przekazywany do naszej skrzynki. Używamy tych danych wyłącznie do odpowiedzi, nigdy w celach marketingowych, i nie wysyłamy automatycznych wiadomości na podany adres. Zgłoszenia z formularza są automatycznie usuwane po roku; napisz do nas, jeśli chcesz je usunąć wcześniej. Adres IP jest używany tylko na krótko, aby ograniczyć wielokrotne wysyłanie, i nie jest przechowywany.",
       "Dodano formularz kontaktowy na stronie (sekcja 9)."),
'nl': ("Als je het contactformulier op onze website gebruikt, ontvangen we wat je invult: je e-mailadres, je bericht en optionele gegevens zoals je land. Het formulier wordt verwerkt op Google Cloud (Cloud Run en Firestore in Seoul, Zuid-Korea) en doorgestuurd naar onze inbox. We gebruiken het alleen om je te antwoorden, nooit voor marketing, en we sturen geen automatische e-mails naar het opgegeven adres. Formulierinzendingen worden na een jaar automatisch verwijderd; mail ons als je wilt dat de jouwe eerder worden verwijderd. Je IP-adres wordt alleen kort gebruikt om herhaalde inzendingen te beperken en wordt niet opgeslagen.",
       "Contactformulier op de website toegevoegd (artikel 9)."),
'uk': ("Якщо ви користуєтеся формою зворотного зв'язку на нашому сайті, ми отримуємо те, що ви ввели: адресу електронної пошти, повідомлення та необов'язкові відомості, наприклад країну. Форма обробляється в Google Cloud (Cloud Run і Firestore у Сеулі, Південна Корея) і пересилається до нашої поштової скриньки. Ми використовуємо ці дані лише для відповіді вам, ніколи для маркетингу, і не надсилаємо автоматичних листів на вказану адресу. Дані з форми автоматично видаляються через рік; напишіть нам, якщо хочете видалити їх раніше. IP-адреса використовується лише недовго, щоб обмежити повторні надсилання, і не зберігається.",
       "Додано відомості про форму зворотного зв'язку на сайті (розділ 9)."),
'ms': ("Jika anda menggunakan borang hubungan di laman web kami, kami menerima apa yang anda isi: alamat e-mel, mesej dan butiran pilihan seperti negara anda. Borang diproses di Google Cloud (Cloud Run dan Firestore di Seoul, Korea Selatan) dan dimajukan ke peti masuk kami. Kami menggunakannya hanya untuk membalas anda, tidak sekali-kali untuk pemasaran, dan kami tidak menghantar e-mel automatik ke alamat yang anda isi. Isian borang dipadam secara automatik selepas setahun; e-mel kami jika anda mahu ia dipadam lebih awal. Alamat IP anda hanya digunakan seketika untuk mengehadkan penghantaran berulang dan tidak disimpan.",
       "Menambah borang hubungan di laman web (Bahagian 9)."),
'fil': ("Kung gagamitin mo ang contact form sa aming website, natatanggap namin ang inilagay mo: ang iyong email address, mensahe, at mga opsyonal na detalye gaya ng iyong bansa. Pinoproseso ang form sa Google Cloud (Cloud Run at Firestore sa Seoul, South Korea) at ipinapasa sa aming inbox. Ginagamit lang namin ito para sagutin ka, hindi kailanman para sa marketing, at hindi kami nagpapadala ng awtomatikong email sa address na inilagay mo. Awtomatikong binubura ang mga entry ng form pagkalipas ng isang taon; mag-email sa amin kung gusto mong mabura nang mas maaga. Ginagamit lang sandali ang iyong IP address para limitahan ang paulit-ulit na pagpapadala at hindi ito iniimbak.",
       "Idinagdag ang contact form sa aming website (Seksyon 9)."),
}

for code, (para, hist) in P.items():
    p = os.path.join(DIR, code + '.json')
    raw = open(p, encoding='utf-8').read(); d = json.loads(raw)
    sec = {s['id']: s for s in d['sections']}
    if 'contact form' not in sec['email']['html'] and 'site-contact' not in sec['email']['html']:
        sec['email']['html'] += f'<p>{para}</p>'
    h = sec['history']['html']
    if 'datetime="2026-10-15"' not in h:
        sec['history']['html'] = h.replace('<ul class="legal-history">',
            f'<ul class="legal-history"><li><time datetime="2026-10-15">2026-10-15</time> {hist}</li>', 1)
    new, n = re.subn(r'(?<!\d)8(?!\d)', '15', d['updated'], count=1)
    if n != 1:
        raise SystemExit(f'{code}: 날짜 치환 실패 {d["updated"]}')
    d['updated'] = new
    ind = 2 if '\n  "' in raw[:200] else 1
    open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, ensure_ascii=False, indent=ind) + ('\n' if raw.endswith('\n') else ''))
    print(code, new)
