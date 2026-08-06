&#x20;17. Gün – Model Hazırlık Kontrolü ve Backend Hata Yönetimi



Tarih: 7 Ağustos 2026



&#x20;Günün Amacı



Bugünkü çalışmanın amacı, Backend uygulamasındaki `/health` endpointini geliştirmek ve model servisinin gerçek çalışma durumunu API üzerinden kontrol edilebilir hale getirmekti.



Ayrıca modelin hazır olmaması veya model servisinin yüklenememesi durumlarında Backend uygulamasının hata vererek kapanmasını önlemek hedeflendi.



Yapılan Çalışmalar



&#x20;1. Model Hazırlık Kontrolünün Eklenmesi



backend/app/model\_service.py dosyasındaki NLIModelService sınıfına is\_ready() metodu eklendi.



Bu metot aşağıdaki bileşenlerin kullanılabilir durumda olup olmadığını kontrol etmektedir:



\- Tokenizer nesnesinin oluşturulması

\- Model nesnesinin oluşturulması

\- Tokenizer değerinin boş olmaması

\- Model değerinin boş olmaması



Model ve tokenizer başarılı şekilde yüklenmişse metot `True`, aksi durumda `False` döndürmektedir.



&#x20;2. HealthResponse Şemasının Geliştirilmesi



`backend/app/schemas.py` dosyasındaki `HealthResponse` şeması genişletildi.



Yeni response yapısına aşağıdaki alanlar eklendi:



\- status

\- model\_ready

\- model\_status

\- device

\- detail



Bu alanlar sayesinde Backend ve model servisinin durumu daha ayrıntılı şekilde görüntülenebilmektedir.



Başarılı bir health response örneği:



json

{

&#x20; "status": "healthy",

&#x20; "model\_ready": true,

&#x20; "model\_status": "ready",

&#x20; "device": "cuda",

&#x20; "detail": null

}



3\. Health Endpointinin Geliştirilmesi



backend/app/main.py dosyasındaki /health endpointi yeniden düzenlendi.



Endpoint artık üç farklı durumu yönetmektedir.



Model Hazır Durumu



Model ve tokenizer başarılı şekilde yüklendiğinde:



status: healthy

model\_ready: true

model\_status: ready

Kullanılan cihaz: cpu veya cuda



değerleri döndürülmektedir.



Model Hazır Değil Durumu



Model servisi oluşturulmuş ancak model kullanıma hazır değilse:



status: degraded

model\_ready: false

model\_status: not\_ready

detail: Model service is not ready.



değerleri döndürülmektedir.



Model Servisi Hatası



Model servisi yüklenirken bir hata oluşursa hata yakalanmaktadır.



Bu durumda API kapanmak yerine:



status: degraded

model\_ready: false

model\_status: unavailable

Hata ayrıntısı



bilgilerini döndürmektedir.



4\. FakeModelService Sınıfının Güncellenmesi



Otomatik testlerde gerçek modeli yüklememek için kullanılan FakeModelService sınıfı güncellendi.



Sınıfa aşağıdaki özellikler eklendi:



Test cihazını belirten device değeri

Modelin hazır olduğunu belirten is\_ready() metodu



Bu sayede /health endpointi gerçek model yüklenmeden test edilebildi.



5\. Yeni Health Endpoint Testlerinin Eklenmesi



tests/test\_api.py dosyasına model durumlarını kontrol eden yeni testler eklendi.



Test edilen durumlar:

Modelin hazır olması

Modelin hazır olmaması

Model servisinin yüklenirken hata vermesi



Her durumda HTTP durum kodu ve JSON response içeriği ayrı ayrı kontrol edildi.



API testlerinin sonucu:

13 passed, 1 warning in 9.23s



6\. Tüm Proje Testlerinin Çalıştırılması



Projedeki bütün otomatik testler yeniden çalıştırıldı.



Test sonucu:



23 passed in 9.49s



Önceki 21 teste iki yeni test eklendi ve mevcut testlerin hiçbirinde bozulma oluşmadı.



7\. Smoke Test Dosyasının Güncellenmesi



backend/smoke\_test.py dosyasındaki /health kontrolü eski response yapısını beklediği için ilk çalıştırmada smoke test başarısız oldu.



Smoke test, yeni health response alanlarını kontrol edecek şekilde güncellendi.



Kontrol edilen alanlar:



status

model\_ready

model\_status

device

detail



Güncellemeden sonra gerçek model ile smoke test tekrar çalıştırıldı.



Sonuç:

\[PASS] Root endpoint

\[PASS] Health endpoint

\[PASS] Predict endpoint: ENTAILMENT 0.860682 cuda

\[PASS] Empty premise validation

\[PASS] Empty hypothesis validation



All backend smoke tests passed.



Gerçek modelin CUDA üzerinde çalıştığı ve Backend ile başarılı şekilde entegre olduğu yeniden doğrulandı.



Karşılaşılan Sorun



/health endpointinin response yapısı geliştirildikten sonra mevcut smoke test eski JSON yapısını beklediği için başarısız oldu.



Sorunun Backend veya model servisinden kaynaklanmadığı belirlendi. smoke\_test.py dosyasındaki health kontrolü yeni response yapısına göre güncellendi ve sorun çözüldü.



Gün Sonu Sonucu



Model servisinin hazır olup olmadığını kontrol eden sistem başarıyla geliştirildi.



/health endpointi artık yalnızca Backend uygulamasının çalıştığını değil, aynı zamanda modelin durumunu, kullanılan cihazı ve oluşabilecek hata ayrıntılarını da göstermektedir.



Model hazır olmadığında veya yükleme sırasında hata oluştuğunda API kapanmadan kontrollü bir response döndürmektedir.



Toplam 23 otomatik test ve gerçek model ile yapılan Backend smoke testleri başarıyla tamamlandı.



Sonraki Gün İçin Plan

/predict endpointindeki hata yönetimini geliştirmek

Model tahmini sırasında oluşabilecek hataları kontrollü şekilde yakalamak

Standart Backend hata cevapları hazırlamak

Yeni hata senaryoları için otomatik testler eklemek

Güncellenen Backend yapısını yeniden test etmek

