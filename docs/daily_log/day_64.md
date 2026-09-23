\# Day 64



Bugün projeye TXT ve PDF dosya yükleme özelliği eklendi.



Backend tarafında FastAPI UploadFile ve File kullanılarak yeni /upload endpointi oluşturuldu.



Dosya yükleme işlemi JWT authentication ile korundu.



Sadece .txt ve .pdf dosyalarının yüklenmesine izin verildi.



Dosya boyutu için maksimum 5 MB sınırı eklendi.



TXT dosyalarının UTF-8 metin içeriğinin okunması sağlandı.



UTF-8 BOM problemi utf-8-sig kullanılarak düzeltildi.



PDF dosyalarındaki metinlerin okunması için pypdf kütüphanesi kullanıldı.



FileUploadResponse modeli schemas.py dosyasına eklendi.



requirements.txt dosyasına pypdf paketi eklendi.



Frontend API servisine uploadFile fonksiyonu eklendi.



Premise ve Hypothesis alanları için ayrı TXT/PDF yükleme seçenekleri oluşturuldu.



Yüklenen dosyadan çıkarılan metnin ilgili textarea alanına otomatik olarak aktarılması sağlandı.



Dosya yükleme alanları için yeni CSS stilleri eklendi.



TXT dosya yükleme işlemi PowerShell üzerinden test edildi ve başarılı oldu.



PDF dosya yükleme işlemi PowerShell üzerinden test edildi ve başarılı oldu.



Dosya yükleme işlemi web arayüzü üzerinden de test edildi.



Yüklenen PDF ve TXT içerikleri kullanılarak NLI tahmini başarıyla gerçekleştirildi.



Test sonucunda ENTAILMENT tahmini %95.84 confidence değeri ile elde edildi.



Yeni analiz Analysis History bölümüne başarıyla kaydedildi.



Frontend ESLint kontrolü başarılı şekilde tamamlandı.



Frontend production build testi başarılı şekilde tamamlandı.



Sonuç:

TXT ve PDF dosya yükleme desteği başarıyla tamamlandı.

Backend ve frontend entegrasyonu doğrulandı.

Dosyadan metin çıkarma ve NLI analiz akışı başarılı şekilde test edildi.



Sonraki Gün İçin Plan



Dosya yükleme özelliği için ek hata kontrolleri ve kullanıcı deneyimi geliştirmeleri yapmak.
