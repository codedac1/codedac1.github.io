# -*- coding: utf-8 -*-
"""AutoStart+ 6.6.0 사이트 반영 — 앱 페이지 기능 목록에 '실행 지연(PRO)' 한 줄(21개 언어, 2026-10-28).

드래그 순서 줄(features[2]) 바로 뒤에 넣는다. 문구는 Play 긴 설명
(Data/listings/edits/autostart_delay_setup_20261028.py)의 실행 지연 불릿과 같은 말이다. 두 번 돌려도 한 번만 들어간다.

    python scripts/edits/autostart_660_20261028.py
    node scripts/gen_site.js
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LINE = {
    "en": "Launch delay (PRO): wait a few seconds before the first app and space the rest apart, so car head units and slow devices finish starting up first",
    "ko": "실행 지연(PRO): 첫 앱 전에 몇 초 기다리고 앱 사이에 간격을 두어, 헤드유닛·느린 기기가 다 켜진 뒤에 엽니다",
    "ja": "起動の待ち時間（PRO）：最初のアプリの前に数秒待ち、アプリ同士の間隔もあけるので、ヘッドユニットや動作の遅い端末でも準備ができてから開きます",
    "zh": "启动延迟（PRO）：第一个应用前等待几秒，应用之间也留出间隔，让车机和较慢的设备先完成启动",
    "de": "Startverzögerung (PRO): vor der ersten App ein paar Sekunden warten und die Apps mit Abstand öffnen, damit Headunits und langsame Geräte erst fertig starten",
    "es": "Retraso de inicio (PRO): espera unos segundos antes de la primera app y separa las demás, para que las radios de coche y los dispositivos lentos terminen de arrancar",
    "fr": "Délai de lancement (PRO) : quelques secondes avant la première appli et entre les suivantes, pour les autoradios et appareils lents",
    "it": "Ritardo di avvio (PRO): attende qualche secondo prima della prima app e distanzia le altre, così autoradio e dispositivi lenti finiscono prima di avviarsi",
    "pt": "Atraso de abertura (PRO): espera alguns segundos antes do primeiro app e espaça os demais, para que centrais multimídia e aparelhos lentos terminem de iniciar",
    "nl": "Startvertraging (PRO): wacht een paar seconden voor de eerste app en laat ruimte tussen de apps, zodat autoradio's en trage apparaten eerst klaar zijn met opstarten",
    "pl": "Opóźnienie uruchamiania (PRO): kilka sekund czekania przed pierwszą aplikacją i odstępy między kolejnymi, żeby radio samochodowe i wolne urządzenia zdążyły się uruchomić",
    "ru": "Задержка запуска (PRO): несколько секунд ожидания перед первым приложением и паузы между остальными, чтобы автомагнитола или медленное устройство успели загрузиться",
    "uk": "Затримка запуску (PRO): кілька секунд очікування перед першим застосунком і паузи між іншими, щоб автомагнітола чи повільний пристрій встигли завантажитися",
    "tr": "Başlatma gecikmesi (PRO): ilk uygulamadan önce birkaç saniye bekler ve diğerlerini aralıklı açar; araç multimedya üniteleri ve yavaş cihazlar önce tamamen açılır",
    "id": "Jeda mulai (PRO): menunggu beberapa detik sebelum aplikasi pertama dan memberi jarak antar aplikasi, agar head unit dan perangkat lambat selesai menyala dulu",
    "ms": "Lengah mula (PRO): menunggu beberapa saat sebelum apl pertama dan menjarakkan apl seterusnya, supaya unit kepala kereta dan peranti perlahan siap dihidupkan dahulu",
    "vi": "Độ trễ khởi chạy (PRO): chờ vài giây trước ứng dụng đầu tiên và giãn cách các ứng dụng còn lại, để màn hình ô tô và thiết bị chậm khởi động xong trước",
    "th": "หน่วงเวลาการเปิด (PRO): รอสักครู่ก่อนเปิดแอปแรกและเว้นระยะระหว่างแอป เพื่อให้เครื่องเสียงรถยนต์และอุปกรณ์ที่ช้าเปิดเครื่องเสร็จก่อน",
    "hi": "लॉन्च में देरी (PRO): पहले ऐप से पहले कुछ सेकंड रुकें और बाकी ऐप्स के बीच अंतर रखें, ताकि कार हेड यूनिट और धीमे डिवाइस पहले पूरी तरह चालू हो जाएँ",
    "ar": "تأخير التشغيل (PRO): انتظار بضع ثوانٍ قبل أول تطبيق وترك فاصل بين التطبيقات، حتى يكتمل إقلاع شاشات السيارات والأجهزة البطيئة أولًا",
    "fil": "Launch delay (PRO): maghintay ng ilang segundo bago ang unang app at lagyan ng pagitan ang iba, para matapos munang mag-start ang car head unit at mabagal na device",
}

for lang, line in LINE.items():
    p = os.path.join(ROOT, "i18n", f"{lang}.json")
    raw = open(p, encoding="utf-8").read()
    d = json.loads(raw)
    feats = d["apps"]["autostart"]["features"]
    if line in feats:
        print(lang, "skip"); continue
    feats.insert(3, line)
    open(p, "w", encoding="utf-8", newline="").write(json.dumps(d, ensure_ascii=False, indent=2) + ("\n" if raw.endswith("\n") else ""))
    print(lang, "ok", len(feats))
