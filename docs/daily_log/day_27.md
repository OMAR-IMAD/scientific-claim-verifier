27\. Gün - CRUD İşlemleri ve Veritabanı Entegrasyonu



2026-08-17



Bugün veritabanı işlemlerini backend yapısına entegre etmeye devam ettim.



İlk olarak database.py dosyasına get\_db fonksiyonunu ekledim. Bu fonksiyon sayesinde FastAPI endpointleri için veritabanı oturumu oluşturuluyor ve işlem tamamlandıktan sonra oturum güvenli şekilde kapatılıyor.



Daha sonra main.py dosyasında FastAPI Depends yapısını kullanarak /predict endpointine veritabanı oturumu ekledim. Yapılan değişikliklerden sonra API testlerini çalıştırdım ve mevcut 21 test başarılı oldu.



Veritabanı işlemlerini ayrı bir yapıda tutmak için backend/app/crud.py dosyasını oluşturdum.



Bu dosyada aşağıdaki temel CRUD fonksiyonlarını geliştirdim:



\- get\_user\_by\_email: Kullanıcıyı e-posta adresine göre bulmak için kullanıldı.

\- create\_user: Yeni kullanıcı oluşturmak için geliştirildi.

\- create\_analysis: Yeni analiz sonucunu veritabanına kaydetmek için geliştirildi.

\- get\_analyses\_by\_user: Bir kullanıcıya ait analizleri listelemek için geliştirildi.



get\_analyses\_by\_user fonksiyonunda analizlerin en yeni kayıttan eski kayda doğru sıralanmasını sağladım. Aynı created\_at değerine sahip kayıtlar için id alanını ikinci sıralama kriteri olarak kullandım.



CRUD fonksiyonlarını önce manuel olarak test ettim. Test kullanıcıları ve analiz kayıtları başarıyla oluşturuldu, okundu ve test sonrasında silindi.



Daha sonra tests/test\_crud.py dosyasını oluşturdum. Testlerde gerçek proje veritabanını etkilememek için geçici SQLite in-memory veritabanı kullandım.



Eklenen CRUD testleri:



\- Olmayan kullanıcının None döndürmesi.

\- Kullanıcı oluşturma ve e-posta ile tekrar bulma.

\- Kullanıcıya ait analizleri oluşturma ve en yeni kayıt önce olacak şekilde listeleme.



CRUD testlerinin tamamı başarılı oldu.



Sonuç:



\- get\_db veritabanı dependency yapısı eklendi.

\- /predict endpointi veritabanı oturumu ile çalışacak şekilde hazırlandı.

\- CRUD katmanı oluşturuldu.

\- Kullanıcı oluşturma ve kullanıcı arama işlemleri geliştirildi.

\- Analiz oluşturma ve kullanıcı analizlerini listeleme işlemleri geliştirildi.

\- Analiz sıralaması en yeni kayıt önce olacak şekilde düzenlendi.

\- SQLite in-memory tabanlı CRUD testleri eklendi.

\- 3 CRUD testi başarılı.

\- Toplam 43 proje testi başarılı.

\- Backend smoke test başarılı.

\- Gerçek model CUDA üzerinde başarılı şekilde çalıştı.

\- Proje ilerlemesi yaklaşık %39 seviyesine ulaştı.



Sonraki Gün İçin Plan



CRUD işlemlerini geliştirmeye devam etmek ve kullanıcı doğrulama sistemi için gerekli backend altyapısını hazırlamak.