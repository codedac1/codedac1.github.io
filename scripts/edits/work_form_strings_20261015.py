# -*- coding: utf-8 -*-
"""'함께 만들기' 입력 폼 문구 (2026-10-15). i18n/<lang>.json 의 ui 에 form.* 키를 넣는다.

폼 상단 조건 줄(form.p.note / form.i.note)은 work_mail_templates_20261015.py 의 메일 서식 첫 줄과
같은 문장을 괄호만 빼고 쓴다 — 메일·폼 어느 쪽으로 와도 같은 조건을 읽게 한다.
예산 구간 숫자는 서버(Data/site-contact/main.py LABELS)와 같아야 한다.
"""
import importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location('mt', os.path.join(HERE, 'work_mail_templates_20261015.py'))
mt = importlib.util.module_from_spec(spec); spec.loader.exec_module(mt)

K = ['what', 'audience', 'aud.me', 'aud.business', 'aud.public', 'features', 'platforms', 'web', 'budget', 'pick',
     'b1', 'b2', 'b3', 'unsure', 'timeline', 'refs', 'problem', 'app', 'today', 'devices', 'beta', 'country',
     'email', 'email.hint', 'req', 'consent', 'privacy', 'send', 'sending', 'sent', 'err', 'err.email',
     'err.required', 'err.rate', 'mail', 'close']

F = {
'en': ["What do you want to build?", "Who is it for?", "Yourself", "Your business or clients", "The general public",
       "Top 3 features for the first version", "Platform", "Web", "Budget", "Select",
       "Under $3,000", "$3,000–10,000", "Over $10,000", "Not sure yet", "When do you need it?",
       "Reference apps or existing materials (designs, data, code)",
       "What is inconvenient, and when does it happen?", "What would the app do?", "How do you handle it today?",
       "Which device would you use it on?", "I'd like to try an early version", "Country",
       "Your email", "We'll reply to this address.", "* Required",
       "I agree that CodeDAC uses this information only to reply to my request.", "Privacy Policy",
       "Send", "Sending…", "Thanks — it's sent. We'll reply to your email.",
       "Couldn't send it. Please try again, or write to us at", "Please check your email address.",
       "Please fill in the required fields and tick the agreement.",
       "Too many messages for now. Please try again later, or write to us at", "Prefer your mail app?", "Close"],
'ko': ["무엇을 만들고 싶으신가요?", "누가 쓰나요?", "본인", "회사·고객", "일반 사용자",
       "첫 버전에 꼭 필요한 기능 3가지", "플랫폼", "웹", "예산", "선택",
       "$3,000 미만", "$3,000~10,000", "$10,000 이상", "아직 모름", "희망 일정",
       "참고할 앱이나 이미 있는 자료 (디자인·데이터·코드)",
       "어떤 점이 불편한가요? 언제 겪나요?", "어떤 앱이면 좋겠나요?", "지금은 어떻게 해결하고 계신가요?",
       "어떤 기기에서 쓰시나요?", "시제품이 나오면 먼저 써 보고 싶어요", "국가",
       "이메일", "이 주소로 답장을 드립니다.", "* 필수",
       "CodeDAC가 이 정보를 문의에 답하는 데에만 쓰는 것에 동의합니다.", "개인정보처리방침",
       "보내기", "보내는 중…", "보냈습니다. 이메일로 답장을 드리겠습니다.",
       "보내지 못했습니다. 다시 시도하시거나 이 주소로 메일을 보내 주세요:", "이메일 주소를 확인해 주세요.",
       "필수 항목을 채우고 동의에 체크해 주세요.",
       "잠시 후 다시 시도하시거나 이 주소로 메일을 보내 주세요:", "메일 앱으로 보내고 싶으신가요?", "닫기"],
'ja': ["何を作りたいですか？", "誰が使いますか？", "ご自身", "会社・お客様", "一般ユーザー",
       "最初のバージョンに必要な機能を3つ", "プラットフォーム", "Web", "予算", "選択",
       "$3,000未満", "$3,000〜10,000", "$10,000以上", "未定", "希望スケジュール",
       "参考アプリや既存の資料（デザイン・データ・コード）",
       "何が不便ですか？どんなときに困りますか？", "どんなアプリならいいですか？", "今はどうやって対処していますか？",
       "使う端末", "試作版ができたら試してみたい", "国",
       "メールアドレス", "このアドレスに返信します。", "* 必須",
       "CodeDAC がこの情報をお問い合わせへの返信にのみ使うことに同意します。", "プライバシーポリシー",
       "送信", "送信中…", "送信しました。メールで返信します。",
       "送信できませんでした。もう一度お試しいただくか、こちらへメールしてください：", "メールアドレスをご確認ください。",
       "必須項目を入力し、同意にチェックしてください。",
       "しばらくしてからお試しいただくか、こちらへメールしてください：", "メールアプリで送りたい場合", "閉じる"],
'zh': ["您想做什么？", "给谁用？", "自己", "公司或客户", "普通用户",
       "第一版最需要的 3 个功能", "平台", "网页", "预算", "请选择",
       "$3,000 以下", "$3,000–10,000", "$10,000 以上", "还不确定", "期望时间",
       "参考应用或现有资料（设计、数据、代码）",
       "哪里不方便？什么时候会遇到？", "希望应用做什么？", "现在是怎么解决的？",
       "在哪种设备上用？", "做出试用版后我想先试用", "国家",
       "您的邮箱", "我们会回复到这个地址。", "* 必填",
       "我同意 CodeDAC 仅将这些信息用于回复我的请求。", "隐私政策",
       "发送", "正在发送…", "已发送，我们会通过邮件回复您。",
       "发送失败。请重试，或发邮件到", "请检查邮箱地址。",
       "请填写必填项并勾选同意。",
       "请稍后再试，或发邮件到", "想用邮件应用发送？", "关闭"],
'es': ["¿Qué quieres crear?", "¿Para quién es?", "Para ti", "Tu empresa o clientes", "El público en general",
       "Las 3 funciones clave de la primera versión", "Plataforma", "Web", "Presupuesto", "Elige",
       "Menos de $3,000", "$3,000–10,000", "Más de $10,000", "Aún no lo sé", "¿Para cuándo lo necesitas?",
       "Apps de referencia o materiales existentes (diseños, datos, código)",
       "¿Qué te resulta incómodo y cuándo ocurre?", "¿Qué haría la app?", "¿Cómo lo resuelves hoy?",
       "¿En qué dispositivo la usarías?", "Me gustaría probar una versión temprana", "País",
       "Tu correo", "Te responderemos a esta dirección.", "* Obligatorio",
       "Acepto que CodeDAC use esta información solo para responder a mi solicitud.", "Política de privacidad",
       "Enviar", "Enviando…", "Enviado, gracias. Te responderemos por correo.",
       "No se pudo enviar. Inténtalo de nuevo o escríbenos a", "Revisa tu dirección de correo.",
       "Completa los campos obligatorios y marca la casilla de aceptación.",
       "Inténtalo más tarde o escríbenos a", "¿Prefieres tu app de correo?", "Cerrar"],
'fr': ["Que voulez-vous créer ?", "Pour qui ?", "Vous", "Votre entreprise ou vos clients", "Le grand public",
       "Les 3 fonctions essentielles de la première version", "Plateforme", "Web", "Budget", "Choisir",
       "Moins de 3 000 $", "3 000 – 10 000 $", "Plus de 10 000 $", "Je ne sais pas encore", "Pour quand ?",
       "Applis de référence ou éléments existants (maquettes, données, code)",
       "Qu'est-ce qui vous gêne, et à quel moment ?", "Que ferait l'appli ?", "Comment faites-vous aujourd'hui ?",
       "Sur quel appareil l'utiliseriez-vous ?", "J'aimerais essayer une première version", "Pays",
       "Votre e-mail", "Nous répondrons à cette adresse.", "* Obligatoire",
       "J'accepte que CodeDAC utilise ces informations uniquement pour répondre à ma demande.", "Politique de confidentialité",
       "Envoyer", "Envoi…", "Merci, c'est envoyé. Nous vous répondrons par e-mail.",
       "Échec de l'envoi. Réessayez ou écrivez-nous à", "Vérifiez votre adresse e-mail.",
       "Remplissez les champs obligatoires et cochez la case d'accord.",
       "Réessayez plus tard ou écrivez-nous à", "Vous préférez votre messagerie ?", "Fermer"],
'de': ["Was möchten Sie bauen?", "Für wen?", "Für Sie selbst", "Ihr Unternehmen oder Ihre Kunden", "Die Allgemeinheit",
       "Die 3 wichtigsten Funktionen der ersten Version", "Plattform", "Web", "Budget", "Auswählen",
       "Unter 3.000 $", "3.000–10.000 $", "Über 10.000 $", "Noch offen", "Bis wann?",
       "Referenz-Apps oder vorhandene Unterlagen (Designs, Daten, Code)",
       "Was ist umständlich, und wann passiert es?", "Was soll die App tun?", "Wie lösen Sie es heute?",
       "Auf welchem Gerät würden Sie sie nutzen?", "Ich möchte eine frühe Version testen", "Land",
       "Ihre E-Mail", "An diese Adresse antworten wir.", "* Pflichtfeld",
       "Ich bin einverstanden, dass CodeDAC diese Angaben nur zur Beantwortung meiner Anfrage nutzt.", "Datenschutzerklärung",
       "Senden", "Wird gesendet …", "Danke, gesendet. Wir antworten per E-Mail.",
       "Senden fehlgeschlagen. Bitte erneut versuchen oder schreiben Sie an", "Bitte prüfen Sie Ihre E-Mail-Adresse.",
       "Bitte füllen Sie die Pflichtfelder aus und bestätigen Sie die Einwilligung.",
       "Bitte später erneut versuchen oder schreiben Sie an", "Lieber per Mail-App?", "Schließen"],
'pt': ["O que você quer criar?", "Para quem é?", "Para você", "Sua empresa ou clientes", "O público em geral",
       "As 3 funções principais da primeira versão", "Plataforma", "Web", "Orçamento", "Selecione",
       "Menos de US$ 3.000", "US$ 3.000–10.000", "Mais de US$ 10.000", "Ainda não sei", "Para quando você precisa?",
       "Apps de referência ou materiais existentes (designs, dados, código)",
       "O que é incômodo e quando acontece?", "O que o app faria?", "Como você resolve isso hoje?",
       "Em qual dispositivo você usaria?", "Quero testar uma versão inicial", "País",
       "Seu e-mail", "Vamos responder para este endereço.", "* Obrigatório",
       "Concordo que a CodeDAC use estas informações apenas para responder ao meu pedido.", "Política de Privacidade",
       "Enviar", "Enviando…", "Enviado, obrigado. Vamos responder por e-mail.",
       "Não foi possível enviar. Tente de novo ou escreva para", "Confira seu endereço de e-mail.",
       "Preencha os campos obrigatórios e marque a concordância.",
       "Tente mais tarde ou escreva para", "Prefere seu app de e-mail?", "Fechar"],
'ru': ["Что вы хотите создать?", "Для кого?", "Для себя", "Для компании или клиентов", "Для всех",
       "3 главные функции первой версии", "Платформа", "Веб", "Бюджет", "Выберите",
       "До $3,000", "$3,000–10,000", "Более $10,000", "Пока не знаю", "Когда нужно?",
       "Приложения-образцы или готовые материалы (дизайн, данные, код)",
       "Что неудобно и когда это происходит?", "Что должно делать приложение?", "Как вы решаете это сейчас?",
       "На каком устройстве будете пользоваться?", "Хочу попробовать раннюю версию", "Страна",
       "Ваш email", "Мы ответим на этот адрес.", "* Обязательно",
       "Я согласен(на), что CodeDAC использует эти данные только для ответа на мой запрос.", "Политика конфиденциальности",
       "Отправить", "Отправка…", "Отправлено, спасибо. Мы ответим по email.",
       "Не удалось отправить. Попробуйте ещё раз или напишите на", "Проверьте адрес email.",
       "Заполните обязательные поля и отметьте согласие.",
       "Попробуйте позже или напишите на", "Удобнее через почтовое приложение?", "Закрыть"],
'it': ["Cosa vuoi realizzare?", "Per chi è?", "Per te", "La tua azienda o i clienti", "Il pubblico",
       "Le 3 funzioni principali della prima versione", "Piattaforma", "Web", "Budget", "Seleziona",
       "Meno di $3.000", "$3.000–10.000", "Oltre $10.000", "Non so ancora", "Per quando ti serve?",
       "App di riferimento o materiali esistenti (design, dati, codice)",
       "Cosa ti risulta scomodo, e quando succede?", "Cosa farebbe l'app?", "Come lo risolvi oggi?",
       "Su quale dispositivo la useresti?", "Vorrei provare una prima versione", "Paese",
       "La tua email", "Risponderemo a questo indirizzo.", "* Obbligatorio",
       "Accetto che CodeDAC usi queste informazioni solo per rispondere alla mia richiesta.", "Informativa sulla privacy",
       "Invia", "Invio…", "Inviato, grazie. Ti risponderemo via email.",
       "Invio non riuscito. Riprova o scrivici a", "Controlla il tuo indirizzo email.",
       "Compila i campi obbligatori e spunta il consenso.",
       "Riprova più tardi o scrivici a", "Preferisci la tua app di posta?", "Chiudi"],
'ar': ["ماذا تريد أن تبني؟", "لمن هو؟", "لنفسك", "لشركتك أو عملائك", "للجمهور",
       "أهم 3 ميزات في الإصدار الأول", "المنصة", "الويب", "الميزانية", "اختر",
       "أقل من 3,000 دولار", "3,000–10,000 دولار", "أكثر من 10,000 دولار", "لا أعرف بعد", "متى تحتاجه؟",
       "تطبيقات مرجعية أو مواد موجودة (تصاميم، بيانات، شيفرة)",
       "ما الذي يزعجك، ومتى يحدث؟", "ماذا سيفعل التطبيق؟", "كيف تتعامل معه اليوم؟",
       "على أي جهاز ستستخدمه؟", "أود تجربة نسخة مبكرة", "البلد",
       "بريدك الإلكتروني", "سنرد على هذا العنوان.", "* مطلوب",
       "أوافق على أن تستخدم CodeDAC هذه المعلومات فقط للرد على طلبي.", "سياسة الخصوصية",
       "إرسال", "جارٍ الإرسال…", "تم الإرسال، شكرًا. سنرد عليك بالبريد الإلكتروني.",
       "تعذّر الإرسال. حاول مرة أخرى أو راسلنا على", "تحقق من عنوان بريدك الإلكتروني.",
       "املأ الحقول المطلوبة وحدد خانة الموافقة.",
       "حاول لاحقًا أو راسلنا على", "تفضّل تطبيق البريد؟", "إغلاق"],
'hi': ["आप क्या बनाना चाहते हैं?", "यह किसके लिए है?", "आपके लिए", "आपके बिज़नेस या ग्राहकों के लिए", "आम लोगों के लिए",
       "पहले वर्शन के 3 सबसे ज़रूरी फ़ीचर", "प्लेटफ़ॉर्म", "वेब", "बजट", "चुनें",
       "$3,000 से कम", "$3,000–10,000", "$10,000 से ज़्यादा", "अभी तय नहीं", "कब तक चाहिए?",
       "संदर्भ ऐप या मौजूदा सामग्री (डिज़ाइन, डेटा, कोड)",
       "क्या असुविधाजनक है, और यह कब होता है?", "ऐप क्या करेगा?", "आज आप इसे कैसे संभालते हैं?",
       "आप इसे किस डिवाइस पर इस्तेमाल करेंगे?", "मैं शुरुआती वर्शन आज़माना चाहूँगा/चाहूँगी", "देश",
       "आपका ईमेल", "हम इसी पते पर जवाब देंगे।", "* ज़रूरी",
       "मैं सहमत हूँ कि CodeDAC इस जानकारी का इस्तेमाल सिर्फ़ मेरे अनुरोध का जवाब देने के लिए करेगा।", "निजता नीति",
       "भेजें", "भेजा जा रहा है…", "भेज दिया गया, धन्यवाद। हम ईमेल से जवाब देंगे।",
       "भेजा नहीं जा सका। फिर कोशिश करें या हमें यहाँ लिखें:", "कृपया अपना ईमेल पता जाँचें।",
       "ज़रूरी फ़ील्ड भरें और सहमति पर टिक करें।",
       "थोड़ी देर बाद कोशिश करें या हमें यहाँ लिखें:", "ईमेल ऐप से भेजना चाहते हैं?", "बंद करें"],
'id': ["Apa yang ingin Anda buat?", "Untuk siapa?", "Anda sendiri", "Bisnis atau klien Anda", "Publik",
       "3 fitur terpenting untuk versi pertama", "Platform", "Web", "Anggaran", "Pilih",
       "Di bawah $3.000", "$3.000–10.000", "Di atas $10.000", "Belum tahu", "Kapan dibutuhkan?",
       "Aplikasi acuan atau bahan yang sudah ada (desain, data, kode)",
       "Apa yang merepotkan, dan kapan terjadinya?", "Apa yang akan dilakukan aplikasinya?", "Bagaimana Anda mengatasinya sekarang?",
       "Di perangkat apa Anda akan memakainya?", "Saya ingin mencoba versi awal", "Negara",
       "Email Anda", "Kami akan membalas ke alamat ini.", "* Wajib",
       "Saya setuju CodeDAC memakai informasi ini hanya untuk membalas permintaan saya.", "Kebijakan Privasi",
       "Kirim", "Mengirim…", "Terkirim, terima kasih. Kami akan membalas lewat email.",
       "Gagal mengirim. Coba lagi atau kirim email ke", "Periksa alamat email Anda.",
       "Isi kolom wajib dan centang persetujuan.",
       "Coba lagi nanti atau kirim email ke", "Lebih suka lewat aplikasi email?", "Tutup"],
'th': ["อยากสร้างอะไร", "ใครเป็นผู้ใช้", "ตัวคุณเอง", "ธุรกิจหรือลูกค้าของคุณ", "คนทั่วไป",
       "ฟีเจอร์สำคัญ 3 อย่างในเวอร์ชันแรก", "แพลตฟอร์ม", "เว็บ", "งบประมาณ", "เลือก",
       "ต่ำกว่า $3,000", "$3,000–10,000", "มากกว่า $10,000", "ยังไม่แน่ใจ", "ต้องการเมื่อไร",
       "แอปอ้างอิงหรือเอกสารที่มีอยู่ (ดีไซน์ ข้อมูล โค้ด)",
       "อะไรที่ไม่สะดวก และเกิดขึ้นเมื่อไร", "อยากให้แอปทำอะไร", "ตอนนี้คุณแก้ปัญหานี้อย่างไร",
       "จะใช้บนอุปกรณ์ไหน", "อยากลองเวอร์ชันแรกก่อน", "ประเทศ",
       "อีเมลของคุณ", "เราจะตอบกลับที่อีเมลนี้", "* จำเป็น",
       "ฉันยินยอมให้ CodeDAC ใช้ข้อมูลนี้เพื่อตอบคำขอของฉันเท่านั้น", "นโยบายความเป็นส่วนตัว",
       "ส่ง", "กำลังส่ง…", "ส่งแล้ว ขอบคุณ เราจะตอบกลับทางอีเมล",
       "ส่งไม่สำเร็จ ลองอีกครั้งหรือส่งอีเมลมาที่", "โปรดตรวจสอบที่อยู่อีเมล",
       "โปรดกรอกช่องที่จำเป็นและทำเครื่องหมายยินยอม",
       "โปรดลองใหม่ภายหลังหรือส่งอีเมลมาที่", "อยากส่งผ่านแอปอีเมลไหม", "ปิด"],
'vi': ["Bạn muốn làm gì?", "Dành cho ai?", "Bản thân bạn", "Doanh nghiệp hoặc khách hàng của bạn", "Công chúng",
       "3 tính năng quan trọng nhất của phiên bản đầu", "Nền tảng", "Web", "Ngân sách", "Chọn",
       "Dưới $3.000", "$3.000–10.000", "Trên $10.000", "Chưa rõ", "Khi nào cần?",
       "Ứng dụng tham khảo hoặc tài liệu sẵn có (thiết kế, dữ liệu, mã nguồn)",
       "Điều gì bất tiện, và xảy ra khi nào?", "Ứng dụng sẽ làm gì?", "Hiện bạn xử lý thế nào?",
       "Bạn sẽ dùng trên thiết bị nào?", "Tôi muốn dùng thử bản đầu tiên", "Quốc gia",
       "Email của bạn", "Chúng tôi sẽ trả lời qua địa chỉ này.", "* Bắt buộc",
       "Tôi đồng ý để CodeDAC chỉ dùng thông tin này để trả lời yêu cầu của tôi.", "Chính sách quyền riêng tư",
       "Gửi", "Đang gửi…", "Đã gửi, cảm ơn bạn. Chúng tôi sẽ trả lời qua email.",
       "Không gửi được. Hãy thử lại hoặc gửi email tới", "Vui lòng kiểm tra địa chỉ email.",
       "Vui lòng điền các mục bắt buộc và đánh dấu đồng ý.",
       "Hãy thử lại sau hoặc gửi email tới", "Muốn gửi bằng ứng dụng email?", "Đóng"],
'tr': ["Ne yapmak istiyorsunuz?", "Kimin için?", "Kendiniz", "Şirketiniz veya müşterileriniz", "Herkes",
       "İlk sürüm için en önemli 3 özellik", "Platform", "Web", "Bütçe", "Seçin",
       "$3.000 altı", "$3.000–10.000", "$10.000 üstü", "Henüz bilmiyorum", "Ne zamana lazım?",
       "Örnek uygulamalar veya mevcut materyaller (tasarım, veri, kod)",
       "Ne zahmetli ve ne zaman oluyor?", "Uygulama ne yapmalı?", "Bugün bunu nasıl hallediyorsunuz?",
       "Hangi cihazda kullanacaksınız?", "İlk sürümü denemek isterim", "Ülke",
       "E-postanız", "Bu adrese yanıt vereceğiz.", "* Zorunlu",
       "CodeDAC'in bu bilgileri yalnızca talebime yanıt vermek için kullanmasını kabul ediyorum.", "Gizlilik Politikası",
       "Gönder", "Gönderiliyor…", "Gönderildi, teşekkürler. E-postayla yanıt vereceğiz.",
       "Gönderilemedi. Tekrar deneyin veya şu adrese yazın:", "Lütfen e-posta adresinizi kontrol edin.",
       "Lütfen zorunlu alanları doldurun ve onay kutusunu işaretleyin.",
       "Lütfen daha sonra deneyin veya şu adrese yazın:", "E-posta uygulamanızla mı göndermek istersiniz?", "Kapat"],
'pl': ["Co chcesz zbudować?", "Dla kogo?", "Dla siebie", "Dla firmy lub klientów", "Dla wszystkich",
       "3 najważniejsze funkcje pierwszej wersji", "Platforma", "Web", "Budżet", "Wybierz",
       "Poniżej 3000 $", "3000–10 000 $", "Powyżej 10 000 $", "Jeszcze nie wiem", "Na kiedy?",
       "Aplikacje wzorcowe lub istniejące materiały (projekty, dane, kod)",
       "Co jest uciążliwe i kiedy się to zdarza?", "Co miałaby robić aplikacja?", "Jak radzisz sobie z tym dziś?",
       "Na jakim urządzeniu będziesz jej używać?", "Chcę wypróbować wczesną wersję", "Kraj",
       "Twój e-mail", "Odpowiemy na ten adres.", "* Wymagane",
       "Zgadzam się, aby CodeDAC używało tych informacji wyłącznie do odpowiedzi na moje zgłoszenie.", "Polityka prywatności",
       "Wyślij", "Wysyłanie…", "Wysłano, dziękujemy. Odpowiemy e-mailem.",
       "Nie udało się wysłać. Spróbuj ponownie lub napisz na", "Sprawdź adres e-mail.",
       "Wypełnij wymagane pola i zaznacz zgodę.",
       "Spróbuj później lub napisz na", "Wolisz aplikację pocztową?", "Zamknij"],
'nl': ["Wat wil je laten bouwen?", "Voor wie?", "Voor jezelf", "Je bedrijf of klanten", "Iedereen",
       "De 3 belangrijkste functies van de eerste versie", "Platform", "Web", "Budget", "Kies",
       "Minder dan $3.000", "$3.000–10.000", "Meer dan $10.000", "Weet ik nog niet", "Wanneer heb je het nodig?",
       "Voorbeeld-apps of bestaand materiaal (ontwerpen, data, code)",
       "Wat is onhandig, en wanneer gebeurt het?", "Wat zou de app moeten doen?", "Hoe los je het nu op?",
       "Op welk apparaat zou je hem gebruiken?", "Ik wil graag een vroege versie proberen", "Land",
       "Je e-mailadres", "We antwoorden naar dit adres.", "* Verplicht",
       "Ik ga ermee akkoord dat CodeDAC deze gegevens alleen gebruikt om op mijn verzoek te reageren.", "Privacybeleid",
       "Versturen", "Bezig met versturen…", "Verstuurd, bedankt. We antwoorden per e-mail.",
       "Versturen mislukt. Probeer het opnieuw of mail naar", "Controleer je e-mailadres.",
       "Vul de verplichte velden in en vink de toestemming aan.",
       "Probeer het later opnieuw of mail naar", "Liever via je mailapp?", "Sluiten"],
'uk': ["Що ви хочете створити?", "Для кого?", "Для себе", "Для компанії чи клієнтів", "Для всіх",
       "3 головні функції першої версії", "Платформа", "Веб", "Бюджет", "Оберіть",
       "До $3,000", "$3,000–10,000", "Понад $10,000", "Ще не знаю", "Коли потрібно?",
       "Застосунки-зразки або наявні матеріали (дизайн, дані, код)",
       "Що незручно і коли це трапляється?", "Що має робити застосунок?", "Як ви розв'язуєте це зараз?",
       "На якому пристрої користуватиметеся?", "Хочу спробувати ранню версію", "Країна",
       "Ваш email", "Ми відповімо на цю адресу.", "* Обов'язково",
       "Я погоджуюся, що CodeDAC використовує ці дані лише для відповіді на мій запит.", "Політика конфіденційності",
       "Надіслати", "Надсилання…", "Надіслано, дякуємо. Ми відповімо на email.",
       "Не вдалося надіслати. Спробуйте ще раз або напишіть на", "Перевірте адресу email.",
       "Заповніть обов'язкові поля та позначте згоду.",
       "Спробуйте пізніше або напишіть на", "Зручніше через поштовий застосунок?", "Закрити"],
'ms': ["Apa yang anda mahu bina?", "Untuk siapa?", "Diri sendiri", "Perniagaan atau pelanggan anda", "Orang ramai",
       "3 ciri terpenting untuk versi pertama", "Platform", "Web", "Bajet", "Pilih",
       "Bawah $3,000", "$3,000–10,000", "Atas $10,000", "Belum pasti", "Bila diperlukan?",
       "Aplikasi rujukan atau bahan sedia ada (reka bentuk, data, kod)",
       "Apa yang menyusahkan, dan bila ia berlaku?", "Apa yang aplikasi itu akan buat?", "Bagaimana anda mengatasinya sekarang?",
       "Pada peranti apa anda akan menggunakannya?", "Saya mahu mencuba versi awal", "Negara",
       "E-mel anda", "Kami akan membalas ke alamat ini.", "* Wajib",
       "Saya bersetuju CodeDAC menggunakan maklumat ini hanya untuk membalas permintaan saya.", "Dasar Privasi",
       "Hantar", "Menghantar…", "Dihantar, terima kasih. Kami akan membalas melalui e-mel.",
       "Gagal dihantar. Cuba lagi atau e-mel kami di", "Sila semak alamat e-mel anda.",
       "Sila isi ruangan wajib dan tandakan persetujuan.",
       "Cuba sebentar lagi atau e-mel kami di", "Lebih suka aplikasi e-mel?", "Tutup"],
'fil': ["Ano ang gusto mong ipagawa?", "Para kanino?", "Para sa sarili mo", "Negosyo o kliyente mo", "Publiko",
       "Ang 3 pinakamahalagang feature sa unang bersyon", "Platform", "Web", "Budget", "Pumili",
       "Mas mababa sa $3,000", "$3,000–10,000", "Higit sa $10,000", "Hindi pa sigurado", "Kailan mo kailangan?",
       "Mga reference app o kasalukuyang materyales (disenyo, data, code)",
       "Ano ang abala, at kailan ito nangyayari?", "Ano ang gagawin ng app?", "Paano mo ito hinaharap ngayon?",
       "Saang device mo ito gagamitin?", "Gusto kong subukan ang maagang bersyon", "Bansa",
       "Iyong email", "Sa address na ito kami sasagot.", "* Kailangan",
       "Pumapayag akong gamitin ng CodeDAC ang impormasyong ito para lang sagutin ang aking kahilingan.", "Patakaran sa Privacy",
       "Ipadala", "Ipinapadala…", "Naipadala na, salamat. Sasagot kami sa email.",
       "Hindi naipadala. Subukan ulit o mag-email sa", "Pakisuri ang iyong email address.",
       "Punan ang mga kailangang field at i-check ang pagpayag.",
       "Subukan ulit mamaya o mag-email sa", "Mas gusto mo ba ang email app?", "Isara"],
}


import re

# 예산 4구간 (사용자 결정 10/15): <$1,000 / $1,000–3,000 / $3,000–10,000 / >$10,000 / 모름.
# 금액 기준은 모든 나라 같게(우리 비용은 고객 나라와 무관). 위 F 의 b1(“$3,000 미만”)·b2(“3,000–10,000”) 표기에서
# 각 언어의 숫자 서식을 그대로 살려 b0(<1,000)·새 b1(1,000–3,000)을 만든다.
# 한국어·일본어만 원·엔 대략값을 덧붙인다(언어=나라가 거의 1:1). 환율 2026-10-14 1달러≈1,337원·158엔, 반올림.
LOCAL = {
    'ko': ["$1,000 미만 (약 130만 원 미만)", "$1,000~3,000 (약 130만~400만 원)",
           "$3,000~10,000 (약 400만~1,300만 원)", "$10,000 이상 (약 1,300만 원 이상)"],
    'ja': ["$1,000未満（約16万円未満）", "$1,000〜3,000（約16万〜48万円）",
           "$3,000〜10,000（約48万〜160万円）", "$10,000以上（約160万円以上）"],
}
FIX = {'pl': ("Poniżej 1000 $", "1000–3000 $")}


def budget_4tier(code, ui):
    if code in LOCAL:
        ui['form.b0'], ui['form.b1'], ui['form.b2'], ui['form.b3'] = LOCAL[code]
        return
    lt3, mid = ui['form.b1'], ui['form.b2']           # F 의 원래 값: “$3,000 미만”, “$3,000–10,000”
    b0 = lt3.replace('3', '1', 1)
    b1 = re.sub(r'10([ .,]?)000', lambda m: '3' + m.group(1) + '000', mid.replace('3', '1', 1), count=1)
    if code in FIX:
        b0, b1 = FIX[code]
    ui['form.b0'], ui['form.b1'] = b0, b1                # b2(3,000–10,000)·b3(>10,000)는 그대로


def strip_paren(s):
    s = s.strip()
    for a, b in (('(', ')'), ('（', '）')):
        if s.startswith(a) and s.endswith(b):
            return s[1:-1].strip()
    return s


def main():
    I18N = os.path.join(ROOT, 'i18n')
    langs = sorted(f[:-5] for f in os.listdir(I18N) if f.endswith('.json'))
    for code in langs:
        vals = F[code]
        if len(vals) != len(K):
            sys.exit(f'{code}: 값 {len(vals)}개, 키 {len(K)}개')
        path = os.path.join(I18N, code + '.json')
        raw = open(path, encoding='utf-8').read()
        data = json.loads(raw)
        ui = data['ui']
        for k, v in zip(K, vals):
            ui['form.' + k] = v
        budget_4tier(code, ui)
        t = mt.T[code]
        sub = dict(cta=ui['ideas.cta'], a=ui['work.a.title'], b=ui['work.b.title'], B1=mt.B1, B2=mt.B2)
        ui['form.p.note'] = strip_paren(t['pn'].format(**sub))
        ui['form.i.note'] = strip_paren(t['inote'].format(**sub))
        indent = 2 if '\n  "' in raw[:200] else 1
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=indent) + ('\n' if raw.endswith('\n') else ''))
        print(code, 'ok', end='  ')


if __name__ == '__main__':
    main()
