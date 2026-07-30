&#x20;10. Gün – OpenAPI Fixture Yapısının Oluşturulması



Tarih: 31 Temmuz 2026



&#x20;Günün Amacı



Bugün OpenAPI dokümantasyonunu kontrol eden testlerde tekrar kullanılan işlemleri ortak bir pytest fixture yapısına taşımak amaçlandı.



Bu düzenleme ile /openapi.json endpointine yapılan tekrar eden isteklerin azaltılması ve test dosyasının daha düzenli hâle getirilmesi hedeflendi.



&#x20;Yapılan Çalışmalar



İlk olarak tests/test\_api.py dosyası açıldı ve OpenAPI dokümantasyonunu kontrol eden testler incelendi.



Aşağıdaki iki testin aynı işlemleri tekrar gerçekleştirdiği görüldü:



\- test\_openapi\_contains\_error\_response\_schema

\- test\_openapi\_contains\_custom\_422\_examples



Her iki testte de aşağıdaki işlemler ayrı ayrı yapılıyordu:



\- /openapi.json endpointine GET isteği gönderilmesi

\- HTTP durum kodunun 200 olduğunun kontrol edilmesi

\- Response verisinin JSON formatına dönüştürülmesi



Bu tekrarları kaldırmak için yeni bir pytest fixture oluşturuldu:



openapi\_schema



Fixture içinde /openapi.json endpointine istek gönderildi.



Response durum kodunun 200 olduğu doğrulandı ve oluşturulan OpenAPI şeması JSON verisi olarak testlere geri döndürüldü.



&#x20;OpenAPI Testlerinin Düzenlenmesi



test\_openapi\_contains\_error\_response\_schema fonksiyonuna aşağıdaki fixture parametresi eklendi:



openapi\_schema: dict\[str, Any]



Testin içindeki tekrar eden HTTP isteği ve JSON dönüştürme kodları kaldırıldı.



Aynı düzenleme aşağıdaki test için de uygulandı:



test\_openapi\_contains\_custom\_422\_examples



Böylece iki OpenAPI testi de ortak openapi\_schema fixture yapısını kullanmaya başladı.



&#x20;Karşılaşılan Durum



Fixture ilk eklendiğinde yanlışlıkla `test\_root\_endpoint` fonksiyonunun başlangıcından sonra yerleştirildi.



Bu nedenle ana endpoint testinin bazı satırları fixture içinde kalmış gibi görünüyordu.



Kod kontrol edilerek `openapi\_schema` fixture yapısı `test\_root\_endpoint` fonksiyonundan önceki doğru konuma taşındı.



Daha sonra ana endpoint testinin kodları ve girintileri tekrar kontrol edildi.



&#x20;Dosya Kontrolü



Değişikliklerden sonra test dosyasının Python yazım kurallarına uygunluğu kontrol edildi.



Kullanılan komut:



.\\.venv\\Scripts\\python.exe -m py\_compile tests\\test\_api.py



Komut herhangi bir hata mesajı vermeden tamamlandı.



Böylece tests/test\_api.py dosyasında syntax hatası bulunmadığı doğrulandı.



&#x20;Otomatik Testler



Tüm API testleri yeniden çalıştırıldı.



Kullanılan komut:



.\\.venv\\Scripts\\python.exe -m pytest tests\\test\_api.py -v



Test sonucu:



11 passed, 1 warning in 19.37s



Toplam on bir testin tamamı başarıyla geçti.



Warning mesajı testlerin çalışmasını veya sonuçlarını etkilemedi.



&#x20;Gün Sonu Sonucu



OpenAPI şemasını hazırlayan ortak openapi\_schema fixture yapısı oluşturuldu.



İki farklı testte tekrar edilen /openapi.json isteği ve response dönüştürme kodları kaldırıldı.



Test dosyasındaki kod tekrarı azaltıldı ve testlerin okunabilirliği geliştirildi.



Yapılan düzenlemelerin mevcut API davranışlarını bozmadığı otomatik testlerle doğrulandı.



&#x20;Sonraki Gün İçin Plan



\- NLI model değerlendirme dosyalarını incelemek

\- Validation verisi üzerinde model performansını ölçmek

\- Accuracy, precision, recall ve F1-score sonuçlarını kaydetmek

\- Model hata analizine başlamak

