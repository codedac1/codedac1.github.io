# -*- coding: utf-8 -*-
"""2026-09-28 사이트 문구 정정 + AI 인용용 무료/Pro FAQ 보강 (21개 언어).

1) 정정 — 9/23 스토어 등록정보에서 이미 고친 과장이 사이트에 남아 있었다.
   - VolumeBooster: '통화(calls)'도 커진다 — 전역 세션 효과는 통화 경로에 걸리지 않는다. 삭제.
   - AutoStart: '부팅이 끝나는 순간' — 실제로는 재부팅 후 첫 잠금 해제 때(BOOT_COMPLETED) 실행된다.
     '잠금 화면에서도 부팅 배너' — 배너는 잠금 해제(USER_PRESENT)까지 기다린다. 둘 다 사실대로.
2) 추가 — 무료와 Pro 차이를 말하는 FAQ 가 없던 3개 앱(Clipboard 안드로이드 · FloatCryptoWin · PhotoCleanerWin).
   근거: Clipboard/CLAUDE.md·SettingsManager(그룹 3개·기능별 Free Pass), FloatCryptoWin/CLAUDE.md(2코인·1알림·
   30초·1D ↔ 10·무제한·10초·7D/30D, 광고 없음), PhotoCleanerWin/CLAUDE.md(탐지 무료·내보내기 하루 3번·PDF/인쇄·
   항상 가리기·마스크 색 Pro, 광고·워터마크 없음).

실행: python scripts/edits/2026-09-28-honest-ai.py  (i18n/<lang>.json 을 고쳐 쓴다 — 원문이 없으면 멈춘다)
"""
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")

# ── AutoStart: (태그라인, 기능1, 기능5, (긴 설명 원문 조각, 새 조각)) ───────────────────────
AS = {
    "en": ("Auto start your apps after every reboot, as soon as you unlock your phone. No root, set once, runs forever.",
           "Auto starts your selected apps after every reboot, as soon as you unlock the phone — no root, no custom ROM",
           "After a reboot, a banner starts your whole list in one tap as soon as you unlock the phone (PRO)",
           ("the moment the device finishes booting", "after every reboot, as soon as you unlock the phone")),
    "ko": ("재부팅할 때마다, 잠금을 풀면 원하는 앱이 알아서 실행됩니다. 루트 불필요, 한 번만 설정하세요.",
           "재부팅 후 잠금을 풀면 골라 둔 앱을 자동 실행 — 루트도 커스텀 롬도 필요 없음",
           "재부팅 후 잠금을 풀면 배너 한 번의 탭으로 목록 전체를 실행 (PRO)",
           ("기기 부팅이 끝나는 순간 골라 둔 앱을", "재부팅 후 잠금을 푸는 순간 골라 둔 앱을")),
    "ja": ("再起動のたび、ロックを解除すればお好みのアプリが自動で立ち上がります。root不要、設定は一度きり、ずっと動作。",
           "再起動後、ロックを解除すると選んだアプリを自動起動 — root もカスタム ROM も不要",
           "再起動後にロックを解除すると、バナーからリスト全体をワンタップ起動（PRO）",
           ("端末の起動が終わった瞬間に", "再起動後にロックを解除した瞬間に")),
    "zh": ("每次重启后，一解锁手机就自动启动你的应用。无需 root，一次设置，长久生效。",
           "每次重启后一解锁就自动启动你选定的应用 —— 无需 Root，无需第三方 ROM",
           "重启后一解锁，悬浮横幅即可一键启动整个列表（PRO）",
           ("设备开机完成的那一刻它们就会自己运行", "每次重启后一解锁手机，它们就会自己运行")),
    "de": ("Starte deine Apps nach jedem Neustart automatisch, sobald du das Handy entsperrst. Kein Root, einmal einrichten, läuft für immer.",
           "Startet die ausgewählten Apps nach jedem Neustart, sobald du das Gerät entsperrst — ohne Root, ohne Custom-ROM",
           "Nach einem Neustart startet ein Banner die ganze Liste mit einem Tipp, sobald du entsperrst (PRO)",
           ("sobald das Gerät fertig gebootet hat, starten sie von selbst",
            "nach jedem Neustart starten sie von selbst, sobald du das Gerät entsperrst")),
    "es": ("Inicia tus apps automáticamente tras cada reinicio, en cuanto desbloqueas el teléfono. Sin root, configúralo una vez y funciona para siempre.",
           "Abre las apps seleccionadas tras cada reinicio, en cuanto desbloqueas el dispositivo, sin root ni ROM personalizada",
           "Tras un reinicio, un banner lanza toda tu lista con un toque en cuanto desbloqueas (PRO)",
           ("en cuanto el dispositivo termina de arrancar, se abren solas",
            "tras cada reinicio, en cuanto desbloqueas el dispositivo, se abren solas")),
    "fil": ("Awtomatikong i-start ang mga app mo tuwing magre-restart ang telepono, sa sandaling i-unlock mo ito. Walang root, isang setup lang, tumatakbo habambuhay.",
            "Binubuksan ang piniling apps pagkatapos ng bawat restart, sa sandaling i-unlock mo ang device — walang root, walang custom ROM",
            "Pagkatapos mag-restart, isang banner ang naglulunsad ng buong listahan sa isang tap kapag na-unlock mo na (PRO)",
            ("sa oras na matapos mag-boot ang device", "pagkatapos ng bawat restart, sa sandaling i-unlock mo ang device")),
    "fr": ("Lancez vos applis automatiquement après chaque redémarrage, dès que vous déverrouillez le téléphone. Sans root, réglé une fois, actif pour toujours.",
           "Lance les applis choisies après chaque redémarrage, dès que vous déverrouillez l'appareil — sans root ni ROM personnalisée",
           "Après un redémarrage, une bannière lance toute la liste d'un toucher dès le déverrouillage (PRO)",
           ("dès que l'appareil a fini de démarrer, elles s'ouvrent toutes seules",
            "après chaque redémarrage, dès que vous déverrouillez l'appareil, elles s'ouvrent toutes seules")),
    "hi": ("हर रीस्टार्ट के बाद, फ़ोन अनलॉक करते ही अपने ऐप्स अपने-आप शुरू करें। रूट नहीं, एक बार सेट करें, हमेशा चलता रहे।",
           "हर रीस्टार्ट के बाद डिवाइस अनलॉक करते ही आपके चुने हुए ऐप्स अपने आप शुरू — न रूट, न कस्टम ROM",
           "रीस्टार्ट के बाद अनलॉक करते ही बैनर से पूरी सूची एक टैप में शुरू (PRO)",
           ("डिवाइस का बूट पूरा होते ही वे अपने आप चलने लगते हैं",
            "हर रीस्टार्ट के बाद डिवाइस अनलॉक करते ही वे अपने आप चलने लगते हैं")),
    "id": ("Jalankan aplikasi otomatis setiap kali ponsel dinyalakan ulang, begitu kamu membuka kuncinya. Tanpa root, atur sekali, berjalan selamanya.",
           "Menjalankan aplikasi pilihanmu setelah setiap restart, begitu perangkat dibuka kuncinya — tanpa root, tanpa ROM kustom",
           "Setelah restart, banner menjalankan seluruh daftar sekali ketuk begitu kamu membuka kunci (PRO)",
           ("begitu perangkat selesai booting semuanya terbuka sendiri",
            "setelah setiap restart, begitu perangkat dibuka kuncinya, semuanya terbuka sendiri")),
    "it": ("Avvia automaticamente le tue app dopo ogni riavvio, appena sblocchi il telefono. Nessun root, imposta una volta, funziona per sempre.",
           "Avvia le app selezionate dopo ogni riavvio, appena sblocchi il dispositivo — senza root né ROM personalizzate",
           "Dopo un riavvio, un banner lancia tutto l'elenco con un tocco appena sblocchi (PRO)",
           ("appena il dispositivo ha finito di avviarsi, partono da sole",
            "dopo ogni riavvio, appena sblocchi il dispositivo, partono da sole")),
    "ms": ("Auto start aplikasi anda selepas setiap kali telefon dimulakan semula, sebaik sahaja anda membuka kuncinya. Tanpa root, tetapkan sekali, berjalan selamanya.",
           "Memulakan apl pilihan anda selepas setiap mula semula, sebaik peranti dibuka kunci — tanpa root, tanpa ROM tersuai",
           "Selepas mula semula, sepanduk menjalankan seluruh senarai dengan satu ketikan sebaik anda membuka kunci (PRO)",
           ("sebaik peranti selesai but, semuanya terbuka sendiri",
            "selepas setiap mula semula, sebaik peranti dibuka kunci, semuanya terbuka sendiri")),
    "nl": ("Start je apps automatisch na elke herstart, zodra je je telefoon ontgrendelt. Geen root, één keer instellen, werkt voor altijd.",
           "Start je gekozen apps na elke herstart, zodra je het toestel ontgrendelt — zonder root of custom ROM",
           "Na een herstart start een banner je hele lijst met één tik zodra je ontgrendelt (PRO)",
           ("zodra het toestel klaar is met opstarten, gaan ze vanzelf open",
            "na elke herstart gaan ze vanzelf open zodra je het toestel ontgrendelt")),
    "pl": ("Automatycznie uruchamiaj aplikacje po każdym restarcie, gdy tylko odblokujesz telefon. Bez roota, ustaw raz, działa zawsze.",
           "Uruchamia wybrane aplikacje po każdym restarcie, gdy tylko odblokujesz urządzenie — bez roota i custom ROM-u",
           "Po restarcie baner uruchamia całą listę jednym dotknięciem, gdy tylko odblokujesz (PRO)",
           ("gdy tylko urządzenie zakończy uruchamianie, otworzą się same",
            "po każdym restarcie, gdy tylko odblokujesz urządzenie, otworzą się same")),
    "pt": ("Inicie seus apps automaticamente após cada reinício, assim que você desbloqueia o celular. Sem root, configure uma vez, funciona para sempre.",
           "Inicia os apps escolhidos após cada reinício, assim que você desbloqueia o aparelho — sem root e sem ROM personalizada",
           "Após um reinício, um banner abre toda a lista com um toque assim que você desbloqueia (PRO)",
           ("assim que o aparelho termina de ligar, eles abrem sozinhos",
            "após cada reinício, assim que você desbloqueia o aparelho, eles abrem sozinhos")),
    "ru": ("Автоматический запуск приложений после каждой перезагрузки — как только вы разблокируете телефон. Без root, настройте один раз — работает всегда.",
           "Запускает выбранные приложения после каждой перезагрузки, как только вы разблокируете устройство — без root и кастомной прошивки",
           "После перезагрузки баннер запускает весь список одним касанием, как только вы разблокируете (PRO)",
           ("как только устройство загрузится, они откроются сами",
            "после каждой перезагрузки, как только вы разблокируете устройство, они откроются сами")),
    "th": ("เปิดแอปของคุณให้อัตโนมัติหลังรีสตาร์ททุกครั้ง ทันทีที่ปลดล็อกเครื่อง ไม่ต้องรูท ตั้งค่าครั้งเดียว ใช้ได้ตลอด",
           "เปิดแอปที่เลือกไว้หลังรีสตาร์ททุกครั้ง ทันทีที่ปลดล็อกเครื่อง — ไม่ต้องรูท ไม่ต้องลง ROM พิเศษ",
           "หลังรีสตาร์ท แบนเนอร์เปิดทั้งรายการด้วยการแตะครั้งเดียวทันทีที่ปลดล็อก (PRO)",
           ("พอเครื่องบูตเสร็จแอปก็ทำงานเอง", "หลังรีสตาร์ททุกครั้ง พอปลดล็อกเครื่องแอปก็ทำงานเอง")),
    "tr": ("Uygulamalarınızı her yeniden başlatmadan sonra, telefonun kilidini açar açmaz otomatik başlatın. Root yok, bir kez ayarla, hep çalışsın.",
           "Her yeniden başlatmadan sonra, cihazın kilidini açar açmaz seçtiğiniz uygulamaları başlatır — root ve özel ROM gerekmez",
           "Yeniden başlatmadan sonra, kilidi açar açmaz bir banner listenizin tamamını tek dokunuşla başlatır (PRO)",
           ("cihaz açılışını tamamladığı anda kendiliğinden başlasınlar",
            "her yeniden başlatmadan sonra cihazın kilidini açar açmaz kendiliğinden başlasınlar")),
    "uk": ("Автоматичний запуск застосунків після кожного перезавантаження — щойно ви розблокуєте телефон. Без root, налаштуйте один раз — працює завжди.",
           "Запускає вибрані застосунки після кожного перезавантаження, щойно ви розблокуєте пристрій — без root і кастомної прошивки",
           "Після перезавантаження банер відкриває весь список одним дотиком, щойно ви розблокуєте (PRO)",
           ("щойно пристрій завершить запуск, вони відкриються самі",
            "після кожного перезавантаження, щойно ви розблокуєте пристрій, вони відкриються самі")),
    "vi": ("Tự động mở ứng dụng sau mỗi lần khởi động lại, ngay khi bạn mở khóa điện thoại. Không cần root, cài một lần, chạy mãi.",
           "Tự mở các ứng dụng đã chọn sau mỗi lần khởi động lại, ngay khi mở khóa máy — không root, không ROM tùy chỉnh",
           "Sau khi khởi động lại, banner mở cả danh sách chỉ với một chạm ngay khi bạn mở khóa (PRO)",
           ("ngay khi máy khởi động xong chúng tự mở", "sau mỗi lần khởi động lại, ngay khi bạn mở khóa máy chúng tự mở")),
    "ar": ("شغّل تطبيقاتك تلقائيًا بعد كل إعادة تشغيل، بمجرد فتح قفل هاتفك. بدون روت، إعداد لمرة واحدة، ويعمل إلى الأبد.",
           "تشغيل التطبيقات المختارة بعد كل إعادة تشغيل بمجرد فتح قفل الجهاز — بدون Root ولا رومات مخصصة",
           "بعد إعادة التشغيل، يشغّل بانر قائمتك كاملة بنقرة واحدة بمجرد فتح القفل (PRO)",
           ("في اللحظة التي ينتهي فيها إقلاع الجهاز", "بعد كل إعادة تشغيل بمجرد فتح قفل الجهاز")),
}

# ── VolumeBooster: 통화 삭제 — (긴 설명 원문, 새), (FAQ 1 답 원문, 새) ────────────────────
VB = {
    "en": (("hard-to-hear videos, calls, music and games", "hard-to-hear videos, music and games"),
           ("music, videos, YouTube, games and calls alike", "music, videos, YouTube and games alike")),
    "ar": (("والمكالمات والموسيقى", "والموسيقى"), ("والألعاب والمكالمات", "والألعاب")),
    "de": (("Videos, Anrufe, Musik", "Videos, Musik"), ("YouTube, Spiele und Anrufe", "YouTube und Spiele")),
    "es": (("de oír, llamadas, música", "de oír, música"), ("YouTube, juegos y llamadas", "YouTube y juegos")),
    "fil": (("marinig, tawag, musika", "marinig, musika"), ("YouTube, laro at tawag", "YouTube at laro")),
    "fr": (("à entendre, appels, musique", "à entendre, musique"), ("YouTube, jeux et appels", "YouTube et jeux")),
    "hi": (("वीडियो, कॉल, संगीत", "वीडियो, संगीत"), ("YouTube, गेम और कॉल सब पर", "YouTube और गेम सब पर")),
    "id": (("didengar, panggilan, musik", "didengar, musik"), ("YouTube, game, maupun panggilan", "YouTube, maupun game")),
    "it": (("da sentire, chiamate, musica", "da sentire, musica"), ("YouTube, giochi e chiamate", "YouTube e giochi")),
    "ja": (("動画・通話・音楽・ゲーム", "動画・音楽・ゲーム"), ("YouTube、ゲーム、通話すべてに", "YouTube、ゲームすべてに")),
    "ko": (("영상·통화·음악·게임", "영상·음악·게임"), ("유튜브·게임·통화 모두에", "유튜브·게임 모두에")),
    "ms": (("didengar, panggilan, muzik", "didengar, muzik"), ("YouTube, permainan dan panggilan", "YouTube dan permainan")),
    "nl": (("video’s, gesprekken, muziek", "video’s, muziek"), ("YouTube, games en gesprekken", "YouTube en games")),
    "pl": (("filmy, rozmowy, muzykę", "filmy, muzykę"), ("YouTube, gry i rozmowy", "YouTube i gry")),
    "pt": (("de ouvir, chamadas, música", "de ouvir, música"), ("YouTube, jogos e chamadas", "YouTube e jogos")),
    "ru": (("видео, звонки, музыка", "видео, музыка"), ("YouTube, игры и звонки", "YouTube и игры")),
    "th": (("วิดีโอที่ฟังยาก สายโทร เพลง", "วิดีโอที่ฟังยาก เพลง"), ("YouTube เกม และสายโทร", "YouTube และเกม")),
    "tr": (("videolar, aramalar, müzik", "videolar, müzik"), ("YouTube, oyun ve aramalar dahil", "YouTube ve oyunlar dahil")),
    "uk": (("відео, дзвінки, музику", "відео, музику"), ("YouTube, ігри та дзвінки", "YouTube та ігри")),
    "vi": (("video khó nghe, cuộc gọi, nhạc", "video khó nghe, nhạc"), ("YouTube, game và cuộc gọi đều vậy", "YouTube và game đều vậy")),
    "zh": (("视频、通话、音乐和游戏", "视频、音乐和游戏"), ("YouTube、游戏和通话都适用", "YouTube 和游戏都适用")),
}

# ── 새 FAQ: 무료와 Pro ───────────────────────────────────────────────────────────
FAQ = {
    "clipboard": {
        "en": ("What is free, and what does Pro add?",
               "Free keeps your text and image clipboard history with search, snippets, up to 3 groups, the floating panel, the widget and the selection-menu shortcut, and it shows ads. Pro removes the ads and adds phone-to-PC sync through your own Google Drive, unlimited image clips, the expanded floating panel and widget, unlimited groups, PDF export and backup restore — monthly, yearly or as a one-time lifetime purchase. If you need one of these for just a day, a short ad unlocks it for 24 hours."),
        "ko": ("무료로 무엇을 쓸 수 있고, Pro는 무엇이 다른가요?",
               "무료로 텍스트·이미지 클립보드 기록과 검색, 스니펫, 그룹 3개, 플로팅 패널, 위젯, 텍스트 선택 메뉴 저장을 쓸 수 있고 광고가 표시됩니다. Pro는 광고를 없애고 내 구글 드라이브를 통한 폰↔PC 동기화, 이미지 클립 무제한, 확장 플로팅 패널과 위젯, 그룹 무제한, PDF 내보내기, 백업 복원을 더합니다. 월간·연간 구독이나 한 번 결제하는 평생 이용권으로 살 수 있습니다. 하루만 필요하다면 짧은 광고를 보고 해당 기능을 24시간 쓸 수 있습니다."),
        "ja": ("無料で何が使えて、Pro では何が増えますか?",
               "無料でテキストと画像のクリップボード履歴、検索、スニペット、3つまでのグループ、フローティングパネル、ウィジェット、テキスト選択メニューからの保存が使え、広告が表示されます。Pro は広告をなくし、自分の Google ドライブを使ったスマホ↔PC 同期、画像クリップ無制限、拡張フローティングパネルとウィジェット、グループ無制限、PDF 書き出し、バックアップの復元を追加します。月額・年額、または一度きりの買い切りで購入できます。1日だけ必要なら、短い広告でその機能を24時間使えます。"),
        "zh": ("免费能用什么？Pro 多了什么？",
               "免费版提供文本和图片剪贴板历史、搜索、片段、最多 3 个分组、悬浮面板、小组件以及文本选择菜单保存，并显示广告。Pro 去除广告，并增加通过你自己的 Google 云端硬盘进行的手机↔电脑同步、无限图片剪辑、扩展悬浮面板和小组件、无限分组、PDF 导出和备份恢复——可按月、按年订阅，或一次性买断。如果只需要用一天，看一段短广告即可解锁该功能 24 小时。"),
        "de": ("Was ist kostenlos, und was bringt Pro?",
               "Kostenlos bekommst du den Verlauf für Text und Bilder mit Suche, Snippets, bis zu 3 Gruppen, das schwebende Panel, das Widget und das Speichern über das Textauswahlmenü, dazu Werbung. Pro entfernt die Werbung und bringt die Synchronisierung zwischen Handy und PC über dein eigenes Google Drive, unbegrenzte Bild-Clips, das erweiterte Panel und Widget, unbegrenzte Gruppen, PDF-Export und das Wiederherstellen von Backups — monatlich, jährlich oder als einmaliger Lifetime-Kauf. Brauchst du etwas nur einen Tag, schaltet eine kurze Werbung es für 24 Stunden frei."),
        "es": ("¿Qué es gratis y qué añade Pro?",
               "Gratis tienes el historial de texto e imágenes con búsqueda, fragmentos, hasta 3 grupos, el panel flotante, el widget y el guardado desde el menú de selección de texto, con anuncios. Pro quita los anuncios y añade la sincronización entre móvil y PC a través de tu propio Google Drive, clips de imagen ilimitados, el panel flotante y el widget ampliados, grupos ilimitados, exportación a PDF y restauración de copias de seguridad, con pago mensual, anual o único de por vida. Si solo lo necesitas un día, un anuncio corto lo desbloquea durante 24 horas."),
        "fil": ("Ano ang libre, at ano ang dagdag ng Pro?",
                "Libre ang history ng text at larawan na may search, snippets, hanggang 3 grupo, ang floating panel, ang widget at ang pag-save mula sa text selection menu, at may ads. Tinatanggal ng Pro ang ads at nagdadagdag ng phone-to-PC sync sa sarili mong Google Drive, walang limitasyong image clips, mas malaking floating panel at widget, walang limitasyong grupo, PDF export at pag-restore ng backup — buwanan, taunan o isang beses na lifetime na bili. Kung isang araw lang ang kailangan, isang maikling ad ang magbubukas nito nang 24 oras."),
        "fr": ("Qu’est-ce qui est gratuit, et qu’apporte Pro ?",
               "La version gratuite garde l’historique du texte et des images avec la recherche, les extraits, jusqu’à 3 groupes, le panneau flottant, le widget et l’enregistrement depuis le menu de sélection de texte, avec des publicités. Pro supprime les publicités et ajoute la synchronisation téléphone-PC via votre propre Google Drive, des clips image illimités, le panneau flottant et le widget étendus, des groupes illimités, l’export PDF et la restauration des sauvegardes — au mois, à l’année ou en achat unique à vie. Si vous n’en avez besoin que pour une journée, une courte publicité le débloque pendant 24 heures."),
        "hi": ("मुफ़्त में क्या मिलता है, और Pro में क्या जुड़ता है?",
               "मुफ़्त में टेक्स्ट और इमेज का क्लिपबोर्ड इतिहास, खोज, स्निपेट, 3 तक ग्रुप, फ्लोटिंग पैनल, विजेट और टेक्स्ट चुनने वाले मेन्यू से सेव करना मिलता है, और विज्ञापन दिखते हैं। Pro विज्ञापन हटाता है और आपकी अपनी Google Drive से फ़ोन↔PC सिंक, असीमित इमेज क्लिप, बड़ा फ्लोटिंग पैनल और विजेट, असीमित ग्रुप, PDF एक्सपोर्ट और बैकअप रिस्टोर जोड़ता है — मासिक, वार्षिक या एक बार की लाइफ़टाइम खरीद। अगर सिर्फ़ एक दिन के लिए चाहिए, तो एक छोटा विज्ञापन उसे 24 घंटे के लिए खोल देता है।"),
        "id": ("Apa yang gratis, dan apa tambahan Pro?",
               "Versi gratis menyimpan riwayat teks dan gambar dengan pencarian, cuplikan, hingga 3 grup, panel mengambang, widget, dan simpan dari menu pilihan teks, dengan iklan. Pro menghapus iklan dan menambahkan sinkronisasi ponsel↔PC lewat Google Drive milikmu sendiri, klip gambar tanpa batas, panel mengambang dan widget yang diperluas, grup tanpa batas, ekspor PDF, dan pemulihan cadangan — bulanan, tahunan, atau sekali beli seumur hidup. Jika hanya perlu sehari, iklan singkat membukanya selama 24 jam."),
        "it": ("Cosa è gratis e cosa aggiunge Pro?",
               "Gratis hai la cronologia di testo e immagini con ricerca, snippet, fino a 3 gruppi, il pannello flottante, il widget e il salvataggio dal menu di selezione del testo, con pubblicità. Pro toglie la pubblicità e aggiunge la sincronizzazione telefono↔PC tramite il tuo Google Drive, clip immagine illimitate, pannello flottante e widget ampliati, gruppi illimitati, esportazione PDF e ripristino dei backup — mensile, annuale o con acquisto unico a vita. Se ti serve per un solo giorno, una breve pubblicità lo sblocca per 24 ore."),
        "ms": ("Apa yang percuma, dan apa tambahan Pro?",
               "Versi percuma menyimpan sejarah teks dan imej dengan carian, petikan, sehingga 3 kumpulan, panel terapung, widget dan simpan dari menu pilihan teks, dengan iklan. Pro membuang iklan dan menambah penyegerakan telefon↔PC melalui Google Drive anda sendiri, klip imej tanpa had, panel terapung dan widget yang diperluas, kumpulan tanpa had, eksport PDF dan pemulihan sandaran — bulanan, tahunan atau belian sekali seumur hidup. Jika perlu untuk sehari sahaja, iklan pendek membukanya selama 24 jam."),
        "nl": ("Wat is gratis, en wat voegt Pro toe?",
               "Gratis krijg je de geschiedenis van tekst en afbeeldingen met zoeken, fragmenten, tot 3 groepen, het zwevende paneel, de widget en opslaan via het tekstselectiemenu, met advertenties. Pro haalt de advertenties weg en voegt synchronisatie tussen telefoon en pc via je eigen Google Drive toe, onbeperkte afbeeldingsclips, het uitgebreide zwevende paneel en de widget, onbeperkte groepen, PDF-export en back-up terugzetten — per maand, per jaar of als eenmalige lifetime-aankoop. Heb je iets maar één dag nodig, dan ontgrendelt een korte advertentie het voor 24 uur."),
        "pl": ("Co jest za darmo, a co dodaje Pro?",
               "Za darmo masz historię tekstu i obrazów z wyszukiwaniem, fragmentami, do 3 grup, pływający panel, widżet i zapisywanie z menu zaznaczania tekstu, z reklamami. Pro usuwa reklamy i dodaje synchronizację telefon↔PC przez Twój własny Dysk Google, nielimitowane klipy obrazów, powiększony pływający panel i widżet, nielimitowane grupy, eksport do PDF i przywracanie kopii zapasowych — miesięcznie, rocznie lub jednorazowo na zawsze. Jeśli potrzebujesz czegoś tylko na jeden dzień, krótka reklama odblokuje to na 24 godziny."),
        "pt": ("O que é grátis e o que o Pro acrescenta?",
               "Grátis você tem o histórico de texto e imagens com busca, trechos, até 3 grupos, o painel flutuante, o widget e o salvamento pelo menu de seleção de texto, com anúncios. O Pro remove os anúncios e acrescenta a sincronização entre celular e PC pelo seu próprio Google Drive, clipes de imagem ilimitados, painel flutuante e widget ampliados, grupos ilimitados, exportação em PDF e restauração de backup — mensal, anual ou em compra única vitalícia. Se precisar só por um dia, um anúncio curto libera o recurso por 24 horas."),
        "ru": ("Что доступно бесплатно и что добавляет Pro?",
               "Бесплатно доступны история текста и изображений с поиском, сниппеты, до 3 групп, плавающая панель, виджет и сохранение из меню выделения текста, с рекламой. Pro убирает рекламу и добавляет синхронизацию телефона с ПК через ваш собственный Google Диск, неограниченные клипы-изображения, расширенные плавающую панель и виджет, неограниченные группы, экспорт в PDF и восстановление из резервной копии — помесячно, на год или разовой покупкой навсегда. Если что-то нужно лишь на день, короткая реклама откроет это на 24 часа."),
        "th": ("ฟรีใช้อะไรได้บ้าง และ Pro เพิ่มอะไร",
               "รุ่นฟรีเก็บประวัติคลิปบอร์ดทั้งข้อความและรูปภาพ พร้อมการค้นหา ข้อความสำเร็จรูป กลุ่มได้ 3 กลุ่ม แผงลอย วิดเจ็ต และการบันทึกจากเมนูเลือกข้อความ โดยมีโฆษณา Pro ไม่มีโฆษณา และเพิ่มการซิงก์โทรศัพท์↔PC ผ่าน Google Drive ของคุณเอง คลิปรูปภาพไม่จำกัด แผงลอยและวิดเจ็ตแบบขยาย กลุ่มไม่จำกัด ส่งออก PDF และกู้คืนข้อมูลสำรอง มีแบบรายเดือน รายปี หรือซื้อครั้งเดียวใช้ตลอดชีพ ถ้าต้องการใช้แค่วันเดียว ดูโฆษณาสั้น ๆ เพื่อปลดล็อกฟีเจอร์นั้น 24 ชั่วโมง"),
        "tr": ("Ücretsiz sürümde neler var, Pro neler ekliyor?",
               "Ücretsiz sürüm; arama, parçacıklar, en fazla 3 grup, yüzen panel, widget ve metin seçim menüsünden kaydetme ile metin ve görsel pano geçmişini tutar, reklam gösterir. Pro reklamları kaldırır ve kendi Google Drive’ınız üzerinden telefon↔PC eşitleme, sınırsız görsel klibi, genişletilmiş yüzen panel ve widget, sınırsız grup, PDF dışa aktarma ve yedekten geri yükleme ekler — aylık, yıllık ya da tek seferlik ömür boyu satın alma. Yalnızca bir gün lazımsa kısa bir reklam onu 24 saatliğine açar."),
        "uk": ("Що доступно безкоштовно і що додає Pro?",
               "Безкоштовно доступні історія тексту й зображень із пошуком, сніпети, до 3 груп, плаваюча панель, віджет і збереження з меню виділення тексту, з рекламою. Pro прибирає рекламу й додає синхронізацію телефона з ПК через ваш власний Google Диск, необмежені кліпи-зображення, розширені плаваючу панель і віджет, необмежені групи, експорт у PDF і відновлення з резервної копії — щомісяця, на рік або разовою покупкою назавжди. Якщо щось потрібно лише на день, коротка реклама відкриє це на 24 години."),
        "vi": ("Bản miễn phí có gì, và Pro thêm gì?",
               "Bản miễn phí lưu lịch sử clipboard văn bản và hình ảnh kèm tìm kiếm, đoạn mẫu, tối đa 3 nhóm, bảng nổi, widget và lưu từ menu chọn văn bản, có quảng cáo. Pro bỏ quảng cáo và thêm đồng bộ điện thoại↔PC qua Google Drive của chính bạn, clip hình ảnh không giới hạn, bảng nổi và widget mở rộng, nhóm không giới hạn, xuất PDF và khôi phục bản sao lưu — theo tháng, theo năm hoặc mua một lần trọn đời. Nếu chỉ cần trong một ngày, một quảng cáo ngắn sẽ mở tính năng đó trong 24 giờ."),
        "ar": ("ما المجاني، وماذا يضيف Pro؟",
               "النسخة المجانية تحفظ سجل الحافظة للنصوص والصور مع البحث والمقتطفات وحتى 3 مجموعات واللوحة العائمة والأداة والحفظ من قائمة تحديد النص، مع إعلانات. يزيل Pro الإعلانات ويضيف المزامنة بين الهاتف والكمبيوتر عبر Google Drive الخاص بك، ومقاطع صور بلا حدود، ولوحة عائمة وأداة موسعتين، ومجموعات بلا حدود، والتصدير إلى PDF واستعادة النسخ الاحتياطية — باشتراك شهري أو سنوي أو شراء لمرة واحدة مدى الحياة. وإن احتجت ميزة ليوم واحد فقط، فإعلان قصير يفتحها لمدة 24 ساعة."),
    },
    "floatcryptowin": {
        "en": ("What is free, and what does Pro add?",
               "Free follows 2 coins with 1 price alert, refreshes every 30 seconds and shows the 1-day chart — and the ticker has no time limit. Pro is a one-time purchase that raises this to 10 coins, unlimited alerts, a 10-second refresh and the 7-day and 30-day charts. The Windows version has no ads."),
        "ko": ("무료로 무엇을 쓸 수 있고, Pro는 무엇이 다른가요?",
               "무료로 코인 2개와 가격 알림 1개를 쓰고, 시세는 30초마다 갱신되며 1일 차트를 볼 수 있습니다. 티커 사용 시간에는 제한이 없습니다. Pro는 한 번 결제로 코인 10개, 알림 무제한, 10초 갱신, 7일·30일 차트를 엽니다. Windows 버전에는 광고가 없습니다."),
        "ja": ("無料で何が使えて、Pro では何が増えますか?",
               "無料ではコイン2つと価格アラート1つを使え、30秒ごとに更新され、1日チャートを表示できます。ティッカーに時間制限はありません。Pro は買い切りで、コイン10個、アラート無制限、10秒更新、7日・30日チャートが使えます。Windows 版に広告はありません。"),
        "zh": ("免费能用什么？Pro 多了什么？",
               "免费版可关注 2 个币种、设置 1 个价格提醒，每 30 秒刷新一次，并显示 1 天走势图，行情条没有使用时长限制。Pro 为一次性购买，可提升到 10 个币种、无限提醒、10 秒刷新以及 7 天和 30 天走势图。Windows 版没有广告。"),
        "de": ("Was ist kostenlos, und was bringt Pro?",
               "Kostenlos verfolgst du 2 Coins mit 1 Preisalarm, die Kurse aktualisieren sich alle 30 Sekunden und du siehst das 1-Tages-Diagramm — der Ticker hat kein Zeitlimit. Pro ist ein einmaliger Kauf und erweitert das auf 10 Coins, unbegrenzte Alarme, 10-Sekunden-Aktualisierung und die 7- und 30-Tages-Diagramme. Die Windows-Version hat keine Werbung."),
        "es": ("¿Qué es gratis y qué añade Pro?",
               "Gratis sigues 2 monedas con 1 alerta de precio, se actualiza cada 30 segundos y muestra el gráfico de 1 día, y el ticker no tiene límite de tiempo. Pro es un pago único que lo amplía a 10 monedas, alertas ilimitadas, actualización cada 10 segundos y los gráficos de 7 y 30 días. La versión de Windows no tiene anuncios."),
        "fil": ("Ano ang libre, at ano ang dagdag ng Pro?",
                "Sa libre, 2 coin at 1 price alert ang masusundan mo, nagre-refresh bawat 30 segundo at may 1-day chart — at walang time limit ang ticker. Ang Pro ay isang beses na bili na nagtataas nito sa 10 coin, walang limitasyong alert, 10-segundong refresh at 7-day at 30-day chart. Walang ads ang bersyon sa Windows."),
        "fr": ("Qu’est-ce qui est gratuit, et qu’apporte Pro ?",
               "En gratuit, vous suivez 2 cryptos avec 1 alerte de prix, l’actualisation se fait toutes les 30 secondes et le graphique sur 1 jour est affiché — le bandeau n’a aucune limite de durée. Pro est un achat unique qui passe à 10 cryptos, des alertes illimitées, une actualisation toutes les 10 secondes et les graphiques sur 7 et 30 jours. La version Windows n’a pas de publicité."),
        "hi": ("मुफ़्त में क्या मिलता है, और Pro में क्या जुड़ता है?",
               "मुफ़्त में 2 कॉइन और 1 प्राइस अलर्ट, हर 30 सेकंड में रिफ़्रेश और 1 दिन का चार्ट मिलता है — और टिकर पर समय की कोई सीमा नहीं है। Pro एक बार की खरीद है जो इसे 10 कॉइन, असीमित अलर्ट, 10 सेकंड रिफ़्रेश और 7 व 30 दिन के चार्ट तक बढ़ाता है। Windows वर्शन में कोई विज्ञापन नहीं है।"),
        "id": ("Apa yang gratis, dan apa tambahan Pro?",
               "Versi gratis memantau 2 koin dengan 1 peringatan harga, diperbarui setiap 30 detik, dan menampilkan grafik 1 hari — ticker tidak punya batas waktu. Pro adalah pembelian sekali yang menaikkannya menjadi 10 koin, peringatan tanpa batas, pembaruan 10 detik, serta grafik 7 dan 30 hari. Versi Windows tidak memiliki iklan."),
        "it": ("Cosa è gratis e cosa aggiunge Pro?",
               "Gratis segui 2 monete con 1 avviso di prezzo, l’aggiornamento avviene ogni 30 secondi e vedi il grafico a 1 giorno — il ticker non ha limiti di tempo. Pro è un acquisto unico che porta a 10 monete, avvisi illimitati, aggiornamento ogni 10 secondi e i grafici a 7 e 30 giorni. La versione Windows non ha pubblicità."),
        "ms": ("Apa yang percuma, dan apa tambahan Pro?",
               "Versi percuma mengikuti 2 syiling dengan 1 amaran harga, dikemas kini setiap 30 saat dan memaparkan carta 1 hari — ticker tiada had masa. Pro ialah belian sekali yang menaikkannya kepada 10 syiling, amaran tanpa had, kemas kini 10 saat serta carta 7 dan 30 hari. Versi Windows tiada iklan."),
        "nl": ("Wat is gratis, en wat voegt Pro toe?",
               "Gratis volg je 2 munten met 1 prijsalarm, wordt elke 30 seconden ververst en zie je de grafiek van 1 dag — de koersbalk heeft geen tijdslimiet. Pro is een eenmalige aankoop die dat verhoogt naar 10 munten, onbeperkte alarmen, verversen elke 10 seconden en de grafieken van 7 en 30 dagen. De Windows-versie heeft geen advertenties."),
        "pl": ("Co jest za darmo, a co dodaje Pro?",
               "Za darmo śledzisz 2 kryptowaluty z 1 alertem cenowym, odświeżanie co 30 sekund i wykres 1-dniowy — a pasek kursów nie ma limitu czasu. Pro to jednorazowy zakup, który zwiększa to do 10 kryptowalut, nielimitowanych alertów, odświeżania co 10 sekund i wykresów 7- i 30-dniowych. Wersja na Windows nie ma reklam."),
        "pt": ("O que é grátis e o que o Pro acrescenta?",
               "Grátis você acompanha 2 moedas com 1 alerta de preço, a atualização é a cada 30 segundos e o gráfico de 1 dia aparece — e o ticker não tem limite de tempo. O Pro é uma compra única que amplia para 10 moedas, alertas ilimitados, atualização a cada 10 segundos e os gráficos de 7 e 30 dias. A versão para Windows não tem anúncios."),
        "ru": ("Что доступно бесплатно и что добавляет Pro?",
               "Бесплатно можно следить за 2 монетами с 1 ценовым оповещением, обновление каждые 30 секунд и график за 1 день — а у тикера нет ограничения по времени. Pro — разовая покупка: 10 монет, неограниченные оповещения, обновление каждые 10 секунд и графики за 7 и 30 дней. В версии для Windows нет рекламы."),
        "th": ("ฟรีใช้อะไรได้บ้าง และ Pro เพิ่มอะไร",
               "รุ่นฟรีติดตามได้ 2 เหรียญพร้อมการแจ้งเตือนราคา 1 รายการ อัปเดตทุก 30 วินาที และดูกราฟ 1 วันได้ โดยแถบราคาไม่มีจำกัดเวลาใช้งาน Pro เป็นการซื้อครั้งเดียว เพิ่มเป็น 10 เหรียญ แจ้งเตือนไม่จำกัด อัปเดตทุก 10 วินาที และกราฟ 7 วันกับ 30 วัน รุ่น Windows ไม่มีโฆษณา"),
        "tr": ("Ücretsiz sürümde neler var, Pro neler ekliyor?",
               "Ücretsiz sürümde 2 coin ve 1 fiyat alarmı takip edilir, fiyatlar 30 saniyede bir yenilenir ve 1 günlük grafik gösterilir — fiyat çubuğunun süre sınırı yoktur. Pro tek seferlik bir satın almadır ve bunu 10 coin, sınırsız alarm, 10 saniyelik yenileme ile 7 ve 30 günlük grafiklere çıkarır. Windows sürümünde reklam yoktur."),
        "uk": ("Що доступно безкоштовно і що додає Pro?",
               "Безкоштовно можна стежити за 2 монетами з 1 ціновим сповіщенням, оновлення щоразу за 30 секунд і графік за 1 день — а тикер не має обмеження за часом. Pro — разова покупка: 10 монет, необмежені сповіщення, оновлення щоразу за 10 секунд і графіки за 7 та 30 днів. У версії для Windows немає реклами."),
        "vi": ("Bản miễn phí có gì, và Pro thêm gì?",
               "Bản miễn phí theo dõi 2 đồng coin với 1 cảnh báo giá, cập nhật mỗi 30 giây và hiển thị biểu đồ 1 ngày — thanh giá không giới hạn thời gian. Pro là gói mua một lần, nâng lên 10 đồng coin, cảnh báo không giới hạn, cập nhật mỗi 10 giây cùng biểu đồ 7 ngày và 30 ngày. Bản Windows không có quảng cáo."),
        "ar": ("ما المجاني، وماذا يضيف Pro؟",
               "في النسخة المجانية تتابع عملتين مع تنبيه سعر واحد، ويتحدث السعر كل 30 ثانية مع مخطط يوم واحد — ولا يوجد حد زمني لشريط الأسعار. Pro شراء لمرة واحدة يرفع ذلك إلى 10 عملات وتنبيهات بلا حدود وتحديث كل 10 ثوانٍ ومخططي 7 و30 يومًا. لا توجد إعلانات في نسخة Windows."),
    },
    "photocleanerwin": {
        "en": ("What is free, and what does Pro add?",
               "Finding personal info is free and unlimited, and you can save, copy or share the masked copy of 3 documents a day for free. Pro is a one-time purchase that removes the daily limit and adds PDF export, printing, the always-hide list and your choice of mask color. There are no ads and no watermark, on either version."),
        "ko": ("무료로 무엇을 쓸 수 있고, Pro는 무엇이 다른가요?",
               "개인정보 찾기는 무료이고 횟수 제한이 없으며, 가린 사본의 저장·복사·공유는 하루 3개 문서까지 무료입니다. Pro는 한 번 결제로 하루 한도를 없애고 PDF 저장, 인쇄, 항상 가릴 단어 목록, 가림 색상 선택을 더합니다. 어느 쪽에도 광고와 워터마크는 없습니다."),
        "ja": ("無料で何が使えて、Pro では何が増えますか?",
               "個人情報の検出は無料で回数制限がなく、隠したコピーの保存・コピー・共有は1日3ドキュメントまで無料です。Pro は買い切りで、1日の上限をなくし、PDF 書き出し、印刷、常に隠す語句のリスト、マスクの色選択を追加します。どちらにも広告や透かしはありません。"),
        "zh": ("免费能用什么？Pro 多了什么？",
               "查找个人信息免费且不限次数，每天可免费保存、复制或分享 3 份已遮盖文档。Pro 为一次性购买，取消每日上限，并增加 PDF 导出、打印、始终遮盖列表和遮盖颜色选择。两个版本都没有广告和水印。"),
        "de": ("Was ist kostenlos, und was bringt Pro?",
               "Das Finden persönlicher Daten ist kostenlos und unbegrenzt, und die geschwärzte Kopie von 3 Dokumenten pro Tag kannst du kostenlos speichern, kopieren oder teilen. Pro ist ein einmaliger Kauf, hebt das Tageslimit auf und bringt PDF-Export, Drucken, die Liste immer zu schwärzender Begriffe und die freie Wahl der Maskenfarbe. Es gibt keine Werbung und kein Wasserzeichen."),
        "es": ("¿Qué es gratis y qué añade Pro?",
               "Detectar datos personales es gratis e ilimitado, y puedes guardar, copiar o compartir gratis la copia tapada de 3 documentos al día. Pro es un pago único que quita el límite diario y añade la exportación a PDF, la impresión, la lista de términos que siempre se tapan y el color de máscara a elegir. No hay anuncios ni marca de agua."),
        "fil": ("Ano ang libre, at ano ang dagdag ng Pro?",
                "Libre at walang limitasyon ang paghahanap ng personal na impormasyon, at libre mong mase-save, makokopya o maibabahagi ang natakpang kopya ng 3 dokumento bawat araw. Ang Pro ay isang beses na bili na nag-aalis ng daily limit at nagdadagdag ng PDF export, pag-print, listahan ng laging itatago at pagpili ng kulay ng mask. Walang ads at walang watermark."),
        "fr": ("Qu’est-ce qui est gratuit, et qu’apporte Pro ?",
               "La détection des informations personnelles est gratuite et illimitée, et vous pouvez enregistrer, copier ou partager gratuitement la copie masquée de 3 documents par jour. Pro est un achat unique qui supprime la limite quotidienne et ajoute l’export PDF, l’impression, la liste des termes toujours masqués et le choix de la couleur du masque. Aucune publicité, aucun filigrane."),
        "hi": ("मुफ़्त में क्या मिलता है, और Pro में क्या जुड़ता है?",
               "निजी जानकारी ढूँढना मुफ़्त और असीमित है, और ढकी हुई कॉपी को रोज़ 3 दस्तावेज़ों तक मुफ़्त में सेव, कॉपी या शेयर कर सकते हैं। Pro एक बार की खरीद है जो रोज़ की सीमा हटाता है और PDF एक्सपोर्ट, प्रिंट, हमेशा छिपाने वाली सूची और मास्क का रंग चुनना जोड़ता है। कोई विज्ञापन या वॉटरमार्क नहीं है।"),
        "id": ("Apa yang gratis, dan apa tambahan Pro?",
               "Menemukan info pribadi gratis dan tanpa batas, dan kamu bisa menyimpan, menyalin, atau membagikan salinan yang sudah ditutup untuk 3 dokumen per hari secara gratis. Pro adalah pembelian sekali yang menghapus batas harian dan menambahkan ekspor PDF, cetak, daftar yang selalu disembunyikan, dan pilihan warna masker. Tidak ada iklan dan tanpa tanda air."),
        "it": ("Cosa è gratis e cosa aggiunge Pro?",
               "Trovare i dati personali è gratis e illimitato, e puoi salvare, copiare o condividere gratis la copia oscurata di 3 documenti al giorno. Pro è un acquisto unico che toglie il limite giornaliero e aggiunge esportazione PDF, stampa, l’elenco dei termini da nascondere sempre e la scelta del colore della maschera. Niente pubblicità e nessuna filigrana."),
        "ms": ("Apa yang percuma, dan apa tambahan Pro?",
               "Mencari maklumat peribadi adalah percuma dan tanpa had, dan anda boleh menyimpan, menyalin atau berkongsi salinan yang telah ditutup bagi 3 dokumen sehari secara percuma. Pro ialah belian sekali yang membuang had harian dan menambah eksport PDF, cetakan, senarai yang sentiasa disembunyikan dan pilihan warna topeng. Tiada iklan dan tiada tera air."),
        "nl": ("Wat is gratis, en wat voegt Pro toe?",
               "Persoonlijke gegevens vinden is gratis en onbeperkt, en de afgedekte kopie van 3 documenten per dag kun je gratis opslaan, kopiëren of delen. Pro is een eenmalige aankoop die de daglimiet opheft en PDF-export, afdrukken, de lijst met altijd te verbergen termen en een eigen maskerkleur toevoegt. Geen advertenties en geen watermerk."),
        "pl": ("Co jest za darmo, a co dodaje Pro?",
               "Wyszukiwanie danych osobowych jest darmowe i bez limitu, a zakrytą kopię 3 dokumentów dziennie możesz za darmo zapisać, skopiować lub udostępnić. Pro to jednorazowy zakup, który znosi dzienny limit i dodaje eksport do PDF, drukowanie, listę zawsze ukrywanych słów i wybór koloru maski. Bez reklam i bez znaku wodnego."),
        "pt": ("O que é grátis e o que o Pro acrescenta?",
               "Encontrar informações pessoais é grátis e ilimitado, e você pode salvar, copiar ou compartilhar de graça a cópia mascarada de 3 documentos por dia. O Pro é uma compra única que remove o limite diário e acrescenta exportação em PDF, impressão, a lista de termos sempre ocultos e a escolha da cor da máscara. Sem anúncios e sem marca d’água."),
        "ru": ("Что доступно бесплатно и что добавляет Pro?",
               "Поиск личных данных бесплатен и не ограничен, а сохранить, скопировать или отправить закрытую копию можно бесплатно для 3 документов в день. Pro — разовая покупка: снимает дневной лимит и добавляет экспорт в PDF, печать, список всегда скрываемых слов и выбор цвета маски. Нет рекламы и водяных знаков."),
        "th": ("ฟรีใช้อะไรได้บ้าง และ Pro เพิ่มอะไร",
               "การค้นหาข้อมูลส่วนตัวใช้ฟรีไม่จำกัด และบันทึก คัดลอก หรือแชร์สำเนาที่ปิดข้อมูลแล้วได้ฟรีวันละ 3 เอกสาร Pro เป็นการซื้อครั้งเดียว ยกเลิกขีดจำกัดรายวัน และเพิ่มการส่งออก PDF การพิมพ์ รายการคำที่ซ่อนเสมอ และการเลือกสีของแถบปิด ไม่มีโฆษณาและไม่มีลายน้ำ"),
        "tr": ("Ücretsiz sürümde neler var, Pro neler ekliyor?",
               "Kişisel bilgileri bulmak ücretsiz ve sınırsızdır; maskelenmiş kopyayı günde 3 belge için ücretsiz kaydedebilir, kopyalayabilir ya da paylaşabilirsiniz. Pro tek seferlik bir satın almadır; günlük sınırı kaldırır ve PDF dışa aktarma, yazdırma, her zaman gizlenecekler listesi ile maske rengi seçimini ekler. Reklam ve filigran yoktur."),
        "uk": ("Що доступно безкоштовно і що додає Pro?",
               "Пошук особистих даних безкоштовний і необмежений, а зберегти, скопіювати або надіслати закриту копію можна безкоштовно для 3 документів на день. Pro — разова покупка: знімає денний ліміт і додає експорт у PDF, друк, список слів, які завжди приховуються, і вибір кольору маски. Немає реклами й водяних знаків."),
        "vi": ("Bản miễn phí có gì, và Pro thêm gì?",
               "Tìm thông tin cá nhân là miễn phí và không giới hạn, và bạn có thể lưu, sao chép hoặc chia sẻ miễn phí bản đã che của 3 tài liệu mỗi ngày. Pro là gói mua một lần, bỏ giới hạn hằng ngày và thêm xuất PDF, in, danh sách luôn ẩn và chọn màu che. Không có quảng cáo và không có hình mờ."),
        "ar": ("ما المجاني، وماذا يضيف Pro؟",
               "العثور على المعلومات الشخصية مجاني وبلا حدود، ويمكنك حفظ النسخة المحجوبة أو نسخها أو مشاركتها مجانًا لثلاثة مستندات يوميًا. Pro شراء لمرة واحدة يزيل الحد اليومي ويضيف التصدير إلى PDF والطباعة وقائمة الإخفاء الدائم واختيار لون القناع. لا توجد إعلانات ولا علامة مائية."),
    },
}


def main():
    langs = sorted(f[:-5] for f in os.listdir(os.path.join(ROOT, "i18n")) if f.endswith(".json"))
    problems = []
    for lang in langs:
        p = os.path.join(ROOT, "i18n", lang + ".json")
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        apps = data["apps"]

        a = apps["autostart"]
        tag, f0, f4, (old, new) = AS[lang]
        a["tagline"], a["features"][0], a["features"][4] = tag, f0, f4
        if a["long"].count(old) != 1:
            problems.append((lang, "autostart.long", old))
        a["long"] = a["long"].replace(old, new)

        v = apps["volumebooster"]
        (lo, ln), (fo, fn) = VB[lang]
        if v["long"].count(lo) != 1:
            problems.append((lang, "volumebooster.long", lo))
        if v["faq"][0]["a"].count(fo) != 1:
            problems.append((lang, "volumebooster.faq0", fo))
        v["long"] = v["long"].replace(lo, ln)
        v["faq"][0]["a"] = v["faq"][0]["a"].replace(fo, fn)

        for slug, table in FAQ.items():
            q, ans = table[lang]
            faq = apps[slug].setdefault("faq", [])
            if not any(x["q"] == q for x in faq):
                faq.append({"q": q, "a": ans})

        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
    if problems:
        for x in problems:
            print("!! 원문을 못 찾음(또는 여러 번):", x)
        sys.exit(1)
    print("OK", len(langs), "개 언어")


if __name__ == "__main__":
    main()
