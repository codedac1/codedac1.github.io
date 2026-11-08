# -*- coding: utf-8 -*-
"""개인정보처리방침: Windows 구매 기록을 보내는 앱에 Clipboard+·FloatNote+ 추가 (2026-11-08).

11-02 두 앱이 Pro 를 다시 팔기 시작했는데 구매 보고(PurchaseReport)가 빠져 있었다 — 앱 다음 버전에 넣으면서
방침 6항의 앱 목록과 변경 이력, '최종 개정' 날짜(3 → 8)를 21개 언어에 반영한다.
앱별 표의 'CodeDAC 구매 기록' 칩은 scan_app_privacy.js 를 다시 돌리면 앱 소스에서 잡힌다.
다시 돌려도 이미 들어가 있으면 건너뛴다.
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATE = "2026-11-08"

H = {
 "en": "Added Clipboard+ and FloatNote+ for Windows to the apps that send a purchase record when a PRO purchase completes (Section 6).",
 "ko": "PRO 구매가 완료되면 구매 기록을 보내는 앱에 Windows용 Clipboard+와 FloatNote+를 추가했습니다(6항).",
 "ja": "PROの購入完了時に購入記録を送るアプリに、Windows版のClipboard+とFloatNote+を追加しました（第6項）。",
 "zh": "在完成 PRO 购买时发送购买记录的应用中新增了 Windows 版 Clipboard+ 和 FloatNote+（第 6 条）。",
 "de": "Clipboard+ und FloatNote+ für Windows zu den Apps hinzugefügt, die nach Abschluss eines PRO-Kaufs einen Kaufdatensatz senden (Abschnitt 6).",
 "es": "Se añadieron Clipboard+ y FloatNote+ para Windows a las apps que envían un registro de compra al completarse una compra de PRO (apartado 6).",
 "pt": "Adicionamos o Clipboard+ e o FloatNote+ para Windows aos apps que enviam um registro de compra quando uma compra do PRO é concluída (item 6).",
 "fr": "Ajout de Clipboard+ et FloatNote+ pour Windows aux applications qui envoient un enregistrement d'achat lorsqu'un achat PRO est finalisé (section 6).",
 "it": "Aggiunti Clipboard+ e FloatNote+ per Windows alle app che inviano un registro di acquisto al completamento di un acquisto PRO (punto 6).",
 "nl": "Clipboard+ en FloatNote+ voor Windows toegevoegd aan de apps die een aankoopbericht sturen wanneer een PRO-aankoop is voltooid (artikel 6).",
 "pl": "Dodano Clipboard+ i FloatNote+ dla Windows do aplikacji, które wysyłają zapis zakupu po zakończeniu zakupu PRO (punkt 6).",
 "ru": "Clipboard+ и FloatNote+ для Windows добавлены в список приложений, которые отправляют запись о покупке после завершения покупки PRO (раздел 6).",
 "uk": "Clipboard+ і FloatNote+ для Windows додано до застосунків, які надсилають запис про покупку після завершення покупки PRO (розділ 6).",
 "tr": "PRO satın alma tamamlandığında satın alma kaydı gönderen uygulamalara Windows için Clipboard+ ve FloatNote+ eklendi (madde 6).",
 "ar": "أُضيف Clipboard+‎ وFloatNote+‎ لنظام Windows إلى التطبيقات التي ترسل سجل شراء عند اكتمال عملية شراء PRO (البند 6).",
 "hi": "PRO खरीदारी पूरी होने पर खरीद रिकॉर्ड भेजने वाले ऐप्स में Windows के लिए Clipboard+ और FloatNote+ जोड़े गए (धारा 6)।",
 "id": "Menambahkan Clipboard+ dan FloatNote+ untuk Windows ke aplikasi yang mengirim catatan pembelian saat pembelian PRO selesai (bagian 6).",
 "ms": "Menambah Clipboard+ dan FloatNote+ untuk Windows kepada apl yang menghantar rekod pembelian apabila pembelian PRO selesai (seksyen 6).",
 "fil": "Idinagdag ang Clipboard+ at FloatNote+ para sa Windows sa mga app na nagpapadala ng tala ng pagbili kapag nakumpleto ang pagbili ng PRO (seksyon 6).",
 "th": "เพิ่ม Clipboard+ และ FloatNote+ สำหรับ Windows ในรายชื่อแอปที่ส่งบันทึกการซื้อเมื่อการซื้อ PRO เสร็จสมบูรณ์ (ข้อ 6)",
 "vi": "Bổ sung Clipboard+ và FloatNote+ cho Windows vào các ứng dụng gửi bản ghi mua hàng khi giao dịch mua PRO hoàn tất (mục 6).",
}


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "i18n", "privacy", "*.json")))
    assert len(files) == 21 and len(H) == 21, (len(files), len(H))
    for f in files:
        lang = os.path.basename(f)[:-5]
        raw = open(f, encoding="utf-8").read()
        d = json.loads(raw)
        if DATE in raw:
            print("skip", lang); continue
        # 6항 — 구매 기록 문단의 앱 목록. 구분자(", "·"・"·"、"·" أو ")는 언어마다 달라 PhotoCleaner+ 와 ReadFocus+ 사이에서 읽는다.
        sec = d["sections"][5]
        h = sec["html"]
        m = re.search(r"PhotoCleaner\+(.{1,12}?)ReadFocus\+", h)
        assert m and h.count("PhotoCleaner+") == 1 and "FloatNote+" not in h, lang
        sep = m.group(1)
        lrm = "‎" if "‎" in sep else ""
        h = h.replace("PhotoCleaner+", f"Clipboard+{sep}FloatNote+{sep}PhotoCleaner+", 1)
        if lrm:
            h = h.replace(f"Clipboard+{sep}", f"Clipboard+{sep}", 1)   # 아랍어: 구분자에 LRM 이 이미 들어 있다
        sec["html"] = h
        hs = next(s for s in d["sections"] if s["id"] == "history")
        assert hs["html"].startswith('<ul class="legal-history">'), lang
        hs["html"] = hs["html"].replace('<ul class="legal-history">',
                                        f'<ul class="legal-history"><li><time datetime="{DATE}">{DATE}</time> {H[lang]}</li>', 1)
        n = len(re.findall(r"(?<!\d)3(?!\d)", d["updated"]))
        assert n == 1, (lang, d["updated"])
        d["updated"] = re.sub(r"(?<!\d)3(?!\d)", "8", d["updated"])
        indent = 2 if raw.startswith("{\n  ") else None
        with open(f, "w", encoding="utf-8", newline="\n") as fo:
            fo.write(json.dumps(d, ensure_ascii=False, indent=indent) + ("\n" if raw.endswith("\n") else ""))
        print("ok", lang, "|", sep.strip() or repr(sep), "|", d["updated"])


if __name__ == "__main__":
    main()
