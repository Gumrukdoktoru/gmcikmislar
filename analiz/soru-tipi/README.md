# 2021–2025 GM Sınavları – Soru Tipi (alt tip) Etiketleri

500 sorunun her biri tek bir sözlükle etiketlendi: **ana tip** (10), **alt tip** (39) ve dokuz **biçim bayrağı**. Sentez ve üretim tarifleri `2027-GM-` deposunda: `00-SORU-YAZARI-ANALIZI-VE-PROMPTLAR/12-SORU-TIPI-KATALOGU`.

| Dosya | İçerik |
|---|---|
| `ETIKET-SOZLUGU.md` | Ana tip, alt tip, bayrak ve ölçülerin tanımları (etiketleme standardı) |
| `20xx-alt-tip-etiketleri.csv` | O yılın 100 sorusu, satır başına bir soru (sütunlar aşağıda) |
| `20xx-alt-tip-ornekleri.md` | O yılda kullanılan her alt tip için kitapçıktan aynen alınmış örnek soru(lar), "Kurgu" notu ve tereddütlü etiketlerin gerekçeleri ("Sınır durumlar") |
| `TOPLU-SAYIMLAR.md` | Beş yılın toplu sayımları: ana tip × yıl, alt tip × yıl × alan, alan içi paylar, her alt tipin harf/uzunluk/şık türü/bayrak dağılımı ve **500 sorunun tek tek "doğru cevap nasıl kurulmuş" notu** |
| `topla.py` | `python3 topla.py <bu klasör>` → `TOPLU-SAYIMLAR.md` dosyasını CSV'lerden yeniden üretir |

**CSV sütunları:** `yil, no, alan, ana_tip, alt_tip, F_MATRIS, F_MUTLAK, F_TUZAKVERI, F_TUMU, F_YALNIZ, F_DAYANAK, F_MADDENO, F_SERI, F_GUNCEL, oncul_sayisi, sik_turu, dogru_harf, dogru_uzunluk, kok_yuklem, kok_ozet, cevap_kurulumu`

Notlar:

- Örnek dosyalarında geçen `exams/20xx_red.txt`, kitapçık PDF'inden renk bilgisiyle çıkarılan çalışma metnidir (depoya eklenmedi).
- Örnek dosyalarının biçimi yıldan yıla biraz farklıdır (her yıl ayrı bir çalışma oturumunda hazırlandı); içerik standardı aynıdır.
- `cevap_kurulumu` ve "Kurgu" notları analiz yorumudur. Mevzuat gerekçesi olarak kullanmadan önce ilgili hükümden doğrulanmalıdır.
- Anahtarı tartışmalı sorular: 2021/89-90, 2022/94, 2023/72-73, 2024/46, 2025/12 ve 2025/16.
