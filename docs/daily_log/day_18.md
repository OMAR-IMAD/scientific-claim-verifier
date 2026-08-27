18\. Gün – Predict Endpoint Hata Yönetimi ve API Dokümantasyonu



Tarih: 8 Ağustos 2026



&#x20;Günün Amacı



Bugünkü çalışmanın amacı, `/predict` endpointindeki hata yönetimini geliştirmek ve model servisinde oluşabilecek farklı hata durumlarını kontrollü şekilde yönetmekti.



Ayrıca yeni hata durumlarının OpenAPI dokümantasyonunda gösterilmesi ve otomatik testlerle doğrulanması hedeflendi.



&#x20;Yapılan Çalışmalar



&#x20;1. Predict Endpoint Mevcut Yapısının İncelenmesi



İlk olarak `backend/app/main.py` dosyasındaki `/predict` endpointi incelendi.



Mevcut yapıda model servisi doğrudan oluşturuluyor ve tahmin işlemi doğrudan çalıştırılıyordu.



Bu nedenle model servisinin yüklenememesi, modelin hazır olmaması veya tahmin sırasında hata oluşması gibi durumlar için özel hata yönetimi bulunmuyordu.



&#x20;2. Model Servisi Yükleme Hatasının Yönetilmesi



get\_model\_service() çağrısı `try-except` yapısı içerisine alındı.



Model servisi herhangi bir nedenle oluşturulamazsa API artık kontrolsüz şekilde hata vermek yerine aşağıdaki HTTP cevabını döndürmektedir:



text

Status Code: 503



{

&#x20; "detail": "Model service is unavailable."

}



Bu sayede model yükleme problemi oluştuğunda istemciye anlaşılır ve kontrollü bir hata cevabı gönderilmektedir.



3\. Model Hazırlık Durumunun Kontrol Edilmesi



Model servisi başarılı şekilde oluşturulduktan sonra is\_ready() metodu kullanılarak modelin kullanıma hazır olup olmadığı kontrol edildi.



Model hazır değilse aşağıdaki cevap döndürülmektedir:

Status Code: 503



Response:

{

&#x20; "detail": "Model service is not ready."

}



Bu kontrol sayesinde hazır olmayan bir model üzerinde tahmin işlemi başlatılması engellendi.



4\. Tahmin İşlemi Hatalarının Yönetilmesi



model\_service.predict() işlemi ayrı bir try-except bloğu içerisine alındı.



Model tahmini sırasında beklenmeyen bir hata oluşursa API aşağıdaki cevabı döndürmektedir:



Status Code: 500



Response:



{

&#x20; "detail": "Prediction failed."

}



Böylece model inference işlemi sırasında meydana gelebilecek hatalar Backend tarafından kontrollü şekilde yönetilmektedir.



5\. Başarılı Tahmin Akışının Kontrol Edilmesi



Yeni hata yönetimi eklendikten sonra normal /predict işleminin çalışmaya devam edip etmediği test edildi.



Başarılı tahmin testi sorunsuz şekilde geçti.



Bu sonuç, yeni hata yönetiminin mevcut başarılı tahmin akışını bozmadığını gösterdi.



6\. Model Servisi Hatası İçin Otomatik Test



tests/test\_api.py dosyasına model servisi yüklenemediğinde /predict endpointinin davranışını kontrol eden yeni bir test eklendi.



Test sırasında get\_model\_service() fonksiyonunun hata üretmesi simüle edildi.



Beklenen sonuç:



503 Service Unavailable



Test başarıyla tamamlandı.



7\. Model Hazır Değil Durumu İçin Otomatik Test



Model servisinin mevcut olduğu ancak modelin hazır olmadığı senaryo için yeni bir test eklendi.



Test sırasında is\_ready() metodunun False döndürmesi sağlandı.



Beklenen cevap:



{

&#x20; "detail": "Model service is not ready."

}



Test başarıyla tamamlandı.



8\. Tahmin Hatası İçin Otomatik Test



Model servisi hazır olmasına rağmen predict() işleminin hata verdiği senaryo test edildi.



Test sırasında tahmin metodunun RuntimeError üretmesi simüle edildi.



Beklenen cevap:



{

&#x20; "detail": "Prediction failed."

}



HTTP durum kodu:



500



Test başarıyla tamamlandı.



9\. API Testlerinin Çalıştırılması



Yeni hata senaryoları eklendikten sonra tüm API testleri çalıştırıldı.



İlk aşamada API test sonucu:



16 passed



Daha sonra OpenAPI testi de eklendikten sonra API test sayısı 17'ye yükseldi.



Son API test sonucu:



17 passed, 1 warning in 12.87s



Tüm API testleri başarıyla tamamlandı.



10\. OpenAPI Hata Dokümantasyonunun Geliştirilmesi



/predict endpointinin OpenAPI dokümantasyonuna yeni hata cevapları eklendi.



Dokümante edilen yeni durumlar:

500 – Prediction Execution Failed



Tahmin işlemi sırasında hata oluştuğunda kullanılan response tanımlandı.



{

&#x20; "detail": "Prediction failed."

}

503 – Model Service Error



İki farklı 503 durumu dokümante edildi:



Model servisi kullanılamıyorsa:

{

&#x20; "detail": "Model service is unavailable."

}



Model hazır değilse:

{

&#x20; "detail": "Model service is not ready."

}



Bu hata cevaplarında mevcut ErrorResponse şeması kullanıldı.



11\. OpenAPI Otomatik Testinin Eklenmesi



OpenAPI şemasında 500 ve 503 response tanımlarının gerçekten bulunduğunu doğrulayan yeni bir test eklendi.



Test aşağıdaki noktaları kontrol etmektedir:



/predict altında 500 response bulunması

/predict altında 503 response bulunması

Hata açıklamalarının doğru olması



Test sonucu:

test\_openapi\_contains\_predict\_error\_responses PASSED



12\. Tüm Proje Testlerinin Çalıştırılması



Günün tüm geliştirmeleri tamamlandıktan sonra proje testlerinin tamamı yeniden çalıştırıldı.



Sonuç:



27 passed in 10.64s



Önceki gün toplam 23 test bulunurken bugün yeni testlerle birlikte toplam test sayısı 27'ye yükseldi.



Mevcut testlerde herhangi bir bozulma oluşmadı.



13\. Gerçek Model ile Smoke Test



Son olarak Backend ile gerçek model arasındaki entegrasyon yeniden kontrol edildi.



Smoke test sonucu:



\[PASS] Root endpoint

\[PASS] Health endpoint

\[PASS] Predict endpoint: ENTAILMENT 0.860682 cuda

\[PASS] Empty premise validation

\[PASS] Empty hypothesis validation



All backend smoke tests passed.



Gerçek modelin CUDA üzerinde çalışmaya devam ettiği ve yeni hata yönetiminin normal tahmin işlemini etkilemediği doğrulandı.



Gün Sonu Sonucu



Bugünkü çalışmada /predict endpointinin hata yönetimi önemli ölçüde geliştirildi.



Backend artık model servisi yüklenemediğinde, model hazır olmadığında ve tahmin işlemi sırasında hata oluştuğunda farklı ve kontrollü HTTP cevapları döndürmektedir.



Yeni hata durumları otomatik testlerle kontrol edildi ve OpenAPI dokümantasyonuna eklendi.



Gün sonunda toplam 27 otomatik test başarıyla geçti ve gerçek model ile yapılan smoke test de sorunsuz tamamlandı.



Sonraki Gün İçin Plan

Backend hata cevaplarının yapısını daha ayrıntılı incelemek

Tekrarlanan hata yönetimi kodlarını düzenlemek

Model servisinde oluşabilecek ek hata senaryolarını belirlemek

API test kapsamını genişletmek

Backend yapısını bir sonraki geliştirme aşamasına hazırlamak

