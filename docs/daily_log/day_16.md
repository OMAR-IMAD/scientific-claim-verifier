&#x20;16. Gün – Backend Yapısının Kontrolü ve Gerçek Model Entegrasyonunun Doğrulanması



Tarih: 6 Ağustos 2026



&#x20;Yapılan Çalışmalar



Bugün projenin Backend geliştirme aşamasına geçildi. İlk olarak mevcut FastAPI yapısı incelendi ve Backend dosyalarının aşağıdaki klasörde bulunduğu doğrulandı:



\- backend/app/main.py

\- backend/app/schemas.py

\- backend/app/model\_service.py



Mevcut API yapısında aşağıdaki endpointlerin bulunduğu görüldü:



\- GET /

\- GET /health

\- POST /predict



main.py, schemas.py ve model\_service.py dosyaları Python syntax kontrolünden geçirildi. Herhangi bir syntax hatası bulunmadı.



&#x20;Model Servisinin İncelenmesi



model\_service.py dosyası incelendi. Servisin sahte bir model yerine eğitilen gerçek NLI modelini kullandığı doğrulandı.



Model aşağıdaki klasörden yüklenmektedir:



models/improved\_test/final\_model



Model klasöründe gerekli dosyaların bulunduğu kontrol edildi:



\- config.json

\- model.safetensors

\- tokenizer.json

\- tokenizer\_config.json

\- training\_args.bin



Modelin yüklenmesi için AutoTokenizer ve AutoModelForSequenceClassification sınıflarının kullanıldığı görüldü.



Model servisi tahmin sonucuyla birlikte aşağıdaki bilgileri döndürmektedir:



\- Tahmin sınıfı

\- Confidence değeri

\- Üç sınıfa ait olasılık skorları

\- Kullanılan cihaz



&#x20;Gerçek Model Testi



Model servisi doğrudan çalıştırılarak aşağıdaki örnek üzerinde test edildi:



\- Premise: A man is playing a guitar.

\- Hypothesis: A person is making music.



Elde edilen sonuç:



\- Prediction: ENTAILMENT

\- Confidence: 0.860682

\- Device: cuda



Bu test ile gerçek modelin başarıyla yüklendiği ve GPU üzerinde çalıştığı doğrulandı.



&#x20;API Entegrasyon Testleri



Gerçek model ile /predict endpointi test edildi. API isteği başarılı şekilde işlendi ve HTTP `200` durum kodu döndürüldü.



Response içerisinde aşağıdaki alanların bulunduğu doğrulandı:



\- premise

\- hypothesis

\- prediction

\- confidence

\- scores

\- device



Modelin üç farklı NLI sınıfını doğru isimlerle döndürdüğü kontrol edildi:



text

ENTAILMENT: 0.860682

CONTRADICTION: 0.989833

NEUTRAL: 0.514358



Test sonuçları:



Boş premise isteği: HTTP 422

Boş hypothesis isteği: HTTP 422



API tarafından aşağıdaki hata mesajlarının doğru şekilde döndürüldüğü görüldü:



Premise cannot be empty.

Hypothesis cannot be empty.

Smoke Test Dosyasının Hazırlanması



Backend yapısının temel bileşenlerini tek komutla kontrol etmek için aşağıdaki dosya oluşturuldu:

backend/smoke\_test.py



Bu dosyada aşağıdaki kontroller gerçekleştirildi:



Root endpoint kontrolü

Health endpoint kontrolü

Gerçek model ile predict endpoint kontrolü

Response alanlarının kontrolü

Confidence değerinin sınır kontrolü

Üç sınıf skorunun kontrolü

Skorların toplamının yaklaşık 1.0 olması

Boş premise doğrulaması

Boş hypothesis doğrulaması



Smoke test aşağıdaki komutla çalıştırıldı:

.\\.venv\\Scripts\\python.exe -m backend.smoke\_test



Test sonucu:

\[PASS] Root endpoint

\[PASS] Health endpoint

\[PASS] Predict endpoint

\[PASS] Empty premise validation

\[PASS] Empty hypothesis validation



All backend smoke tests passed.

Genel Test Sonucu



Projenin tüm otomatik testleri tekrar çalıştırıldı:

.\\.venv\\Scripts\\python.exe -m pytest -v



Test sonucu:



21 passed in 9.56s



Gün Sonu Sonucu



Backend yapısı, API endpointleri, şemalar ve model servisi ayrıntılı olarak kontrol edildi.



Eğitilen gerçek modelin FastAPI Backend ile başarılı şekilde entegre olduğu ve CUDA üzerinde çalıştığı doğrulandı.



Ayrıca Backend ile model arasındaki entegrasyonu hızlı şekilde kontrol eden tekrar kullanılabilir bir smoke test dosyası hazırlandı.



Sonraki Gün İçin Plan

Backend hata yönetimini geliştirmek

Model yükleme hatalarını kontrollü şekilde yönetmek

Health endpointine model durumu bilgisi eklemek

Yeni Backend testleri hazırlamak

