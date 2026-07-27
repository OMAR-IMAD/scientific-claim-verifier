&#x20;6. Gün – API Hata Yanıtlarının Düzenlenmesi



Tarih: 27 Temmuz 2026



&#x20;Günün Amacı



Bugün API hata yanıtlarını daha anlaşılır hâle getirmek ve Swagger sayfasında boş giriş hatalarını örneklerle göstermek amaçlandı.



Yapılan Çalışmalar



İlk olarak backend/app/schemas.py dosyasına yeni bir ErrorResponse modeli eklendi.



Bu model, API tarafından döndürülen basit hata mesajlarını temsil etmektedir:



\- detail



Örnek hata mesajı olarak aşağıdaki değer tanımlandı:



Premise cannot be empty.



Daha sonra backend/app/main.py dosyasında ErrorResponse modeli import edildi. POST /predict endpointinin 422 hata yanıtı yeniden düzenlendi.



Swagger dokümantasyonuna iki farklı hata örneği eklendi:



\- Empty premise

\- Empty hypothesis



Bu örneklerde aşağıdaki mesajlar gösterildi:



Premise cannot be empty.



Hypothesis cannot be empty.



&#x20;Karşılaşılan Sorun



main.py dosyası düzenlenirken @app.post() bölümündeki bir kapatma parantezi eksik kaldı. Dosya kontrol edildiğinde aşağıdaki hata alındı:



SyntaxError: ( was never closed



İlgili satırlar incelendi ve eksik parantez eklendi. Ayrıca yanlışlıkla tekrarlanan def predict\_claim ifadesi düzeltildi.



Düzeltmeden sonra dosyalar tekrar kontrol edildi ve herhangi bir yazım hatası görülmedi.



Otomatik Testler



Değişikliklerden sonra mevcut API testleri tekrar çalıştırıldı.



Kullanılan komut:



.\\.venv\\Scripts\\python.exe -m pytest tests\\test\_api.py -v



Test sonucu:



9 passed, 1 warning in 41.88s



Dokuz testin tamamı başarıyla geçti. Warning mesajı testlerin çalışmasını etkilemedi.



&#x20;Swagger Kontrolü



Backend sunucusu çalıştırıldı ve Swagger sayfası açıldı.



POST /predict endpointinin 422 bölümünde iki hata örneğinin listelendiği görüldü.



Empty premise seçildiğinde:



Premise cannot be empty.



Empty hypothesis seçildiğinde:



Hypothesis cannot be empty.



mesajlarının doğru şekilde görüntülendiği doğrulandı.



Kontroller tamamlandıktan sonra sunucu güvenli şekilde durduruldu.



\## Gün Sonu Sonucu



API hata yanıtları için ortak bir model oluşturuldu. Boş premise ve hypothesis girişlerine ait hata örnekleri Swagger dokümantasyonuna eklendi.



Karşılaşılan yazım hatası giderildi ve yapılan değişikliklerin mevcut API işlevlerini bozmadığı otomatik testlerle doğrulandı.



&#x20;Sonraki Gün İçin Plan



\- Hata yanıtları için yeni otomatik testler eklemek

\- Swagger hata şemalarını tekrar kontrol etmek

\- API hata yönetimini geliştirmek

