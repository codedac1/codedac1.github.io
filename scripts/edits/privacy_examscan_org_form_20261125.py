"""개인정보처리방침 10항(문의) — ExamScan 기관 도입 문의 폼이 받는 항목 추가 (2026-11-25).

21개 언어 i18n/privacy/<lang>.json:
  1) sections[id=email].html 끝에 한 문단 추가(기관명·유형·대수 + 선택: 담당자 이름·전화·시험 일정, 견적·시범 안내에만 사용)
  2) sections[id=history] 목록 맨 앞에 이력 한 줄
  3) updated 의 날짜 20 -> 25
두 번 돌려도 같은 결과(이미 있으면 건너뜀).
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MARK = 'data-exs-org'
T = {
 "ko": ("ExamScan 기관 도입·단체 구매 문의 폼에서는 기관명, 기관 유형, 필요 대수를 받고, 원하시는 경우 담당자 이름, 전화번호, 시험 일정도 받습니다. 이 정보는 견적과 시범 운영 안내에만 쓰며, 위 문의 폼과 같은 방식으로 처리·보관합니다.",
        "ExamScan 기관 도입·단체 구매 문의 폼이 받는 항목(기관명·유형·대수, 선택: 담당자 이름·전화번호·시험 일정)을 추가했습니다(10항)."),
 "en": ("The ExamScan institution and group purchase form collects the institution name, type and number of devices needed and, if you choose, a contact name, phone number and exam dates. This information is used only to send a quote and pilot details, and is processed and kept in the same way as the contact form above.",
        "Added the fields collected by the ExamScan institution and group purchase form (institution name, type, number of devices; optional contact name, phone number and exam dates) (Section 10)."),
 "ja": ("ExamScanの機関導入・団体購入のお問い合わせフォームでは、機関名、機関の種類、必要台数を、ご希望の場合は担当者名、電話番号、試験日程もお預かりします。これらは見積もりと試験導入のご案内にのみ使用し、上記のお問い合わせフォームと同じ方法で処理・保管します。",
        "ExamScanの機関導入・団体購入のお問い合わせフォームで受け取る項目（機関名・種類・台数、任意：担当者名・電話番号・試験日程）を追加しました（第10項）。"),
 "zh": ("ExamScan 机构采购与团体购买咨询表单会收集机构名称、机构类型和所需台数，如您愿意，还会收集联系人姓名、电话号码和考试日期。这些信息仅用于发送报价和试用安排，并按与上述咨询表单相同的方式处理和保存。",
        "新增 ExamScan 机构采购与团体购买咨询表单所收集的项目（机构名称、类型、台数；可选：联系人姓名、电话号码、考试日期）（第 10 条）。"),
 "de": ("Das ExamScan-Formular für Einrichtungen und Sammelbestellungen erfasst den Namen der Einrichtung, ihre Art und die Anzahl der benötigten Geräte sowie auf Wunsch einen Ansprechpartner, eine Telefonnummer und Prüfungstermine. Diese Angaben werden nur für ein Angebot und Informationen zu einem Pilotbetrieb verwendet und wie beim obigen Kontaktformular verarbeitet und aufbewahrt.",
        "Die im ExamScan-Formular für Einrichtungen und Sammelbestellungen erfassten Angaben ergänzt (Name, Art, Anzahl der Geräte; optional Ansprechpartner, Telefonnummer, Prüfungstermine) (Abschnitt 10)."),
 "es": ("El formulario de ExamScan para instituciones y compras en grupo recoge el nombre de la institución, su tipo y el número de dispositivos necesarios y, si lo deseas, un nombre de contacto, un teléfono y las fechas de examen. Esta información solo se usa para enviar un presupuesto y detalles de una prueba piloto, y se trata y conserva igual que el formulario de contacto anterior.",
        "Se añadieron los datos que recoge el formulario de ExamScan para instituciones y compras en grupo (nombre, tipo, número de dispositivos; opcionales: nombre de contacto, teléfono y fechas de examen) (sección 10)."),
 "fr": ("Le formulaire ExamScan pour les établissements et les achats groupés recueille le nom de l'établissement, son type et le nombre d'appareils nécessaires et, si vous le souhaitez, un nom de contact, un numéro de téléphone et les dates d'examen. Ces informations servent uniquement à envoyer un devis et les modalités d'un pilote, et sont traitées et conservées comme pour le formulaire de contact ci-dessus.",
        "Ajout des informations recueillies par le formulaire ExamScan pour les établissements et les achats groupés (nom, type, nombre d'appareils ; facultatif : nom de contact, téléphone, dates d'examen) (section 10)."),
 "it": ("Il modulo ExamScan per istituti e acquisti di gruppo raccoglie il nome dell'istituto, il tipo e il numero di dispositivi necessari e, se lo desideri, un nome di riferimento, un numero di telefono e le date degli esami. Queste informazioni servono solo a inviare un preventivo e i dettagli di un progetto pilota e sono trattate e conservate come per il modulo di contatto sopra.",
        "Aggiunti i dati raccolti dal modulo ExamScan per istituti e acquisti di gruppo (nome, tipo, numero di dispositivi; facoltativi: nome di riferimento, telefono, date degli esami) (sezione 10)."),
 "pt": ("O formulário do ExamScan para instituições e compras em grupo coleta o nome da instituição, o tipo e o número de aparelhos necessários e, se você quiser, um nome de contato, telefone e datas das provas. Essas informações são usadas apenas para enviar um orçamento e detalhes de um piloto, e são tratadas e guardadas da mesma forma que o formulário de contato acima.",
        "Incluímos os dados coletados pelo formulário do ExamScan para instituições e compras em grupo (nome, tipo, número de aparelhos; opcionais: nome de contato, telefone, datas das provas) (seção 10)."),
 "nl": ("Het ExamScan-formulier voor instellingen en groepsaankopen vraagt de naam van de instelling, het type en het aantal benodigde apparaten en, als je dat wilt, een contactpersoon, telefoonnummer en examendata. Deze gegevens gebruiken we alleen voor een offerte en informatie over een pilot, en ze worden op dezelfde manier verwerkt en bewaard als bij het contactformulier hierboven.",
        "De gegevens toegevoegd die het ExamScan-formulier voor instellingen en groepsaankopen vraagt (naam, type, aantal apparaten; optioneel contactpersoon, telefoonnummer, examendata) (artikel 10)."),
 "pl": ("Formularz ExamScan dla instytucji i zakupów grupowych zbiera nazwę instytucji, jej rodzaj i liczbę potrzebnych urządzeń, a jeśli chcesz, także imię i nazwisko osoby kontaktowej, numer telefonu i terminy egzaminów. Dane te służą wyłącznie do przesłania oferty i informacji o pilotażu i są przetwarzane oraz przechowywane tak samo jak w powyższym formularzu kontaktowym.",
        "Dodano dane zbierane przez formularz ExamScan dla instytucji i zakupów grupowych (nazwa, rodzaj, liczba urządzeń; opcjonalnie osoba kontaktowa, telefon, terminy egzaminów) (sekcja 10)."),
 "ru": ("Форма ExamScan для учреждений и групповых покупок собирает название учреждения, его тип и нужное количество устройств, а по вашему желанию — имя контактного лица, телефон и даты экзаменов. Эти данные используются только для отправки предложения и условий пилотного запуска и обрабатываются и хранятся так же, как в форме обратной связи выше.",
        "Добавлены данные, которые собирает форма ExamScan для учреждений и групповых покупок (название, тип, количество устройств; по желанию — контактное лицо, телефон, даты экзаменов) (раздел 10)."),
 "uk": ("Форма ExamScan для закладів і групових закупівель збирає назву закладу, його тип і потрібну кількість пристроїв, а за вашим бажанням — ім'я контактної особи, телефон і дати іспитів. Ці дані використовуються лише для надсилання пропозиції та умов пілотного запуску й обробляються та зберігаються так само, як у формі зворотного зв'язку вище.",
        "Додано дані, які збирає форма ExamScan для закладів і групових закупівель (назва, тип, кількість пристроїв; за бажанням — контактна особа, телефон, дати іспитів) (розділ 10)."),
 "tr": ("ExamScan kurum ve toplu satın alma formu kurum adını, türünü ve gereken cihaz sayısını, isterseniz ilgili kişinin adını, telefon numarasını ve sınav tarihlerini alır. Bu bilgiler yalnızca teklif ve pilot uygulama bilgisi göndermek için kullanılır ve yukarıdaki iletişim formuyla aynı şekilde işlenip saklanır.",
        "ExamScan kurum ve toplu satın alma formunun aldığı bilgiler eklendi (kurum adı, türü, cihaz sayısı; isteğe bağlı: ilgili kişi, telefon, sınav tarihleri) (10. bölüm)."),
 "id": ("Formulir ExamScan untuk institusi dan pembelian kelompok mengumpulkan nama institusi, jenisnya, dan jumlah perangkat yang dibutuhkan, serta jika Anda mau, nama kontak, nomor telepon, dan jadwal ujian. Informasi ini hanya digunakan untuk mengirim penawaran harga dan rincian uji coba, serta diproses dan disimpan dengan cara yang sama seperti formulir kontak di atas.",
        "Menambahkan data yang dikumpulkan formulir ExamScan untuk institusi dan pembelian kelompok (nama, jenis, jumlah perangkat; opsional: nama kontak, telepon, jadwal ujian) (bagian 10)."),
 "ms": ("Borang ExamScan untuk institusi dan pembelian berkumpulan mengumpul nama institusi, jenisnya dan bilangan peranti yang diperlukan, serta jika anda mahu, nama untuk dihubungi, nombor telefon dan tarikh peperiksaan. Maklumat ini hanya digunakan untuk menghantar sebut harga dan butiran perintis, dan diproses serta disimpan dengan cara yang sama seperti borang hubungan di atas.",
        "Menambah data yang dikumpul oleh borang ExamScan untuk institusi dan pembelian berkumpulan (nama, jenis, bilangan peranti; pilihan: nama untuk dihubungi, telefon, tarikh peperiksaan) (seksyen 10)."),
 "vi": ("Biểu mẫu ExamScan dành cho tổ chức và mua theo nhóm thu thập tên tổ chức, loại hình và số thiết bị cần, và nếu bạn muốn, tên người liên hệ, số điện thoại và lịch thi. Thông tin này chỉ dùng để gửi báo giá và thông tin chạy thử, được xử lý và lưu giữ giống như biểu mẫu liên hệ ở trên.",
        "Bổ sung các thông tin mà biểu mẫu ExamScan dành cho tổ chức và mua theo nhóm thu thập (tên, loại hình, số thiết bị; tùy chọn: tên người liên hệ, điện thoại, lịch thi) (mục 10)."),
 "th": ("แบบฟอร์มสำหรับสถาบันและการซื้อแบบกลุ่มของ ExamScan จะเก็บชื่อสถาบัน ประเภท และจำนวนเครื่องที่ต้องการ และหากคุณต้องการ จะเก็บชื่อผู้ติดต่อ หมายเลขโทรศัพท์ และกำหนดการสอบด้วย ข้อมูลนี้ใช้เพื่อส่งใบเสนอราคาและรายละเอียดการทดลองใช้เท่านั้น และประมวลผลและจัดเก็บแบบเดียวกับแบบฟอร์มติดต่อด้านบน",
        "เพิ่มข้อมูลที่แบบฟอร์มสำหรับสถาบันและการซื้อแบบกลุ่มของ ExamScan เก็บ (ชื่อ ประเภท จำนวนเครื่อง; ไม่บังคับ: ชื่อผู้ติดต่อ โทรศัพท์ กำหนดการสอบ) (ข้อ 10)"),
 "hi": ("ExamScan का संस्थान और समूह खरीद फ़ॉर्म संस्थान का नाम, प्रकार और ज़रूरी डिवाइसों की संख्या लेता है, और आप चाहें तो संपर्क व्यक्ति का नाम, फ़ोन नंबर और परीक्षा की तारीखें भी लेता है। यह जानकारी केवल कोटेशन और पायलट की जानकारी भेजने के लिए इस्तेमाल होती है और ऊपर के संपर्क फ़ॉर्म की तरह ही संसाधित और रखी जाती है।",
        "ExamScan के संस्थान और समूह खरीद फ़ॉर्म में ली जाने वाली जानकारी जोड़ी गई (नाम, प्रकार, डिवाइसों की संख्या; वैकल्पिक: संपर्क व्यक्ति, फ़ोन, परीक्षा की तारीखें) (धारा 10)।"),
 "ar": ("يجمع نموذج ExamScan للمؤسسات والشراء الجماعي اسم المؤسسة ونوعها وعدد الأجهزة المطلوبة، وإن رغبت اسم جهة الاتصال ورقم الهاتف ومواعيد الامتحانات. تُستخدم هذه المعلومات فقط لإرسال عرض سعر وتفاصيل التشغيل التجريبي، وتُعالج وتُحفظ بالطريقة نفسها التي يُعامل بها نموذج التواصل أعلاه.",
        "أضفنا البيانات التي يجمعها نموذج ExamScan للمؤسسات والشراء الجماعي (الاسم والنوع وعدد الأجهزة؛ اختياري: جهة الاتصال والهاتف ومواعيد الامتحانات) (القسم 10)."),
 "fil": ("Kinokolekta ng form ng ExamScan para sa mga institusyon at maramihang pagbili ang pangalan ng institusyon, uri nito at bilang ng kailangang device, at kung gusto mo, ang pangalan ng contact person, numero ng telepono at mga petsa ng exam. Ginagamit lang ang impormasyong ito para magpadala ng quotation at detalye ng pilot, at pinoproseso at iniimbak ito sa parehong paraan ng contact form sa itaas.",
        "Idinagdag ang mga impormasyong kinokolekta ng form ng ExamScan para sa mga institusyon at maramihang pagbili (pangalan, uri, bilang ng device; opsyonal: contact person, telepono, petsa ng exam) (Seksyon 10)."),
}


def main():
    for code, (para, hist) in T.items():
        p = os.path.join(ROOT, 'i18n', 'privacy', f'{code}.json')
        d = json.load(open(p, encoding='utf-8'))
        email = next(s for s in d['sections'] if s['id'] == 'email')
        if MARK in email['html']:
            print('skip', code)
            continue
        email['html'] += f'<p {MARK}>{para}</p>'
        h = next(s for s in d['sections'] if s['id'] == 'history')
        h['html'] = h['html'].replace('<ul class="legal-history">',
                                      f'<ul class="legal-history"><li><time datetime="2026-11-25">2026-11-25</time> {hist}</li>', 1)
        d['updated'] = re.sub(r'(?<!\d)20(?!\d)', '25', d['updated'], count=1)
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print('ok', code, d['updated'])


if __name__ == '__main__':
    main()
