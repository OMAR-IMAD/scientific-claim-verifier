30\. Gün - JWT ile Korumalı Endpoint ve Mevcut Kullanıcı Doğrulaması



2026-08-20



Bugün projede JWT tabanlı kimlik doğrulama sistemini geliştirmeye devam ettim.



İlk olarak security.py dosyasına HTTPBearer yapısını ekledim. Bu yapı ile Authorization header üzerinden Bearer token alınmasını sağladım.



Daha sonra get\_current\_user fonksiyonunu oluşturdum. Bu fonksiyon gelen JWT tokenı doğruluyor, token içindeki sub bilgisini kontrol ediyor ve kullanıcıyı veritabanından buluyor. Token gönderilmediğinde, geçersiz veya süresi dolmuş token kullanıldığında ve kullanıcı veritabanında bulunmadığında 401 hata kodu döndürülüyor.



get\_current\_user fonksiyonu için otomatik testler ekledim. Geçerli token, eksik token, geçersiz token ve veritabanında bulunmayan kullanıcı senaryolarını test ettim. security.py için toplam 9 test başarılı oldu.



Daha sonra main.py dosyasına /me endpointini ekledim. Bu endpoint sadece geçerli JWT Bearer token ile erişilebiliyor ve giriş yapan kullanıcının id ve email bilgilerini döndürüyor.



API testlerine /me endpointi için yeni testler ekledim. Giriş yapan kullanıcının bilgilerinin doğru dönmesi ve token olmadan erişimin 401 ile reddedilmesi kontrol edildi. test\_api.py içinde toplam 28 test başarılı oldu.



Son olarak tüm proje testlerini çalıştırdım ve toplam 65 test başarılı oldu. Backend smoke test de başarılı şekilde tamamlandı ve gerçek NLI modeli CUDA üzerinde çalışmaya devam etti.



Ayrıca gerçek veritabanı kullanılarak kayıt, giriş ve /me işlemlerini birlikte test ettim. Kullanıcı kaydı 201, giriş işlemi 200 ve korumalı /me endpointi 200 durum kodu ile başarılı oldu.



Sonuç:



\- HTTP Bearer authentication yapısı eklendi.

\- get\_current\_user authentication dependency oluşturuldu.

\- JWT token doğrulaması geliştirildi.

\- Eksik ve geçersiz token kontrolleri eklendi.

\- Kullanıcının veritabanında bulunma kontrolü eklendi.

\- /me korumalı endpointi oluşturuldu.

\- security.py testleri 9 başarılı.

\- test\_api.py testleri 28 başarılı.

\- Toplam 65 proje testi başarılı.

\- Backend smoke test başarılı.

\- Gerçek model CUDA üzerinde başarılı şekilde çalıştı.

\- Register -> Login -> JWT -> /me akışı gerçek veritabanı üzerinde başarıyla test edildi.

\- Proje ilerlemesi yaklaşık %43 seviyesine ulaştı.



Sonraki Gün İçin Plan

JWT doğrulamasını tahmin işlemleri ile birleştirmek, /predict endpointini kullanıcı hesabı ile ilişkilendirmek ve analiz sonuçlarını kullanıcıya bağlı şekilde veritabanına kaydetmeye başlamak.
