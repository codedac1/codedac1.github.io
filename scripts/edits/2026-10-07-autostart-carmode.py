"""AutoStart+ 사이트 문구에 차량 모드(6.4.8, 10/7 스토어 반영) 추가 — 21개 언어.

- long: 끝에 차량 모드 문단(스토어 정본 00_master_listings.csv 의 🚗 문단 본문을 그대로)
- features[1](앱 검색·추가)를 차량 모드 줄로 교체 — features 는 6개 고정
- faq: "차량 헤드유닛에서도 되나요?" 추가(답 = 같은 문단). AI 도우미가 "head unit auto start" 류 질문에 이 페이지를 집도록.
몇 번 돌려도 같은 결과(이미 들어가 있으면 건너뜀).
"""
import csv, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
CSV = ROOT.parent / "Data" / "listings" / "00_master_listings.csv"
PLAY2SITE = {"en-US": "en", "ar": "ar", "de-DE": "de", "es-ES": "es", "fil": "fil", "fr-FR": "fr", "hi-IN": "hi",
             "id": "id", "it-IT": "it", "ja-JP": "ja", "ko-KR": "ko", "ms": "ms", "nl-NL": "nl", "pl-PL": "pl",
             "pt-BR": "pt", "ru-RU": "ru", "th": "th", "tr-TR": "tr", "uk": "uk", "vi": "vi", "zh-CN": "zh"}

FEATURE = {
 "en": "Car Mode for head units: your apps open again every time the screen wakes from sleep — free",
 "ar": "وضع السيارة لشاشات السيارات: تُفتح تطبيقاتك من جديد كلما استيقظت الشاشة من السكون — مجانًا",
 "de": "Automodus für Autoradios: Deine Apps öffnen sich bei jedem Aufwachen des Bildschirms wieder — kostenlos",
 "es": "Modo coche para radios de coche: tus apps se vuelven a abrir cada vez que la pantalla sale del reposo — gratis",
 "fil": "Car Mode para sa head unit: muling bubukas ang iyong mga app tuwing magigising ang screen — libre",
 "fr": "Mode voiture pour autoradios : vos applis se rouvrent à chaque sortie de veille de l'écran — gratuit",
 "hi": "कार हेड यूनिट के लिए कार मोड: स्क्रीन के स्लीप से जागने पर हर बार आपके ऐप फिर से खुलते हैं — मुफ़्त",
 "id": "Mode Mobil untuk head unit: aplikasimu terbuka lagi setiap kali layar bangun dari tidur — gratis",
 "it": "Modalità auto per autoradio: le tue app si riaprono ogni volta che lo schermo esce dallo standby — gratis",
 "ja": "ヘッドユニット向け車載モード：画面がスリープから戻るたびにアプリがもう一度開く — 無料",
 "ko": "헤드유닛용 차량 모드: 화면이 절전에서 깨어날 때마다 앱을 다시 실행 — 무료",
 "ms": "Mod Kereta untuk unit kepala: apl anda dibuka semula setiap kali skrin bangun daripada tidur — percuma",
 "nl": "Automodus voor autoradio's: je apps gaan weer open telkens als het scherm uit de slaapstand komt — gratis",
 "pl": "Tryb samochodowy dla radioodtwarzaczy: aplikacje otwierają się ponownie przy każdym wybudzeniu ekranu — za darmo",
 "pt": "Modo carro para centrais multimídia: seus apps abrem de novo toda vez que a tela sai do repouso — grátis",
 "ru": "Автомобильный режим для автомагнитол: приложения снова открываются при каждом пробуждении экрана — бесплатно",
 "th": "โหมดรถยนต์สำหรับจอติดรถยนต์: แอปเปิดขึ้นอีกครั้งทุกครั้งที่หน้าจอตื่นจากโหมดพัก — ฟรี",
 "tr": "Multimedya cihazları için Araç modu: ekran uykudan her uyandığında uygulamalarınız yeniden açılır — ücretsiz",
 "uk": "Автомобільний режим для автомагнітол: застосунки знову відкриваються щоразу, коли екран прокидається — безкоштовно",
 "vi": "Chế độ ô tô cho màn hình ô tô: ứng dụng tự mở lại mỗi khi màn hình thức dậy từ chế độ ngủ — miễn phí",
 "zh": "车机专用车载模式：屏幕每次从休眠中亮起，应用都会重新打开 — 免费",
}
QUESTION = {
 "en": "Does AutoStart+ work on Android car head units?",
 "ar": "هل يعمل AutoStart+ على شاشات السيارات العاملة بنظام أندرويد؟",
 "de": "Funktioniert AutoStart+ auf Android-Autoradios?",
 "es": "¿Funciona AutoStart+ en radios de coche Android?",
 "fil": "Gumagana ba ang AutoStart+ sa mga Android car head unit?",
 "fr": "AutoStart+ fonctionne-t-il sur les autoradios Android ?",
 "hi": "क्या AutoStart+ Android कार हेड यूनिट पर काम करता है?",
 "id": "Apakah AutoStart+ berfungsi di head unit mobil Android?",
 "it": "AutoStart+ funziona sulle autoradio Android?",
 "ja": "AutoStart+ は Android の車載ヘッドユニットでも使えますか？",
 "ko": "안드로이드 차량 헤드유닛에서도 작동하나요?",
 "ms": "Adakah AutoStart+ berfungsi pada unit kepala kereta Android?",
 "nl": "Werkt AutoStart+ op Android-autoradio's?",
 "pl": "Czy AutoStart+ działa na radioodtwarzaczach samochodowych z Androidem?",
 "pt": "O AutoStart+ funciona em centrais multimídia Android?",
 "ru": "Работает ли AutoStart+ на Android-автомагнитолах?",
 "th": "AutoStart+ ใช้กับจอแอนดรอยด์ติดรถยนต์ได้ไหม",
 "tr": "AutoStart+ Android araç multimedya cihazlarında çalışır mı?",
 "uk": "Чи працює AutoStart+ на Android-автомагнітолах?",
 "vi": "AutoStart+ có hoạt động trên màn hình Android ô tô không?",
 "zh": "AutoStart+ 能在安卓车机上使用吗？",
}

body = {}
for r in csv.DictReader(open(CSV, encoding="utf-8-sig")):
    if r["package"] != "com.codedac.autostart": continue
    lines = r["full_description"].split("\n")
    i = next(i for i, l in enumerate(lines) if l.startswith("🚗"))
    body[PLAY2SITE[r["language"]]] = lines[i + 1].strip()
assert len(body) == 21, body.keys()

for lang, text in sorted(body.items()):
    p = ROOT / "i18n" / f"{lang}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    a = d["apps"]["autostart"]
    if text not in a["long"]:
        a["long"] = a["long"].rstrip() + " " + text
    if a["features"][1] != FEATURE[lang]:
        a["features"][1] = FEATURE[lang]
    if not any(f["q"] == QUESTION[lang] for f in a["faq"]):
        a["faq"].insert(1, {"q": QUESTION[lang], "a": text})
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(lang, "ok")
