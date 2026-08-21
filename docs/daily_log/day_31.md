31. Gün - Tahmin Sonuçlarının Kullanıcıya Bağlı Olarak Kaydedilmesi



2026-08-21



Bugün /predict endpointini kullanıcı hesabı ve veritabanı ile ilişkilendirdim.



Endpoint içine get\_current\_user ve veritabanı bağlantısını ekledim. Böylece tahmin işlemi sadece giriş yapmış kullanıcı tarafından kullanılabilir hale geldi.



Modelden gelen tahmin sonucunu create\_analysis fonksiyonu ile veritabanına kaydettim. Kayıt sırasında kullanıcının id bilgisi, premise, hypothesis, prediction, confidence ve sınıf skorları saklanıyor.



Daha sonra backend smoke testlerini çalıştırdım. Kayıt, giriş, korumalı endpoint, model tahmini, doğrulama kontrolleri ve test verilerinin temizlenmesi başarıyla tamamlandı.



Son olarak git diff --check ile değişiklikleri kontrol ettim ve herhangi bir hata görülmedi.



Sonuç:



/predict endpointi JWT ile korumalı hale getirildi.

Tahmin işlemi giriş yapan kullanıcı ile ilişkilendirildi.

Tahmin sonuçları veritabanına kaydedilmeye başlandı.

Prediction ve confidence değerleri kaydedildi.

Entailment, Neutral ve Contradiction skorları kaydedildi.

Backend smoke testleri başarıyla geçti.

Kod değişikliklerinde biçimlendirme hatası bulunmadı.



Sonraki Gün İçin Plan



Kullanıcının daha önce yaptığı analizleri görebilmesi için analiz geçmişi endpointi üzerinde çalışmaya başlamak.

