49\. Gün - Frontend Login Entegrasyonu ve JWT Yönetimi



2026-09-08



Bugün Frontend tarafına kullanıcı giriş işlemi eklendi.



frontend/src/services/api.js dosyasına loginUser fonksiyonu eklendi. Bu fonksiyon ile kullanıcı email ve şifre bilgileri /login endpointine POST isteği olarak gönderildi.



Başarılı giriş sonrasında Backend tarafından dönen JWT access token localStorage içine kaydedildi. Böylece /predict isteğinde token manuel olarak eklenmeden otomatik şekilde kullanılmaya başlandı.



App.jsx dosyasına Email ve Password alanları, Login butonu ve giriş durum mesajları eklendi. Boş alan kontrolü ve hatalı giriş mesajları test edildi.



Frontend ve Backend birlikte çalıştırılarak canlı test yapıldı. day47@example.com hesabı ile giriş başarıyla tamamlandı ve “Login successful.” mesajı alındı.



Daha sonra Scientific Claim Verifier üzerinden bir /predict testi yapıldı. Sonuç ENTAILMENT olarak alındı ve confidence değeri %93.13 olarak görüntülendi.



Frontend kodu ESLint ile kontrol edildi ve hata bulunmadı. Production build testi de başarıyla tamamlandı.



Sonuç:

Frontend login sistemi başarıyla eklendi.

JWT token otomatik olarak localStorage içine kaydedildi.

Login sonrası korumalı /predict endpointi başarıyla çalıştırıldı.

Frontend ve Backend bağlantısı canlı olarak test edildi.

ESLint ve production build testleri başarıyla geçti.



Sonraki Gün İçin Plan



Login durumunu kullanıcı arayüzünde daha düzenli göstermek ve kullanıcı deneyimini geliştirmek.
