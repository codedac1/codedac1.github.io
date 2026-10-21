# -*- coding: utf-8 -*-
"""개인정보처리방침: Clipboard+(Android) 자동 저장이 쓰는 접근성 서비스 안내 (2026-10-21, 앱 10.14.0).

i18n/privacy/<lang>.json 21개에
  - 7항(권한) — Rotate+ 접근성 항목 바로 뒤에 Clipboard+ 접근성 항목
  - 변경 이력 맨 앞에 2026-10-21 항목
  - '최종 개정' 날짜 18 → 21
을 넣는다. 앱별 표의 '접근성 서비스'는 scan_app_privacy.js 를 다시 돌리면 매니페스트에서 잡힌다.
다시 돌려도 이미 들어가 있으면 건너뛴다.
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

T = {
 "en": ("(Clipboard+, optional) — used only when you turn on Auto-save (off by default), to notice the moment you tap Copy in another app or the system shows its “Copied” message, so the copied item is saved without opening Clipboard+. The service is set up so that it cannot read screen content; it does not record the text you type, and clips marked as passwords are not saved. Saved clips stay on your device (and, if you turned on PC sync, go only to your own Google Drive) and are never sent to us. You can turn it off at any time in the app’s settings or your device’s accessibility settings.",
        "Added the accessibility service used by Auto-save, an optional feature of Clipboard+ (Android) (section 7)."),
 "ko": ("(Clipboard+, 선택) — 기본으로 꺼져 있는 ‘자동 저장’을 켠 경우에만, 다른 앱에서 ‘복사’를 누르거나 시스템이 ‘복사했어요’ 안내를 띄우는 순간을 알아차려 복사한 내용을 앱을 열지 않아도 저장하는 데 사용합니다. 이 서비스는 화면 내용을 읽을 수 없도록 설정되어 있으며, 입력하는 텍스트를 기록하지 않고, 비밀번호로 표시된 클립은 저장하지 않습니다. 저장한 클립은 기기에만 남고(PC 동기화를 켠 경우 사용자 본인의 Google Drive로만 갑니다) 회사로 전송되지 않습니다. 앱 설정이나 기기의 접근성 설정에서 언제든지 끌 수 있습니다.",
        "Android용 Clipboard+의 선택 기능인 자동 저장이 사용하는 접근성 서비스 안내를 추가했습니다(7항)."),
 "ja": ("（Clipboard+、任意）— 初期設定でオフの「自動保存」をオンにした場合にのみ、ほかのアプリで「コピー」をタップした瞬間や、システムが「コピーしました」と表示した瞬間を検知し、Clipboard+を開かなくてもコピーした内容を保存するために使います。このサービスは画面の内容を読み取れないように設定されており、入力した文字を記録せず、パスワードとして指定されたクリップは保存しません。保存したクリップは端末内にのみ残り（PC同期をオンにした場合はご自身のGoogleドライブにのみ送られます）、当社に送信されることはありません。アプリの設定または端末のユーザー補助設定からいつでもオフにできます。",
        "Android版Clipboard+の任意機能である自動保存が使用するユーザー補助サービスについての説明を追加しました（第7項）。"),
 "zh": ("（Clipboard+，可选）— 仅在你开启默认关闭的“自动保存”时使用：感知你在其他应用中点按“复制”或系统显示“已复制”提示的那一刻，从而无需打开 Clipboard+ 即可保存复制的内容。该服务被设置为无法读取屏幕内容，不会记录你输入的文字，也不会保存标记为密码的剪贴内容。保存的剪贴内容只留在设备上（如果你开启了电脑同步，只会发送到你自己的 Google 云端硬盘），绝不会发送给我们。你可以随时在应用设置或设备的无障碍设置中关闭它。",
        "新增 Clipboard+（Android）的可选功能“自动保存”所使用的无障碍服务说明（第 7 条）。"),
 "de": ("(Clipboard+, optional) — wird nur verwendet, wenn du „Automatisch speichern“ (standardmäßig aus) einschaltest: Er bemerkt den Moment, in dem du in einer anderen App auf „Kopieren“ tippst oder das System „Kopiert“ anzeigt, damit das Kopierte gespeichert wird, ohne Clipboard+ zu öffnen. Der Dienst ist so eingerichtet, dass er keine Bildschirminhalte lesen kann; er zeichnet keine Eingaben auf, und als Passwort markierte Clips werden nicht gespeichert. Gespeicherte Clips bleiben auf deinem Gerät (bei aktivierter PC-Synchronisierung nur in deinem eigenen Google Drive) und werden nie an uns gesendet. Du kannst ihn jederzeit in den App-Einstellungen oder in den Bedienungshilfen deines Geräts ausschalten.",
        "Hinweis zum Bedienungshilfendienst ergänzt, den die optionale Funktion „Automatisch speichern“ von Clipboard+ (Android) verwendet (Abschnitt 7)."),
 "es": ("(Clipboard+, opcional) — se usa solo si activas el guardado automático (desactivado por defecto), para detectar el momento en que tocas Copiar en otra app o el sistema muestra el aviso “Copiado”, de modo que lo copiado se guarde sin abrir Clipboard+. El servicio está configurado para no poder leer el contenido de la pantalla; no registra lo que escribes y no guarda los clips marcados como contraseñas. Los clips guardados se quedan en tu dispositivo (y, si activaste la sincronización con el PC, solo van a tu propio Google Drive) y nunca se nos envían. Puedes desactivarlo cuando quieras en los ajustes de la app o en los ajustes de accesibilidad del dispositivo.",
        "Se añadió el servicio de accesibilidad que usa el guardado automático, una función opcional de Clipboard+ (Android) (apartado 7)."),
 "pt": ("(Clipboard+, opcional) — usado somente se você ativar o salvamento automático (desativado por padrão), para perceber o momento em que você toca em Copiar em outro app ou o sistema mostra o aviso “Copiado”, de modo que o conteúdo copiado seja salvo sem abrir o Clipboard+. O serviço é configurado para não conseguir ler o conteúdo da tela; ele não registra o que você digita e não salva clipes marcados como senha. Os clipes salvos ficam no seu dispositivo (e, se você ativou a sincronização com o PC, vão apenas para o seu próprio Google Drive) e nunca são enviados para nós. Você pode desativá-lo a qualquer momento nas configurações do app ou nas configurações de acessibilidade do dispositivo.",
        "Adicionamos o serviço de acessibilidade usado pelo salvamento automático, um recurso opcional do Clipboard+ (Android) (item 7)."),
 "fr": ("(Clipboard+, facultatif) — utilisé uniquement si vous activez l’enregistrement automatique (désactivé par défaut), pour repérer le moment où vous touchez Copier dans une autre appli ou où le système affiche « Copié », afin d’enregistrer l’élément copié sans ouvrir Clipboard+. Le service est configuré pour ne pas pouvoir lire le contenu de l’écran ; il n’enregistre pas ce que vous tapez et n’enregistre pas les éléments marqués comme mots de passe. Les éléments enregistrés restent sur votre appareil (et, si vous avez activé la synchronisation avec le PC, vont uniquement vers votre propre Google Drive) et ne nous sont jamais envoyés. Vous pouvez le désactiver à tout moment dans les paramètres de l’appli ou dans les paramètres d’accessibilité de l’appareil.",
        "Ajout du service d’accessibilité utilisé par l’enregistrement automatique, une fonction facultative de Clipboard+ (Android) (section 7)."),
 "it": ("(Clipboard+, facoltativo) — usato solo se attivi il salvataggio automatico (disattivato di default), per accorgersi del momento in cui tocchi Copia in un’altra app o il sistema mostra l’avviso “Copiato”, così ciò che hai copiato viene salvato senza aprire Clipboard+. Il servizio è configurato per non poter leggere il contenuto dello schermo; non registra ciò che digiti e non salva gli elementi contrassegnati come password. Gli elementi salvati restano sul dispositivo (e, se hai attivato la sincronizzazione con il PC, vanno solo sul tuo Google Drive) e non ci vengono mai inviati. Puoi disattivarlo in qualsiasi momento nelle impostazioni dell’app o nelle impostazioni di accessibilità del dispositivo.",
        "Aggiunto il servizio di accessibilità usato dal salvataggio automatico, una funzione facoltativa di Clipboard+ (Android) (punto 7)."),
 "nl": ("(Clipboard+, optioneel) — alleen gebruikt als je Automatisch opslaan (standaard uit) inschakelt, om het moment op te merken waarop je in een andere app op Kopiëren tikt of het systeem ‘Gekopieerd’ toont, zodat het gekopieerde wordt bewaard zonder Clipboard+ te openen. De service is zo ingesteld dat hij geen scherminhoud kan lezen; hij registreert niet wat je typt en bewaart geen als wachtwoord gemarkeerde clips. Bewaarde clips blijven op je apparaat (en gaan, als je pc-synchronisatie hebt ingeschakeld, alleen naar je eigen Google Drive) en worden nooit naar ons verstuurd. Je kunt hem altijd uitschakelen in de app-instellingen of de toegankelijkheidsinstellingen van je apparaat.",
        "Uitleg toegevoegd over de toegankelijkheidsservice die Automatisch opslaan, een optionele functie van Clipboard+ (Android), gebruikt (artikel 7)."),
 "pl": ("(Clipboard+, opcjonalnie) — używana tylko po włączeniu automatycznego zapisu (domyślnie wyłączony), aby wykryć chwilę, gdy dotykasz „Kopiuj” w innej aplikacji lub system pokazuje komunikat „Skopiowano”, dzięki czemu skopiowana treść zapisuje się bez otwierania Clipboard+. Usługa jest skonfigurowana tak, że nie może odczytywać zawartości ekranu; nie rejestruje tego, co wpisujesz, i nie zapisuje elementów oznaczonych jako hasła. Zapisane elementy zostają na urządzeniu (a po włączeniu synchronizacji z PC trafiają tylko na Twój własny Dysk Google) i nigdy nie są do nas wysyłane. Możesz ją w każdej chwili wyłączyć w ustawieniach aplikacji lub w ustawieniach ułatwień dostępu urządzenia.",
        "Dodano informacje o usłudze ułatwień dostępu używanej przez automatyczny zapis — opcjonalną funkcję Clipboard+ (Android) (punkt 7)."),
 "ru": ("(Clipboard+, по желанию) — используется, только если вы включили автосохранение (по умолчанию выключено), чтобы заметить момент, когда вы нажимаете «Копировать» в другом приложении или система показывает «Скопировано», и сохранить скопированное без открытия Clipboard+. Служба настроена так, что не может читать содержимое экрана; она не записывает вводимый текст и не сохраняет элементы, помеченные как пароли. Сохранённые элементы остаются на устройстве (а при включённой синхронизации с ПК попадают только на ваш Google Диск) и никогда не отправляются нам. Её можно в любой момент отключить в настройках приложения или в настройках специальных возможностей устройства.",
        "Добавлены сведения о службе специальных возможностей, которую использует автосохранение — дополнительная функция Clipboard+ (Android) (раздел 7)."),
 "uk": ("(Clipboard+, за бажанням) — використовується, лише якщо ви ввімкнули автозбереження (типово вимкнено), щоб помітити момент, коли ви торкаєтеся «Копіювати» в іншому застосунку або система показує «Скопійовано», і зберегти скопійоване без відкриття Clipboard+. Службу налаштовано так, що вона не може читати вміст екрана; вона не записує введений текст і не зберігає елементи, позначені як паролі. Збережені елементи залишаються на пристрої (а за ввімкненої синхронізації з ПК потрапляють лише на ваш Google Диск) і ніколи не надсилаються нам. Її можна будь-коли вимкнути в налаштуваннях застосунку або в налаштуваннях спеціальних можливостей пристрою.",
        "Додано відомості про службу спеціальних можливостей, яку використовує автозбереження — додаткова функція Clipboard+ (Android) (розділ 7)."),
 "tr": ("(Clipboard+, isteğe bağlı) — yalnızca varsayılan olarak kapalı olan otomatik kaydetmeyi açarsanız kullanılır: başka bir uygulamada Kopyala’ya dokunduğunuz ya da sistemin “Kopyalandı” mesajını gösterdiği anı fark eder, böylece kopyaladığınız Clipboard+ açılmadan kaydedilir. Hizmet ekran içeriğini okuyamayacak şekilde ayarlanmıştır; yazdığınız metni kaydetmez ve parola olarak işaretlenen klipleri kaydetmez. Kaydedilen klipler cihazınızda kalır (PC eşitlemesini açtıysanız yalnızca kendi Google Drive’ınıza gider) ve bize asla gönderilmez. Uygulama ayarlarından veya cihazınızın erişilebilirlik ayarlarından istediğiniz zaman kapatabilirsiniz.",
        "Clipboard+ (Android) uygulamasının isteğe bağlı özelliği otomatik kaydetmenin kullandığı erişilebilirlik hizmeti açıklaması eklendi (madde 7)."),
 "ar": ("(Clipboard+‎، اختياري) — يُستخدم فقط إذا شغّلت الحفظ التلقائي (متوقف افتراضيًا)، لملاحظة لحظة نقرك على «نسخ» في تطبيق آخر أو عرض النظام لرسالة «تم النسخ»، حتى يُحفظ ما نسخته دون فتح Clipboard+‎. الخدمة مُعدّة بحيث لا يمكنها قراءة محتوى الشاشة؛ ولا تسجّل ما تكتبه، ولا تحفظ العناصر المميزة ككلمات مرور. تبقى العناصر المحفوظة على جهازك (وإذا شغّلت المزامنة مع الكمبيوتر فإنها تذهب إلى Google Drive الخاص بك فقط) ولا تُرسل إلينا أبدًا. يمكنك إيقافها في أي وقت من إعدادات التطبيق أو من إعدادات إمكانية الوصول في جهازك.",
        "أُضيف توضيح لخدمة تسهيل الاستخدام التي يستخدمها الحفظ التلقائي، وهو ميزة اختيارية في Clipboard+‎ (Android) (البند 7)."),
 "hi": ("(Clipboard+, वैकल्पिक) — सिर्फ़ तब इस्तेमाल होती है जब आप अपने-आप सेव (डिफ़ॉल्ट रूप से बंद) चालू करते हैं, ताकि उस पल को पहचाना जा सके जब आप किसी दूसरे ऐप में कॉपी पर टैप करते हैं या सिस्टम \"कॉपी किया गया\" संदेश दिखाता है, और कॉपी की गई चीज़ Clipboard+ खोले बिना सेव हो जाए। यह सेवा इस तरह सेट है कि स्क्रीन की सामग्री नहीं पढ़ सकती; यह आपकी टाइप की गई चीज़ें रिकॉर्ड नहीं करती और पासवर्ड के रूप में चिह्नित क्लिप सेव नहीं करती। सेव की गई क्लिप आपके डिवाइस पर ही रहती हैं (PC सिंक चालू होने पर सिर्फ़ आपकी अपनी Google Drive में जाती हैं) और हमें कभी नहीं भेजी जातीं। आप इसे कभी भी ऐप की सेटिंग या डिवाइस की सुलभता सेटिंग में बंद कर सकते हैं।",
        "Clipboard+ (Android) की वैकल्पिक सुविधा अपने-आप सेव द्वारा इस्तेमाल की जाने वाली सुलभता सेवा की जानकारी जोड़ी गई (धारा 7)।"),
 "id": ("(Clipboard+, opsional) — hanya digunakan jika Anda mengaktifkan simpan otomatis (nonaktif secara default), untuk mendeteksi saat Anda mengetuk Salin di aplikasi lain atau sistem menampilkan pesan \"Disalin\", sehingga yang disalin tersimpan tanpa membuka Clipboard+. Layanan ini diatur agar tidak dapat membaca konten layar; layanan ini tidak merekam teks yang Anda ketik dan tidak menyimpan klip yang ditandai sebagai sandi. Klip yang tersimpan tetap di perangkat Anda (dan jika sinkronisasi PC aktif, hanya masuk ke Google Drive Anda sendiri) dan tidak pernah dikirim ke kami. Anda dapat menonaktifkannya kapan saja di setelan aplikasi atau setelan aksesibilitas perangkat.",
        "Menambahkan penjelasan layanan aksesibilitas yang digunakan oleh simpan otomatis, fitur opsional Clipboard+ (Android) (bagian 7)."),
 "ms": ("(Clipboard+, pilihan) — hanya digunakan jika anda menghidupkan simpan automatik (mati secara lalai), untuk mengesan saat anda mengetik Salin dalam apl lain atau sistem memaparkan mesej \"Disalin\", supaya salinan disimpan tanpa membuka Clipboard+. Perkhidmatan ini ditetapkan supaya tidak dapat membaca kandungan skrin; ia tidak merakam teks yang anda taip dan tidak menyimpan klip yang ditanda sebagai kata laluan. Klip yang disimpan kekal pada peranti anda (dan jika penyegerakan PC dihidupkan, hanya pergi ke Google Drive anda sendiri) dan tidak pernah dihantar kepada kami. Anda boleh mematikannya pada bila-bila masa dalam tetapan apl atau tetapan kebolehcapaian peranti.",
        "Menambah penerangan perkhidmatan kebolehcapaian yang digunakan oleh simpan automatik, ciri pilihan Clipboard+ (Android) (seksyen 7)."),
 "fil": ("(Clipboard+, opsyonal) — ginagamit lang kapag in-on mo ang awtomatikong pag-save (naka-off bilang default), para mapansin ang sandaling nag-tap ka ng Kopyahin sa ibang app o nagpakita ang system ng \"Nakopya\", para ma-save ang kinopya nang hindi binubuksan ang Clipboard+. Naka-set up ang serbisyo para hindi nito mabasa ang laman ng screen; hindi nito itinatala ang tina-type mo at hindi sine-save ang mga clip na minarkahang password. Nananatili sa device mo ang mga na-save na clip (at kung naka-on ang PC sync, sa sarili mong Google Drive lang napupunta) at hindi kailanman ipinapadala sa amin. Maaari mo itong i-off anumang oras sa mga setting ng app o sa mga setting ng accessibility ng device.",
        "Idinagdag ang paliwanag sa accessibility service na ginagamit ng awtomatikong pag-save, isang opsyonal na feature ng Clipboard+ (Android) (seksyon 7)."),
 "th": ("(Clipboard+, ไม่บังคับ) — ใช้เฉพาะเมื่อคุณเปิดบันทึกอัตโนมัติ (ปิดไว้เป็นค่าเริ่มต้น) เพื่อรับรู้ช่วงเวลาที่คุณแตะคัดลอกในแอปอื่นหรือระบบแสดงข้อความ \"คัดลอกแล้ว\" แล้วบันทึกสิ่งที่คัดลอกโดยไม่ต้องเปิด Clipboard+ บริการนี้ถูกตั้งค่าให้อ่านเนื้อหาบนหน้าจอไม่ได้ ไม่บันทึกข้อความที่คุณพิมพ์ และไม่บันทึกคลิปที่ระบุว่าเป็นรหัสผ่าน คลิปที่บันทึกจะอยู่ในอุปกรณ์ของคุณเท่านั้น (หากเปิดการซิงค์กับพีซี จะไปที่ Google Drive ของคุณเองเท่านั้น) และจะไม่ถูกส่งมาให้เรา คุณปิดได้ทุกเมื่อในการตั้งค่าของแอปหรือการตั้งค่าการช่วยเหลือพิเศษของอุปกรณ์",
        "เพิ่มคำอธิบายบริการการช่วยเหลือพิเศษที่ใช้โดยบันทึกอัตโนมัติ ซึ่งเป็นฟีเจอร์เสริมของ Clipboard+ (Android) (ข้อ 7)"),
 "vi": ("(Clipboard+, tùy chọn) — chỉ dùng khi bạn bật tự động lưu (mặc định tắt), để nhận biết khoảnh khắc bạn nhấn Sao chép trong ứng dụng khác hoặc hệ thống hiện thông báo \"Đã sao chép\", nhờ đó nội dung đã sao chép được lưu mà không cần mở Clipboard+. Dịch vụ được thiết lập để không thể đọc nội dung màn hình; không ghi lại văn bản bạn nhập và không lưu các mục được đánh dấu là mật khẩu. Các mục đã lưu chỉ ở trên thiết bị của bạn (nếu bật đồng bộ với PC, chỉ đi vào Google Drive của chính bạn) và không bao giờ được gửi cho chúng tôi. Bạn có thể tắt bất cứ lúc nào trong cài đặt của ứng dụng hoặc cài đặt hỗ trợ tiếp cận của thiết bị.",
        "Bổ sung giải thích về dịch vụ hỗ trợ tiếp cận mà tự động lưu, một tính năng tùy chọn của Clipboard+ (Android), sử dụng (mục 7)."),
}
DATE = "2026-10-21"


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "i18n", "privacy", "*.json")))
    assert len(files) == 21 and len(T) == 21, (len(files), len(T))
    for f in files:
        lang = os.path.basename(f)[:-5]
        bullet, hist = T[lang]
        raw = open(f, encoding="utf-8").read()
        d = json.loads(raw)
        perm = next(s for s in d["sections"] if s["id"] == "permissions")
        if "Clipboard+" in perm["html"] and DATE in raw:
            print("skip", lang); continue
        label = d["perms"]["accessibility"]
        # Rotate+ 접근성 항목(<li><strong>라벨</strong>…) 바로 뒤에 넣는다.
        m = re.search(r"<li><strong>" + re.escape(label) + r"</strong>[^<]*?Rotate\+.*?</li>", perm["html"])
        if not m:
            raise SystemExit(f"{lang}: Rotate+ 접근성 항목을 못 찾음")
        new_li = f"<li><strong>{label}</strong> {bullet}</li>"
        perm["html"] = perm["html"][:m.end()] + new_li + perm["html"][m.end():]
        hs = next(s for s in d["sections"] if s["id"] == "history")
        assert hs["html"].startswith('<ul class="legal-history">'), lang
        hs["html"] = hs["html"].replace('<ul class="legal-history">',
                                        f'<ul class="legal-history"><li><time datetime="{DATE}">{DATE}</time> {hist}</li>', 1)
        assert d["updated"].count("18") == 1, (lang, d["updated"])
        d["updated"] = d["updated"].replace("18", "21")
        indent = 2 if raw.startswith("{\n  ") else None
        with open(f, "w", encoding="utf-8", newline="\n") as fo:
            fo.write(json.dumps(d, ensure_ascii=False, indent=indent) + ("\n" if raw.endswith("\n") else ""))
        print("ok", lang)


if __name__ == "__main__":
    main()
