28\. Gün - Kullanıcı Kayıt ve Şifre Güvenliği Altyapısı



2026-08-18



Bugün projede kullanıcı kayıt ve şifre güvenliği altyapısını geliştirdim.



İlk olarak pwdlib paketini Argon2 desteği ile kurdum ve requirements-base.txt dosyasına gerekli bağımlılığı ekledim.



Daha sonra backend/app/security.py dosyasını oluşturdum. Bu dosyada kullanıcı şifrelerini güvenli şekilde saklamak için hash\_password ve verify\_password fonksiyonlarını geliştirdim. Şifreleme işlemlerinde Argon2 algoritmasını kullandım. Fonksiyonları manuel olarak test ettim ve doğru şifrenin kabul edildiğini, yanlış şifrenin ise reddedildiğini doğruladım.



Security işlemleri için tests/test\_security.py dosyasını oluşturdum. Şifre oluşturma, doğru şifre doğrulama ve yanlış şifreyi reddetme işlemleri için 3 test ekledim. Tüm security testleri başarılı oldu.



Daha sonra schemas.py dosyasına kullanıcı işlemleri için yeni Pydantic modelleri ekledim:



\- UserCreate: Yeni kullanıcı kayıt verilerini doğrulamak için.

\- UserLogin: Kullanıcı giriş verilerini doğrulamak için.

\- UserResponse: API üzerinden sadece güvenli kullanıcı bilgilerini döndürmek için.



UserCreate modelinde e-posta adresinin boşluklarını temizleme, küçük harfe dönüştürme ve temel e-posta kontrolü işlemlerini ekledim. Şifre için minimum 8 ve maksimum 128 karakter sınırı belirledim.



UserResponse modelinde sadece id ve email alanlarının dışarı verilmesini sağladım. hashed\_password alanının API response içinde görünmediğini test ettim.



Daha sonra main.py dosyasına /register endpointini ekledim. Bu endpoint yeni kullanıcı oluşturulmadan önce e-posta adresinin veritabanında bulunup bulunmadığını kontrol ediyor. Kullanıcı daha önce kayıtlıysa 409 hata kodu döndürülüyor. Yeni kullanıcı oluşturulurken şifre Argon2 ile hash edilerek veritabanına kaydediliyor.



Register endpointini gerçek veritabanı üzerinde manuel olarak test ettim. Yeni kullanıcı kaydı 201 durum kodu ile başarılı oldu. Aynı e-posta ile ikinci kayıt denemesi 409 durum kodu ile reddedildi.



Ayrıca test\_api.py dosyasına register endpointi için otomatik testler ekledim. Başarılı kayıt ve tekrar eden e-posta senaryoları test edildi.



Sonuç:



\- pwdlib ve Argon2 desteği eklendi.

\- Şifre hash ve doğrulama fonksiyonları geliştirildi.

\- 3 security testi başarılı oldu.

\- UserCreate ve UserLogin modelleri oluşturuldu.

\- UserResponse modeli oluşturuldu.

\- hashed\_password bilgisinin API üzerinden görünmesi engellendi.

\- /register endpointi oluşturuldu.

\- Yeni kullanıcı kaydı başarıyla test edildi.

\- Tekrar eden e-posta kaydı 409 ile engellendi.

\- Toplam 53 proje testi başarılı oldu.

\- Backend smoke test başarılı oldu.

\- Gerçek model CUDA üzerinde başarılı şekilde çalıştı.

\- Proje ilerlemesi yaklaşık %40 seviyesine ulaştı.



Sonraki Gün İçin Plan



Kullanıcı giriş işlemini geliştirmek ve JWT tabanlı kimlik doğrulama altyapısına başlamak.