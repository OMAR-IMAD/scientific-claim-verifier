7\. Gün – OpenAPI Hata Şemalarının Otomatik Testleri



Tarih: 28 Temmuz 2026



&#x20;Günün Amacı



Bugün Swagger ve OpenAPI dokümantasyonunda bulunan özel 422 hata örneklerini otomatik testlerle kontrol etmek amaçlandı.



&#x20;Yapılan Çalışmalar



tests/test\_api.py dosyasına OpenAPI dokümantasyonunu kontrol eden yeni testler eklendi.



İlk testte /openapi.json endpointi üzerinden POST /predict işleminin `422` hata yanıtı incelendi.



Aşağıdaki hata örneklerinin OpenAPI içinde bulunduğu doğrulandı:



\- empty\_premise

\- empty\_hypothesis



Bu örneklerdeki mesajlar kontrol edildi:



\- Premise cannot be empty.

\- Hypothesis cannot be empty.



Daha sonra ErrorResponse modelinin OpenAPI şeması için ayrı bir test eklendi.



Bu testte aşağıdaki özellikler doğrulandı:



\- Şema türünün `object` olması

\- detail alanının zorunlu olması

\- detail alanının veri türünün string olması

\- Alan açıklamasının doğru görüntülenmesi



&#x20;Karşılaşılan Durum



İkinci test eklendikten sonra test sayısının on olduğu görüldü. Önceden eklenen özel 422 örnek testi dosyada bulunmuyordu.



Dosya kontrol edildi ve eksik test yeniden eklendi. Böylece iki OpenAPI testi de aynı dosyada korundu.



&#x20;Test Sonucu



Tüm API testleri tekrar çalıştırıldı.



Kullanılan komut:



.\\.venv\\Scripts\\python.exe -m pytest tests\\test\_api.py -v



Sonuç:



11 passed, 1 warning in 10.67s



Toplam on bir testin tamamı başarıyla geçti. Warning mesajı test sonuçlarını etkilemedi.



Başarılı olan yeni testler:



\- test\_openapi\_contains\_error\_response\_schema

\- test\_openapi\_contains\_custom\_422\_examples



&#x20;Gün Sonu Sonucu



ErrorResponse şeması ve özel 422 hata örnekleri otomatik testlerle kontrol altına alındı.



Swagger dokümantasyonunda yapılabilecek gelecekteki değişikliklerin hata şemalarını veya örneklerini bozması durumunda testlerin bunu tespit edebilmesi sağlandı.



&#x20;Sonraki Gün İçin Plan



\- API testlerini daha düzenli gruplandırmak

\- Testlerde tekrar kullanılan verileri ortak yapıya taşımak

\- Backend test altyapısını geliştirmeye devam etmek

