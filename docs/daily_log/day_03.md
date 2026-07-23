&#x20;3. Gün – API Otomatik Testlerinin Hazırlanması



Tarih: 24 Temmuz 2026



&#x20;Günün Amacı



Bugün FastAPI backend için otomatik testler hazırlamak ve API’nin doğru ve hatalı isteklerde nasıl çalıştığını kontrol etmek amaçlandı.



&#x20;Yapılan Çalışmalar



İlk olarak proje ortamında =pytest= kütüphanesinin kurulu olup olmadığı kontrol edildi. Genel Python ortamında pytest bulunamadı. Daha sonra sanal ortamın Python dosyası kullanıldı ve pytest sürümünün `8.4.2` olduğu görüldü.



API testleri için aşağıdaki dosya oluşturuldu:



tests/test\_api.py



Testlerde FastAPI =TestClient= kullanıldı. Gerçek NLI modelinin her testte yüklenmesini önlemek için sabit bir sonuç döndüren sahte model servisi hazırlandı.



Aşağıdaki durumlar test edildi:



\- GET / endpointinin çalışması

\- GET /health endpointinin çalışması

\- Geçerli bir POST /predict isteği

\- Boş premise gönderilmesi

\- Boş hypothesis gönderilmesi

\- Eksik premise gönderilmesi

\- Eksik hypothesis gönderilmesi

\- Geçersiz JSON gönderilmesi



İlk çalıştırmada altı test hazırlandı ve aşağıdaki sonuç alındı:



6 passed, 1 warning in 14.52s



Daha sonra eksik premise ve geçersiz JSON testleri eklendi. Testler tekrar çalıştırıldı ve sonuç şu şekilde oldu:



8 passed, 1 warning in 9.56s



Sekiz testin tamamı başarıyla geçti. Görünen warning mesajının test sonuçlarını etkilemediği görüldü.



&#x20;Karşılaşılan Sorun



PowerShell açıldığında sanal ortam aktif olmadığı için ilk komut genel Python ile çalıştı ve pytest bulunamadı. Sorun, sanal ortamdaki Python dosyasının doğrudan kullanılmasıyla çözüldü.



&#x20;Gün Sonu Sonucu



Backend API için temel otomatik test altyapısı oluşturuldu. Başarılı tahmin istekleri ile boş, eksik ve hatalı girişler kontrol edildi. API’nin bu durumlarda beklenen HTTP yanıtlarını verdiği doğrulandı.



&#x20;Sonraki Gün İçin Plan



\- Request ve response şemalarını düzenlemek

\- Swagger açıklamalarını geliştirmek

\- Mevcut testleri yeni yapılara göre güncellemek

