35\. Gün - Analiz Geçmişinde Tahmin Filtresi



2026-08-25



Bugün analiz geçmişinde filtreleme özelliği üzerinde çalıştım.



Öncelikle get\_analyses\_by\_user fonksiyonuna isteğe bağlı prediction parametresi ekledim. Böylece kullanıcının analiz geçmişi ENTAILMENT, NEUTRAL veya CONTRADICTION sonucuna göre filtrelenebilir hale geldi.



Daha sonra /history endpointine prediction query parametresi ekledim. PredictionLabel kullanılarak sadece geçerli tahmin değerlerinin kabul edilmesi sağlandı.



Filtre kullanılmadığında mevcut analiz geçmişinin normal şekilde çalışmaya devam ettiği kontrol edildi.



Filtreleme özelliği ve geçersiz prediction değeri için yeni API testleri eklendi. Geçersiz bir değer gönderildiğinde 422 hata cevabı döndüğü doğrulandı.



API testlerinde 37 test, tüm proje testlerinde ise toplam 74 test başarıyla geçti. git diff --check kontrolünde herhangi bir biçimlendirme hatası bulunmadı.



Sonuç:

Analiz geçmişine prediction filtresi eklendi.

ENTAILMENT, NEUTRAL ve CONTRADICTION değerleri destekleniyor.

Geçersiz filtre değerleri 422 ile reddediliyor.

Mevcut history endpointinin eski davranışı korunuyor.

Yeni API testleri başarıyla geçti.

Toplam 74 proje testi başarılı oldu.



Sonraki Gün İçin Plan



Analiz geçmişinde metin tabanlı arama özelliği üzerinde çalışmaya başlamak.

