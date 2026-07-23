2\. Gün – Tahmin API’sinin Test Edilmesi ve Sonuçların Belgelenmesi



&#x20;Tarih: 23 Temmuz 2026   9:00 - 13:12



Günün Amacı



Bu günün amacı, birinci gün geliştirilen FastAPI backend yapısını yeniden çalıştırmak, eğitilmiş NLI modelinin `/predict` endpointi üzerinden doğru şekilde kullanılabildiğini doğrulamak ve Entailment, Contradiction ve Neutral sınıflarının her biri için ayrı testler gerçekleştirmektir.



Ayrıca API’nin tahmin sonucuyla birlikte her sınıfa ait güven skorlarını doğru biçimde döndürüp döndürmediği incelenmiştir.



&#x20;Yapılan Çalışmalar



&#x20;1. Sanal Ortamın ve Backend Sunucusunun Başlatılması



Proje klasöründe Python sanal ortamı aktif edildi.



FastAPI uygulaması aşağıdaki komut kullanılarak çalıştırıldı:



powershell

python -m uvicorn backend.app.main:app --reload



Uvicorn sunucusu aşağıdaki yerel adreste başarıyla başlatıldı:



http://127.0.0.1:8000



Terminalde aşağıdaki mesajın görülmesiyle uygulamanın başarılı şekilde çalıştığı doğrulandı:



Application startup complete.



2\. Swagger API Dokümantasyonunun Açılması



FastAPI tarafından otomatik olarak oluşturulan Swagger dokümantasyonu aşağıdaki adres üzerinden açıldı:



http://127.0.0.1:8000/docs



Dokümantasyon sayfasında aşağıdaki endpointlerin kullanılabilir olduğu görüldü:



GET /

GET /health

POST /predict



Bu gün özellikle POST /predict endpointi üzerinde testler gerçekleştirildi.



3\. Entailment Testi



İlk testte, hypothesis cümlesinin premise cümlesinden mantıksal olarak çıkarılabildiği bir örnek kullanıldı.



Gönderilen Veri



{

&#x20; "premise": "A man is playing a guitar on stage.",

&#x20; "hypothesis": "A person is performing music."

}



API Sonucu

HTTP durum kodu: 200 OK

Tahmin: ENTAILMENT

Güven skoru: %89,81

Kullanılan cihaz: cuda

Sınıf Skorları

Entailment: %89,81

Neutral: %9,05

Contradiction: %1,15



Bu sonuç doğru kabul edildi. Çünkü sahnede gitar çalan bir kişinin müzik yaptığı premise cümlesinden mantıksal olarak çıkarılabilmektedir.



4\. Contradiction Testi



İkinci testte, premise ve hypothesis cümlelerinin açık biçimde birbiriyle çeliştiği bir örnek kullanıldı.



Gönderilen Veri



{

&#x20; "premise": "The laboratory door is open.",

&#x20; "hypothesis": "The laboratory door is closed."

}



API Sonucu

HTTP durum kodu: 200 OK

Tahmin: CONTRADICTION

Güven skoru: %96,60

Kullanılan cihaz: cuda

Sınıf Skorları

Entailment: %2,70

Neutral: %0,70

Contradiction: %96,60



Model bu örneği yüksek bir güven skoruyla doğru şekilde Contradiction olarak sınıflandırdı. Bir kapının aynı bağlamda hem açık hem de kapalı olması mümkün olmadığı için iki cümle birbiriyle çelişmektedir.



5\. Neutral Testi



Üçüncü testte, hypothesis cümlesindeki bilginin premise cümlesinde belirtilmediği bir örnek kullanıldı.



Gönderilen Veri



{

&#x20; "premise": "A scientist is conducting an experiment in a laboratory.",

&#x20; "hypothesis": "The scientist is wearing a blue shirt."

}



API Sonucu

HTTP durum kodu: 200 OK

Tahmin: NEUTRAL

Güven skoru: %63,27

Kullanılan cihaz: cuda

Sınıf Skorları

Entailment: %0,40

Neutral: %63,27

Contradiction: %36,31



Bu sonuç doğru kabul edildi. Premise cümlesinde bilim insanının kıyafeti veya gömleğinin rengi hakkında herhangi bir bilgi bulunmamaktadır. Bu nedenle hypothesis cümlesi ne doğrulanabilmekte ne de kesin olarak çürütülebilmektedir.



Neutral testindeki güven skorunun diğer iki teste göre daha düşük olduğu gözlemlendi. Bunun nedeni, Neutral örneklerinin bazı durumlarda model açısından daha fazla belirsizlik içermesidir.



6\. API Yanıt Yapısının İncelenmesi



POST /predict endpointinin her testte aşağıdaki bilgileri döndürdüğü doğrulandı:



Gönderilen premise metni

Gönderilen hypothesis metni

Tahmin edilen sınıf

Tahmin güven skoru

Üç sınıfa ait ayrı güven skorları



Modelin çalıştığı cihaz bilgisi



Örnek yanıt yapısı aşağıdaki gibidir:



{

&#x20; "premise": "Example premise",

&#x20; "hypothesis": "Example hypothesis",

&#x20; "prediction": "ENTAILMENT",

&#x20; "confidence": 0.89,

&#x20; "scores": {

&#x20;   "ENTAILMENT": 0.89,

&#x20;   "NEUTRAL": 0.09,

&#x20;   "CONTRADICTION": 0.02

&#x20; },

&#x20; "device": "cuda"

}



Bu yapı, ileride geliştirilecek frontend sonuç sayfasında tahminin ve güven skorlarının kullanıcıya açık şekilde gösterilebilmesi için uygundur.



7\. GPU Kullanımının Doğrulanması



Üç testin tamamında API yanıtındaki cihaz bilgisi aşağıdaki gibi döndü:



cuda

Bu sonuç, eğitilmiş modelin tahmin işlemlerinde NVIDIA ekran kartını başarıyla kullandığını göstermektedir.



8\. Sunucu Kayıtlarının Kontrol Edilmesi



PowerShell üzerindeki Uvicorn kayıtları incelendi.



Üç tahmin isteğinin tamamı aşağıdaki şekilde başarıyla tamamlandı:



POST /predict HTTP/1.1 200 OK



Herhangi bir uygulama hatası veya sunucu hatası oluşmadı.



Testler tamamlandıktan sonra backend sunucusu Ctrl + C ile güvenli şekilde durduruldu.



Test Sonuçlarının Özeti

| Test                                                  | Beklenen Sonuç | Model Sonucu  |  Güven |

| -----------------------------------------------| ---------------------- | ------------------- | --------: |

| Gitar çalan kişi müzik yapmaktadır  | Entailment            | Entailment        | %89,81 |

| Kapı açık / Kapı kapalı                     | Contradiction       | Contradiction    | %96,60 |

| Bilim insanının mavi gömlek giymesi | Neutral                | Neutral              | %63,27 |



Üç temel NLI sınıfının tamamı doğru şekilde tahmin edilmiştir.



Karşılaşılan Durumlar

Model ilk tahmin isteğinde belleğe yüklendiği için işlem diğer isteklere göre biraz daha uzun sürdü.

Neutral örneğinin güven skoru Entailment ve Contradiction örneklerine göre daha düşük çıktı.

Bu durum bir hata olarak değerlendirilmedi; Neutral örneklerinde daha fazla anlamsal belirsizlik bulunabilmektedir.

Swagger arayüzü sayesinde API istekleri ayrı bir frontend olmadan kolayca test edildi.

Gün Sonu Sonucu



FastAPI backend uygulaması başarıyla çalıştırıldı ve eğitilmiş NLI modelinin web API ile entegrasyonu doğrulandı.



POST /predict endpointi Entailment, Contradiction ve Neutral sınıflarının tamamında doğru sonuç üretti. API her tahmin için güven skorlarını, üç sınıfın olasılık dağılımını ve kullanılan cihaz bilgisini başarıyla döndürdü.



Bu testlerle birlikte modelin yalnızca komut satırında değil, REST API üzerinden de kullanılabildiği doğrulanmış oldu.



Sonraki Gün İçin Plan

API için otomatik test dosyalarının hazırlanması

Başarılı tahmin senaryolarının test edilmesi

Boş premise ve hypothesis girişlerinin test edilmesi

Eksik veya hatalı JSON isteklerinin incelenmesi

API hata yanıtlarının belgelenmesi









