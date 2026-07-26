&#x20;5. Gün – Swagger Örneklerinin Geliştirilmesi ve Response Model Kontrolü



Tarih: 26 Temmuz 2026



&#x20;Günün Amacı



Bugün Swagger dokümantasyonunda request ve response örneklerini daha anlaşılır hâle getirmek ve prediction yanıtının doğru yapıda döndürüldüğünü otomatik test ile kontrol etmek amaçlandı.



&#x20;Yapılan Çalışmalar



İlk olarak backend/app/schemas.py dosyası güncellendi. Pydantic modellerine `ConfigDict` kullanılarak örnek JSON verileri eklendi.



Aşağıdaki modeller için Swagger örnekleri hazırlandı:



\- RootResponse

\- HealthResponse

\- PredictionRequest

\- PredictionScores

\- PredictionResponse



Premise, hypothesis, confidence skorları ve modelin kullandığı cihaz bilgisi için açıklamalar eklendi.



Daha sonra Swagger sayfası kontrol edildi. POST /predict bölümünde request örneğinin doğru şekilde görüntülendiği görüldü:



\- Premise: A man is playing a guitar on stage.

\- Hypothesis: A person is performing music.



İlk kontrolde başarılı response örneğinde genel "string" ve 1 değerleri gösteriliyordu. Bu nedenle backend/app/main.py dosyasındaki POST /predict endpointine özel bir 200 response örneği eklendi.



Yapılan değişiklikten sonra Swagger sayfasında aşağıdaki bilgiler doğru şekilde görüntülendi:



\- prediction: ENTAILMENT

\- confidence: 0.90

\- Entailment, Neutral ve Contradiction skorları

\- device: cuda



&#x20;Yeni Otomatik Test



Prediction yanıtının tam yapısını kontrol etmek için `tests/test\_api.py` dosyasına yeni bir test eklendi.



Bu test aşağıdaki alanların response içinde bulunduğunu kontrol etmektedir:



\- premise

\- hypothesis

\- prediction

\- confidence

\- scores

\- device



Ayrıca scores alanında üç NLI sınıfının bulunduğu ve confidence değerinin 0.0 ile 1.0 arasında olduğu doğrulandı.



&#x20;Test Sonucu



Yeni test eklendikten sonra toplam dokuz otomatik test çalıştırıldı.



Test sonucu:



9 passed, 1 warning in 11.02s



Dokuz testin tamamı başarıyla geçti. Warning mesajı test sonuçlarını etkilemedi.



&#x20;Gün Sonu Sonucu



Swagger request ve response örnekleri geliştirildi. Kullanıcıların API’ye hangi verileri göndereceği ve nasıl bir sonuç alacağı daha açık hâle getirildi.



Prediction response yapısı yeni bir otomatik test ile kontrol altına alındı. Yapılan değişikliklerin API’nin mevcut çalışmasını bozmadığı doğrulandı.



&#x20;Sonraki Gün İçin Plan



\- API hata yanıtlarını daha ayrıntılı incelemek

\- Hata mesajları için ortak bir yapı planlamak

\- Otomatik testlere yeni hata senaryoları eklemek

