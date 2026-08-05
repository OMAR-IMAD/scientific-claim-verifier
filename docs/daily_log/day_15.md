&#x20;15. Gün – Model Confidence Değerlerinin İncelenmesi



Tarih: 5 Ağustos 2026



&#x20;Yapılan Çalışmalar



Bugün modelin tahminleriyle birlikte confidence değerlerini hesaplamak için `evaluate\_full.py` dosyasında düzenlemeler yapıldı.



Model çıktısındaki logits değerlerine softmax uygulandı. Daha sonra her tahmin için en yüksek olasılık confidence değeri olarak alındı.



`predict\_dataframe` fonksiyonu artık tahmin sınıflarıyla birlikte confidence değerlerini de döndürüyor.



Yanlış tahminlerin kaydedildiği CSV dosyalarına `confidence` sütunu eklendi.



Değerlendirme sonuçlarına şu bilgiler de eklendi:



\- Genel confidence ortalaması

\- Doğru tahminlerin confidence ortalaması

\- Yanlış tahminlerin confidence ortalaması

\- 0.60 altında kalan tahmin sayısı

\- Kullanılan confidence sınırı



\## Kontroller



Kod düzenlemeleri sırasında bazı girinti hataları oluştu. Hatalı satırlar kontrol edilerek düzeltildi.



Dosyanın syntax kontrolü tekrar yapıldı ve hata alınmadı.



Daha sonra projenin bütün testleri çalıştırıldı:



powershell

.\\.venv\\Scripts\\python.exe -m pytest -v



Test sonucu:



21 passed, 1 warning in 47.97s



Değerlendirme Sonuçları



Model iki validation veri seti üzerinde tekrar çalıştırıldı.



Validation Matched

Accuracy: %74.58

Macro F1: %74.37

Ortalama confidence: 0.8337

Doğru tahmin ortalaması: 0.8704

Yanlış tahmin ortalaması: 0.7261

0.60 altında kalan tahmin sayısı: 1289

Toplam yanlış tahmin: 2495

0.90 ve üzeri confidence ile yapılan yanlış tahmin: 554



Validation Mismatched

Accuracy: %75.54

Macro F1: %75.34

Ortalama confidence: 0.8390

Doğru tahmin ortalaması: 0.8747

Yanlış tahmin ortalaması: 0.7286

0.60 altında kalan tahmin sayısı: 1251

Toplam yanlış tahmin: 2405

0.90 ve üzeri confidence ile yapılan yanlış tahmin: 557

Gün Sonu Sonucu



Doğru tahminlerin confidence ortalamasının yanlış tahminlerden daha yüksek olduğu görüldü.



Bununla birlikte bazı yanlış tahminlerin confidence değerinin 0.99 seviyesine yaklaştığı tespit edildi. Bu nedenle yüksek confidence değerinin her zaman doğru sonuç anlamına gelmediği görüldü.



Analiz sonuçları aşağıdaki dosyada kaydedildi:



reports/error\_analysis/model\_confidence\_analysis.md



Sonraki Gün İçin Plan

Model deneylerini karşılaştırmak

Elde edilen sonuçları tek tabloda toplamak

En başarılı model ayarlarını belirlemek

Model geliştirme aşamasının genel sonucunu hazırlamak

