48\. Gün - Frontend API Yapısının Düzenlenmesi



2026-09-07



Bugün Frontend tarafındaki Backend API bağlantı yapısını daha düzenli hale getirdim.



API işlemlerini App.jsx dosyasından ayırmak için frontend/src/services klasörü oluşturuldu ve api.js dosyası eklendi. /predict endpointine gönderilen POST isteği, JWT access token kullanımı ve hata kontrolü bu dosyaya taşındı.



App.jsx dosyası sadeleştirilerek doğrudan fetch işlemi kaldırıldı. Bunun yerine verifyClaim fonksiyonu kullanılarak API bağlantısı ayrı bir servis üzerinden çalıştırıldı.



Yapılan değişikliklerden sonra Frontend kodu ESLint ile kontrol edildi ve herhangi bir hata bulunmadı. Production build testi de başarıyla tamamlandı.



Son olarak Frontend ve Backend birlikte çalıştırılarak canlı test yapıldı. JWT token yenilendi ve Scientific Claim Verifier arayüzünden yapılan testte Entailment sonucu başarıyla alındı.



Sonuç:

Frontend API yapısı daha düzenli hale getirildi.

API işlemleri ayrı bir servis dosyasına taşındı.

JWT ile korunan /predict endpointi başarıyla çalıştırıldı.

Frontend ve Backend bağlantısı canlı olarak test edildi.

ESLint ve production build testleri başarıyla tamamlandı.



Sonraki Gün İçin Plan



Frontend tarafında kullanıcı deneyimini geliştirmek ve API servis yapısını genişletmeye devam etmek.
