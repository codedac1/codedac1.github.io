"""2026-10-20 안드로이드 클립보드 가이드 정정 — "평소처럼 복사"가 자동 저장으로 읽혀 Android 10+ 제한을 반영.

방법 2 에 문단 1개 추가, 2단계 문장 교체, FAQ 1개 추가, updated 날짜. 21개 언어, 한 번만 돌린다(이미 반영됐으면 건너뜀).
용어는 앱 문자열(values-*/save_m1~3_title)과 맞췄다. ar 은 'Clipboard+' 뒤 U+200E.
"""
import json, os, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "android-clipboard-history"
DATE = "2026-10-20"
CP = "Clipboard+"
CP_AR = "Clipboard+‎"

T = {
 "ko": ("다만 안드로이드 10부터는 화면에 떠 있는 앱(과 쓰는 중인 키보드)만 클립보드를 읽을 수 있어서, 어떤 클립보드 앱도 뒤에 있는 동안 복사한 것을 저절로 다 저장하지는 못합니다. 복사한 직후 앱을 한 번 앞으로 불러오면 저장됩니다.",
        "복사한 직후 저장합니다. 화면 가장자리의 버블을 누르거나, 홈 화면 위젯의 저장 버튼을 누르거나, 앱을 열면 방금 복사한 내용이 저장됩니다. 글자라면 다른 앱에서 선택한 뒤 선택 메뉴의 Clipboard+를 고르는 방법이 복사를 거치지 않아 가장 확실합니다.",
        "권한을 다 줬는데 복사한 게 전부 저장되지 않아요.",
        "안드로이드 10부터 바뀐 개인정보 보호 규칙 때문입니다. 화면에 떠 있지 않은 앱은 클립보드를 읽을 수 없고, 이 제한은 권한 설정으로 끌 수 없습니다. 복사한 직후 버블·위젯·앱 열기로 저장하거나, 글자는 선택 메뉴의 Clipboard+를 쓰세요. 시스템 클립보드는 마지막 하나만 갖고 있어서, 저장하기 전에 다른 걸 복사하면 앞의 내용은 사라집니다."),
 "en": ("One catch: since Android 10, only the app on screen (and the keyboard you're typing with) can read the clipboard, so no clipboard app can quietly save everything you copy while it sits in the background. Bringing the app to the front right after you copy saves it.",
        "Save right after you copy. Tap the floating bubble at the edge of the screen, tap the save button on the home-screen widget, or open the app, and what you just copied is saved. For text, selecting it in another app and choosing Clipboard+ from the selection menu is the most reliable way, because it skips the clipboard entirely.",
        "I granted every permission, but not everything I copy gets saved.",
        "That's the privacy rule Android introduced in version 10. An app that isn't on screen can't read the clipboard, and no permission setting turns this off. Save right after copying with the bubble, the widget or by opening the app, or use Clipboard+ in the text selection menu for text. The system clipboard only holds the last item, so if you copy something else before saving, the earlier item is gone."),
 "ja": ("ただし Android 10 以降は、画面に表示中のアプリ(と入力中のキーボード)しかクリップボードを読めないため、どのクリップボードアプリも裏にある間のコピーを自動ですべて保存することはできません。コピーした直後にアプリを一度前面に出すと保存されます。",
        "コピーした直後に保存します。画面端のバブルをタップする、ホーム画面のウィジェットの保存ボタンを押す、またはアプリを開くと、今コピーした内容が保存されます。テキストなら、ほかのアプリで選択して選択メニューから Clipboard+ を選ぶ方法が、クリップボードを経由しないので最も確実です。",
        "権限をすべて許可したのに、コピーしたものが全部は保存されません。",
        "Android 10 で導入されたプライバシー保護のルールによるものです。画面に表示されていないアプリはクリップボードを読めず、この制限は権限設定ではオフにできません。コピー直後にバブル・ウィジェット・アプリを開くことで保存するか、テキストは選択メニューの Clipboard+ を使ってください。システムのクリップボードは最後の1件しか保持しないため、保存前に別のものをコピーすると前の内容は消えます。"),
 "zh": ("不过从 Android 10 开始，只有显示在屏幕上的应用（以及正在使用的输入法）才能读取剪贴板，所以任何剪贴板应用都无法在后台自动保存你复制的所有内容。复制后立刻把应用调到前台一次，就能保存。",
        "复制后立即保存。点按屏幕边缘的悬浮气泡、点按主屏幕小部件的保存按钮，或打开应用，刚才复制的内容就会被保存。如果是文字，在其他应用中选中后从选择菜单里选 Clipboard+ 最可靠，因为这样完全不经过剪贴板。",
        "我已经授予了所有权限，为什么复制的内容没有全部保存？",
        "这是 Android 10 引入的隐私保护规则。不在屏幕上的应用无法读取剪贴板，而且这一限制无法通过权限设置关闭。请在复制后立即通过悬浮气泡、小部件或打开应用来保存，文字可以使用选择菜单中的 Clipboard+。系统剪贴板只保留最后一项，保存前如果又复制了别的内容，之前的内容就会消失。"),
 "es": ("Eso sí: desde Android 10, solo la app que está en pantalla (y el teclado que estás usando) puede leer el portapapeles, así que ninguna app de portapapeles puede guardar sola todo lo que copias mientras está en segundo plano. Si traes la app al frente justo después de copiar, se guarda.",
        "Guarda justo después de copiar. Toca la burbuja flotante en el borde de la pantalla, toca el botón de guardar del widget de la pantalla de inicio o abre la app, y lo que acabas de copiar se guarda. Para texto, lo más seguro es seleccionarlo en otra app y elegir Clipboard+ en el menú de selección, porque no pasa por el portapapeles.",
        "Di todos los permisos, pero no se guarda todo lo que copio.",
        "Es la regla de privacidad que Android introdujo en la versión 10. Una app que no está en pantalla no puede leer el portapapeles, y ningún ajuste de permisos lo desactiva. Guarda justo después de copiar con la burbuja, el widget o abriendo la app, o usa Clipboard+ en el menú de selección de texto. El portapapeles del sistema solo guarda el último elemento, así que si copias otra cosa antes de guardar, lo anterior se pierde."),
 "pt": ("Só um detalhe: desde o Android 10, só o app que está na tela (e o teclado que você está usando) consegue ler a área de transferência, então nenhum app de área de transferência consegue salvar sozinho tudo o que você copia enquanto fica em segundo plano. Trazer o app para a frente logo depois de copiar salva o conteúdo.",
        "Salve logo depois de copiar. Toque na bolha flutuante na borda da tela, toque no botão de salvar do widget da tela inicial ou abra o app, e o que você acabou de copiar é salvo. Para texto, o jeito mais garantido é selecionar em outro app e escolher Clipboard+ no menu de seleção, porque assim nem passa pela área de transferência.",
        "Dei todas as permissões, mas nem tudo o que copio é salvo.",
        "É a regra de privacidade que o Android trouxe na versão 10. Um app que não está na tela não consegue ler a área de transferência, e nenhuma configuração de permissão desliga isso. Salve logo depois de copiar com a bolha, o widget ou abrindo o app, ou use o Clipboard+ no menu de seleção de texto. A área de transferência do sistema guarda só o último item, então se você copiar outra coisa antes de salvar, o anterior se perde."),
 "de": ("Ein Haken: Seit Android 10 kann nur die App auf dem Bildschirm (und die Tastatur, mit der du tippst) die Zwischenablage lesen. Keine Zwischenablage-App kann deshalb im Hintergrund alles automatisch speichern, was du kopierst. Holst du die App direkt nach dem Kopieren kurz nach vorne, wird es gespeichert.",
        "Direkt nach dem Kopieren speichern. Tippe auf die schwebende Blase am Bildschirmrand, auf die Speichern-Taste im Widget auf dem Startbildschirm oder öffne die App – dann wird das gerade Kopierte gespeichert. Bei Text ist es am zuverlässigsten, ihn in einer anderen App zu markieren und im Auswahlmenü Clipboard+ zu wählen, weil das die Zwischenablage ganz umgeht.",
        "Ich habe alle Berechtigungen erteilt, aber nicht alles Kopierte wird gespeichert.",
        "Das liegt an der Datenschutzregel, die Android mit Version 10 eingeführt hat. Eine App, die nicht auf dem Bildschirm ist, kann die Zwischenablage nicht lesen, und keine Berechtigung schaltet das ab. Speichere direkt nach dem Kopieren über die Blase, das Widget oder durch Öffnen der App, oder nutze für Text Clipboard+ im Auswahlmenü. Die System-Zwischenablage hält nur den letzten Eintrag – kopierst du vor dem Speichern etwas anderes, ist der vorherige weg."),
 "fr": ("Une précision : depuis Android 10, seule l'app affichée à l'écran (et le clavier que vous utilisez) peut lire le presse-papiers. Aucune app de presse-papiers ne peut donc enregistrer seule tout ce que vous copiez pendant qu'elle est en arrière-plan. Ramener l'app au premier plan juste après la copie l'enregistre.",
        "Enregistrez juste après avoir copié. Touchez la bulle flottante au bord de l'écran, touchez le bouton d'enregistrement du widget de l'écran d'accueil ou ouvrez l'app : ce que vous venez de copier est enregistré. Pour du texte, le plus fiable est de le sélectionner dans une autre app et de choisir Clipboard+ dans le menu de sélection, car cela ne passe pas du tout par le presse-papiers.",
        "J'ai accordé toutes les autorisations, mais tout ce que je copie n'est pas enregistré.",
        "C'est la règle de confidentialité introduite par Android 10. Une app qui n'est pas à l'écran ne peut pas lire le presse-papiers, et aucun réglage d'autorisation ne le désactive. Enregistrez juste après la copie avec la bulle, le widget ou en ouvrant l'app, ou utilisez Clipboard+ dans le menu de sélection pour le texte. Le presse-papiers du système ne garde que le dernier élément : si vous copiez autre chose avant d'enregistrer, le précédent est perdu."),
 "it": ("Un'avvertenza: da Android 10 solo l'app sullo schermo (e la tastiera che stai usando) può leggere gli appunti, quindi nessuna app per gli appunti può salvare da sola tutto ciò che copi mentre è in background. Se porti l'app in primo piano subito dopo aver copiato, viene salvato.",
        "Salva subito dopo aver copiato. Tocca la bolla flottante sul bordo dello schermo, tocca il pulsante salva del widget nella schermata Home oppure apri l'app, e ciò che hai appena copiato viene salvato. Per il testo, il modo più sicuro è selezionarlo in un'altra app e scegliere Clipboard+ dal menu di selezione, perché non passa affatto dagli appunti.",
        "Ho concesso tutti i permessi, ma non tutto ciò che copio viene salvato.",
        "È la regola sulla privacy introdotta da Android 10. Un'app che non è sullo schermo non può leggere gli appunti e nessuna impostazione dei permessi lo disattiva. Salva subito dopo aver copiato con la bolla, il widget o aprendo l'app, oppure usa Clipboard+ nel menu di selezione del testo. Gli appunti di sistema conservano solo l'ultimo elemento: se copi altro prima di salvare, quello precedente va perso."),
 "ru": ("Есть нюанс: начиная с Android 10 читать буфер обмена может только приложение на экране (и клавиатура, которой вы пользуетесь), поэтому ни одно приложение для буфера обмена не может само сохранять всё, что вы копируете, пока работает в фоне. Если сразу после копирования вывести приложение на экран, текст сохранится.",
        "Сохраняйте сразу после копирования. Нажмите на плавающий пузырёк у края экрана, на кнопку сохранения в виджете на главном экране или откройте приложение — и только что скопированное сохранится. Для текста надёжнее всего выделить его в другом приложении и выбрать Clipboard+ в меню выделения: так буфер обмена вообще не используется.",
        "Я дал все разрешения, но сохраняется не всё, что я копирую.",
        "Это правило конфиденциальности, появившееся в Android 10. Приложение, которого нет на экране, не может читать буфер обмена, и никакие разрешения это не отключают. Сохраняйте сразу после копирования через пузырёк, виджет или открыв приложение, а для текста используйте Clipboard+ в меню выделения. Системный буфер хранит только последний элемент, поэтому если до сохранения скопировать что-то другое, предыдущее пропадёт."),
 "uk": ("Є нюанс: починаючи з Android 10 читати буфер обміну може лише застосунок на екрані (і клавіатура, якою ви користуєтеся), тож жоден застосунок для буфера обміну не може сам зберігати все, що ви копіюєте, поки працює у фоні. Якщо одразу після копіювання вивести застосунок на екран, вміст збережеться.",
        "Зберігайте одразу після копіювання. Торкніться плаваючої бульбашки біля краю екрана, кнопки збереження у віджеті на головному екрані або відкрийте застосунок — і щойно скопійоване збережеться. Для тексту найнадійніше виділити його в іншому застосунку й вибрати Clipboard+ у меню виділення: так буфер обміну взагалі не використовується.",
        "Я надав усі дозволи, але зберігається не все, що я копіюю.",
        "Це правило конфіденційності, запроваджене в Android 10. Застосунок, якого немає на екрані, не може читати буфер обміну, і жодні дозволи цього не вимикають. Зберігайте одразу після копіювання через бульбашку, віджет або відкривши застосунок, а для тексту використовуйте Clipboard+ у меню виділення. Системний буфер зберігає лише останній елемент, тож якщо до збереження скопіювати щось інше, попереднє зникне."),
 "pl": ("Jedno zastrzeżenie: od Androida 10 schowek może odczytać tylko aplikacja widoczna na ekranie (i klawiatura, której używasz), więc żadna aplikacja do schowka nie zapisze sama wszystkiego, co kopiujesz, gdy działa w tle. Jeśli zaraz po skopiowaniu przywołasz aplikację na ekran, treść zostanie zapisana.",
        "Zapisuj zaraz po skopiowaniu. Dotknij pływającej bańki przy krawędzi ekranu, przycisku zapisu w widżecie na ekranie głównym albo otwórz aplikację — to, co właśnie skopiowałeś, zostanie zapisane. W przypadku tekstu najpewniej jest zaznaczyć go w innej aplikacji i wybrać Clipboard+ z menu zaznaczania, bo wtedy schowek w ogóle nie jest używany.",
        "Dałem wszystkie uprawnienia, a nie wszystko, co kopiuję, się zapisuje.",
        "To zasada prywatności wprowadzona w Androidzie 10. Aplikacja, której nie ma na ekranie, nie może odczytać schowka, i żadne ustawienie uprawnień tego nie wyłącza. Zapisuj zaraz po skopiowaniu bańką, widżetem lub otwierając aplikację, a tekst przez Clipboard+ w menu zaznaczania. Systemowy schowek przechowuje tylko ostatni element, więc jeśli przed zapisaniem skopiujesz coś innego, poprzednia treść przepadnie."),
 "nl": ("Eén kanttekening: sinds Android 10 kan alleen de app op het scherm (en het toetsenbord waarmee je typt) het klembord lezen. Geen enkele klembord-app kan dus vanzelf alles opslaan wat je kopieert terwijl hij op de achtergrond staat. Haal je de app direct na het kopiëren even naar voren, dan wordt het opgeslagen.",
        "Sla direct na het kopiëren op. Tik op de zwevende bubbel aan de rand van het scherm, op de bewaarknop van de widget op je startscherm of open de app, en wat je net hebt gekopieerd wordt opgeslagen. Voor tekst is de betrouwbaarste manier om hem in een andere app te selecteren en Clipboard+ te kiezen in het selectiemenu, omdat dat het klembord helemaal overslaat.",
        "Ik heb alle rechten gegeven, maar niet alles wat ik kopieer wordt opgeslagen.",
        "Dat komt door de privacyregel die Android in versie 10 invoerde. Een app die niet op het scherm staat, kan het klembord niet lezen, en geen enkele rechteninstelling zet dat uit. Sla direct na het kopiëren op via de bubbel, de widget of door de app te openen, of gebruik voor tekst Clipboard+ in het selectiemenu. Het systeemklembord bewaart alleen het laatste item, dus als je vóór het opslaan iets anders kopieert, is het vorige weg."),
 "tr": ("Bir ayrıntı: Android 10'dan beri panoyu yalnızca ekrandaki uygulama (ve kullandığınız klavye) okuyabiliyor; bu yüzden hiçbir pano uygulaması arka plandayken kopyaladığınız her şeyi kendiliğinden kaydedemez. Kopyaladıktan hemen sonra uygulamayı bir kez öne getirirseniz kaydedilir.",
        "Kopyaladıktan hemen sonra kaydedin. Ekran kenarındaki yüzen balona, ana ekrandaki widget'ın kaydet düğmesine dokunun ya da uygulamayı açın; az önce kopyaladığınız şey kaydedilir. Metin içinse en güvenilir yol, onu başka bir uygulamada seçip seçim menüsünden Clipboard+'ı seçmektir; çünkü bu yöntem panoyu hiç kullanmaz.",
        "Tüm izinleri verdim ama kopyaladığım her şey kaydedilmiyor.",
        "Bu, Android 10 ile gelen gizlilik kuralından kaynaklanır. Ekranda olmayan bir uygulama panoyu okuyamaz ve hiçbir izin ayarı bunu kapatmaz. Kopyaladıktan hemen sonra balon, widget veya uygulamayı açarak kaydedin; metin için seçim menüsündeki Clipboard+'ı kullanın. Sistem panosu yalnızca son öğeyi tutar; kaydetmeden önce başka bir şey kopyalarsanız önceki kaybolur."),
 "id": ("Satu catatan: sejak Android 10, hanya aplikasi yang tampil di layar (dan keyboard yang sedang Anda pakai) yang bisa membaca papan klip, jadi tidak ada aplikasi papan klip yang bisa menyimpan sendiri semua yang Anda salin selagi berada di latar belakang. Membawa aplikasi ke depan tepat setelah menyalin akan menyimpannya.",
        "Simpan tepat setelah menyalin. Ketuk gelembung melayang di tepi layar, ketuk tombol simpan di widget layar utama, atau buka aplikasi, dan yang baru saja Anda salin akan tersimpan. Untuk teks, cara paling andal adalah memilihnya di aplikasi lain lalu memilih Clipboard+ dari menu pilihan, karena cara ini sama sekali tidak melewati papan klip.",
        "Saya sudah memberi semua izin, tetapi tidak semua yang saya salin tersimpan.",
        "Itu karena aturan privasi yang diperkenalkan Android 10. Aplikasi yang tidak tampil di layar tidak bisa membaca papan klip, dan tidak ada pengaturan izin yang bisa mematikannya. Simpan tepat setelah menyalin lewat gelembung, widget, atau dengan membuka aplikasi, atau gunakan Clipboard+ di menu pilihan teks. Papan klip sistem hanya menyimpan item terakhir, jadi jika Anda menyalin hal lain sebelum menyimpan, yang sebelumnya hilang."),
 "ms": ("Satu perkara: sejak Android 10, hanya aplikasi yang dipaparkan pada skrin (dan papan kekunci yang sedang anda gunakan) boleh membaca papan klip, jadi tiada aplikasi papan klip yang boleh menyimpan sendiri semua yang anda salin semasa berada di latar belakang. Membawa aplikasi ke hadapan sejurus selepas menyalin akan menyimpannya.",
        "Simpan sejurus selepas menyalin. Ketik gelembung terapung di tepi skrin, ketik butang simpan pada widget skrin utama, atau buka aplikasi, dan apa yang baru anda salin akan disimpan. Untuk teks, cara paling pasti ialah memilihnya dalam aplikasi lain dan memilih Clipboard+ daripada menu pilihan, kerana cara ini langsung tidak melalui papan klip.",
        "Saya sudah memberi semua kebenaran, tetapi tidak semua yang saya salin disimpan.",
        "Ini disebabkan peraturan privasi yang diperkenalkan dalam Android 10. Aplikasi yang tiada pada skrin tidak boleh membaca papan klip, dan tiada tetapan kebenaran yang boleh mematikannya. Simpan sejurus selepas menyalin melalui gelembung, widget atau dengan membuka aplikasi, atau gunakan Clipboard+ dalam menu pilihan teks. Papan klip sistem hanya menyimpan item terakhir, jadi jika anda menyalin perkara lain sebelum menyimpan, yang sebelumnya hilang."),
 "fil": ("Isang paalala: mula Android 10, ang app lang na nasa screen (at ang keyboard na ginagamit mo) ang nakakabasa ng clipboard, kaya walang clipboard app na kusang makakapag-save ng lahat ng kinokopya mo habang nasa background ito. Kapag dinala mo ang app sa harap pagkatapos mismong kumopya, nase-save ito.",
        "Mag-save agad pagkatapos kumopya. I-tap ang floating bubble sa gilid ng screen, i-tap ang save button ng widget sa home screen, o buksan ang app, at mase-save ang kakakopya mo lang. Para sa text, pinakasigurado ang piliin ito sa ibang app at piliin ang Clipboard+ sa selection menu, dahil hindi na ito dumadaan sa clipboard.",
        "Ibinigay ko na ang lahat ng permission, pero hindi lahat ng kinokopya ko ay nase-save.",
        "Dahil ito sa privacy rule na ipinakilala ng Android 10. Hindi mababasa ng app na wala sa screen ang clipboard, at walang permission setting na makakapatay nito. Mag-save agad pagkatapos kumopya gamit ang bubble, ang widget o sa pagbukas ng app, o gamitin ang Clipboard+ sa text selection menu. Ang huling item lang ang hawak ng system clipboard, kaya kung may kinopya kang iba bago mag-save, mawawala ang nauna."),
 "vi": ("Có một lưu ý: từ Android 10, chỉ ứng dụng đang hiển thị trên màn hình (và bàn phím bạn đang dùng) mới đọc được bộ nhớ tạm, nên không ứng dụng bộ nhớ tạm nào có thể tự lưu mọi thứ bạn sao chép khi đang chạy nền. Đưa ứng dụng lên trước ngay sau khi sao chép thì nội dung sẽ được lưu.",
        "Lưu ngay sau khi sao chép. Chạm vào bong bóng nổi ở mép màn hình, chạm nút lưu trên tiện ích ở màn hình chính, hoặc mở ứng dụng, và nội dung bạn vừa sao chép sẽ được lưu. Với văn bản, cách chắc chắn nhất là chọn nó trong ứng dụng khác rồi chọn Clipboard+ trong menu chọn văn bản, vì cách này hoàn toàn không đi qua bộ nhớ tạm.",
        "Tôi đã cấp mọi quyền nhưng không phải mọi thứ tôi sao chép đều được lưu.",
        "Đó là do quy tắc quyền riêng tư Android áp dụng từ phiên bản 10. Ứng dụng không hiển thị trên màn hình không thể đọc bộ nhớ tạm, và không có cài đặt quyền nào tắt được điều này. Hãy lưu ngay sau khi sao chép bằng bong bóng, tiện ích hoặc bằng cách mở ứng dụng, hoặc dùng Clipboard+ trong menu chọn văn bản. Bộ nhớ tạm của hệ thống chỉ giữ mục cuối cùng, nên nếu bạn sao chép thứ khác trước khi lưu, mục trước sẽ mất."),
 "th": ("ข้อควรรู้: ตั้งแต่ Android 10 มีเพียงแอปที่แสดงอยู่บนหน้าจอ (และคีย์บอร์ดที่คุณกำลังใช้) เท่านั้นที่อ่านคลิปบอร์ดได้ แอปคลิปบอร์ดใดก็ไม่สามารถบันทึกทุกอย่างที่คุณคัดลอกเองได้ขณะอยู่เบื้องหลัง หากเรียกแอปขึ้นมาด้านหน้าทันทีหลังคัดลอก ข้อมูลจะถูกบันทึก",
        "บันทึกทันทีหลังคัดลอก แตะบับเบิลลอยที่ขอบหน้าจอ แตะปุ่มบันทึกบนวิดเจ็ตหน้าจอหลัก หรือเปิดแอป สิ่งที่คุณเพิ่งคัดลอกจะถูกบันทึก สำหรับข้อความ วิธีที่แน่นอนที่สุดคือเลือกข้อความในแอปอื่นแล้วเลือก Clipboard+ จากเมนูการเลือก เพราะไม่ต้องผ่านคลิปบอร์ดเลย",
        "ให้สิทธิ์ครบทุกอย่างแล้ว แต่สิ่งที่คัดลอกไม่ถูกบันทึกทั้งหมด",
        "เป็นเพราะกฎความเป็นส่วนตัวที่ Android เริ่มใช้ในเวอร์ชัน 10 แอปที่ไม่ได้แสดงบนหน้าจอจะอ่านคลิปบอร์ดไม่ได้ และไม่มีการตั้งค่าสิทธิ์ใดปิดข้อจำกัดนี้ได้ ให้บันทึกทันทีหลังคัดลอกด้วยบับเบิล วิดเจ็ต หรือการเปิดแอป หรือใช้ Clipboard+ ในเมนูการเลือกข้อความ คลิปบอร์ดของระบบเก็บได้เพียงรายการล่าสุด ถ้าคัดลอกอย่างอื่นก่อนบันทึก รายการก่อนหน้าจะหายไป"),
 "hi": ("एक बात ध्यान रखें: Android 10 से सिर्फ़ स्क्रीन पर दिख रहा ऐप (और जिस कीबोर्ड से आप टाइप कर रहे हैं) ही क्लिपबोर्ड पढ़ सकता है, इसलिए कोई भी क्लिपबोर्ड ऐप बैकग्राउंड में रहते हुए आपकी कॉपी की गई हर चीज़ अपने-आप सेव नहीं कर सकता। कॉपी करने के तुरंत बाद ऐप को एक बार सामने लाने पर वह सेव हो जाती है।",
        "कॉपी करने के तुरंत बाद सेव करें। स्क्रीन के किनारे पर फ़्लोटिंग बबल पर टैप करें, होम स्क्रीन विजेट के सेव बटन पर टैप करें या ऐप खोलें, और अभी कॉपी की गई चीज़ सेव हो जाएगी। टेक्स्ट के लिए सबसे पक्का तरीका है उसे दूसरे ऐप में चुनकर सिलेक्शन मेन्यू से Clipboard+ चुनना, क्योंकि इसमें क्लिपबोर्ड का इस्तेमाल ही नहीं होता।",
        "मैंने सारी अनुमतियाँ दे दी हैं, फिर भी कॉपी की गई हर चीज़ सेव नहीं होती।",
        "यह Android 10 में आए गोपनीयता नियम की वजह से है। जो ऐप स्क्रीन पर नहीं है वह क्लिपबोर्ड नहीं पढ़ सकता, और किसी भी अनुमति सेटिंग से यह बंद नहीं होता। कॉपी करने के तुरंत बाद बबल, विजेट या ऐप खोलकर सेव करें, या टेक्स्ट के लिए सिलेक्शन मेन्यू में Clipboard+ इस्तेमाल करें। सिस्टम क्लिपबोर्ड सिर्फ़ आखिरी आइटम रखता है, इसलिए सेव करने से पहले कुछ और कॉपी करने पर पिछला आइटम चला जाता है।"),
 "ar": ("ملاحظة: منذ Android 10 لا يستطيع قراءة الحافظة إلا التطبيق الظاهر على الشاشة (ولوحة المفاتيح التي تكتب بها)، لذا لا يستطيع أي تطبيق للحافظة أن يحفظ تلقائيًا كل ما تنسخه أثناء عمله في الخلفية. إذا أحضرت التطبيق إلى الواجهة مباشرةً بعد النسخ فسيُحفظ المحتوى.",
        f"احفظ مباشرةً بعد النسخ. اضغط الفقاعة العائمة على حافة الشاشة، أو زر الحفظ في أداة الشاشة الرئيسية، أو افتح التطبيق، فيُحفظ ما نسخته للتو. أما النص فأضمن طريقة هي تحديده في تطبيق آخر ثم اختيار {CP_AR} من قائمة التحديد، لأنها لا تمر بالحافظة إطلاقًا.",
        "منحت كل الأذونات، لكن لا يُحفظ كل ما أنسخه.",
        f"هذا بسبب قاعدة الخصوصية التي أدخلها Android 10. التطبيق غير الظاهر على الشاشة لا يمكنه قراءة الحافظة، ولا يوجد إعداد أذونات يلغي ذلك. احفظ مباشرةً بعد النسخ بالفقاعة أو الأداة أو بفتح التطبيق، أو استخدم {CP_AR} في قائمة تحديد النص. حافظة النظام تحتفظ بآخر عنصر فقط، فإذا نسخت شيئًا آخر قبل الحفظ ضاع العنصر السابق."),
}


def main():
    done = 0
    for f in sorted(glob.glob(os.path.join(HERE, "..", "i18n", "guides", "*.json"))):
        lang = os.path.splitext(os.path.basename(f))[0]
        data = json.load(open(f, encoding="utf-8"))
        g = data["guides"][SLUG]
        add_p, step2, fq, fa = T[lang]
        sec = g["sections"][1]
        if add_p in sec["p"]:
            print(lang, "이미 반영"); continue
        sec["p"].append(add_p)
        sec["steps"][1] = step2
        g["faq"].append({"q": fq, "a": fa})
        g["updated"] = DATE
        with open(f, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        done += 1
    print("반영", done, "/", len(T))


if __name__ == "__main__":
    main()
