&#x20;13. Gün – Hata Sonuçlarının Otomatik Özetlenmesi



Tarih: 3 Ağustos 2026



&#x20;Yapılan Çalışmalar



Bugün modelin yanlış tahmin sonuçlarını otomatik olarak özetlemek için yeni bir Python dosyası hazırlandı:



`src/model/summarize\_errors.py`



Çalışmaya başlamadan önce Git durumu kontrol edildi. Projede bekleyen bir değişiklik olmadığı görüldü.



Hazırlanan Python dosyası aşağıdaki hata dosyalarını okumaktadır:



\- `validation\_matched\_misclassified.csv`

\- `validation\_mismatched\_misclassified.csv`



Kod içerisinde şu işlemler yapıldı:



\- CSV dosyalarının varlığı kontrol edildi.

\- Gerekli sütunların bulunup bulunmadığı kontrol edildi.

\- Gerçek ve tahmin edilen sınıflar arasındaki hata geçişleri hesaplandı.

\- En sık görülen hata türü belirlendi.

\- Bu hatanın genre dağılımı çıkarıldı.

\- Her veri setinden üç örnek seçildi.

\- Sonuçlar Markdown dosyasına otomatik olarak yazdırıldı.



&#x20;Kod Kontrolü



Dosyanın syntax kontrolü aşağıdaki komutla yapıldı:



```powershell

.\\.venv\\Scripts\\python.exe -m py\_compile src\\model\\summarize\_errors.py



Herhangi bir hata alınmadı.



Daha sonra dosya çalıştırıldı:

.\\.venv\\Scripts\\python.exe src\\model\\summarize\_errors.py



Çalıştırma sonucunda aşağıdaki rapor oluşturuldu:



reports/error\_analysis/automatic\_error\_summary.md



Oluşturulan Rapor



Otomatik raporda her validation veri seti için şu bilgiler yer almaktadır:



Toplam yanlış tahmin sayısı

Sınıflar arasındaki hata geçişleri

En sık hata türü

Genre bazlı hata dağılımı

Temsilî yanlış tahmin örnekleri



İki validation veri setindeki toplam yanlış tahmin sayısı:



4900



İlk görüntülemede Türkçe karakterler PowerShell üzerinde bozuk göründü. Dosya UTF-8 olarak tekrar okunduğunda karakterlerin doğru olduğu görüldü.



Kullanılan komut:

Get-Content reports\\error\_analysis\\automatic\_error\_summary.md -Encoding UTF8



Raporun sonunda validation\_mismatched sonuçları, örnekler ve genel sonuç bölümünün bulunduğu kontrol edildi.



Gün Sonu Sonucu



Bugün hata analizini otomatik olarak hazırlayan Python dosyası tamamlandı.



Böylece hata geçişlerini, genre dağılımlarını ve örnekleri her defasında elle hesaplamak yerine tek komutla raporlamak mümkün hale geldi.



Sonraki Gün İçin Plan

Otomatik hata özetleme kodu için testler hazırlamak

Rapor içeriğini farklı durumlarda kontrol etmek

Modelin düşük güvenle yaptığı tahminleri incelemeye başlamak

