# -*- coding: utf-8 -*-
"""Clipboard+ / FloatNote+ 11/26 출시 맞춤 앱 페이지 문구 갱신 (21개 언어, 한 번만 반영).

- clipboard.features[3]: 기간 필터(오늘·이번 주·이번 달·올해)·종류 필터 명시
- clipboardwin.features[2]: 종류·기간 필터
- floatnote: long 색상 문장(8색+원하는 색·체크리스트) + "다른 기기의 새 메모 띄우기" 문장,
  features[1](8색·체크리스트), features[4](목록에 체크리스트 진행·알림 시각·글자 수), faq[2] 동기화 답 끝에 한 문장
- floatnotewin: long 색상 문장 교체 + 같은 문장, features[3], faq[0] 동기화 답 끝에 한 문장
용어는 앱 strings.xml / AppStrings.<lang>.resx 의 filter_period_* · action_checklist ·
sync_auto_float_title(안드로이드) · Settings_RemoteFloating_Title(Windows) 과 맞췄다.
8번째 색이 차콜이라 Windows 판의 "파스텔" 표현은 뺐다.
"""
import json, os, sys

SITE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 언어별: (안드로이드 라벨, Windows 라벨, 문장 템플릿). 템플릿의 {L} 자리에 라벨이 들어간다.
D = {
"en": dict(
 la="Show new notes from other devices", lw="Show new notes from other devices",
 remote="Turn on “{L}” and a new note you leave floating on one device floats on the other too after sync.",
 cb3="Instant keyword search, filters for links, images, text and pinned clips, and period filters: Today, This week, This month, This year",
 cw2="Android-style UI with light/dark themes, group sidebar, snippets, pin/copy/edit, and search with filters by type (links, images, text, pinned) and period (Today, This week, This month, This year)",
 fn_old="Colors, rich text and inline images keep each note distinct",
 fn_new="Eight colors plus custom colors, rich text, checklists and inline images keep each note distinct",
 fn1="8 sticky-note colors plus custom colors from a color wheel or color code, rich text (bold, italic, underline, strikethrough, text color and size) and checklists you tick off with a tap",
 fn4="Library with instant search, pinning and drag-to-reorder that shows each note's checklist progress (such as 2/5), reminder time and character count — dragging a chip to the bottom zone stashes the note instead of deleting it",
 fw_old="Seven pastel colors, rich text and inline images keep notes apart, a library window handles search, pinning and management",
 fw_new="Eight note colors plus custom colors, rich text, checklists and inline images keep notes apart, a library window handles search, pinning and management and shows each note's checklist progress, reminder time and character count",
 fw3="Rich text — bold, italic, underline, strikethrough, text color and size — with 8 note colors plus custom colors, checklists and inline images",
),
"ko": dict(
 la="다른 기기의 새 메모 띄우기", lw="다른 기기의 새 메모 띄우기",
 remote="“{L}”를 켜 두면 한 기기에서 띄워 둔 새 메모가 동기화 뒤 다른 기기에도 떠오릅니다.",
 cb3="키워드 즉시 검색, 링크·이미지·텍스트·고정 필터와 오늘·이번 주·이번 달·올해 기간 필터",
 cw2="안드로이드 스타일 UI — 라이트/다크 테마, 그룹 사이드바, 스니펫, 핀·복사·편집, 종류(링크·이미지·텍스트·고정)와 기간(오늘·이번 주·이번 달·올해) 필터가 있는 검색",
 fn_old="색상과 서식, 인라인 이미지로 메모를 구분하고",
 fn_new="8색과 원하는 색, 서식, 체크리스트, 인라인 이미지로 메모를 구분하고",
 fn1="스티커 메모 8색에 색상환·색 코드로 원하는 색까지, 서식(굵게·기울임·밑줄·취소선·글자색·글자 크기)과 탭 한 번으로 체크하는 체크리스트",
 fn4="보관함: 즉시 검색, 상단 고정, 드래그로 순서 변경, 메모마다 체크리스트 진행(2/5 등)·알림 시각·글자 수 표시 — 칩을 화면 아래 영역으로 끌면 삭제가 아니라 보관",
 fw_old="파스텔 7색과 서식, 본문 이미지로 메모를 구분하고, 보관함 창이 검색·고정·관리를 맡습니다.",
 fw_new="메모 8색과 원하는 색, 서식, 체크리스트, 본문 이미지로 메모를 구분하고, 보관함 창이 검색·고정·관리를 맡으며 메모마다 체크리스트 진행·알림 시각·글자 수를 보여 줍니다.",
 fw3="서식 — 굵게·기울임·밑줄·취소선, 글자 색과 크기 — 여기에 메모 8색과 원하는 색, 체크리스트, 본문 이미지까지",
),
"ar": dict(
 la="إظهار الملاحظات الجديدة من الأجهزة الأخرى", lw="إظهار الملاحظات الجديدة من الأجهزة الأخرى",
 remote="عند تفعيل «{L}»، تطفو الملاحظة الجديدة التي تتركها طافية على أحد الجهازين على الجهاز الآخر أيضًا بعد المزامنة.",
 cb3="بحث فوري بالكلمة المفتاحية، وفلاتر للروابط والصور والنص والمثبتة، وفلاتر للفترة: اليوم وهذا الأسبوع وهذا الشهر وهذا العام",
 cw2="واجهة على طراز Android مع سمات فاتحة/داكنة وشريط جانبي للمجموعات ومقاطع نصية وتثبيت/نسخ/تعديل، وبحث مع فلاتر حسب النوع (الروابط، الصور، النص، المثبتة) والفترة (اليوم، هذا الأسبوع، هذا الشهر، هذا العام)",
 fn_old="تميّز الألوان والنص المنسّق والصور كل ملاحظة",
 fn_new="تميّز ثمانية ألوان مع ألوان مخصّصة والنص المنسّق وقوائم التحقق والصور كل ملاحظة",
 fn1="8 ألوان للملاحظات وألوان مخصّصة من عجلة الألوان أو برمز اللون، ونص منسّق: عريض ومائل وتسطير وشطب ولون وحجم النص، وقوائم تحقق تؤشّر عناصرها بنقرة",
 fn4="أرشيف مع بحث فوري وتثبيت وإعادة ترتيب بالسحب، يعرض لكل ملاحظة تقدّم قائمة التحقق (مثل 2/5) ووقت التذكير وعدد الأحرف؛ سحب المربّع إلى المنطقة السفلية يحفظ الملاحظة بدل حذفها",
 fw_old="تميّز الملاحظات سبعة ألوان باستيل ونص منسّق وصور داخل الملاحظة، بينما تتولى نافذة الأرشيف البحث والتثبيت والتنظيم",
 fw_new="تميّز الملاحظات ثمانية ألوان للملاحظات مع ألوان مخصّصة ونص منسّق وقوائم تحقق وصور داخل الملاحظة، بينما تتولى نافذة الأرشيف البحث والتثبيت والتنظيم وتعرض لكل ملاحظة تقدّم قائمة التحقق ووقت التذكير وعدد الأحرف",
 fw3="نص منسّق — عريض ومائل وتسطير وشطب ولون وحجم النص — مع 8 ألوان للملاحظات وألوان مخصّصة وقوائم تحقق وصور داخلها",
),
"de": dict(
 la="Neue Notizen anderer Geräte anzeigen", lw="Neue Notizen von anderen Geräten anzeigen",
 remote="Ist „{L}“ eingeschaltet, schwebt eine neue Notiz, die du auf einem Gerät schweben lässt, nach der Synchronisierung auch auf dem anderen.",
 cb3="Sofortsuche nach Stichwort, Filter für Links, Bilder, Text und Angeheftetes sowie Zeitraumfilter: Heute, Diese Woche, Dieser Monat, Dieses Jahr",
 cw2="UI im Android-Stil mit hellen/dunklen Designs, Gruppen-Seitenleiste, Snippets, Anheften/Kopieren/Bearbeiten sowie Suche mit Filtern nach Typ (Links, Bilder, Text, Angeheftet) und Zeitraum (Heute, Diese Woche, Dieser Monat, Dieses Jahr)",
 fn_old="Farben, Rich-Text und Bilder halten die Notizen auseinander",
 fn_new="Acht Farben plus eigene Farben, Rich-Text, Checklisten und Bilder halten die Notizen auseinander",
 fn1="8 Haftnotiz-Farben plus eigene Farben per Farbrad oder Farbcode, Rich-Text (fett, kursiv, unterstrichen, durchgestrichen, Textfarbe und -größe) und Checklisten zum Abhaken per Tipp",
 fn4="Archiv mit sofortiger Suche, Anheften und Neuordnen per Ziehen, das bei jeder Notiz Checklisten-Fortschritt (etwa 2/5), Erinnerungszeit und Zeichenzahl zeigt – ein Chip in die Zone am unteren Rand legt die Notiz ab, statt sie zu löschen",
 fw_old="Sieben Pastellfarben, Rich-Text und Bilder in der Notiz halten sie auseinander, ein Archivfenster übernimmt Suche, Anheften und Verwaltung",
 fw_new="Acht Notizfarben plus eigene Farben, Rich-Text, Checklisten und Bilder in der Notiz halten sie auseinander, ein Archivfenster übernimmt Suche, Anheften und Verwaltung und zeigt bei jeder Notiz Checklisten-Fortschritt, Erinnerungszeit und Zeichenzahl",
 fw3="Rich-Text – fett, kursiv, unterstrichen, durchgestrichen, Textfarbe und -größe – dazu 8 Notizfarben plus eigene Farben, Checklisten und Bilder in der Notiz",
),
"es": dict(
 la="Mostrar notas nuevas de otros dispositivos", lw="Mostrar notas nuevas de otros dispositivos",
 remote="Con «{L}» activado, una nota nueva que dejas flotando en un dispositivo también flota en el otro tras sincronizar.",
 cb3="Búsqueda instantánea por palabra clave, filtros de enlaces, imágenes, texto y fijados, y filtros de periodo: Hoy, Esta semana, Este mes, Este año",
 cw2="Interfaz al estilo de Android con temas claro/oscuro, barra lateral de grupos, fragmentos, anclar/copiar/editar y búsqueda con filtros por tipo (enlaces, imágenes, texto, fijados) y periodo (Hoy, Esta semana, Este mes, Este año)",
 fn_old="Los colores, el texto enriquecido y las imágenes distinguen cada nota",
 fn_new="Ocho colores más colores personalizados, el texto enriquecido, las listas de verificación y las imágenes distinguen cada nota",
 fn1="8 colores de nota más colores personalizados con la rueda de color o un código, texto enriquecido (negrita, cursiva, subrayado, tachado, color y tamaño del texto) y listas de verificación que se marcan con un toque",
 fn4="Archivo con búsqueda instantánea, notas fijadas y reordenación arrastrando, que muestra en cada nota el progreso de la lista (como 2/5), la hora del recordatorio y el número de caracteres; llevar un chip a la zona inferior guarda la nota en lugar de borrarla",
 fw_old="Siete colores pastel, texto enriquecido e imágenes dentro de la nota las distinguen; una ventana de archivo se encarga de buscar, fijar y organizar",
 fw_new="Ocho colores de nota más colores personalizados, texto enriquecido, listas de verificación e imágenes dentro de la nota las distinguen; una ventana de archivo se encarga de buscar, fijar y organizar, y muestra en cada nota el progreso de la lista, la hora del recordatorio y el número de caracteres",
 fw3="Texto enriquecido —negrita, cursiva, subrayado, tachado, color y tamaño— con 8 colores de nota más colores personalizados, listas de verificación e imágenes dentro de la nota",
),
"fil": dict(
 la="Ipakita ang mga bagong note mula sa ibang device", lw="Ipakita ang mga bagong tala mula sa ibang device",
 remote="Kapag naka-on ang “{L}”, ang bagong notang iniwan mong nakalutang sa isang device ay lulutang din sa isa pa pagkatapos ng sync.",
 cb3="Agarang paghahanap ayon sa keyword, filter para sa mga link, larawan, teksto, at naka-pin, at filter ng panahon: Ngayong araw, Ngayong linggo, Ngayong buwan, Ngayong taon",
 cw2="Android-style na UI na may light/dark theme, group sidebar, snippet, pin/copy/edit, at search na may filter ayon sa uri (link, larawan, teksto, naka-pin) at panahon (Ngayong araw, Ngayong linggo, Ngayong buwan, Ngayong taon)",
 fn_old="Ang mga kulay, rich text, at larawan ang nagpapaiba sa bawat nota",
 fn_new="Ang 8 kulay at custom na kulay, rich text, checklist, at larawan ang nagpapaiba sa bawat nota",
 fn1="8 kulay ng nota at custom na kulay mula sa color wheel o color code, rich text (bold, italic, underline, strikethrough, kulay at laki ng teksto), at checklist na nati-tick sa isang tap",
 fn4="Aklatan na may agarang paghahanap, pag-pin, at pag-aayos sa pag-drag, na nagpapakita ng progreso ng checklist (gaya ng 2/5), oras ng paalala, at bilang ng character ng bawat nota; ang paghila ng chip sa ibabang bahagi ay nagtatago ng nota, hindi nagbubura",
 fw_old="Pitong pastel na kulay, rich text, at larawan sa loob ng nota ang nagpapaiba sa bawat isa, ang library window ang humahawak sa paghahanap, pag-pin, at pamamahala",
 fw_new="Walong kulay ng nota at custom na kulay, rich text, checklist, at larawan sa loob ng nota ang nagpapaiba sa bawat isa, ang library window ang humahawak sa paghahanap, pag-pin, at pamamahala at nagpapakita ng progreso ng checklist, oras ng paalala, at bilang ng character ng bawat nota",
 fw3="Rich text — bold, italic, underline, strikethrough, kulay at laki ng teksto — kasama ang 8 kulay ng nota at custom na kulay, checklist, at larawan sa loob ng nota",
),
"fr": dict(
 la="Afficher les nouvelles notes des autres appareils", lw="Afficher les nouvelles notes des autres appareils",
 remote="Avec « {L} » activé, une nouvelle note laissée flottante sur un appareil flotte aussi sur l’autre après la synchronisation.",
 cb3="Recherche instantanée par mot-clé, filtres liens, images, texte et épinglés, et filtres de période : Aujourd’hui, Cette semaine, Ce mois-ci, Cette année",
 cw2="Interface de style Android avec thèmes clair/sombre, barre latérale de groupes, extraits, épingler/copier/modifier et recherche avec filtres par type (liens, images, texte, épinglés) et par période (Aujourd’hui, Cette semaine, Ce mois-ci, Cette année)",
 fn_old="Les couleurs, le texte enrichi et les images distinguent chaque note",
 fn_new="Huit couleurs plus des couleurs personnalisées, le texte enrichi, les listes à cocher et les images distinguent chaque note",
 fn1="8 couleurs de pense-bête plus des couleurs personnalisées via la roue chromatique ou un code couleur, texte enrichi (gras, italique, souligné, barré, couleur et taille du texte) et listes à cocher d’un simple appui",
 fn4="Bibliothèque avec recherche instantanée, épinglage et réorganisation par glisser, qui affiche pour chaque note la progression de la liste (par ex. 2/5), l’heure du rappel et le nombre de caractères ; amener une pastille dans la zone du bas range la note au lieu de la supprimer",
 fw_old="Sept couleurs pastel, le texte enrichi et les images dans la note les distinguent, une fenêtre bibliothèque prend en charge la recherche, l'épinglage et la gestion",
 fw_new="Huit couleurs de note plus des couleurs personnalisées, le texte enrichi, les listes à cocher et les images dans la note les distinguent, une fenêtre bibliothèque prend en charge la recherche, l'épinglage et la gestion et affiche pour chaque note la progression de la liste, l’heure du rappel et le nombre de caractères",
 fw3="Texte enrichi — gras, italique, souligné, barré, couleur et taille — avec 8 couleurs de note plus des couleurs personnalisées, des listes à cocher et des images dans la note",
),
"hi": dict(
 la="दूसरे डिवाइस के नए नोट दिखाएँ", lw="दूसरे डिवाइस के नए नोट दिखाएँ",
 remote="“{L}” चालू होने पर, एक डिवाइस पर तैरता छोड़ा गया नया नोट सिंक के बाद दूसरे डिवाइस पर भी तैरने लगता है।",
 cb3="कीवर्ड से तुरंत सर्च, लिंक, इमेज, टेक्स्ट और पिन किए गए आइटम के फ़िल्टर, और अवधि फ़िल्टर: आज, इस सप्ताह, इस महीने, इस साल",
 cw2="Android-स्टाइल UI, लाइट/डार्क थीम, ग्रुप साइडबार, स्निपेट, पिन/कॉपी/एडिट, और प्रकार (लिंक, इमेज, टेक्स्ट, पिन किए गए) व अवधि (आज, इस सप्ताह, इस महीने, इस साल) फ़िल्टर वाला सर्च",
 fn_old="रंग, रिच टेक्स्ट और तस्वीरें हर नोट को अलग पहचान देती हैं",
 fn_new="8 रंग और कस्टम रंग, रिच टेक्स्ट, चेकलिस्ट और तस्वीरें हर नोट को अलग पहचान देती हैं",
 fn1="नोट के 8 रंग, कलर व्हील या कलर कोड से कस्टम रंग, रिच टेक्स्ट (बोल्ड, इटैलिक, अंडरलाइन, स्ट्राइकथ्रू, टेक्स्ट रंग और आकार) और एक टैप से टिक होने वाली चेकलिस्ट",
 fn4="तुरंत खोज, पिन और खींचकर क्रम बदलने वाला संग्रह, जो हर नोट की चेकलिस्ट प्रगति (जैसे 2/5), रिमाइंडर समय और अक्षर संख्या दिखाता है; चिप को नीचे के क्षेत्र में ले जाना नोट को हटाता नहीं, संभालकर रखता है",
 fw_old="सात पेस्टल रंग, रिच टेक्स्ट और नोट के भीतर तस्वीरें नोट्स को अलग पहचान देती हैं, संग्रह विंडो खोज, पिन और प्रबंधन संभालती है",
 fw_new="नोट के आठ रंग और कस्टम रंग, रिच टेक्स्ट, चेकलिस्ट और नोट के भीतर तस्वीरें नोट्स को अलग पहचान देती हैं, संग्रह विंडो खोज, पिन और प्रबंधन संभालती है और हर नोट की चेकलिस्ट प्रगति, रिमाइंडर समय और अक्षर संख्या दिखाती है",
 fw3="रिच टेक्स्ट — बोल्ड, इटैलिक, अंडरलाइन, स्ट्राइकथ्रू, टेक्स्ट रंग और आकार — साथ में नोट के 8 रंग, कस्टम रंग, चेकलिस्ट और नोट के भीतर तस्वीरें",
),
"id": dict(
 la="Tampilkan catatan baru dari perangkat lain", lw="Tampilkan catatan baru dari perangkat lain",
 remote="Dengan “{L}” aktif, catatan baru yang Anda biarkan mengambang di satu perangkat juga akan mengambang di perangkat lain setelah sinkronisasi.",
 cb3="Pencarian instan dengan kata kunci, filter tautan, gambar, teks, dan yang disematkan, serta filter periode: Hari ini, Minggu ini, Bulan ini, Tahun ini",
 cw2="UI bergaya Android dengan tema terang/gelap, sidebar grup, snippet, pin/salin/edit, dan pencarian dengan filter jenis (tautan, gambar, teks, disematkan) dan periode (Hari ini, Minggu ini, Bulan ini, Tahun ini)",
 fn_old="Warna, teks kaya, dan gambar membedakan tiap catatan",
 fn_new="Delapan warna plus warna kustom, teks kaya, daftar periksa, dan gambar membedakan tiap catatan",
 fn1="8 warna catatan plus warna kustom dari roda warna atau kode warna, teks kaya (tebal, miring, garis bawah, coret, warna dan ukuran teks), dan daftar periksa yang dicentang dengan sekali ketuk",
 fn4="Pustaka dengan pencarian seketika, penyematan, dan pengurutan dengan menyeret, yang menampilkan progres daftar periksa (misalnya 2/5), waktu pengingat, dan jumlah karakter tiap catatan; menyeret chip ke area bawah menyimpan catatan, bukan menghapusnya",
 fw_old="Tujuh warna pastel, teks kaya, dan gambar di dalam catatan membedakan satu dari yang lain; jendela pustaka menangani pencarian, penyematan, dan pengelolaan",
 fw_new="Delapan warna catatan plus warna kustom, teks kaya, daftar periksa, dan gambar di dalam catatan membedakan satu dari yang lain; jendela pustaka menangani pencarian, penyematan, dan pengelolaan serta menampilkan progres daftar periksa, waktu pengingat, dan jumlah karakter tiap catatan",
 fw3="Teks kaya — tebal, miring, garis bawah, coret, warna dan ukuran teks — dengan 8 warna catatan plus warna kustom, daftar periksa, dan gambar di dalam catatan",
),
"it": dict(
 la="Mostra le nuove note degli altri dispositivi", lw="Mostra le nuove note dagli altri dispositivi",
 remote="Con «{L}» attivo, una nuova nota lasciata fluttuante su un dispositivo fluttua anche sull'altro dopo la sincronizzazione.",
 cb3="Ricerca immediata per parola chiave, filtri per link, immagini, testo e fissati, e filtri per periodo: Oggi, Questa settimana, Questo mese, Quest’anno",
 cw2="Interfaccia in stile Android con temi chiaro/scuro, barra laterale dei gruppi, snippet, funzioni di aggiungi/copia/modifica e ricerca con filtri per tipo (link, immagini, testo, fissati) e periodo (Oggi, Questa settimana, Questo mese, Quest’anno)",
 fn_old="Colori, testo ricco e immagini distinguono ogni nota",
 fn_new="Otto colori più colori personalizzati, testo ricco, liste di controllo e immagini distinguono ogni nota",
 fn1="8 colori delle note più colori personalizzati dalla ruota dei colori o da un codice, testo ricco (grassetto, corsivo, sottolineato, barrato, colore e dimensione del testo) e liste di controllo da spuntare con un tocco",
 fn4="Archivio con ricerca istantanea, note fissate e riordino trascinando, che mostra per ogni nota l'avanzamento della lista (ad es. 2/5), l'orario del promemoria e il numero di caratteri; portare un chip nell'area in basso mette via la nota invece di eliminarla",
 fw_old="Sette colori pastello, testo ricco e immagini dentro la nota le distinguono, una finestra archivio si occupa di ricerca, note fissate e gestione",
 fw_new="Otto colori delle note più colori personalizzati, testo ricco, liste di controllo e immagini dentro la nota le distinguono, una finestra archivio si occupa di ricerca, note fissate e gestione e mostra per ogni nota l'avanzamento della lista, l'orario del promemoria e il numero di caratteri",
 fw3="Testo ricco — grassetto, corsivo, sottolineato, barrato, colore e dimensione — con 8 colori delle note più colori personalizzati, liste di controllo e immagini dentro la nota",
),
"ja": dict(
 la="他のデバイスの新しいメモを表示", lw="他のデバイスの新しいメモを表示",
 remote="「{L}」をオンにすると、片方のデバイスで浮かべておいた新しいメモが、同期後にもう片方でも浮かびます。",
 cb3="キーワードで瞬時に検索、リンク・画像・テキスト・固定の絞り込みと、今日・今週・今月・今年の期間フィルター",
 cw2="Androidスタイルのライト／ダークテーマUI、グループサイドバー、スニペット、ピン／コピー／編集、種類（リンク・画像・テキスト・固定）と期間（今日・今週・今月・今年）で絞り込める検索",
 fn_old="色と書式、インライン画像でメモを見分けやすくし",
 fn_new="8色と好きな色、書式、チェックリスト、インライン画像でメモを見分けやすくし",
 fn1="付箋の8色に加え、カラーホイールやカラーコードで好きな色も。書式（太字・斜体・下線・取り消し線・文字色・文字サイズ）と、タップでチェックできるチェックリスト",
 fn4="保管庫: 即時検索、上部にピン留め、ドラッグで並べ替え。メモごとにチェックリストの進み具合（2/5 など）・リマインダー時刻・文字数を表示。チップを画面下部の領域へ運ぶと削除ではなく保管",
 fw_old="パステル7色と書式、本文中の画像でメモを見分け、保管庫ウィンドウが検索・ピン留め・管理を担います。",
 fw_new="メモ8色と好きな色、書式、チェックリスト、本文中の画像でメモを見分け、保管庫ウィンドウが検索・ピン留め・管理を担い、メモごとにチェックリストの進み具合・リマインダー時刻・文字数を表示します。",
 fw3="書式 — 太字・斜体・下線・取り消し線、文字色と文字サイズ — に加えてメモ8色と好きな色、チェックリスト、本文中の画像",
),
"ms": dict(
 la="Tunjukkan nota baharu daripada peranti lain", lw="Tunjukkan nota baharu daripada peranti lain",
 remote="Dengan “{L}” dihidupkan, nota baharu yang anda biarkan terapung pada satu peranti turut terapung pada peranti lain selepas penyegerakan.",
 cb3="Carian segera mengikut kata kunci, penapis pautan, imej, teks dan yang disemat, serta penapis tempoh: Hari ini, Minggu ini, Bulan ini, Tahun ini",
 cw2="UI bergaya Android dengan tema cerah/gelap, bar sisi kumpulan, snippet, pin/salin/edit, dan carian dengan penapis jenis (pautan, imej, teks, disemat) dan tempoh (Hari ini, Minggu ini, Bulan ini, Tahun ini)",
 fn_old="Warna, teks kaya dan gambar membezakan setiap nota",
 fn_new="Lapan warna serta warna tersuai, teks kaya, senarai semak dan gambar membezakan setiap nota",
 fn1="8 warna nota serta warna tersuai daripada roda warna atau kod warna, teks kaya (tebal, condong, garis bawah, garis lorek, warna dan saiz teks), dan senarai semak yang ditanda dengan satu ketikan",
 fn4="Simpanan dengan carian serta-merta, penyematan dan susunan seret, yang menunjukkan kemajuan senarai semak (seperti 2/5), masa peringatan dan bilangan aksara setiap nota; menyeret cip ke kawasan bawah menyimpan nota, bukan memadamnya",
 fw_old="Tujuh warna pastel, teks kaya dan gambar dalam nota membezakan setiap satu; tetingkap simpanan menguruskan carian, penyematan dan pengurusan",
 fw_new="Lapan warna nota serta warna tersuai, teks kaya, senarai semak dan gambar dalam nota membezakan setiap satu; tetingkap simpanan menguruskan carian, penyematan dan pengurusan serta menunjukkan kemajuan senarai semak, masa peringatan dan bilangan aksara setiap nota",
 fw3="Teks kaya — tebal, condong, garis bawah, garis lorek, warna dan saiz teks — dengan 8 warna nota serta warna tersuai, senarai semak dan gambar dalam nota",
),
"nl": dict(
 la="Nieuwe notities van andere apparaten tonen", lw="Nieuwe notities van andere apparaten tonen",
 remote="Met ‘{L}’ aan zweeft een nieuwe notitie die je op het ene apparaat laat zweven na synchronisatie ook op het andere.",
 cb3="Direct zoeken op trefwoord, filters voor links, afbeeldingen, tekst en vastgezet, en periodefilters: Vandaag, Deze week, Deze maand, Dit jaar",
 cw2="UI in Android-stijl met lichte/donkere thema's, groepszijbalk, snippets, vastmaken/kopiëren/bewerken en zoeken met filters op type (links, afbeeldingen, tekst, vastgezet) en periode (Vandaag, Deze week, Deze maand, Dit jaar)",
 fn_old="Kleuren, tekstopmaak en afbeeldingen houden je notities uit elkaar",
 fn_new="Acht kleuren plus eigen kleuren, tekstopmaak, checklists en afbeeldingen houden je notities uit elkaar",
 fn1="8 notitiekleuren plus eigen kleuren via een kleurenwiel of kleurcode, tekstopmaak (vet, cursief, onderstreept, doorgehaald, tekstkleur en -grootte) en checklists die je met één tik afvinkt",
 fn4="Archief met directe zoekfunctie, vastpinnen en slepen om te ordenen, dat per notitie de voortgang van de checklist (zoals 2/5), de herinneringstijd en het aantal tekens toont; een chip naar de zone onderaan slepen bergt de notitie op in plaats van hem te verwijderen",
 fw_old="Zeven pasteltinten, tekstopmaak en afbeeldingen in de notitie houden je notities uit elkaar, een archiefvenster verzorgt zoeken, vastpinnen en beheren",
 fw_new="Acht notitiekleuren plus eigen kleuren, tekstopmaak, checklists en afbeeldingen in de notitie houden je notities uit elkaar, een archiefvenster verzorgt zoeken, vastpinnen en beheren en toont per notitie de voortgang van de checklist, de herinneringstijd en het aantal tekens",
 fw3="Tekstopmaak — vet, cursief, onderstreept, doorgehaald, tekstkleur en -grootte — met 8 notitiekleuren plus eigen kleuren, checklists en afbeeldingen in de notitie",
),
"pl": dict(
 la="Pokazuj nowe notatki z innych urządzeń", lw="Pokazuj nowe notatki z innych urządzeń",
 remote="Gdy opcja „{L}” jest włączona, nowa notatka pozostawiona na wierzchu na jednym urządzeniu po synchronizacji pojawia się na wierzchu także na drugim.",
 cb3="Natychmiastowe wyszukiwanie po słowie kluczowym, filtry linków, obrazów, tekstu i przypiętych oraz filtry okresu: Dzisiaj, Ten tydzień, Ten miesiąc, Ten rok",
 cw2="Interfejs w stylu Androida z jasnym/ciemnym motywem, paskiem bocznym grup, fragmentami, przypinaniem/kopiowaniem/edycją oraz wyszukiwaniem z filtrami typu (linki, obrazy, tekst, przypięte) i okresu (Dzisiaj, Ten tydzień, Ten miesiąc, Ten rok)",
 fn_old="Kolory, formatowanie i obrazy odróżniają notatki",
 fn_new="Osiem kolorów plus własne kolory, formatowanie, listy kontrolne i obrazy odróżniają notatki",
 fn1="8 kolorów karteczek plus własne kolory z koła barw lub kodu koloru, formatowanie (pogrubienie, kursywa, podkreślenie, przekreślenie, kolor i rozmiar tekstu) oraz listy kontrolne odhaczane jednym dotknięciem",
 fn4="Archiwum z natychmiastowym wyszukiwaniem, przypinaniem i zmianą kolejności przeciąganiem, które przy każdej notatce pokazuje postęp listy kontrolnej (np. 2/5), godzinę przypomnienia i liczbę znaków; przeciągnięcie kafelka do strefy na dole chowa notatkę, a nie usuwa",
 fw_old="Siedem pastelowych kolorów, formatowanie i obrazy w notatce pozwalają je odróżnić, okno archiwum przejmuje wyszukiwanie, przypinanie i porządkowanie",
 fw_new="Osiem kolorów notatek plus własne kolory, formatowanie, listy kontrolne i obrazy w notatce pozwalają je odróżnić, okno archiwum przejmuje wyszukiwanie, przypinanie i porządkowanie oraz pokazuje przy każdej notatce postęp listy kontrolnej, godzinę przypomnienia i liczbę znaków",
 fw3="Formatowanie — pogrubienie, kursywa, podkreślenie, przekreślenie, kolor i rozmiar tekstu — oraz 8 kolorów notatek plus własne kolory, listy kontrolne i obrazy w notatce",
),
"pt": dict(
 la="Mostrar notas novas de outros dispositivos", lw="Mostrar notas novas de outros dispositivos",
 remote="Com “{L}” ativado, uma nota nova que você deixa flutuando em um aparelho também flutua no outro após a sincronização.",
 cb3="Busca instantânea por palavra-chave, filtros de links, imagens, texto e fixados, e filtros de período: Hoje, Esta semana, Este mês, Este ano",
 cw2="Interface no estilo Android com temas claro/escuro, barra lateral de grupos, snippets, fixar/copiar/editar e pesquisa com filtros por tipo (links, imagens, texto, fixados) e período (Hoje, Esta semana, Este mês, Este ano)",
 fn_old="Cores, texto rico e imagens diferenciam cada nota",
 fn_new="Oito cores mais cores personalizadas, texto rico, listas de verificação e imagens diferenciam cada nota",
 fn1="8 cores de nota mais cores personalizadas pela roda de cores ou código de cor, texto rico (negrito, itálico, sublinhado, tachado, cor e tamanho do texto) e listas de verificação marcadas com um toque",
 fn4="Acervo com busca instantânea, notas fixadas e reordenação arrastando, que mostra em cada nota o progresso da lista (como 2/5), o horário do lembrete e o número de caracteres; levar um chip à área inferior guarda a nota em vez de excluí-la",
 fw_old="Sete cores pastel, texto rico e imagens dentro da nota separam uma da outra; uma janela de acervo cuida de buscar, fixar e organizar",
 fw_new="Oito cores de nota mais cores personalizadas, texto rico, listas de verificação e imagens dentro da nota separam uma da outra; uma janela de acervo cuida de buscar, fixar e organizar e mostra em cada nota o progresso da lista, o horário do lembrete e o número de caracteres",
 fw3="Texto rico — negrito, itálico, sublinhado, tachado, cor e tamanho — com 8 cores de nota mais cores personalizadas, listas de verificação e imagens dentro da nota",
),
"ru": dict(
 la="Показывать новые заметки с других устройств", lw="Показывать новые заметки с других устройств",
 remote="Если включить «{L}», новая заметка, оставленная поверх экрана на одном устройстве, после синхронизации появится поверх экрана и на другом.",
 cb3="Мгновенный поиск по ключевому слову, фильтры ссылок, изображений, текста и закреплённых, а также фильтры по периоду: Сегодня, На этой неделе, В этом месяце, В этом году",
 cw2="Интерфейс в стиле Android со светлой/тёмной темами, боковой панелью групп, сниппетами, закреплением/копированием/редактированием и поиском с фильтрами по типу (ссылки, изображения, текст, закреплённые) и периоду (Сегодня, Эта неделя, Этот месяц, Этот год)",
 fn_old="Цвета, форматирование и изображения помогают различать заметки",
 fn_new="Восемь цветов плюс свои цвета, форматирование, чек-листы и изображения помогают различать заметки",
 fn1="8 цветов стикеров плюс свои цвета с цветового круга или по коду, форматирование (жирный, курсив, подчёркивание, зачёркивание, цвет и размер текста) и чек-листы, где пункт отмечается одним касанием",
 fn4="Хранилище с мгновенным поиском, закреплением и сортировкой перетаскиванием, где у каждой заметки видны прогресс чек-листа (например, 2/5), время напоминания и число символов; перенос чипа в нижнюю зону убирает заметку в хранилище, а не удаляет её",
 fw_old="Семь пастельных цветов, форматирование и изображения внутри заметки помогают их различать, окно хранилища берёт на себя поиск, закрепление и управление",
 fw_new="Восемь цветов заметок плюс свои цвета, форматирование, чек-листы и изображения внутри заметки помогают их различать, окно хранилища берёт на себя поиск, закрепление и управление и показывает у каждой заметки прогресс чек-листа, время напоминания и число символов",
 fw3="Форматирование — жирный, курсив, подчёркивание, зачёркивание, цвет и размер текста — плюс 8 цветов заметок, свои цвета, чек-листы и изображения в заметке",
),
"th": dict(
 la="แสดงโน้ตใหม่จากอุปกรณ์อื่น", lw="แสดงโน้ตใหม่จากอุปกรณ์อื่น",
 remote="เมื่อเปิด “{L}” โน้ตใหม่ที่ปล่อยลอยไว้บนอุปกรณ์หนึ่งจะลอยขึ้นบนอีกเครื่องด้วยหลังซิงก์",
 cb3="ค้นหาด้วยคีย์เวิร์ดได้ทันที ตัวกรองลิงก์ รูปภาพ ข้อความ และรายการที่ปักหมุด พร้อมตัวกรองช่วงเวลา: วันนี้ สัปดาห์นี้ เดือนนี้ ปีนี้",
 cw2="UI สไตล์ Android พร้อมธีมสว่าง/มืด แถบข้างกลุ่ม สนิปเป็ต ปักหมุด/คัดลอก/แก้ไข และการค้นหาพร้อมตัวกรองตามประเภท (ลิงก์ รูปภาพ ข้อความ ปักหมุด) และช่วงเวลา (วันนี้ สัปดาห์นี้ เดือนนี้ ปีนี้)",
 fn_old="สี ข้อความจัดรูปแบบ และรูปภาพช่วยแยกแต่ละโน้ตออกจากกัน",
 fn_new="8 สีพร้อมสีที่กำหนดเอง ข้อความจัดรูปแบบ รายการตรวจสอบ และรูปภาพช่วยแยกแต่ละโน้ตออกจากกัน",
 fn1="สีโน้ต 8 สีและสีที่กำหนดเองจากวงล้อสีหรือรหัสสี ข้อความจัดรูปแบบ (ตัวหนา เอียง ขีดเส้นใต้ ขีดฆ่า สีและขนาดตัวอักษร) และรายการตรวจสอบที่ติ๊กได้ด้วยการแตะครั้งเดียว",
 fn4="คลังโน้ตพร้อมค้นหาทันที ปักหมุด และลากจัดเรียง แสดงความคืบหน้ารายการตรวจสอบ (เช่น 2/5) เวลาแจ้งเตือน และจำนวนตัวอักษรของแต่ละโน้ต การลากชิปไปยังพื้นที่ด้านล่างคือการเก็บโน้ต ไม่ใช่ลบ",
 fw_old="สีพาสเทล 7 สี ข้อความจัดรูปแบบ และรูปภาพในโน้ตช่วยแยกแต่ละใบออกจากกัน ส่วนหน้าต่างคลังดูแลการค้นหา ปักหมุด และจัดการ",
 fw_new="สีโน้ต 8 สีพร้อมสีที่กำหนดเอง ข้อความจัดรูปแบบ รายการตรวจสอบ และรูปภาพในโน้ตช่วยแยกแต่ละใบออกจากกัน ส่วนหน้าต่างคลังดูแลการค้นหา ปักหมุด และจัดการ พร้อมแสดงความคืบหน้ารายการตรวจสอบ เวลาแจ้งเตือน และจำนวนตัวอักษรของแต่ละโน้ต",
 fw3="ข้อความจัดรูปแบบ — ตัวหนา เอียง ขีดเส้นใต้ ขีดฆ่า สีและขนาดตัวอักษร — พร้อมสีโน้ต 8 สี สีที่กำหนดเอง รายการตรวจสอบ และรูปภาพในโน้ต",
),
"tr": dict(
 la="Diğer cihazlardaki yeni notları göster", lw="Diğer cihazlardaki yeni notları göster",
 remote="“{L}” açıkken bir cihazda yüzer bıraktığınız yeni not, senkronizasyondan sonra diğer cihazda da yüzer.",
 cb3="Anahtar kelimeyle anında arama, bağlantı, görsel, metin ve sabitlenenler için filtreler ve dönem filtreleri: Bugün, Bu hafta, Bu ay, Bu yıl",
 cw2="Açık/koyu temalar, grup kenar çubuğu, snippet'ler, sabitleme/kopyalama/düzenleme ve türe (bağlantılar, görseller, metin, sabitlenenler) ve döneme (Bugün, Bu hafta, Bu ay, Bu yıl) göre filtreli arama içeren Android tarzı arayüz",
 fn_old="Renkler, zengin metin ve görseller notları birbirinden ayırır",
 fn_new="Sekiz renk ve özel renkler, zengin metin, kontrol listeleri ve görseller notları birbirinden ayırır",
 fn1="8 not rengi ve renk çarkından ya da renk koduyla özel renkler, zengin metin (kalın, italik, altı çizili, üstü çizili, metin rengi ve boyutu) ve tek dokunuşla işaretlenen kontrol listeleri",
 fn4="Anında arama, sabitleme ve sürükleyerek sıralama sunan, her notun kontrol listesi ilerlemesini (ör. 2/5), hatırlatma saatini ve karakter sayısını gösteren arşiv; çipi alttaki bölgeye bırakmak notu silmez, kaldırır",
 fw_old="Yedi pastel renk, zengin metin ve not içi görseller notları birbirinden ayırır; arşiv penceresi arama, sabitleme ve düzeni üstlenir.",
 fw_new="Sekiz not rengi ve özel renkler, zengin metin, kontrol listeleri ve not içi görseller notları birbirinden ayırır; arşiv penceresi arama, sabitleme ve düzeni üstlenir, her notun kontrol listesi ilerlemesini, hatırlatma saatini ve karakter sayısını gösterir.",
 fw3="Zengin metin — kalın, italik, altı çizili, üstü çizili, metin rengi ve boyutu — ayrıca 8 not rengi, özel renkler, kontrol listeleri ve not içi görseller",
),
"uk": dict(
 la="Показувати нові нотатки з інших пристроїв", lw="Показувати нові нотатки з інших пристроїв",
 remote="Якщо ввімкнути «{L}», нова нотатка, залишена поверх екрана на одному пристрої, після синхронізації з'явиться поверх екрана й на іншому.",
 cb3="Миттєвий пошук за ключовим словом, фільтри посилань, зображень, тексту й закріплених, а також фільтри за періодом: Сьогодні, Цього тижня, Цього місяця, Цього року",
 cw2="Інтерфейс у стилі Android зі світлою/темною темами, бічною панеллю груп, сніпетами, закріпленням/копіюванням/редагуванням і пошуком із фільтрами за типом (посилання, зображення, текст, закріплені) та періодом (Сьогодні, Цей тиждень, Цей місяць, Цей рік)",
 fn_old="Кольори, форматування та зображення допомагають розрізняти нотатки",
 fn_new="Вісім кольорів плюс власні кольори, форматування, чек-листи та зображення допомагають розрізняти нотатки",
 fn1="8 кольорів стікерів плюс власні кольори з колірного кола або за кодом, форматування (жирний, курсив, підкреслення, закреслення, колір і розмір тексту) і чек-листи, де пункт позначається одним дотиком",
 fn4="Сховище з миттєвим пошуком, закріпленням і впорядкуванням перетягуванням, де в кожної нотатки видно прогрес чек-листа (наприклад, 2/5), час нагадування й кількість символів; перенесення чипа в нижню зону ховає нотатку, а не видаляє її",
 fw_old="Сім пастельних кольорів, форматування та зображення всередині нотатки допомагають їх розрізняти, вікно сховища бере на себе пошук, закріплення й керування",
 fw_new="Вісім кольорів нотаток плюс власні кольори, форматування, чек-листи та зображення всередині нотатки допомагають їх розрізняти, вікно сховища бере на себе пошук, закріплення й керування та показує в кожної нотатки прогрес чек-листа, час нагадування й кількість символів",
 fw3="Форматування — жирний, курсив, підкреслення, закреслення, колір і розмір тексту — плюс 8 кольорів нотаток, власні кольори, чек-листи й зображення в нотатці",
),
"vi": dict(
 la="Hiện ghi chú mới từ thiết bị khác", lw="Hiện ghi chú mới từ thiết bị khác",
 remote="Khi bật “{L}”, ghi chú mới bạn để nổi trên một thiết bị cũng sẽ nổi trên thiết bị kia sau khi đồng bộ.",
 cb3="Tìm kiếm tức thì theo từ khóa, bộ lọc liên kết, hình ảnh, văn bản và mục đã ghim, cùng bộ lọc thời gian: Hôm nay, Tuần này, Tháng này, Năm nay",
 cw2="Giao diện kiểu Android với chủ đề sáng/tối, thanh bên nhóm, snippet, ghim/sao chép/chỉnh sửa và tìm kiếm có bộ lọc theo loại (liên kết, hình ảnh, văn bản, đã ghim) và thời gian (Hôm nay, Tuần này, Tháng này, Năm nay)",
 fn_old="Màu sắc, định dạng và hình ảnh giúp phân biệt từng ghi chú",
 fn_new="Tám màu cùng màu tùy chỉnh, định dạng, danh sách kiểm tra và hình ảnh giúp phân biệt từng ghi chú",
 fn1="8 màu ghi chú cùng màu tùy chỉnh từ bánh xe màu hoặc mã màu, định dạng (in đậm, in nghiêng, gạch chân, gạch ngang, màu và cỡ chữ) và danh sách kiểm tra đánh dấu chỉ bằng một chạm",
 fn4="Kho lưu với tìm kiếm tức thì, ghim và kéo để sắp xếp, hiển thị tiến độ danh sách kiểm tra (như 2/5), giờ nhắc và số ký tự của từng ghi chú; kéo chip xuống vùng dưới màn hình là cất đi chứ không xóa",
 fw_old="Bảy màu pastel, định dạng và hình ảnh trong ghi chú giúp phân biệt từng ghi chú; cửa sổ kho lưu lo việc tìm kiếm, ghim và quản lý",
 fw_new="Tám màu ghi chú cùng màu tùy chỉnh, định dạng, danh sách kiểm tra và hình ảnh trong ghi chú giúp phân biệt từng ghi chú; cửa sổ kho lưu lo việc tìm kiếm, ghim và quản lý, đồng thời hiển thị tiến độ danh sách kiểm tra, giờ nhắc và số ký tự của từng ghi chú",
 fw3="Định dạng — in đậm, in nghiêng, gạch chân, gạch ngang, màu và cỡ chữ — cùng 8 màu ghi chú, màu tùy chỉnh, danh sách kiểm tra và hình ảnh trong ghi chú",
),
"zh": dict(
 la="显示其他设备的新便签", lw="显示其他设备的新便签",
 remote="开启“{L}”后，在一台设备上悬浮的新便签，同步后也会悬浮在另一台设备上。",
 cb3="按关键词即时搜索，按链接、图片、文本、已置顶筛选，并可按今天、本周、本月、今年筛选时间段",
 cw2="Android 风格界面，含浅色／深色主题、分组侧栏、常用短语、置顶／复制／编辑，以及可按类型（链接、图片、文本、已置顶）和时间段（今天、本周、本月、今年）筛选的搜索",
 fn_old="颜色、富文本与内嵌图片让每条便签一目了然",
 fn_new="8 种配色加自定义颜色、富文本、清单与内嵌图片让每条便签一目了然",
 fn1="便签 8 种配色，另可用色轮或颜色代码自定义颜色；富文本：粗体、斜体、下划线、删除线、文字颜色与字号；还有轻点即可勾选的清单",
 fn4="收纳库：即时搜索、置顶重要便签、拖动排序，并显示每条便签的清单进度（如 2/5）、提醒时间与字数；把小卡片拖到屏幕底部区域是收起而非删除",
 fw_old="七种柔和配色、富文本与内嵌图片让便签一目了然，收纳窗口负责搜索、置顶与管理",
 fw_new="八种便签配色加自定义颜色、富文本、清单与内嵌图片让便签一目了然，收纳窗口负责搜索、置顶与管理，并显示每条便签的清单进度、提醒时间与字数",
 fw3="富文本——粗体、斜体、下划线、删除线、文字颜色与字号——外加 8 种便签配色、自定义颜色、清单与内嵌图片",
),
}

NOSPACE = {"ja", "zh"}  # 문장을 이어 붙일 때 공백 없이


def append(text, sentence, lang):
    if sentence in text:
        sys.exit(f"{lang}: 이미 반영됨 — 이 스크립트는 한 번만 돌린다")
    return text + ("" if lang in NOSPACE else " ") + sentence


def replace_once(text, old, new, where):
    if text.count(old) != 1:
        sys.exit(f"{where}: 바꿀 문구를 정확히 한 번 찾지 못함 ({text.count(old)}회): {old}")
    return text.replace(old, new)


assert len(D) == 21, len(D)
for lang, d in D.items():
    path = os.path.join(SITE, "i18n", f"{lang}.json")
    with open(path, encoding="utf-8") as f:
        j = json.load(f)
    a = j["apps"]
    ra = d["remote"].format(L=d["la"])
    rw = d["remote"].format(L=d["lw"])

    a["clipboard"]["features"][3] = d["cb3"]
    a["clipboardwin"]["features"][2] = d["cw2"]

    fn = a["floatnote"]
    fn["long"] = append(replace_once(fn["long"], d["fn_old"], d["fn_new"], f"{lang} floatnote.long"), ra, lang)
    fn["features"][1] = d["fn1"]
    fn["features"][4] = d["fn4"]
    fn["faq"][2]["a"] = append(fn["faq"][2]["a"], ra, lang)

    fw = a["floatnotewin"]
    fw["long"] = append(replace_once(fw["long"], d["fw_old"], d["fw_new"], f"{lang} floatnotewin.long"), rw, lang)
    fw["features"][3] = d["fw3"]
    fw["faq"][0]["a"] = append(fw["faq"][0]["a"], rw, lang)

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(j, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("ok", lang)
