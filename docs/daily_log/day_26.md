26\. Gün - Veritabanı ve Alembic Altyapısının Kurulması



2026-08-16



Bugün projeye veritabanı altyapısını ekledim.



İlk olarak SQLAlchemy ve Alembic paketlerini kurdum ve requirements-base.txt dosyasına gerekli bağımlılıkları ekledim. Daha sonra backend/app/database.py dosyasını oluşturarak SQLite bağlantısını hazırladım. Engine, SessionLocal ve Base yapılarını tanımladım. Bağlantıyı SELECT 1 sorgusu ile test ettim ve başarılı şekilde çalıştığını doğruladım.



Yerel veritabanı dosyasının GitHub'a eklenmemesi için .gitignore dosyasına .db ve .sqlite3 uzantılarını ekledim.



Daha sonra backend/app/models.py dosyasını oluşturdum. İlk olarak User modelini hazırladım. Bu modelde id, email, hashed\_password ve created\_at alanlarını tanımladım.



Ardından Analysis modelini ekledim. Bu modelde kullanıcıya ait analiz sonuçlarının saklanması için premise, hypothesis, prediction, confidence, entailment\_score, neutral\_score, contradiction\_score ve created\_at alanlarını oluşturdum. user\_id alanını ForeignKey kullanarak users tablosundaki id alanına bağladım.



SQLite üzerinde users ve analyses tablolarının doğru şekilde oluştuğunu kontrol ettim. Foreign key bağlantısını ve analyses tablosundaki kolonları ayrıca doğruladım.



Son olarak Alembic yapılandırmasını başlattım. alembic.ini dosyasını SQLite veritabanına bağladım ve env.py içinde Base.metadata tanımlamasını yaptım. İlk migration dosyasını autogenerate ile oluşturdum ve upgrade head komutu ile başarıyla uyguladım.



Sonuç:



\- SQLAlchemy ve Alembic kuruldu.

\- SQLite bağlantısı başarıyla çalıştı.

\- User ve Analysis modelleri oluşturuldu.

\- users ve analyses tabloları oluşturuldu.

\- Analysis.user\_id ile users.id arasında Foreign Key bağlantısı kuruldu.

\- İlk Alembic migration oluşturuldu ve uygulandı.

\- Veritabanı Alembic head sürümüne getirildi.

\- Toplam 40 proje testi başarılı.

\- Backend smoke test başarılı.

\- Gerçek model CUDA üzerinde başarılı şekilde çalıştı.

\- git diff --check kontrolünde hata bulunmadı.

\- Proje ilerlemesi yaklaşık %37 seviyesine ulaştı.



Sonraki Gün İçin Plan



Veritabanı işlemlerini backend yapısına entegre etmeye ve temel veri erişim işlemlerini geliştirmeye başlamak.