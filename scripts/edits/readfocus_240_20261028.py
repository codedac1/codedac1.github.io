# -*- coding: utf-8 -*-
"""ReadFocus+ 안드로이드 2.4.0 · Windows 1.0.19 출시용 사이트 문구 (2026-10-28 작성, readfocus-240 브랜치).

두 판 모두 띠 높이·불투명도가 무료가 됐다. 그것을 Pro 로 적은 6곳 × 21개 언어를 고친다:
  RF_F5  apps.readfocus.features[5]        RF_Q2  apps.readfocus.faq[2].a ("무료인가요?")
  RW_F5  apps.readfocuswin.features[5]     RW_Q2  apps.readfocuswin.faq[2].a
  G_A    guides reading-ruler-dyslexia-adhd-android sections[2].p[0]
  G_W    guides reading-ruler-windows sections[2].p[0]
하루 무료 시간은 쓰지 않는다(리스팅과 같은 원칙). 각 칸은 바꾸기 전 값이 OLD 와 같아야 쓴다 — 그 사이 누가 고쳤으면 멈춘다.
두 앱이 출시된 뒤 main 에 병합하고 gen_site 재생성(V 올림)·IndexNow.

    python scripts/edits/readfocus_240_20261028.py
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NEW = {
"en": dict(
 RF_F5="Pro: no ads, 7 more color themes, and keep screen on while reading",
 RF_Q2="Yes. The free version includes both focus modes, 3 color themes and strip height and opacity adjustment, with ads. Pro removes the ads and adds 7 more color themes and Keep Screen On — monthly, yearly or as a one-time lifetime purchase.",
 RW_F5="No ads. Pro is a one-time purchase: premium themes and Keep Screen On",
 RW_Q2="Yes. The free version includes both reading modes, Focus Strip height and opacity, and three of the ten themes. Pro is a one-time purchase — not a subscription — and adds premium themes and Keep Screen On. The Windows version has no ads.",
 G_A="The free version includes both focus modes, 3 color themes, and strip height and opacity adjustment. Pro removes the ads and adds all 10 themes and keep-screen-on.",
 G_W="The free version includes both modes, strip height and opacity settings, and three themes. Pro is a one-time purchase that adds premium themes and keep-screen-on. There are no ads."),
"ko": dict(
 RF_F5="Pro: 광고 없는 환경, 컬러 테마 7종 추가, 화면 자동 꺼짐 방지",
 RF_Q2="네, 무료 버전은 두 가지 모드(줄 강조·읽기 마스크)와 3가지 컬러 테마, 스트립 높이·불투명도 조절을 광고와 함께 제공합니다. Pro는 광고를 없애고 컬러 테마 7종 추가, 화면 자동 꺼짐 방지를 더합니다 — 월간·연간 구독 또는 평생 1회 구매.",
 RW_F5="광고 없음. Pro는 일회성 구매 — 프리미엄 테마, 화면 꺼짐 방지",
 RW_Q2="네. 무료 버전은 두 가지 읽기 모드와 집중 스트립 높이·불투명도 조절, 테마 10종 가운데 3종을 제공합니다. Pro는 구독이 아닌 일회성 구매로, 프리미엄 테마와 화면 꺼짐 방지가 열립니다. Windows 판에는 광고가 없습니다.",
 G_A="무료 버전은 두 가지 모드와 색 테마 3가지, 띠 높이·불투명도 조절을 제공합니다. Pro는 광고를 없애고 테마 10가지 전부와 화면 켜짐 유지를 더합니다.",
 G_W="무료 버전은 두 모드와 띠 높이·불투명도 설정, 테마 3가지를 쓸 수 있습니다. Pro는 일회성 구매로 프리미엄 테마와 화면 켜짐 유지를 더합니다. 광고는 없습니다."),
"ja": dict(
 RF_F5="Pro：広告なし、カラーテーマ7種追加、読書中の画面点灯を維持",
 RF_Q2="はい。無料版では2つのフォーカスモード、3色のテーマ、ストリップの高さと透明度の調整を広告付きで利用できます。Proは広告をなくし、カラーテーマ7種と画面点灯の維持を追加します。月額・年額または買い切りで購入できます。",
 RW_F5="広告なし。Pro は買い切り — プレミアムテーマ、画面の自動オフ防止",
 RW_Q2="はい。無料版では2つの読書モード、フォーカスストリップの高さ・不透明度の調整、10種類のうち3種類のテーマが使えます。Pro はサブスクではなく買い切りで、プレミアムテーマと画面の自動オフ防止が解放されます。Windows版に広告はありません。",
 G_A="無料版には2つのフォーカスモード、3色のテーマ、ストリップの高さと透明度の調整が含まれます。Proは広告をなくし、全10テーマと画面点灯の維持を追加します。",
 G_W="無料版には両方のモード、ストリップの高さと不透明度の設定、3種類のテーマが含まれます。Proは買い切りで、プレミアムテーマと画面の自動オフ防止を追加します。広告はありません。"),
"zh": dict(
 RF_F5="Pro：无广告、另外 7 款配色主题，以及阅读时保持屏幕常亮",
 RF_Q2="可以。免费版包含两种专注模式、3 款配色主题以及聚焦条高度和透明度调节，含广告。Pro 去除广告，并增加另外 7 款配色主题以及屏幕常亮——提供月付、年付和一次性买断。",
 RW_F5="无广告。Pro 为一次性买断：高级主题、防止屏幕熄灭",
 RW_Q2="可以。免费版包含两种阅读模式、专注条高度和不透明度调节，以及 10 款主题中的 3 款。Pro 是一次性买断而非订阅，可解锁高级主题和防止屏幕熄灭。Windows 版没有广告。",
 G_A="免费版包含两种专注模式、3 款配色主题以及聚焦条高度和透明度调节。Pro 去除广告，并增加全部 10 款主题以及屏幕常亮。",
 G_W="免费版包含两种模式、专注条高度和不透明度设置以及三款主题。Pro 为一次性买断，增加高级主题以及防止屏幕熄灭。没有广告。"),
"de": dict(
 RF_F5="Pro: keine Werbung, 7 weitere Farbdesigns und Bildschirm beim Lesen anlassen",
 RF_Q2="Ja. Die kostenlose Version enthält beide Fokusmodi, 3 Farbdesigns sowie einstellbare Höhe und Deckkraft des Streifens, mit Werbung. Pro entfernt die Werbung und ergänzt 7 weitere Farbdesigns und „Bildschirm anlassen“ – monatlich, jährlich oder einmalig auf Lebenszeit.",
 RW_F5="Keine Werbung. Pro ist ein Einmalkauf: Premium-Themes und Bildschirm anlassen",
 RW_Q2="Ja. Die kostenlose Version enthält beide Lesemodi, Höhe und Deckkraft des Fokusstreifens und drei der zehn Themes. Pro ist ein Einmalkauf, kein Abo, und ergänzt Premium-Themes und „Bildschirm anlassen“. Die Windows-Version enthält keine Werbung.",
 G_A="Die Gratisversion enthält beide Fokusmodi, 3 Farbdesigns sowie einstellbare Höhe und Deckkraft des Streifens. Pro entfernt die Werbung und bringt alle 10 Designs sowie „Bildschirm anlassen“.",
 G_W="Die Gratisversion enthält beide Modi, Einstellungen für Höhe und Deckkraft des Streifens und drei Designs. Pro ist ein Einmalkauf und bringt Premium-Designs sowie „Bildschirm anlassen“. Werbung gibt es nicht."),
"es": dict(
 RF_F5="Pro: sin anuncios, 7 temas de color más y pantalla encendida mientras lees",
 RF_Q2="Sí. La versión gratuita incluye los dos modos de enfoque, 3 temas de color y el ajuste de altura y opacidad de la franja, con anuncios. Pro quita los anuncios y añade 7 temas de color más y la pantalla encendida, en modalidad mensual, anual o pago único de por vida.",
 RW_F5="Sin anuncios. Pro es una compra única: temas premium y mantener la pantalla encendida",
 RW_Q2="Sí. La versión gratuita incluye los dos modos de lectura, la altura y opacidad de la franja de enfoque y tres de los diez temas. Pro es una compra única, no una suscripción, y añade temas premium y mantener la pantalla encendida. La versión de Windows no tiene anuncios.",
 G_A="La versión gratuita incluye los dos modos de enfoque, 3 temas de color y el ajuste de altura y opacidad de la franja. Pro quita los anuncios y añade los 10 temas y la pantalla siempre encendida.",
 G_W="La versión gratuita incluye los dos modos, ajustes de altura y opacidad de la franja y tres temas. Pro es una compra única que añade temas premium y pantalla siempre encendida. No hay anuncios."),
"fr": dict(
 RF_F5="Pro : sans publicité, 7 thèmes de couleur de plus et écran maintenu allumé pendant la lecture",
 RF_Q2="Oui. La version gratuite inclut les deux modes de focalisation, 3 thèmes de couleur ainsi que le réglage de la hauteur et de l'opacité de la bande, avec des publicités. La version Pro supprime les publicités et ajoute 7 thèmes de couleur de plus et l'écran maintenu allumé — en mensuel, annuel ou en achat unique à vie.",
 RW_F5="Sans publicité. Pro est un achat unique : thèmes premium et écran toujours allumé",
 RW_Q2="Oui. La version gratuite inclut les deux modes de lecture, la hauteur et l’opacité de la bande de focus et trois des dix thèmes. Pro est un achat unique, pas un abonnement : il ajoute les thèmes premium et le maintien de l’écran allumé. La version Windows ne contient aucune publicité.",
 G_A="La version gratuite inclut les deux modes de focalisation, 3 thèmes de couleur et le réglage de la hauteur et de l’opacité de la bande. Pro supprime les pubs et ajoute les 10 thèmes et l’écran maintenu allumé.",
 G_W="La version gratuite inclut les deux modes, les réglages de hauteur et d’opacité de la bande et trois thèmes. Pro est un achat unique qui ajoute les thèmes premium et l’écran maintenu allumé. Il n’y a pas de publicité."),
"it": dict(
 RF_F5="Pro: nessuna pubblicità, altri 7 temi di colore e schermo sempre acceso durante la lettura",
 RF_Q2="Sì. La versione gratuita include entrambe le modalità di focus, 3 temi di colore e la regolazione di altezza e opacità della striscia, con pubblicità. Pro rimuove la pubblicità e aggiunge altri 7 temi di colore e lo schermo sempre acceso — mensile, annuale o acquisto unico a vita.",
 RW_F5="Nessuna pubblicità. Pro è un acquisto una tantum: temi premium e schermo sempre acceso",
 RW_Q2="Sì. La versione gratuita include entrambe le modalità di lettura, altezza e opacità della striscia di focus e tre dei dieci temi. Pro è un acquisto una tantum, non un abbonamento, e aggiunge i temi premium e lo schermo sempre acceso. La versione Windows non contiene pubblicità.",
 G_A="La versione gratuita include entrambe le modalità di focus, 3 temi di colore e la regolazione di altezza e opacità della striscia. Pro rimuove la pubblicità e aggiunge tutti i 10 temi e lo schermo sempre acceso.",
 G_W="La versione gratuita include entrambe le modalità, le impostazioni di altezza e opacità della striscia e tre temi. Pro è un acquisto una tantum che aggiunge temi premium e schermo sempre acceso. Non ci sono pubblicità."),
"pt": dict(
 RF_F5="Pro: sem anúncios, mais 7 temas de cor e tela sempre ligada durante a leitura",
 RF_Q2="Sim. A versão gratuita inclui os dois modos de foco, 3 temas de cor e o ajuste de altura e opacidade da faixa, com anúncios. O Pro remove os anúncios e adiciona mais 7 temas de cor e tela sempre ligada — mensal, anual ou compra única vitalícia.",
 RW_F5="Sem anúncios. O Pro é uma compra única: temas premium e manter a tela ligada",
 RW_Q2="Sim. A versão gratuita inclui os dois modos de leitura, a altura e a opacidade da faixa de foco e três dos dez temas. O Pro é uma compra única, não uma assinatura, e acrescenta temas premium e manter a tela ligada. A versão para Windows não tem anúncios.",
 G_A="A versão gratuita inclui os dois modos de foco, 3 temas de cor e o ajuste de altura e opacidade da faixa. O Pro remove os anúncios e adiciona todos os 10 temas e a tela sempre ligada.",
 G_W="A versão gratuita inclui os dois modos, ajustes de altura e opacidade da faixa e três temas. O Pro é uma compra única que adiciona temas premium e tela sempre ligada. Não há anúncios."),
"nl": dict(
 RF_F5="Pro: geen advertenties, 7 extra kleurenthema's en scherm aan houden tijdens het lezen",
 RF_Q2="Ja. De gratis versie bevat beide focusmodi, 3 kleurenthema's en instelbare hoogte en dekking van de focusstrip, met advertenties. Pro haalt de advertenties weg en voegt 7 extra kleurenthema's en scherm aan houden toe – maandelijks, jaarlijks of eenmalig levenslang.",
 RW_F5="Geen advertenties. Pro is een eenmalige aankoop: premium thema's en scherm aan houden",
 RW_Q2="Ja. De gratis versie bevat beide leesmodi, hoogte en dekking van de focusstrook en drie van de tien thema's. Pro is een eenmalige aankoop, geen abonnement, en voegt premium thema's en scherm aan houden toe. De Windows-versie bevat geen advertenties.",
 G_A="De gratis versie bevat beide focusmodi, 3 kleurenthema’s en instelbare hoogte en dekking van de strook. Pro haalt advertenties weg en voegt alle 10 thema’s en ‘scherm aan houden’ toe.",
 G_W="De gratis versie bevat beide modi, instellingen voor hoogte en dekking van de strook en drie thema’s. Pro is een eenmalige aankoop die premium thema’s en ‘scherm aan houden’ toevoegt. Er zijn geen advertenties."),
"pl": dict(
 RF_F5="Pro: brak reklam, 7 dodatkowych motywów kolorystycznych oraz utrzymywanie ekranu włączonego podczas czytania",
 RF_Q2="Tak. Wersja darmowa zawiera oba tryby skupienia, 3 motywy kolorystyczne oraz regulację wysokości i krycia paska, z reklamami. Pro usuwa reklamy i dodaje 7 kolejnych motywów kolorystycznych oraz utrzymywanie ekranu włączonego — miesięcznie, rocznie lub jednorazowo na zawsze.",
 RW_F5="Bez reklam. Pro to jednorazowy zakup: motywy premium i „Nie wygaszaj ekranu”",
 RW_Q2="Tak. Wersja bezpłatna zawiera oba tryby czytania, wysokość i krycie paska skupienia oraz trzy z dziesięciu motywów. Pro to jednorazowy zakup, a nie subskrypcja — dodaje motywy premium i „Nie wygaszaj ekranu”. Wersja dla Windows nie zawiera reklam.",
 G_A="Wersja darmowa zawiera oba tryby skupienia, 3 motywy kolorystyczne oraz regulację wysokości i krycia paska. Pro usuwa reklamy i dodaje wszystkie 10 motywów oraz utrzymywanie ekranu włączonego.",
 G_W="Wersja darmowa obejmuje oba tryby, ustawienia wysokości i krycia paska oraz trzy motywy. Pro to jednorazowy zakup, który dodaje motywy premium oraz utrzymywanie ekranu włączonego. Nie ma reklam."),
"ru": dict(
 RF_F5="Pro: без рекламы, ещё 7 цветовых тем и удержание экрана включённым во время чтения",
 RF_Q2="Да. Бесплатная версия включает оба режима фокуса, 3 цветовые темы и настройку высоты и непрозрачности полосы, с рекламой. Pro убирает рекламу и добавляет ещё 7 цветовых тем и удержание экрана включённым — помесячно, на год или разовой покупкой навсегда.",
 RW_F5="Без рекламы. Pro — разовая покупка: премиум-темы и «Не выключать экран»",
 RW_Q2="Да. Бесплатная версия включает оба режима чтения, высоту и непрозрачность полосы фокуса и три темы из десяти. Pro — разовая покупка, а не подписка: добавляет премиум-темы и «Не выключать экран». В версии для Windows нет рекламы.",
 G_A="Бесплатная версия включает оба режима фокуса, 3 цветовые темы и настройку высоты и непрозрачности полосы. Pro убирает рекламу и добавляет все 10 тем и удержание экрана включённым.",
 G_W="Бесплатная версия включает оба режима, настройки высоты и непрозрачности полосы и три темы. Pro — разовая покупка: добавляет премиум-темы и «Не выключать экран». Рекламы нет."),
"uk": dict(
 RF_F5="Pro: без реклами, ще 7 кольорових тем та утримання екрана ввімкненим під час читання",
 RF_Q2="Так. Безкоштовна версія містить обидва режими фокуса, 3 кольорові теми та налаштування висоти й непрозорості смуги, з рекламою. Pro прибирає рекламу й додає ще 7 кольорових тем та утримання екрана ввімкненим — щомісяця, щороку або разовою покупкою назавжди.",
 RW_F5="Без реклами. Pro — разова покупка: преміум-теми і «Не вимикати екран»",
 RW_Q2="Так. Безкоштовна версія містить обидва режими читання, висоту й непрозорість смуги фокуса та три теми з десяти. Pro — разова покупка, а не підписка: додає преміум-теми та «Не вимикати екран». У версії для Windows немає реклами.",
 G_A="Безкоштовна версія містить обидва режими фокуса, 3 колірні теми та налаштування висоти й непрозорості смуги. Pro прибирає рекламу й додає всі 10 тем та утримання екрана ввімкненим.",
 G_W="Безкоштовна версія містить обидва режими, налаштування висоти та непрозорості смуги й три теми. Pro — разова покупка: додає преміум-теми і «Не вимикати екран». Реклами немає."),
"tr": dict(
 RF_F5="Pro: reklamsız deneyim, 7 renk teması daha ve okurken ekranı açık tutma",
 RF_Q2="Evet. Ücretsiz sürüm her iki odak modunu, 3 renk temasını ve şerit yüksekliği ile opaklık ayarını reklamlı olarak sunar. Pro reklamları kaldırır; 7 renk teması daha ve ekranı açık tutma ekler — aylık, yıllık ya da tek seferlik ömür boyu.",
 RW_F5="Reklam yok. Pro tek seferlik satın almadır: premium temalar ve ekran kapanmasını önleme",
 RW_Q2="Evet. Ücretsiz sürüm iki okuma modunu, odak şeridi yüksekliği ve opaklığını ve on temanın üçünü içerir. Pro abonelik değil tek seferlik satın almadır; premium temaları ve ekran kapanmasını önlemeyi ekler. Windows sürümünde reklam yoktur.",
 G_A="Ücretsiz sürüm her iki odak modunu, 3 renk temasını ve şerit yüksekliği ile opaklık ayarını sunar. Pro reklamları kaldırır; 10 temanın tamamını ve ekranı açık tutmayı ekler.",
 G_W="Ücretsiz sürüm iki modu, şerit yüksekliği ile opaklık ayarlarını ve üç temayı sunar. Pro; premium temalar ve ekranı açık tutmayı ekleyen tek seferlik bir satın almadır. Reklam yoktur."),
"ar": dict(
 RF_F5="Pro: بلا إعلانات، و7 سمات ألوان إضافية، وإبقاء الشاشة قيد التشغيل أثناء القراءة",
 RF_Q2="نعم. تتضمن النسخة المجانية وضعَي التركيز وثلاث سمات ألوان وضبط ارتفاع الشريط وعتامته، مع إعلانات. وتزيل Pro الإعلانات وتضيف 7 سمات ألوان إضافية وإبقاء الشاشة قيد التشغيل — باشتراك شهري أو سنوي أو شراء لمرة واحدة مدى الحياة.",
 RW_F5="بلا إعلانات. Pro شراء لمرة واحدة: سمات مميزة ومنع إيقاف تشغيل الشاشة",
 RW_Q2="نعم. يشمل الإصدار المجاني وضعَي القراءة وارتفاع شريط التركيز وعتامته وثلاث سمات من عشر. أما Pro فهو شراء لمرة واحدة وليس اشتراكًا، ويضيف السمات المميزة ومنع إيقاف تشغيل الشاشة. ولا توجد إعلانات في إصدار ويندوز.",
 G_A="تتضمن النسخة المجانية وضعَي التركيز و3 سمات ألوان وضبط ارتفاع الشريط وعتامته. وتزيل Pro الإعلانات، وتضيف السمات العشر كلها وإبقاء الشاشة قيد التشغيل.",
 G_W="تتضمن النسخة المجانية الوضعين وإعدادات ارتفاع الشريط وعتامته وثلاث سمات. وPro شراء لمرة واحدة يضيف السمات المميزة وإبقاء الشاشة قيد التشغيل. ولا توجد إعلانات."),
"hi": dict(
 RF_F5="Pro: विज्ञापन-मुक्त अनुभव, 7 अतिरिक्त रंग थीम, और पढ़ते समय स्क्रीन चालू रखें",
 RF_Q2="हां। फ़्री वर्शन में दोनों फ़ोकस मोड, 3 रंग थीम और स्ट्रिप की ऊंचाई व अपारदर्शिता का समायोजन मिलता है, विज्ञापनों के साथ। Pro विज्ञापन हटाता है और 7 अतिरिक्त रंग थीम और स्क्रीन चालू रखने की सुविधा जोड़ता है — मासिक, वार्षिक या एक बार की लाइफ़टाइम ख़रीद।",
 RW_F5="कोई विज्ञापन नहीं। Pro एक बार की खरीद है: प्रीमियम थीम्स और स्क्रीन चालू रखना",
 RW_Q2="हाँ। मुफ़्त संस्करण में दोनों रीडिंग मोड, फ़ोकस स्ट्रिप की ऊँचाई व अपारदर्शिता, तथा दस में से तीन थीम मिलती हैं। Pro सदस्यता नहीं, एक बार की खरीद है — इसमें प्रीमियम थीम्स और स्क्रीन चालू रखना जुड़ता है। Windows संस्करण में विज्ञापन नहीं हैं।",
 G_A="मुफ़्त वर्शन में दोनों फ़ोकस मोड, 3 रंग थीम और स्ट्रिप की ऊंचाई व अपारदर्शिता का समायोजन है। Pro विज्ञापन हटाता है और सभी 10 थीम और स्क्रीन चालू रखने की सुविधा जोड़ता है।",
 G_W="मुफ़्त वर्शन में दोनों मोड, स्ट्रिप की ऊँचाई और अपारदर्शिता की सेटिंग, और तीन थीम हैं। Pro एक बार की खरीद है जो प्रीमियम थीम और स्क्रीन चालू रखने की सुविधा जोड़ती है। कोई विज्ञापन नहीं है।"),
"th": dict(
 RF_F5="Pro: ไร้โฆษณา ธีมสีเพิ่มอีก 7 แบบ และคงหน้าจอเปิดไว้ขณะอ่าน",
 RF_Q2="ได้ เวอร์ชันฟรีมีโหมดโฟกัสทั้งสองแบบ ธีมสี 3 แบบ และการปรับความสูงกับความทึบของแถบ โดยมีโฆษณา ส่วน Pro ไม่มีโฆษณา และเพิ่มธีมสีอีก 7 แบบ กับการคงหน้าจอเปิดไว้ เลือกได้ทั้งรายเดือน รายปี หรือซื้อครั้งเดียวตลอดชีพ",
 RW_F5="ไม่มีโฆษณา Pro เป็นการซื้อครั้งเดียว: ธีมพรีเมียม และป้องกันหน้าจอดับ",
 RW_Q2="ได้ เวอร์ชันฟรีมีทั้งสองโหมดการอ่าน การปรับความสูงและความทึบของแถบโฟกัส กับธีม 3 แบบจาก 10 แบบ ส่วน Pro เป็นการซื้อครั้งเดียวไม่ใช่การสมัครสมาชิก เพิ่มธีมพรีเมียม และการป้องกันหน้าจอดับ เวอร์ชัน Windows ไม่มีโฆษณา",
 G_A="เวอร์ชันฟรีมีโหมดโฟกัสทั้งสองแบบ ธีมสี 3 แบบ และการปรับความสูงกับความทึบของแถบ Pro ไม่มีโฆษณา พร้อมเพิ่มธีมครบทั้ง 10 แบบ และการคงหน้าจอเปิดไว้",
 G_W="เวอร์ชันฟรีมีทั้งสองโหมด การตั้งค่าความสูงและความทึบของแถบ และธีมสามแบบ Pro เป็นการซื้อครั้งเดียว เพิ่มธีมพรีเมียม และการป้องกันหน้าจอดับ ไม่มีโฆษณา"),
"vi": dict(
 RF_F5="Pro: không quảng cáo, thêm 7 giao diện màu, và giữ màn hình sáng khi đọc",
 RF_Q2="Có. Bản miễn phí có cả hai chế độ tập trung, 3 giao diện màu và chỉnh chiều cao, độ mờ đục của dải, có quảng cáo. Pro bỏ quảng cáo và thêm 7 giao diện màu cùng giữ màn hình sáng — theo tháng, theo năm hoặc mua một lần trọn đời.",
 RW_F5="Không quảng cáo. Pro là mua một lần: chủ đề cao cấp và giữ màn hình luôn bật",
 RW_Q2="Có. Bản miễn phí gồm cả hai chế độ đọc, chiều cao và độ mờ của dải tập trung, cùng ba trong mười chủ đề. Pro là mua một lần chứ không phải thuê bao, bổ sung chủ đề cao cấp và giữ màn hình luôn bật. Bản Windows không có quảng cáo.",
 G_A="Bản miễn phí có cả hai chế độ tập trung, 3 giao diện màu và chỉnh chiều cao, độ mờ đục của dải. Pro bỏ quảng cáo, thêm đủ 10 giao diện và giữ màn hình luôn sáng.",
 G_W="Bản miễn phí có cả hai chế độ, cài đặt chiều cao và độ mờ của dải, và ba giao diện. Pro là mua một lần, thêm giao diện cao cấp và giữ màn hình luôn bật. Không có quảng cáo."),
"id": dict(
 RF_F5="Pro: bebas iklan, 7 tema warna tambahan, dan menjaga layar tetap menyala saat membaca",
 RF_Q2="Ya. Versi gratis mencakup kedua mode fokus, 3 tema warna, serta pengaturan tinggi dan opasitas strip, dengan iklan. Pro menghapus iklan dan menambahkan 7 tema warna lagi serta fitur menjaga layar tetap menyala — bulanan, tahunan, atau sekali bayar seumur hidup.",
 RW_F5="Tanpa iklan. Pro adalah pembelian sekali bayar: tema premium dan tetap nyalakan layar",
 RW_Q2="Ya. Versi gratis mencakup kedua mode membaca, tinggi dan opasitas Pita Fokus, serta tiga dari sepuluh tema. Pro adalah pembelian sekali bayar, bukan langganan, dan menambahkan tema premium serta tetap nyalakan layar. Versi Windows tidak memiliki iklan.",
 G_A="Versi gratis mencakup kedua mode fokus, 3 tema warna, serta pengaturan tinggi dan opasitas strip. Pro menghapus iklan dan menambahkan kesepuluh tema serta fitur menjaga layar tetap menyala.",
 G_W="Versi gratis mencakup kedua mode, pengaturan tinggi dan opasitas strip, serta tiga tema. Pro adalah pembelian sekali bayar yang menambahkan tema premium serta fitur menjaga layar tetap menyala. Tidak ada iklan."),
"ms": dict(
 RF_F5="Pro: tanpa iklan, 7 tema warna tambahan, dan pastikan skrin menyala semasa membaca",
 RF_Q2="Ya. Versi percuma merangkumi kedua-dua mod fokus, 3 tema warna serta pelarasan tinggi dan kelegapan jalur, dengan iklan. Pro membuang iklan dan menambah 7 tema warna lagi dan pastikan skrin menyala — bulanan, tahunan atau belian sekali seumur hidup.",
 RW_F5="Tiada iklan. Pro ialah pembelian sekali sahaja: tema premium dan pastikan skrin menyala",
 RW_Q2="Ya. Versi percuma merangkumi kedua-dua mod bacaan, tinggi dan kelegapan Jalur Fokus serta tiga daripada sepuluh tema. Pro ialah pembelian sekali sahaja, bukan langganan, dan menambah tema premium dan pastikan skrin menyala. Versi Windows tiada iklan.",
 G_A="Versi percuma merangkumi kedua-dua mod fokus, 3 tema warna serta pelarasan tinggi dan kelegapan jalur. Pro membuang iklan dan menambah kesemua 10 tema serta pastikan skrin menyala.",
 G_W="Versi percuma merangkumi kedua-dua mod, tetapan ketinggian dan kelegapan jalur serta tiga tema. Pro ialah pembelian sekali sahaja yang menambah tema premium serta pastikan skrin menyala. Tiada iklan."),
"fil": dict(
 RF_F5="Pro: walang ad, 7 pang color theme, at panatilihing nakabukas ang screen habang nagbabasa",
 RF_Q2="Oo. Kasama sa libreng bersyon ang dalawang focus mode, 3 color theme at ang pag-adjust ng taas at opacity ng strip, na may mga ad. Inaalis ng Pro ang mga ad at nagdaragdag ng 7 pang color theme at pagpapanatiling nakabukas ng screen — buwanan, taunan o isahang lifetime na bili.",
 RW_F5="Walang ads. Isang beses lang ang bayad sa Pro: premium na tema at panatilihing naka-on ang screen",
 RW_Q2="Oo. Kasama sa libreng bersyon ang dalawang mode ng pagbasa, ang taas at opacity ng Focus Strip, at tatlo sa sampung tema. Ang Pro ay isang beses na bayad, hindi subscription, at nagdadagdag ng premium na tema at panatilihing naka-on ang screen. Walang ads ang bersyon para sa Windows.",
 G_A="Kasama sa libreng bersyon ang dalawang focus mode, 3 color theme, at ang pag-adjust ng taas at opacity ng strip. Inaalis ng Pro ang ads at idinaragdag ang lahat ng 10 theme at ang pagpapanatiling nakabukas ng screen.",
 G_W="Kasama sa libreng bersyon ang dalawang mode, settings para sa taas at opacity ng strip, at tatlong theme. Ang Pro ay isang beses na bayad na nagdaragdag ng premium na theme at pagpapanatiling nakabukas ng screen. Walang ads."),
}

# 바뀌기 전 값에 들어 있어야 하는 표지(높이·불투명도를 Pro 쪽에 적은 흔적) — 없으면 그 사이 누가 고친 것이다.
def slots(app_doc, guide_doc):
    a, g = app_doc["apps"], guide_doc["guides"]
    return {
        "RF_F5": (a["readfocus"]["features"], 5),
        "RF_Q2": (a["readfocus"]["faq"][2], "a"),
        "RW_F5": (a["readfocuswin"]["features"], 5),
        "RW_Q2": (a["readfocuswin"]["faq"][2], "a"),
        "G_A": (g["reading-ruler-dyslexia-adhd-android"]["sections"][2]["p"], 0),
        "G_W": (g["reading-ruler-windows"]["sections"][2]["p"], 0),
    }


def main():
    assert len(NEW) == 21, sorted(NEW)
    changed = 0
    for lang, vals in NEW.items():
        pa = os.path.join(ROOT, "i18n", f"{lang}.json")
        pg = os.path.join(ROOT, "i18n", "guides", f"{lang}.json")
        ra, rg = open(pa, encoding="utf-8").read(), open(pg, encoding="utf-8").read()
        da, dg = json.loads(ra), json.loads(rg)
        for key, (obj, idx) in slots(da, dg).items():
            if obj[idx] != vals[key]:
                obj[idx] = vals[key]; changed += 1
        # 원래 파일과 같은 형식으로 쓴다(들여쓰기 2, 한 줄 끝 개행 유무 유지)
        for path, raw, doc in ((pa, ra, da), (pg, rg, dg)):
            indent = 2 if raw.startswith("{\n  ") else (1 if raw.startswith("{\n ") else None)
            out = json.dumps(doc, ensure_ascii=False, indent=indent)
            if raw.endswith("\n"):
                out += "\n"
            open(path, "w", encoding="utf-8", newline="").write(out)
    print(f"{changed} 칸 바꿈")


if __name__ == "__main__":
    sys.exit(main())
