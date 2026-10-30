# -*- coding: utf-8 -*-
"""Clipboard+ for Windows 페이지 FAQ 3번 정정(2026-10-30) — 21개 언어.

Windows 판은 2026-09-05 부터 전 기능 무료(ClipboardWin ProGate.ProEnabled=false)인데 사이트 FAQ 는 아직
"Pro 가 동기화·PDF·백업 가져오기·그룹 무제한을 더한다"고 적혀 있었다. 이 FAQ 가 llms.txt·구조화 데이터(FAQPage)로
그대로 나가 AI 답변이 틀린 사실을 말할 수 있었다.

    python scripts/edits/clipboardwin_free_faq_20261030.py   → node scripts/gen_site.js
"""
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "i18n")
T = {
 "en": ("Is Clipboard+ for Windows free?",
        "Yes. Every feature of the Windows version is free — clipboard history with search, snippets and groups, the quick-pick popup, Google Drive sync, copying image clips, PDF export and backup import and export. No in-app purchases, no ads, no account. (On the phone side, sync is a Pro feature of the Android app.)"),
 "ko": ("Windows용 Clipboard+는 무료인가요?",
        "네. Windows 판은 모든 기능이 무료입니다 — 검색되는 클립보드 기록, 스니펫과 그룹, 빠른 붙여넣기 팝업, Google Drive 동기화, 이미지 클립 복사, PDF 내보내기, 백업 가져오기·내보내기까지. 인앱 결제도, 광고도, 계정도 없습니다. (폰 쪽에서는 동기화가 안드로이드 앱의 Pro 기능입니다.)"),
 "ja": ("Windows版Clipboard+は無料ですか？",
        "はい。Windows版はすべての機能が無料です。検索できるクリップボード履歴、スニペットとグループ、クイックペーストのポップアップ、Google Driveの同期、画像クリップのコピー、PDF出力、バックアップの読み込みと書き出しまで。アプリ内課金も広告もアカウントもありません。（スマホ側では、同期はAndroidアプリのPro機能です。）"),
 "zh": ("Windows 版 Clipboard+ 免费吗？",
        "是的。Windows 版的所有功能都免费——可搜索的剪贴板历史、常用片段与分组、快速粘贴弹窗、Google Drive 同步、复制图片剪贴、PDF 导出以及备份导入和导出。没有应用内购买，没有广告，也不需要账号。（在手机端，同步是 Android 应用的专业版功能。）"),
 "de": ("Ist Clipboard+ für Windows kostenlos?",
        "Ja. Alle Funktionen der Windows-Version sind kostenlos – durchsuchbarer Zwischenablage-Verlauf, Schnipsel und Gruppen, das Schnelleinfüge-Popup, Google-Drive-Sync, das Kopieren von Bild-Clips, PDF-Export sowie Backup-Import und -Export. Keine In-App-Käufe, keine Werbung, kein Konto. (Auf dem Handy ist Sync eine Pro-Funktion der Android-App.)"),
 "es": ("¿Clipboard+ para Windows es gratis?",
        "Sí. Todas las funciones de la versión para Windows son gratis: historial del portapapeles con búsqueda, fragmentos y grupos, la ventana emergente de pegado rápido, sincronización con Google Drive, copiar imágenes, exportar a PDF e importar y exportar copias de seguridad. Sin compras en la app, sin anuncios y sin cuenta. (En el móvil, la sincronización es una función Pro de la app de Android.)"),
 "fr": ("Clipboard+ pour Windows est-il gratuit ?",
        "Oui. Toutes les fonctions de la version Windows sont gratuites : historique du presse-papiers avec recherche, extraits et groupes, la fenêtre de collage rapide, la synchronisation Google Drive, la copie des images, l'export PDF ainsi que l'import et l'export de sauvegardes. Pas d'achat intégré, pas de publicité, pas de compte. (Côté téléphone, la synchronisation est une fonction Pro de l'appli Android.)"),
 "it": ("Clipboard+ per Windows è gratis?",
        "Sì. Tutte le funzioni della versione per Windows sono gratis: cronologia degli appunti con ricerca, frammenti e gruppi, il popup di incolla rapido, la sincronizzazione con Google Drive, la copia delle immagini, l'esportazione in PDF e l'importazione ed esportazione dei backup. Nessun acquisto in-app, nessuna pubblicità, nessun account. (Sul telefono la sincronizzazione è una funzione Pro dell'app Android.)"),
 "pt": ("O Clipboard+ para Windows é gratuito?",
        "Sim. Todos os recursos da versão para Windows são gratuitos: histórico da área de transferência com busca, trechos e grupos, o pop-up de colagem rápida, sincronização com o Google Drive, cópia de imagens, exportação em PDF e importação e exportação de backup. Sem compras no app, sem anúncios e sem conta. (No celular, a sincronização é um recurso Pro do app para Android.)"),
 "nl": ("Is Clipboard+ voor Windows gratis?",
        "Ja. Alle functies van de Windows-versie zijn gratis: doorzoekbare klembordgeschiedenis, fragmenten en groepen, de snelplak-pop-up, synchronisatie via Google Drive, afbeeldingen kopiëren, PDF-export en back-ups importeren en exporteren. Geen in-app-aankopen, geen advertenties, geen account. (Op de telefoon is synchronisatie een Pro-functie van de Android-app.)"),
 "pl": ("Czy Clipboard+ dla Windows jest darmowy?",
        "Tak. Wszystkie funkcje wersji dla Windows są darmowe: historia schowka z wyszukiwaniem, fragmenty i grupy, okienko szybkiego wklejania, synchronizacja przez Dysk Google, kopiowanie obrazów, eksport do PDF oraz import i eksport kopii zapasowych. Bez zakupów w aplikacji, bez reklam, bez konta. (Na telefonie synchronizacja to funkcja Pro aplikacji na Androida.)"),
 "ru": ("Clipboard+ для Windows бесплатный?",
        "Да. Все функции версии для Windows бесплатны: история буфера обмена с поиском, заготовки и группы, всплывающее окно быстрой вставки, синхронизация через Google Диск, копирование изображений, экспорт в PDF, импорт и экспорт резервных копий. Без встроенных покупок, без рекламы, без аккаунта. (На телефоне синхронизация — функция Pro приложения для Android.)"),
 "uk": ("Clipboard+ для Windows безкоштовний?",
        "Так. Усі функції версії для Windows безкоштовні: історія буфера обміну з пошуком, фрагменти й групи, спливне вікно швидкого вставлення, синхронізація через Google Диск, копіювання зображень, експорт у PDF, імпорт і експорт резервних копій. Без вбудованих покупок, без реклами, без облікового запису. (На телефоні синхронізація — функція Pro застосунку для Android.)"),
 "tr": ("Windows için Clipboard+ ücretsiz mi?",
        "Evet. Windows sürümünün tüm özellikleri ücretsizdir: aranabilir pano geçmişi, parçacıklar ve gruplar, hızlı yapıştırma penceresi, Google Drive eşitleme, görsel kopyalama, PDF dışa aktarma ile yedek içe ve dışa aktarma. Uygulama içi satın alma, reklam ve hesap yok. (Telefon tarafında eşitleme, Android uygulamasının bir Pro özelliğidir.)"),
 "id": ("Apakah Clipboard+ untuk Windows gratis?",
        "Ya. Semua fitur versi Windows gratis: riwayat papan klip yang bisa dicari, cuplikan dan grup, popup tempel cepat, sinkronisasi Google Drive, menyalin gambar, ekspor PDF, serta impor dan ekspor cadangan. Tanpa pembelian dalam aplikasi, tanpa iklan, tanpa akun. (Di ponsel, sinkronisasi adalah fitur Pro aplikasi Android.)"),
 "ms": ("Adakah Clipboard+ untuk Windows percuma?",
        "Ya. Semua ciri versi Windows adalah percuma: sejarah papan klip yang boleh dicari, petikan dan kumpulan, tetingkap tampal pantas, penyegerakan Google Drive, salin imej, eksport PDF serta import dan eksport sandaran. Tiada pembelian dalam apl, tiada iklan, tiada akaun. (Di telefon, penyegerakan ialah ciri Pro apl Android.)"),
 "vi": ("Clipboard+ cho Windows có miễn phí không?",
        "Có. Mọi tính năng của bản Windows đều miễn phí: lịch sử clipboard có tìm kiếm, đoạn mẫu và nhóm, cửa sổ dán nhanh, đồng bộ Google Drive, sao chép ảnh, xuất PDF cùng nhập và xuất bản sao lưu. Không mua trong ứng dụng, không quảng cáo, không cần tài khoản. (Trên điện thoại, đồng bộ là tính năng Pro của ứng dụng Android.)"),
 "th": ("Clipboard+ สำหรับ Windows ใช้ฟรีไหม",
        "ใช่ ทุกฟีเจอร์ของเวอร์ชัน Windows ใช้ฟรี — ประวัติคลิปบอร์ดที่ค้นหาได้ สนิปเป็ตและกลุ่ม ป๊อปอัปวางด่วน ซิงก์ผ่าน Google Drive คัดลอกรูปภาพ ส่งออก PDF รวมถึงนำเข้าและส่งออกข้อมูลสำรอง ไม่มีการซื้อในแอป ไม่มีโฆษณา ไม่ต้องมีบัญชี (ฝั่งโทรศัพท์ การซิงก์เป็นฟีเจอร์ Pro ของแอป Android)"),
 "hi": ("क्या Windows के लिए Clipboard+ मुफ़्त है?",
        "हाँ। Windows वर्शन की हर सुविधा मुफ़्त है — खोजने लायक क्लिपबोर्ड हिस्ट्री, स्निपेट और ग्रुप, क्विक-पेस्ट पॉपअप, Google Drive सिंक, इमेज क्लिप कॉपी करना, PDF एक्सपोर्ट और बैकअप इंपोर्ट व एक्सपोर्ट। न इन-ऐप खरीद, न विज्ञापन, न अकाउंट। (फ़ोन पर सिंक Android ऐप की Pro सुविधा है।)"),
 "ar": ("هل Clipboard+ لنظام Windows مجاني؟",
        "نعم. كل ميزات إصدار Windows مجانية: سجل الحافظة مع البحث، والمقتطفات والمجموعات، ونافذة اللصق السريع، والمزامنة عبر Google Drive، ونسخ الصور، والتصدير إلى PDF، واستيراد النسخ الاحتياطية وتصديرها. لا مشتريات داخل التطبيق، ولا إعلانات، ولا حساب. (على الهاتف، المزامنة ميزة Pro في تطبيق Android.)"),
 "fil": ("Libre ba ang Clipboard+ para sa Windows?",
         "Oo. Libre ang bawat feature ng Windows na bersyon — nahahanap na clipboard history, mga snippet at grupo, ang quick-paste popup, Google Drive sync, pagkopya ng mga larawan, PDF export, at pag-import at pag-export ng backup. Walang in-app purchase, walang ad, walang account. (Sa telepono, Pro feature ng Android app ang sync.)"),
}
n = 0
for lang, (q, a) in T.items():
    p = os.path.join(ROOT, f"{lang}.json")
    raw = open(p, encoding="utf-8").read()
    d = json.loads(raw)
    faq = d["apps"]["clipboardwin"]["faq"]
    assert len(faq) >= 3 and "Pro" in faq[2]["q"] + faq[2]["a"] or "专业版" in faq[2]["q"], lang
    faq[2] = {"q": q, "a": a}
    indent = 2 if raw.startswith("{\n  ") else None
    out = json.dumps(d, ensure_ascii=False, indent=indent)
    if raw.endswith("\n"):
        out += "\n"
    open(p, "w", encoding="utf-8", newline="").write(out)
    n += 1
print("updated", n)
