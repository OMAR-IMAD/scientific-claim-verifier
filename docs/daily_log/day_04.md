&#x20;4. Gün – API Şemalarının Düzenlenmesi ve Swagger Dokümantasyonunun Geliştirilmesi



Tarih: 25 Temmuz 2026



&#x20;Günün Amacı



Bugün FastAPI backend yapısındaki request ve response modellerini daha düzenli hâle getirmek ve Swagger dokümantasyonunu geliştirmek amaçlandı.



&#x20;Yapılan Çalışmalar



İlk olarak API modellerini ayrı bir dosyada toplamak için aşağıdaki dosya oluşturuldu:



backend/app/schemas.py



Bu dosyada aşağıdaki Pydantic modelleri tanımlandı:



\- RootResponse

\- HealthResponse

\- PredictionRequest

\- PredictionScores

\- PredictionResponse



Prediction sınıfları için kullanılabilecek sonuçlar ENTAILMENT , NEUTRAL ve CONTRADICTION olarak sınırlandırıldı.



Güven skorlarının 0.0 ile 1.0 arasında olması gerektiği belirtildi. Premise ve hypothesis alanlarına açıklamalar ve örnek metinler eklendi.



Daha sonra backend/app/main.py dosyası düzenlendi. Daha önce main dosyasında bulunan PredictionRequest sınıfı kaldırıldı ve yeni oluşturulan schemas.py dosyasındaki modeller kullanılmaya başlandı.



Root, health ve predict endpointlerine response modelleri eklendi:



\- GET / için RootResponse

\- GET /health için HealthResponse

\- POST /predict için PredictionResponse



Endpointlerin Swagger sayfasında daha anlaşılır görünmesi için summary ve description alanları düzenlendi.



&#x20;Kod Kontrolü



Değişikliklerden sonra Python dosyalarında yazım hatası olup olmadığını kontrol etmek için aşağıdaki komut çalıştırıldı:



.\\.venv\\Scripts\\python.exe -m py\_compile backend\\app\\schemas.py backend\\app\\main.py



Komut herhangi bir hata vermeden tamamlandı.



&#x20;Otomatik Testler



API’nin mevcut davranışlarının bozulmadığını kontrol etmek için sekiz otomatik test tekrar çalıştırıldı.



Kullanılan komut:



.\\.venv\\Scripts\\python.exe -m pytest tests\\test\_api.py -v



Test sonucu:



8 passed, 1 warning in 57.66s



Sekiz testin tamamı başarıyla geçti. Görünen warning mesajı test sonuçlarını etkilemedi.



&#x20;Swagger Kontrolü



Backend sunucusu çalıştırıldı ve Swagger sayfası aşağıdaki adresten açıldı:



http://127.0.0.1:8000/docs



Swagger sayfasında endpoint açıklamalarının güncellendiği görüldü.



Ayrıca Schemas bölümünde aşağıdaki modellerin ayrı olarak görüntülendiği doğrulandı:



\- HealthResponse

\- PredictionRequest

\- PredictionResponse

\- PredictionScores

\- RootResponse



Kontroller tamamlandıktan sonra sunucu güvenli şekilde durduruldu.



&#x20;Gün Sonu Sonucu



API request ve response şemaları ayrı bir dosyada düzenlendi. Main dosyasının yapısı sadeleştirildi ve endpointlerin döndürdüğü veriler açık biçimde tanımlandı.



Swagger dokümantasyonu daha anlaşılır hâle getirildi. Yapılan değişikliklerden sonra bütün otomatik testlerin başarıyla geçtiği doğrulandı.



&#x20;Sonraki Gün İçin Plan



\- Swagger üzerinde request ve response örneklerini incelemek

\- Response model doğrulamasını test etmek

\- API dokümantasyonunda küçük iyileştirmeler yapmak

