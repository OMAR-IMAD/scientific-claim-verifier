&#x20;8. Gün – API Testlerinde Ortak Veri Yapısının Oluşturulması



Tarih: 29 Temmuz 2026



&#x20;Günün Amacı



Bugün API testlerinde tekrar kullanılan verileri ortak bir yapıya taşımak ve test dosyasını daha düzenli hâle getirmek amaçlandı.



&#x20;Yapılan Çalışmalar



İlk olarak tests/test\_api.py dosyası incelendi.



Başarılı prediction testlerinde aynı premise ve hypothesis bilgilerinin birden fazla kez kullanıldığı görüldü.



Fixture desteğini kullanabilmek için dosyaya aşağıdaki import eklendi:



import pytest



Daha sonra tekrar kullanılan geçerli prediction verileri için yeni bir pytest fixture oluşturuldu:



valid\_prediction\_payload



Fixture aşağıdaki iki alanı içermektedir:



\- premise

\- hypothesis



Ortak veri yapısı aşağıdaki testlerde kullanılmaya başlandı:



\- test\_predict\_endpoint

\- test\_prediction\_response\_structure



Bu testlerde bulunan tekrar eden JSON verileri kaldırıldı ve yerine aşağıdaki kullanım eklendi:



json=valid\_prediction\_payload



&#x20;Karşılaşılan Durum



Fixture eklenirken FakeModelService sınıfının sonunda device alanı yanlışlıkla ikinci kez eklendi.



Dosya kontrol edildi ve tekrar eden bölüm kaldırıldı. device alanının yalnızca model sonucunun içindeki doğru konumda kalması sağlandı.



&#x20;Dosya Kontrolü



Değişikliklerden sonra test dosyasının Python yazım kurallarına uygunluğu kontrol edildi.



Kullanılan komut:



.\\.venv\\Scripts\\python.exe -m py\_compile tests\\test\_api.py



Komut sonrasında herhangi bir hata mesajı görülmedi. Böylece dosyada syntax hatası bulunmadığı doğrulandı.



&#x20;Otomatik Testler



Tüm API testleri tekrar çalıştırıldı.



Kullanılan komut:



.\\.venv\\Scripts\\python.exe -m pytest tests\\test\_api.py -v



Test sonucu:



11 passed, 1 warning in 52.03s



Toplam on bir testin tamamı başarıyla geçti. Warning mesajı test sonuçlarını etkilemedi.



&#x20;Gün Sonu Sonucu



API testlerinde tekrar kullanılan geçerli request verileri ortak bir pytest fixture yapısına taşındı.



Test kodundaki tekrar azaltıldı ve testlerin okunabilirliği geliştirildi. Yapılan düzenlemelerin mevcut test davranışlarını bozmadığı doğrulandı.



&#x20;Sonraki Gün İçin Plan



\- Model servisi için ortak fixture oluşturmak

\- Monkeypatch tekrarlarını azaltmak

\- Test dosyasının düzenini geliştirmeye devam etmek

