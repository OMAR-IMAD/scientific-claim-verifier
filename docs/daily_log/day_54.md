54\. Gün - Frontend Analiz Sonuçlarının Görselleştirilmesi



2026-09-13



Bugün Frontend tarafında analiz sonuçlarının kullanıcıya daha düzenli gösterilmesi için arayüz geliştirildi.



App.jsx dosyasında sonuç bölümü yeniden düzenlendi. Prediction ve Confidence bilgileri ayrı ve daha belirgin şekilde gösterildi.



ENTAILMENT, NEUTRAL ve CONTRADICTION sonuçları için yüzde değerlerini gösteren score bar yapısı eklendi.



App.css dosyasında sonuç kartı, başlık, score bar ve renk düzenlemeleri yapıldı. Entailment yeşil, Neutral turuncu ve Contradiction kırmızı renk ile gösterildi.



Verify Claim işlemi tekrar test edildi. Örnek testte ENTAILMENT sonucu %93.13 confidence değeri ile başarıyla gösterildi.



Frontend kodu ESLint ile kontrol edildi ve hata bulunmadı. Production build testi de başarıyla tamamlandı.



Sonuç:

Analiz sonuçları daha düzenli hale getirildi.

Prediction ve Confidence bilgileri geliştirildi.

Üç NLI sınıfı için score bar eklendi.

Yüzde değerleri arayüzde doğru gösterildi.

ESLint ve production build testleri başarılı geçti.



Sonraki Gün İçin Plan



Frontend sonuç ekranını geliştirmeye ve kullanıcı deneyimini daha düzenli hale getirmeye devam etmek.
