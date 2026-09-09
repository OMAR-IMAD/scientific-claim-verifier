50\. Gün - Frontend Oturum Yönetimi ve Logout İşlemi



2026-09-09



Bugün Frontend tarafında kullanıcı oturum yönetimi geliştirildi.



App.jsx dosyasına isLoggedIn durumu eklendi. JWT access token localStorage içinde varsa kullanıcının giriş yapmış olduğu kontrol edildi.



Başarılı giriş işleminden sonra Login formu gizlenerek kullanıcıya "Logged in." mesajı ve Logout butonu gösterildi.



Logout işlemi için handleLogout fonksiyonu eklendi. Bu işlem sırasında access\_token localStorage üzerinden silindi ve kullanıcı giriş durumu kapatıldı.



Login, Logout ve tekrar Login işlemleri canlı olarak test edildi. Ayrıca giriş yaptıktan sonra /predict isteği tekrar test edildi ve ENTAILMENT sonucu %93.13 confidence değeri ile başarıyla alındı.



Frontend kodu ESLint ile kontrol edildi ve hata bulunmadı. Production build testi de başarıyla tamamlandı.



Sonuç:

Frontend oturum yönetimi eklendi.

JWT token kontrolü yapıldı.

Logout işlemi başarıyla çalıştırıldı.

Login sonrası /predict işlemi test edildi.

ESLint ve production build testleri başarılı geçti.



Sonraki Gün İçin Plan



Kullanıcı oturum bilgisini arayüzde daha düzenli göstermek ve kullanıcı deneyimini geliştirmeye devam etmek.
