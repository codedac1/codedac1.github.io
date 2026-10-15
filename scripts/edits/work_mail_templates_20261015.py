# -*- coding: utf-8 -*-
"""'함께 만들기' 메일 서식 개편 (2026-10-15).

실제 문의에서 드러난 문제:
- 유료(프로젝트 의뢰)와 무료(아이디어 제보)를 헷갈린다 — 조건이 카드에만 있고 메일 본문엔 없었다.
- '일정과 예산'을 한 칸에 묶어 두니 금액 없이 온다 → 예산 구간을 고르게 한다.
- 범위를 가늠할 정보(누가 쓰는지, 첫 버전 핵심 기능 3개)와 국가(시간대·통화·출시 지역)가 없었다.
- 아이디어 제보자에게 시제품을 써 볼지 묻지 않았다.
질문은 각 5개 이내. 본문 첫 줄에 조건을 한 줄로 넣어, 잘못 고른 사람이 메일을 쓰다가 알아채게 한다.
예산 구간($3,000 / $10,000)은 사용자 결정으로 바꿀 수 있다 — 숫자만 고치고 다시 돌리면 된다.

{a}/{b} = 카드 제목(work.a.title / work.b.title), {cta} = 아이디어 버튼(ideas.cta) — 각 언어 파일의 기존 값.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
I18N = os.path.join(ROOT, 'i18n')
B1, B3, B2 = '$1,000', '$3,000', '$10,000'  # 10/15 4구간: <1k / 1~3k / 3~10k / >10k

T = {
'en': dict(
 pn="(Paid development: the app will be yours. Just want the app to exist without paying? Use “{cta}”.)",
 p=["What do you want to build? Who is it for (you / your business / the public)?",
    "Top 3 features for the first version",
    "Platform (Android / iOS / Windows / Web)",
    "Budget: under {B1} / {B1}–{B3} / {B3}–{B2} / over {B2} / not sure (any currency is fine)",
    "Timeline, your country (time zone), reference apps or existing materials"],
 inote="(Free: if we build it, it ships as a CodeDAC app anyone can use. We decide whether and when to build it.)",
 i=["What is inconvenient, and when does it happen?",
    "What would the app do? (one sentence is enough)",
    "How do you handle it today?",
    "Which device (Android / Windows), and which country do you live in?",
    "Would you like to try an early version? Yes / No"],
 pick="Not sure which to choose? If you want to own the app and plan to pay for it, choose “{a}”. If you just want such an app to exist, choose “{b}” — it's free."),
'ko': dict(
 pn="(유료 개발입니다. 결과물은 의뢰하신 분의 것입니다. 비용 없이 이런 앱이 생기기만 바라신다면 '{cta}'를 이용해 주세요.)",
 p=["무엇을 만들고 싶으신가요? 누가 쓰나요? (본인 / 회사·고객 / 일반 사용자)",
    "첫 버전에 꼭 필요한 기능 3가지",
    "플랫폼 (Android / iOS / Windows / 웹)",
    "예산: {B1} 미만 / {B1}~{B3} / {B3}~{B2} / {B2} 이상 / 아직 모름 (원화로 적어도 됩니다)",
    "희망 일정, 국가(시간대), 참고할 앱이나 이미 있는 자료"],
 inote="(무료입니다. 만들게 되면 누구나 쓰는 CodeDAC 앱으로 출시되며, 만들지 여부와 시기는 저희가 정합니다.)",
 i=["어떤 점이 불편한가요? 언제 겪나요?",
    "어떤 앱이면 좋겠나요? (한 문장이면 충분합니다)",
    "지금은 어떻게 해결하고 계신가요?",
    "어떤 기기에서 쓰시나요? (Android / Windows) 사는 나라는요?",
    "시제품이 나오면 먼저 써 보시겠어요? 예 / 아니오"],
 pick="어느 쪽인지 헷갈리신다면: 앱을 직접 소유하고 비용을 낼 생각이면 '{a}', 그런 앱이 있기만 하면 된다면 '{b}'(무료)를 골라 주세요."),
'ja': dict(
 pn="（有償の開発です。完成したアプリはご依頼者のものになります。費用なしで「こんなアプリがあれば」という場合は「{cta}」をご利用ください。）",
 p=["何を作りたいですか？誰が使いますか？（ご自身 / 会社・お客様 / 一般ユーザー）",
    "最初のバージョンに必要な機能を3つ",
    "プラットフォーム（Android / iOS / Windows / Web）",
    "予算：{B1}未満 / {B1}〜{B3} / {B3}〜{B2} / {B2}以上 / 未定（円での記入も可）",
    "希望スケジュール、国（タイムゾーン）、参考アプリや既存の資料"],
 inote="（無料です。開発する場合は誰でも使える CodeDAC のアプリとして公開し、作るかどうかと時期はこちらで決めます。）",
 i=["何が不便ですか？どんなときに困りますか？",
    "どんなアプリならいいですか？（一文で十分です）",
    "今はどうやって対処していますか？",
    "使う端末（Android / Windows）と、お住まいの国は？",
    "試作版ができたら試してみますか？ はい / いいえ"],
 pick="どちらか迷ったら：アプリを自分のものにして費用を払う場合は「{a}」、そういうアプリがあればいい場合は「{b}」（無料）をお選びください。"),
'zh': dict(
 pn="（这是付费开发，成品归您所有。如果只是希望有这样一款应用、不打算付费，请使用“{cta}”。）",
 p=["您想做什么？给谁用？（自己 / 公司或客户 / 普通用户）",
    "第一版最需要的 3 个功能",
    "平台（Android / iOS / Windows / 网页）",
    "预算：{B1} 以下 / {B1}–{B3} / {B3}–{B2} / {B2} 以上 / 还不确定（可用人民币填写）",
    "期望时间、所在国家（时区）、参考应用或现有资料"],
 inote="（免费。如果我们决定开发，会作为人人可用的 CodeDAC 应用发布；是否开发以及何时开发由我们决定。）",
 i=["哪里不方便？什么时候会遇到？",
    "希望应用做什么？（一句话就够）",
    "现在是怎么解决的？",
    "在哪种设备上用（Android / Windows）？住在哪个国家？",
    "做出试用版后愿意先试用吗？愿意 / 不愿意"],
 pick="不确定选哪个？想拥有应用并愿意付费，请选“{a}”；只希望有这样一款应用，请选“{b}”（免费）。"),
'es': dict(
 pn="(Desarrollo de pago: la app será tuya. ¿Solo quieres que exista una app así, sin pagar? Usa «{cta}».)",
 p=["¿Qué quieres crear? ¿Para quién es (para ti / tu empresa o clientes / el público)?",
    "Las 3 funciones clave de la primera versión",
    "Plataforma (Android / iOS / Windows / Web)",
    "Presupuesto: menos de {B1} / {B1}–{B3} / {B3}–{B2} / más de {B2} / aún no lo sé (cualquier moneda vale)",
    "Plazo, tu país (zona horaria), apps de referencia o materiales existentes"],
 inote="(Gratis: si la desarrollamos, se publica como app de CodeDAC que cualquiera puede usar. Nosotros decidimos si se hace y cuándo.)",
 i=["¿Qué te resulta incómodo y cuándo ocurre?",
    "¿Qué haría la app? (basta con una frase)",
    "¿Cómo lo resuelves hoy?",
    "¿En qué dispositivo (Android / Windows) y en qué país vives?",
    "¿Te gustaría probar una versión temprana? Sí / No"],
 pick="¿No sabes cuál elegir? Si quieres que la app sea tuya y piensas pagar, elige «{a}». Si solo quieres que exista una app así, elige «{b}»: es gratis."),
'fr': dict(
 pn="(Développement payant : l'appli vous appartiendra. Vous voulez seulement qu'une telle appli existe, sans payer ? Utilisez « {cta} ».)",
 p=["Que voulez-vous créer ? Pour qui (vous / votre entreprise ou vos clients / le grand public) ?",
    "Les 3 fonctions essentielles de la première version",
    "Plateforme (Android / iOS / Windows / Web)",
    "Budget : moins de {B1} / {B1}–{B3} / {B3}–{B2} / plus de {B2} / je ne sais pas encore (toute devise acceptée)",
    "Délai, votre pays (fuseau horaire), applis de référence ou éléments existants"],
 inote="(Gratuit : si nous la développons, elle sort comme appli CodeDAC utilisable par tous. Nous décidons si et quand la créer.)",
 i=["Qu'est-ce qui vous gêne, et à quel moment ?",
    "Que ferait l'appli ? (une phrase suffit)",
    "Comment faites-vous aujourd'hui ?",
    "Sur quel appareil (Android / Windows), et dans quel pays vivez-vous ?",
    "Voulez-vous essayer une première version ? Oui / Non"],
 pick="Vous hésitez ? Si vous voulez posséder l'appli et la financer, choisissez « {a} ». Si vous voulez simplement qu'une telle appli existe, choisissez « {b} » — c'est gratuit."),
'de': dict(
 pn="(Bezahlte Entwicklung: Die App gehört Ihnen. Sie möchten nur, dass es so eine App gibt, ohne zu bezahlen? Nutzen Sie „{cta}“.)",
 p=["Was möchten Sie bauen? Für wen (Sie selbst / Ihr Unternehmen oder Kunden / die Allgemeinheit)?",
    "Die 3 wichtigsten Funktionen der ersten Version",
    "Plattform (Android / iOS / Windows / Web)",
    "Budget: unter {B1} / {B1}–{B3} / {B3}–{B2} / über {B2} / noch offen (jede Währung möglich)",
    "Zeitrahmen, Ihr Land (Zeitzone), Referenz-Apps oder vorhandene Unterlagen"],
 inote="(Kostenlos: Wenn wir sie bauen, erscheint sie als CodeDAC-App für alle. Ob und wann wir sie bauen, entscheiden wir.)",
 i=["Was ist umständlich, und wann passiert es?",
    "Was soll die App tun? (ein Satz reicht)",
    "Wie lösen Sie es heute?",
    "Auf welchem Gerät (Android / Windows), und in welchem Land leben Sie?",
    "Möchten Sie eine frühe Version testen? Ja / Nein"],
 pick="Unsicher? Wenn Ihnen die App gehören soll und Sie dafür bezahlen möchten, wählen Sie „{a}“. Wenn es so eine App einfach geben soll, wählen Sie „{b}“ – kostenlos."),
'pt': dict(
 pn="(Desenvolvimento pago: o app será seu. Só quer que um app assim exista, sem pagar? Use “{cta}”.)",
 p=["O que você quer criar? Para quem (você / sua empresa ou clientes / o público)?",
    "As 3 funções principais da primeira versão",
    "Plataforma (Android / iOS / Windows / Web)",
    "Orçamento: menos de {B1} / {B1}–{B3} / {B3}–{B2} / mais de {B2} / ainda não sei (qualquer moeda serve)",
    "Prazo, seu país (fuso horário), apps de referência ou materiais existentes"],
 inote="(Grátis: se desenvolvermos, ele sai como um app da CodeDAC que qualquer pessoa pode usar. Nós decidimos se e quando fazer.)",
 i=["O que é incômodo e quando acontece?",
    "O que o app faria? (uma frase basta)",
    "Como você resolve isso hoje?",
    "Em qual dispositivo (Android / Windows) e em que país você mora?",
    "Quer testar uma versão inicial? Sim / Não"],
 pick="Na dúvida? Se você quer ser dono do app e pretende pagar por ele, escolha “{a}”. Se só quer que um app assim exista, escolha “{b}” — é grátis."),
'ru': dict(
 pn="(Платная разработка: приложение будет вашим. Просто хотите, чтобы такое приложение появилось, без оплаты? Нажмите «{cta}».)",
 p=["Что вы хотите создать? Для кого (для себя / для компании или клиентов / для всех)?",
    "3 главные функции первой версии",
    "Платформа (Android / iOS / Windows / веб)",
    "Бюджет: до {B1} / {B1}–{B3} / {B3}–{B2} / более {B2} / пока не знаю (можно в любой валюте)",
    "Сроки, ваша страна (часовой пояс), приложения-образцы или готовые материалы"],
 inote="(Бесплатно: если мы его сделаем, оно выйдет как приложение CodeDAC для всех. Делать ли и когда — решаем мы.)",
 i=["Что неудобно и когда это происходит?",
    "Что должно делать приложение? (достаточно одной фразы)",
    "Как вы решаете это сейчас?",
    "На каком устройстве (Android / Windows) и в какой стране вы живёте?",
    "Хотите попробовать раннюю версию? Да / Нет"],
 pick="Не знаете, что выбрать? Если хотите владеть приложением и готовы платить — «{a}». Если просто хотите, чтобы такое приложение было, — «{b}», это бесплатно."),
'it': dict(
 pn="(Sviluppo a pagamento: l'app sarà tua. Vuoi solo che un'app così esista, senza pagare? Usa «{cta}».)",
 p=["Cosa vuoi realizzare? Per chi (te stesso / la tua azienda o i clienti / il pubblico)?",
    "Le 3 funzioni principali della prima versione",
    "Piattaforma (Android / iOS / Windows / Web)",
    "Budget: meno di {B1} / {B1}–{B3} / {B3}–{B2} / oltre {B2} / non so ancora (va bene qualsiasi valuta)",
    "Tempi, il tuo paese (fuso orario), app di riferimento o materiali esistenti"],
 inote="(Gratis: se la sviluppiamo, esce come app CodeDAC per tutti. Decidiamo noi se e quando realizzarla.)",
 i=["Cosa ti risulta scomodo, e quando succede?",
    "Cosa farebbe l'app? (basta una frase)",
    "Come lo risolvi oggi?",
    "Su quale dispositivo (Android / Windows) e in che paese vivi?",
    "Vuoi provare una prima versione? Sì / No"],
 pick="Non sai quale scegliere? Se vuoi che l'app sia tua e intendi pagarla, scegli «{a}». Se vuoi solo che un'app così esista, scegli «{b}»: è gratis."),
'ar': dict(
 pn="(تطوير مدفوع: سيكون التطبيق ملكك. هل تريد فقط أن يوجد تطبيق كهذا دون أن تدفع؟ استخدم «{cta}».)",
 p=["ماذا تريد أن تبني؟ ولمن (لنفسك / لشركتك أو عملائك / للجمهور)؟",
    "أهم 3 ميزات في الإصدار الأول",
    "المنصة (Android / iOS / Windows / الويب)",
    "الميزانية: أقل من {B1} / {B1}–{B3} / {B3}–{B2} / أكثر من {B2} / لا أعرف بعد (أي عملة مقبولة)",
    "الموعد المطلوب، بلدك (المنطقة الزمنية)، تطبيقات مرجعية أو مواد موجودة"],
 inote="(مجاني: إذا طوّرناه، يُنشر كتطبيق من CodeDAC يستخدمه الجميع. نحن نقرر ما إذا كنا سنبنيه ومتى.)",
 i=["ما الذي يزعجك، ومتى يحدث؟",
    "ماذا سيفعل التطبيق؟ (جملة واحدة تكفي)",
    "كيف تتعامل معه اليوم؟",
    "على أي جهاز (Android / Windows)، وفي أي بلد تعيش؟",
    "هل تود تجربة نسخة مبكرة؟ نعم / لا"],
 pick="لست متأكدًا أيهما تختار؟ إذا أردت أن تملك التطبيق وتنوي الدفع، فاختر «{a}». وإذا أردت فقط أن يوجد تطبيق كهذا، فاختر «{b}» — مجانًا."),
'hi': dict(
 pn="(यह पेड डेवलपमेंट है: ऐप आपका होगा। बिना पैसे दिए बस ऐसा ऐप चाहिए? तो “{cta}” इस्तेमाल करें।)",
 p=["आप क्या बनाना चाहते हैं? यह किसके लिए है (आपके लिए / आपके बिज़नेस या ग्राहकों के लिए / आम लोगों के लिए)?",
    "पहले वर्शन के 3 सबसे ज़रूरी फ़ीचर",
    "प्लेटफ़ॉर्म (Android / iOS / Windows / वेब)",
    "बजट: {B1} से कम / {B1}–{B3} / {B3}–{B2} / {B2} से ज़्यादा / अभी तय नहीं (किसी भी मुद्रा में लिख सकते हैं)",
    "समय-सीमा, आपका देश (टाइम ज़ोन), संदर्भ ऐप या मौजूदा सामग्री"],
 inote="(मुफ़्त: अगर हम इसे बनाते हैं, तो यह सबके लिए CodeDAC ऐप के रूप में आएगा। बनाना है या नहीं और कब, यह हम तय करते हैं।)",
 i=["क्या असुविधाजनक है, और यह कब होता है?",
    "ऐप क्या करेगा? (एक वाक्य काफ़ी है)",
    "आज आप इसे कैसे संभालते हैं?",
    "किस डिवाइस पर (Android / Windows), और आप किस देश में रहते हैं?",
    "क्या आप शुरुआती वर्शन आज़माना चाहेंगे? हाँ / नहीं"],
 pick="तय नहीं कर पा रहे? अगर ऐप आपका हो और आप भुगतान करेंगे, तो “{a}” चुनें। अगर बस ऐसा ऐप मौजूद हो, तो “{b}” चुनें — यह मुफ़्त है।"),
'id': dict(
 pn="(Pengembangan berbayar: aplikasinya jadi milik Anda. Hanya ingin aplikasi seperti ini ada tanpa membayar? Gunakan “{cta}”.)",
 p=["Apa yang ingin Anda buat? Untuk siapa (Anda sendiri / bisnis atau klien Anda / publik)?",
    "3 fitur terpenting untuk versi pertama",
    "Platform (Android / iOS / Windows / Web)",
    "Anggaran: di bawah {B1} / {B1}–{B3} / {B3}–{B2} / di atas {B2} / belum tahu (mata uang apa pun boleh)",
    "Target waktu, negara Anda (zona waktu), aplikasi acuan atau bahan yang sudah ada"],
 inote="(Gratis: jika kami membuatnya, aplikasi dirilis sebagai aplikasi CodeDAC untuk semua orang. Kami yang memutuskan apakah dan kapan dibuat.)",
 i=["Apa yang merepotkan, dan kapan terjadinya?",
    "Apa yang akan dilakukan aplikasinya? (satu kalimat cukup)",
    "Bagaimana Anda mengatasinya sekarang?",
    "Di perangkat apa (Android / Windows), dan di negara mana Anda tinggal?",
    "Mau mencoba versi awal? Ya / Tidak"],
 pick="Bingung memilih? Jika ingin memiliki aplikasinya dan siap membayar, pilih “{a}”. Jika hanya ingin aplikasi seperti itu ada, pilih “{b}” — gratis."),
'th': dict(
 pn="(เป็นงานพัฒนาแบบมีค่าใช้จ่าย แอปจะเป็นของคุณ ถ้าแค่อยากให้มีแอปแบบนี้โดยไม่จ่ายเงิน ให้ใช้ “{cta}”)",
 p=["อยากสร้างอะไร ใครเป็นผู้ใช้ (ตัวคุณเอง / ธุรกิจหรือลูกค้า / คนทั่วไป)",
    "ฟีเจอร์สำคัญ 3 อย่างในเวอร์ชันแรก",
    "แพลตฟอร์ม (Android / iOS / Windows / เว็บ)",
    "งบประมาณ: ต่ำกว่า {B1} / {B1}–{B3} / {B3}–{B2} / มากกว่า {B2} / ยังไม่แน่ใจ (ใช้สกุลเงินใดก็ได้)",
    "กำหนดเวลา ประเทศของคุณ (เขตเวลา) แอปอ้างอิงหรือเอกสารที่มีอยู่"],
 inote="(ฟรี ถ้าเราสร้าง แอปจะเผยแพร่เป็นแอปของ CodeDAC ที่ทุกคนใช้ได้ เราเป็นผู้ตัดสินใจว่าจะสร้างหรือไม่และเมื่อไร)",
 i=["อะไรที่ไม่สะดวก และเกิดขึ้นเมื่อไร",
    "อยากให้แอปทำอะไร (ประโยคเดียวก็พอ)",
    "ตอนนี้คุณแก้ปัญหานี้อย่างไร",
    "ใช้บนอุปกรณ์ไหน (Android / Windows) และอยู่ประเทศอะไร",
    "อยากลองเวอร์ชันแรกก่อนไหม ใช่ / ไม่"],
 pick="ไม่แน่ใจว่าจะเลือกแบบไหน ถ้าอยากเป็นเจ้าของแอปและพร้อมจ่าย เลือก “{a}” ถ้าแค่อยากให้มีแอปแบบนี้ เลือก “{b}” ซึ่งฟรี"),
'vi': dict(
 pn="(Phát triển có trả phí: ứng dụng sẽ thuộc về bạn. Chỉ muốn có một ứng dụng như vậy mà không trả phí? Hãy dùng “{cta}”.)",
 p=["Bạn muốn làm gì? Dành cho ai (bản thân / doanh nghiệp hoặc khách hàng / công chúng)?",
    "3 tính năng quan trọng nhất của phiên bản đầu",
    "Nền tảng (Android / iOS / Windows / Web)",
    "Ngân sách: dưới {B1} / {B1}–{B3} / {B3}–{B2} / trên {B2} / chưa rõ (ghi bằng đơn vị tiền nào cũng được)",
    "Thời hạn, quốc gia của bạn (múi giờ), ứng dụng tham khảo hoặc tài liệu sẵn có"],
 inote="(Miễn phí: nếu chúng tôi làm, nó sẽ ra mắt như một ứng dụng CodeDAC cho mọi người. Làm hay không và khi nào là do chúng tôi quyết định.)",
 i=["Điều gì bất tiện, và xảy ra khi nào?",
    "Ứng dụng sẽ làm gì? (một câu là đủ)",
    "Hiện bạn xử lý thế nào?",
    "Trên thiết bị nào (Android / Windows), và bạn sống ở nước nào?",
    "Bạn có muốn dùng thử bản đầu tiên không? Có / Không"],
 pick="Chưa biết chọn bên nào? Nếu muốn sở hữu ứng dụng và sẵn sàng trả phí, hãy chọn “{a}”. Nếu chỉ muốn có một ứng dụng như vậy, hãy chọn “{b}” — miễn phí."),
'tr': dict(
 pn="(Ücretli geliştirme: uygulama sizin olur. Ödeme yapmadan sadece böyle bir uygulamanın olmasını mı istiyorsunuz? “{cta}” seçeneğini kullanın.)",
 p=["Ne yapmak istiyorsunuz? Kimin için (kendiniz / şirketiniz veya müşterileriniz / herkes)?",
    "İlk sürüm için en önemli 3 özellik",
    "Platform (Android / iOS / Windows / Web)",
    "Bütçe: {B1} altı / {B1}–{B3} / {B3}–{B2} / {B2} üstü / henüz bilmiyorum (herhangi bir para birimi olabilir)",
    "Zaman planı, ülkeniz (saat dilimi), örnek uygulamalar veya mevcut materyaller"],
 inote="(Ücretsiz: Yaparsak herkesin kullanabileceği bir CodeDAC uygulaması olarak yayımlanır. Yapıp yapmayacağımıza ve ne zaman yapacağımıza biz karar veririz.)",
 i=["Ne zahmetli ve ne zaman oluyor?",
    "Uygulama ne yapmalı? (tek cümle yeterli)",
    "Bugün bunu nasıl hallediyorsunuz?",
    "Hangi cihazda (Android / Windows) ve hangi ülkede yaşıyorsunuz?",
    "İlk sürümü denemek ister misiniz? Evet / Hayır"],
 pick="Hangisini seçeceğinizden emin değil misiniz? Uygulamanın sizin olmasını istiyor ve ödeme yapmayı düşünüyorsanız “{a}”, sadece böyle bir uygulamanın var olmasını istiyorsanız “{b}” (ücretsiz)."),
'pl': dict(
 pn="(Płatne tworzenie: aplikacja będzie Twoja. Chcesz tylko, żeby taka aplikacja powstała, bez płacenia? Użyj „{cta}”.)",
 p=["Co chcesz zbudować? Dla kogo (dla siebie / dla firmy lub klientów / dla wszystkich)?",
    "3 najważniejsze funkcje pierwszej wersji",
    "Platforma (Android / iOS / Windows / Web)",
    "Budżet: poniżej {B1} / {B1}–{B3} / {B3}–{B2} / powyżej {B2} / jeszcze nie wiem (dowolna waluta)",
    "Termin, Twój kraj (strefa czasowa), aplikacje wzorcowe lub istniejące materiały"],
 inote="(Za darmo: jeśli ją zbudujemy, wyjdzie jako aplikacja CodeDAC dla wszystkich. To my decydujemy, czy i kiedy powstanie.)",
 i=["Co jest uciążliwe i kiedy się to zdarza?",
    "Co miałaby robić aplikacja? (wystarczy jedno zdanie)",
    "Jak radzisz sobie z tym dziś?",
    "Na jakim urządzeniu (Android / Windows) i w jakim kraju mieszkasz?",
    "Chcesz wypróbować wczesną wersję? Tak / Nie"],
 pick="Nie wiesz, co wybrać? Jeśli aplikacja ma być Twoja i zamierzasz za nią zapłacić, wybierz „{a}”. Jeśli chcesz tylko, żeby taka aplikacja istniała, wybierz „{b}” — za darmo."),
'nl': dict(
 pn="(Betaalde ontwikkeling: de app wordt van jou. Wil je alleen dat zo'n app bestaat, zonder te betalen? Gebruik ‘{cta}’.)",
 p=["Wat wil je laten bouwen? Voor wie (jezelf / je bedrijf of klanten / iedereen)?",
    "De 3 belangrijkste functies van de eerste versie",
    "Platform (Android / iOS / Windows / Web)",
    "Budget: minder dan {B1} / {B1}–{B3} / {B3}–{B2} / meer dan {B2} / weet ik nog niet (elke valuta is goed)",
    "Planning, je land (tijdzone), voorbeeld-apps of bestaand materiaal"],
 inote="(Gratis: als we hem bouwen, verschijnt hij als CodeDAC-app voor iedereen. Wij bepalen of en wanneer hij gebouwd wordt.)",
 i=["Wat is onhandig, en wanneer gebeurt het?",
    "Wat zou de app moeten doen? (één zin is genoeg)",
    "Hoe los je het nu op?",
    "Op welk apparaat (Android / Windows), en in welk land woon je?",
    "Wil je een vroege versie uitproberen? Ja / Nee"],
 pick="Twijfel je? Wil je dat de app van jou is en ben je van plan te betalen, kies dan ‘{a}’. Wil je alleen dat zo'n app bestaat, kies dan ‘{b}’ — gratis."),
'uk': dict(
 pn="(Платна розробка: застосунок буде вашим. Просто хочете, щоб такий застосунок з'явився, без оплати? Натисніть «{cta}».)",
 p=["Що ви хочете створити? Для кого (для себе / для компанії чи клієнтів / для всіх)?",
    "3 головні функції першої версії",
    "Платформа (Android / iOS / Windows / веб)",
    "Бюджет: до {B1} / {B1}–{B3} / {B3}–{B2} / понад {B2} / ще не знаю (можна в будь-якій валюті)",
    "Терміни, ваша країна (часовий пояс), застосунки-зразки або наявні матеріали"],
 inote="(Безкоштовно: якщо ми його зробимо, він вийде як застосунок CodeDAC для всіх. Чи робити і коли — вирішуємо ми.)",
 i=["Що незручно і коли це трапляється?",
    "Що має робити застосунок? (достатньо одного речення)",
    "Як ви розв'язуєте це зараз?",
    "На якому пристрої (Android / Windows) і в якій країні ви живете?",
    "Хочете спробувати ранню версію? Так / Ні"],
 pick="Не знаєте, що обрати? Якщо хочете володіти застосунком і готові платити — «{a}». Якщо просто хочете, щоб такий застосунок існував, — «{b}», це безкоштовно."),
'ms': dict(
 pn="(Pembangunan berbayar: aplikasi itu milik anda. Hanya mahu aplikasi sebegini wujud tanpa membayar? Gunakan “{cta}”.)",
 p=["Apa yang anda mahu bina? Untuk siapa (diri sendiri / perniagaan atau pelanggan anda / orang ramai)?",
    "3 ciri terpenting untuk versi pertama",
    "Platform (Android / iOS / Windows / Web)",
    "Bajet: bawah {B1} / {B1}–{B3} / {B3}–{B2} / atas {B2} / belum pasti (sebarang mata wang boleh)",
    "Jangka masa, negara anda (zon waktu), aplikasi rujukan atau bahan sedia ada"],
 inote="(Percuma: jika kami membinanya, ia dilancarkan sebagai aplikasi CodeDAC untuk semua orang. Kami yang menentukan sama ada dan bila ia dibina.)",
 i=["Apa yang menyusahkan, dan bila ia berlaku?",
    "Apa yang aplikasi itu akan buat? (satu ayat sudah cukup)",
    "Bagaimana anda mengatasinya sekarang?",
    "Pada peranti apa (Android / Windows), dan di negara mana anda tinggal?",
    "Mahu mencuba versi awal? Ya / Tidak"],
 pick="Tidak pasti mana satu? Jika anda mahu memiliki aplikasi itu dan bersedia membayar, pilih “{a}”. Jika anda cuma mahu aplikasi sebegitu wujud, pilih “{b}” — percuma."),
'fil': dict(
 pn="(Bayad na development: sa iyo ang app. Gusto mo lang na magkaroon ng ganitong app nang hindi nagbabayad? Gamitin ang “{cta}”.)",
 p=["Ano ang gusto mong ipagawa? Para kanino (sarili mo / negosyo o kliyente mo / publiko)?",
    "Ang 3 pinakamahalagang feature sa unang bersyon",
    "Platform (Android / iOS / Windows / Web)",
    "Budget: mas mababa sa {B1} / {B1}–{B3} / {B3}–{B2} / higit sa {B2} / hindi pa sigurado (puwede kahit anong currency)",
    "Timeline, bansa mo (time zone), mga reference app o kasalukuyang materyales"],
 inote="(Libre: kung gagawin namin ito, ilalabas ito bilang CodeDAC app na magagamit ng lahat. Kami ang magpapasya kung gagawin ito at kailan.)",
 i=["Ano ang abala, at kailan ito nangyayari?",
    "Ano ang gagawin ng app? (sapat na ang isang pangungusap)",
    "Paano mo ito hinaharap ngayon?",
    "Sa anong device (Android / Windows), at saang bansa ka nakatira?",
    "Gusto mo bang subukan ang maagang bersyon? Oo / Hindi"],
 pick="Hindi sigurado kung alin? Kung gusto mong sa iyo ang app at handa kang magbayad, piliin ang “{a}”. Kung gusto mo lang na may ganitong app, piliin ang “{b}” — libre."),
}

def body(note, qs):
    return note + '\n\n' + ''.join(f'{n}. {q}\n- \n\n' for n, q in enumerate(qs, 1)).rstrip('\n') + '\n'

def main():
    langs = sorted(f[:-5] for f in os.listdir(I18N) if f.endswith('.json'))
    missing = set(langs) - set(T)
    if missing:
        sys.exit(f'번역 없음: {sorted(missing)}')
    for code in langs:
        path = os.path.join(I18N, code + '.json')
        raw = open(path, encoding='utf-8').read()
        data = json.loads(raw)
        ui = data['ui']; t = T[code]
        sub = dict(cta=ui['ideas.cta'], a=ui['work.a.title'], b=ui['work.b.title'], B1=B1, B2=B2, B3=B3)
        fill = lambda s: s.format(**sub)
        ui['services.mail.body'] = body(fill(t['pn']), [fill(q) for q in t['p']])
        ui['ideas.mail.body'] = body(fill(t['inote']), [fill(q) for q in t['i']])
        ui['work.pick'] = fill(t['pick'])
        indent = 2 if '\n  "' in raw[:200] else 1
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=indent) + ('\n' if raw.endswith('\n') else ''))
        print(code, 'ok')

if __name__ == '__main__':
    main()
