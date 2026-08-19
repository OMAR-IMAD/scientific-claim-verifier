29\. Gün - Kullanıcı Girişi ve JWT Kimlik Doğrulama



2026-08-19



Bugün projede kullanıcı giriş sistemi ve JWT tabanlı kimlik doğrulama altyapısını geliştirdim.



İlk olarak PyJWT paketini kurdum ve requirements-base.txt dosyasına gerekli bağımlılığı ekledim.



Daha sonra security.py dosyasına JWT işlemleri için gerekli yapıları ekledim. HS256 algoritmasını kullandım ve access token süresini 30 dakika olarak belirledim. create\_access\_token fonksiyonu ile kullanıcı e-posta bilgisini içeren ve süreli JWT token oluşturma işlemini geliştirdim.



Ayrıca decode\_access\_token fonksiyonunu ekledim. Bu fonksiyon ile JWT token doğrulama, token içindeki sub ve exp alanlarını kontrol etme işlemlerini gerçekleştirdim.



schemas.py dosyasına TokenResponse modelini ekledim. Bu model access\_token ve token\_type alanlarını içeriyor.



main.py dosyasına /login endpointini ekledim. Kullanıcı giriş yaparken e-posta adresi veritabanında kontrol ediliyor ve parola hash değeri ile doğrulanıyor. Bilgiler doğruysa JWT access token oluşturuluyor. Yanlış parola veya kayıtlı olmayan e-posta durumunda 401 hata kodu döndürülüyor.



JWT ve login işlemleri için yeni otomatik testler ekledim. Token oluşturma, token çözme, başarılı giriş, yanlış parola ve kayıtlı olmayan e-posta senaryolarını test ettim.



Son olarak gerçek SQLite veritabanı üzerinde geçici bir kullanıcı oluşturarak kayıt ve giriş işlemlerini manuel olarak test ettim. Kullanıcı kaydı 201 ve giriş işlemi 200 durum kodu ile başarılı oldu. Giriş sonucunda access\_token ve bearer token\_type değeri doğru şekilde döndürüldü.



Sonuç:



\- PyJWT projeye eklendi.

\- JWT access token oluşturma işlemi geliştirildi.

\- JWT doğrulama ve çözme fonksiyonu eklendi.

\- TokenResponse modeli oluşturuldu.

\- /login endpointi oluşturuldu.

\- Yanlış parola ve kayıtlı olmayan kullanıcı için 401 kontrolü eklendi.

\- Toplam 59 proje testi başarılı oldu.

\- Backend smoke test başarılı oldu.

\- Gerçek model CUDA üzerinde başarılı şekilde çalıştı.

\- Gerçek veritabanında register ve login işlemleri başarıyla test edildi.

\- Proje ilerlemesi yaklaşık %41 seviyesine ulaştı.



Sonraki Gün İçin Plan

JWT token kullanarak korumalı endpoint yapısını geliştirmek ve giriş yapan kullanıcıyı belirleyen authentication dependency yapısına başlamak.
