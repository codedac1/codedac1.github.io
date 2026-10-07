"""VolumeBooster+·FloatTimer+·FloatNote+ 에 "안드로이드 차량 헤드유닛에서도 쓸 수 있나요?" FAQ — 21개 언어.

10/6~7 출시분에 헤드유닛(가로·높이 ~400dp) 첫 실행 화면 레이아웃이 들어갔다. 고친 건 첫 실행(온보딩)
화면뿐이라 답도 "설정 화면이 넓고 낮은 가로 화면에 맞춰져 있다" 까지만 말한다(과장 금지).
최소 Android 는 각 앱 minSdk(VolumeBooster 24=7.0, FloatTimer·FloatNote 26=8.0), 권한 이름은 앱 strings 의
guide_sys_overlay_title 번역 그대로. 몇 번 돌려도 같은 결과.
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]

Q = {
 "en": "Can I use {app} on an Android car head unit?",
 "ar": "هل يمكنني استخدام {app} على شاشة سيارة تعمل بنظام أندرويد؟",
 "de": "Kann ich {app} auf einem Android-Autoradio nutzen?",
 "es": "¿Puedo usar {app} en una radio de coche Android?",
 "fil": "Magagamit ko ba ang {app} sa isang Android car head unit?",
 "fr": "Puis-je utiliser {app} sur un autoradio Android ?",
 "hi": "क्या मैं {app} को Android कार हेड यूनिट पर इस्तेमाल कर सकता हूँ?",
 "id": "Bisakah saya memakai {app} di head unit mobil Android?",
 "it": "Posso usare {app} su un'autoradio Android?",
 "ja": "{app} は Android の車載ヘッドユニットでも使えますか？",
 "ko": "안드로이드 차량 헤드유닛에서도 쓸 수 있나요?",
 "ms": "Bolehkah saya menggunakan {app} pada unit kepala kereta Android?",
 "nl": "Kan ik {app} gebruiken op een Android-autoradio?",
 "pl": "Czy mogę używać {app} na radioodtwarzaczu samochodowym z Androidem?",
 "pt": "Posso usar o {app} em uma central multimídia Android?",
 "ru": "Можно ли пользоваться {app} на Android-автомагнитоле?",
 "th": "ใช้ {app} กับจอแอนดรอยด์ติดรถยนต์ได้ไหม",
 "tr": "{app} uygulamasını Android araç multimedya cihazında kullanabilir miyim?",
 "uk": "Чи можна користуватися {app} на Android-автомагнітолі?",
 "vi": "Tôi có thể dùng {app} trên màn hình Android ô tô không?",
 "zh": "{app} 能在安卓车机上使用吗？",
}
REQ = {
 "en": "Yes, if your head unit has Google Play and runs Android {v} or later.",
 "ar": "نعم، إذا كانت شاشة سيارتك تحتوي على Google Play وتعمل بنظام Android {v} أو أحدث.",
 "de": "Ja, wenn dein Autoradio Google Play hat und mit Android {v} oder neuer läuft.",
 "es": "Sí, si tu radio de coche tiene Google Play y Android {v} o posterior.",
 "fil": "Oo, kung may Google Play ang iyong car head unit at Android {v} o mas bago ito.",
 "fr": "Oui, si votre autoradio dispose de Google Play et tourne sous Android {v} ou plus récent.",
 "hi": "हाँ, अगर आपकी कार हेड यूनिट में Google Play है और वह Android {v} या उससे नए वर्शन पर चलती है।",
 "id": "Ya, jika head unit mobil Anda punya Google Play dan menjalankan Android {v} atau lebih baru.",
 "it": "Sì, se la tua autoradio ha Google Play e usa Android {v} o versioni successive.",
 "ja": "はい。Google Play があり、Android {v} 以降で動く車載ヘッドユニットなら使えます。",
 "ko": "네. Google Play가 있고 Android {v} 이상인 차량 헤드유닛이라면 사용할 수 있습니다.",
 "ms": "Ya, jika unit kepala kereta anda mempunyai Google Play dan menjalankan Android {v} atau lebih baharu.",
 "nl": "Ja, als je autoradio Google Play heeft en Android {v} of nieuwer draait.",
 "pl": "Tak, jeśli radioodtwarzacz ma Google Play i działa na Androidzie {v} lub nowszym.",
 "pt": "Sim, se a sua central multimídia tiver Google Play e rodar Android {v} ou mais recente.",
 "ru": "Да, если на автомагнитоле есть Google Play и установлен Android {v} или новее.",
 "th": "ได้ หากจอแอนดรอยด์ติดรถยนต์ของคุณมี Google Play และใช้ Android {v} ขึ้นไป",
 "tr": "Evet, araç multimedya cihazınızda Google Play varsa ve Android {v} veya üstü çalışıyorsa.",
 "uk": "Так, якщо на автомагнітолі є Google Play і встановлено Android {v} або новіший.",
 "vi": "Có, nếu màn hình Android ô tô của bạn có Google Play và chạy Android {v} trở lên.",
 "zh": "可以。只要车机装有 Google Play，且系统为 Android {v} 或更高版本即可使用。",
}
LAND = {
 "en": "The setup screens are laid out for wide, short landscape displays.",
 "ar": "صُممت شاشات الإعداد لتناسب الشاشات الأفقية العريضة والقصيرة.",
 "de": "Die Einrichtungsbildschirme sind für breite, flache Querformat-Displays ausgelegt.",
 "es": "Las pantallas de configuración están pensadas para pantallas horizontales anchas y bajas.",
 "fil": "Inayos ang mga setup screen para sa malapad at mababang landscape na display.",
 "fr": "Les écrans de configuration sont conçus pour les affichages paysage larges et bas.",
 "hi": "सेटअप स्क्रीनें चौड़े, कम ऊँचाई वाले लैंडस्केप डिस्प्ले के लिए बनाई गई हैं।",
 "id": "Layar penyiapan dirancang untuk layar lanskap yang lebar dan pendek.",
 "it": "Le schermate di configurazione sono pensate per display orizzontali larghi e bassi.",
 "ja": "初期設定の画面は横長で背の低いディスプレイに合わせてあります。",
 "ko": "처음 설정 화면은 넓고 낮은 가로 화면에 맞춰져 있습니다.",
 "ms": "Skrin persediaan direka untuk paparan landskap yang lebar dan rendah.",
 "nl": "De installatieschermen zijn gemaakt voor brede, lage liggende displays.",
 "pl": "Ekrany konfiguracji są przygotowane na szerokie, niskie wyświetlacze poziome.",
 "pt": "As telas de configuração foram feitas para displays horizontais largos e baixos.",
 "ru": "Экраны первой настройки рассчитаны на широкие и невысокие горизонтальные дисплеи.",
 "th": "หน้าตั้งค่าเริ่มต้นจัดวางให้พอดีกับจอแนวนอนที่กว้างและเตี้ย",
 "tr": "Kurulum ekranları geniş ve alçak yatay ekranlar için düzenlendi.",
 "uk": "Екрани першого налаштування розраховані на широкі й невисокі горизонтальні дисплеї.",
 "vi": "Các màn hình thiết lập được bố trí cho màn hình ngang rộng và thấp.",
 "zh": "初始设置界面已适配宽而矮的横屏。",
}
VB = {
 "en": "How much louder it gets depends on the head unit's own amplifier and speakers.",
 "ar": "يعتمد مقدار رفع الصوت على مضخم شاشة السيارة ومكبرات الصوت فيها.",
 "de": "Wie viel lauter es wird, hängt vom Verstärker und den Lautsprechern des Autoradios ab.",
 "es": "Cuánto más fuerte suene depende del amplificador y los altavoces de la radio.",
 "fil": "Kung gaano kalakas ang madadagdag ay depende sa amplifier at speaker ng head unit.",
 "fr": "Le gain de volume dépend de l'amplificateur et des haut-parleurs de l'autoradio.",
 "hi": "आवाज़ कितनी बढ़ेगी, यह हेड यूनिट के एम्पलीफ़ायर और स्पीकर पर निर्भर करता है।",
 "id": "Seberapa keras hasilnya tergantung pada amplifier dan speaker head unit.",
 "it": "Quanto aumenta il volume dipende dall'amplificatore e dagli altoparlanti dell'autoradio.",
 "ja": "どこまで大きくなるかは、ヘッドユニットのアンプとスピーカーによります。",
 "ko": "얼마나 더 커지는지는 헤드유닛의 앰프와 스피커에 따라 다릅니다.",
 "ms": "Sejauh mana bunyi menjadi lebih kuat bergantung pada penguat dan pembesar suara unit kepala.",
 "nl": "Hoeveel harder het wordt, hangt af van de versterker en speakers van de autoradio.",
 "pl": "To, o ile będzie głośniej, zależy od wzmacniacza i głośników radioodtwarzacza.",
 "pt": "O quanto o som fica mais alto depende do amplificador e dos alto-falantes da central.",
 "ru": "Насколько станет громче, зависит от усилителя и динамиков автомагнитолы.",
 "th": "เสียงจะดังขึ้นได้แค่ไหนขึ้นอยู่กับแอมป์และลำโพงของจอติดรถยนต์",
 "tr": "Sesin ne kadar yükseleceği cihazın amfisine ve hoparlörlerine bağlıdır.",
 "uk": "Наскільки стане гучніше, залежить від підсилювача й динаміків автомагнітоли.",
 "vi": "Âm lượng tăng được bao nhiêu tùy vào bộ khuếch đại và loa của màn hình ô tô.",
 "zh": "能增大多少取决于车机自身的功放和扬声器。",
}
FT = {
 "en": "The floating timer stays on top of navigation or music.",
 "ar": "يبقى المؤقت العائم فوق تطبيقات الملاحة أو الموسيقى.",
 "de": "Der schwebende Timer bleibt über Navigation oder Musik.",
 "es": "El temporizador flotante se queda encima de la navegación o la música.",
 "fil": "Nananatili ang floating timer sa ibabaw ng navigation o music app.",
 "fr": "Le minuteur flottant reste au-dessus de la navigation ou de la musique.",
 "hi": "फ़्लोटिंग टाइमर नेविगेशन या म्यूज़िक ऐप के ऊपर बना रहता है।",
 "id": "Timer mengambang tetap di atas aplikasi navigasi atau musik.",
 "it": "Il timer fluttuante resta sopra la navigazione o la musica.",
 "ja": "フローティングタイマーはナビや音楽アプリの上に表示されたままです。",
 "ko": "플로팅 타이머가 내비게이션이나 음악 앱 위에 떠 있습니다.",
 "ms": "Pemasa terapung kekal di atas apl navigasi atau muzik.",
 "nl": "De zwevende timer blijft boven navigatie of muziek staan.",
 "pl": "Pływający minutnik pozostaje nad nawigacją lub muzyką.",
 "pt": "O timer flutuante fica por cima da navegação ou da música.",
 "ru": "Плавающий таймер остаётся поверх навигации или музыки.",
 "th": "ตัวจับเวลาแบบลอยจะอยู่เหนือแอปนำทางหรือเพลง",
 "tr": "Yüzen zamanlayıcı navigasyon veya müziğin üzerinde kalır.",
 "uk": "Плаваючий таймер залишається поверх навігації чи музики.",
 "vi": "Bộ hẹn giờ nổi luôn nằm trên ứng dụng dẫn đường hoặc nhạc.",
 "zh": "悬浮计时器会一直显示在导航或音乐应用上方。",
}
FN = {
 "en": "Notes float on top of navigation or music.",
 "ar": "تطفو الملاحظات فوق تطبيقات الملاحة أو الموسيقى.",
 "de": "Notizen schweben über Navigation oder Musik.",
 "es": "Las notas flotan encima de la navegación o la música.",
 "fil": "Lumulutang ang mga nota sa ibabaw ng navigation o music app.",
 "fr": "Les notes flottent au-dessus de la navigation ou de la musique.",
 "hi": "नोट्स नेविगेशन या म्यूज़िक ऐप के ऊपर तैरते रहते हैं।",
 "id": "Catatan melayang di atas aplikasi navigasi atau musik.",
 "it": "Le note fluttuano sopra la navigazione o la musica.",
 "ja": "メモはナビや音楽アプリの上に浮かんで表示されます。",
 "ko": "메모가 내비게이션이나 음악 앱 위에 떠 있습니다.",
 "ms": "Nota terapung di atas apl navigasi atau muzik.",
 "nl": "Notities zweven boven navigatie of muziek.",
 "pl": "Notatki unoszą się nad nawigacją lub muzyką.",
 "pt": "As notas flutuam por cima da navegação ou da música.",
 "ru": "Заметки плавают поверх навигации или музыки.",
 "th": "โน้ตจะลอยอยู่เหนือแอปนำทางหรือเพลง",
 "tr": "Notlar navigasyon veya müziğin üzerinde yüzer.",
 "uk": "Нотатки плавають поверх навігації чи музики.",
 "vi": "Ghi chú nổi trên ứng dụng dẫn đường hoặc nhạc.",
 "zh": "便签会浮在导航或音乐应用上方。",
}
PERM = {  # FloatTimer strings guide_sys_overlay_title
 "en": "Display over other apps", "ar": "الظهور فوق التطبيقات الأخرى", "de": "Über anderen Apps einblenden",
 "es": "Mostrar sobre otras apps", "fil": "Ipakita sa ibabaw ng ibang app", "fr": "Superposition sur d’autres applis",
 "hi": "दूसरे ऐप्स के ऊपर दिखाएँ", "id": "Tampilkan di atas aplikasi lain", "it": "Mostra sopra altre app",
 "ja": "他のアプリの上に重ねて表示", "ko": "다른 앱 위에 표시", "ms": "Papar di atas apl lain",
 "nl": "Weergeven over andere apps", "pl": "Wyświetlanie nad innymi aplikacjami", "pt": "Sobrepor a outros apps",
 "ru": "Поверх других приложений", "th": "แสดงทับแอปอื่น", "tr": "Diğer uygulamaların üzerinde göster",
 "uk": "Поверх інших застосунків", "vi": "Hiển thị trên các ứng dụng khác", "zh": "显示在其他应用的上层",
}
OVERLAY = {
 "en": "The head unit must allow “{p}”.", "ar": "يجب أن تسمح شاشة السيارة بإذن «{p}».",
 "de": "Das Autoradio muss „{p}“ erlauben.", "es": "La radio debe permitir «{p}».",
 "fil": "Dapat payagan ng head unit ang “{p}”.", "fr": "L'autoradio doit autoriser « {p} ».",
 "hi": "हेड यूनिट में “{p}” की अनुमति होनी चाहिए।", "id": "Head unit harus mengizinkan “{p}”.",
 "it": "L'autoradio deve consentire «{p}».", "ja": "ヘッドユニットで「{p}」を許可できる必要があります。",
 "ko": "헤드유닛에서 “{p}” 권한을 허용할 수 있어야 합니다.", "ms": "Unit kepala mesti membenarkan “{p}”.",
 "nl": "De autoradio moet ‘{p}’ toestaan.", "pl": "Radioodtwarzacz musi zezwalać na „{p}”.",
 "pt": "A central precisa permitir “{p}”.", "ru": "Автомагнитола должна разрешать «{p}».",
 "th": "จอติดรถยนต์ต้องอนุญาต “{p}” ได้", "tr": "Cihazın “{p}” iznine izin vermesi gerekir.",
 "uk": "Автомагнітола має дозволяти «{p}».", "vi": "Màn hình ô tô phải cho phép “{p}”.", "zh": "车机需要允许“{p}”。",
}
SP = {"ja": "", "zh": "", "th": " "}

def answer(lang, parts):
    return SP.get(lang, " ").join(parts)

for lang in Q:
    p = ROOT / "i18n" / f"{lang}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    for slug, v, mid, overlay in (("volumebooster", "7.0", VB, False), ("floattimer", "8.0", FT, True), ("floatnote", "8.0", FN, True)):
        a = d["apps"][slug]
        q = Q[lang].format(app=a["name"])
        if lang == "ko":
            q = f"{a['name']}, " + q
        parts = [REQ[lang].format(v=v)]
        if overlay:
            parts += [mid[lang], LAND[lang], OVERLAY[lang].format(p=PERM[lang])]
        else:
            parts += [LAND[lang], mid[lang]]
        a["faq"] = [f for f in a["faq"] if f["q"] != q] + [{"q": q, "a": answer(lang, parts)}]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(lang, "ok")
