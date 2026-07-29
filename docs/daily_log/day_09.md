&#x20;9. Gün – Model Servisi Fixture Yapısının Oluşturulması



Tarih: 30 Temmuz 2026



&#x20;Günün Amacı



Bugün API testlerinde tekrar edilen model servisi hazırlama işlemlerini ortak bir pytest fixture yapısına taşımak amaçlandı.



Bu düzenleme ile test kodundaki monkeypatch tekrarlarının azaltılması ve testlerin daha okunabilir hâle getirilmesi hedeflendi.



&#x20;Yapılan Çalışmalar



İlk olarak tests/test\_api.py dosyası açıldı ve model servisini kullanan testler incelendi.



Aşağıdaki testlerin aynı monkeypatch.setattr kodunu tekrar kullandığı görüldü:



\- test\_predict\_endpoint

\- test\_prediction\_response\_structure



Bu tekrarı ortadan kaldırmak için yeni bir pytest fixture oluşturuldu:



mock\_model\_service



Fixture içinde FakeModelService sınıfından ortak bir sahte model servisi oluşturuldu.



Daha sonra monkeypatch.setattr kullanılarak gerçek get\_model\_service fonksiyonunun test sırasında bu sahte servisi döndürmesi sağlandı.



Fixture yapısı test tamamlandıktan sonra sahte model servisini geri döndürecek şekilde hazırlandı.



&#x20;Testlerin Düzenlenmesi



test\_predict\_endpoint testindeki doğrudan monkeypatch kodu kaldırıldı.



Test fonksiyonuna aşağıdaki fixture eklendi:



mock\_model\_service: FakeModelService



Aynı düzenleme test\_prediction\_response\_structure testi için de uygulandı.



Böylece iki testte tekrar edilen aşağıdaki yapı kaldırıldı:



monkeypatch.setattr



Model servisi hazırlama işlemi artık tek bir ortak fixture üzerinden gerçekleştirilmektedir.



&#x20;Karşılaşılan Durum



test\_predict\_endpoint düzenlenirken response = client.post(...) bloğunun girintisi yanlışlıkla fazla bırakıldı.



Kod kontrol edilerek blok bir seviye sola taşındı ve fonksiyon içindeki diğer komutlarla aynı hizaya getirildi.



Daha sonra her iki testin fonksiyon parametreleri ve girintileri tekrar kontrol edildi.



Dosya Kontrolü



Değişikliklerden sonra test dosyasının Python yazım kurallarına uygunluğu kontrol edildi.



Kullanılan komut:



.\\.venv\\Scripts\\python.exe -m py\_compile tests\\test\_api.py



Komut herhangi bir hata mesajı vermeden tamamlandı.



Böylece tests/test\_api.py dosyasında syntax hatası bulunmadığı doğrulandı.



\## Otomatik Testler



Tüm API testleri yeniden çalıştırıldı.



Kullanılan komut:



.\\.venv\\Scripts\\python.exe -m pytest tests\\test\_api.py -v



Test sonucu:



11 passed, 1 warning in 48.01s



Toplam on bir testin tamamı başarıyla geçti.



Warning mesajı testlerin çalışmasını veya sonuçlarını etkilemedi.



Gün Sonu Sonucu



Model servisini hazırlayan ortak mock\_model\_service fixture yapısı oluşturuldu.



İki farklı testte tekrar edilen monkeypatch kodları kaldırıldı.



Testlerin okunabilirliği ve bakım kolaylığı geliştirildi. Yapılan düzenlemenin mevcut API davranışlarını bozmadığı otomatik testlerle doğrulandı.



&#x20;Sonraki Gün İçin Plan



\- OpenAPI verileri için ortak fixture oluşturmak

\- Tekrar kullanılan response verilerini ortak yapıya taşımak

\- Test dosyasının düzenini geliştirmeye devam etmek

