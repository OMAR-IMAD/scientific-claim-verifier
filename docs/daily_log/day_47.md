47\. Gün - Frontend ve Backend API Entegrasyonu



2026-09-06



Bugün React tabanlı Frontend ile FastAPI Backend arasındaki bağlantı üzerinde çalıştım.



Backend tarafında CORS ayarları yapılarak localhost:5173 üzerinden gelen Frontend isteklerine izin verildi. Daha sonra Frontend tarafında /predict endpointine POST isteği gönderen yapı hazırlandı.



JWT access token localStorage üzerinden alınarak Authorization header içinde Backend'e gönderildi. Premise ve Hypothesis alanlarındaki veriler JSON formatında /predict endpointine gönderildi.



Backend'den dönen prediction, confidence ve sınıf skorları Frontend üzerinde gösterildi.



Sistem üç farklı örnek ile test edildi:

Entailment sonucu başarıyla alındı.

Contradiction sonucu başarıyla alındı.

Neutral sonucu başarıyla alındı.



Son olarak Frontend kodu ESLint ile kontrol edildi ve production build testi başarıyla tamamlandı.



Sonuç:

Frontend ve Backend bağlantısı başarıyla kuruldu.

JWT ile korunan /predict endpointi Frontend üzerinden çalıştırıldı.

NLI modelinin üç sınıf sonucu arayüzde başarıyla gösterildi.

ESLint ve production build testleri başarılı geçti.



Sonraki Gün İçin Plan



Frontend tarafında kullanıcı deneyimini geliştirmek ve API bağlantı yapısını daha düzenli hale getirmek.
