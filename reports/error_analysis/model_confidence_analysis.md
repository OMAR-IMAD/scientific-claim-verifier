&#x20;Model Confidence Analizi



Tarih: 5 Ağustos 2026



Bu çalışmada modelin tahminleriyle birlikte confidence değerleri de hesaplandı. Bunun için model çıktısındaki logits değerlerine softmax uygulandı ve en yüksek olasılık confidence değeri olarak kaydedildi.



Confidence değerleri yanlış tahmin CSV dosyalarına eklendi. Ayrıca genel ortalama, doğru tahmin ortalaması, yanlış tahmin ortalaması ve düşük confidence sayısı JSON raporuna kaydedildi.



&#x20;Validation Matched Sonuçları



\- Ortalama confidence: 0.8337

\- Doğru tahminlerin ortalaması: 0.8704

\- Yanlış tahminlerin ortalaması: 0.7261

\- 0.60 altında kalan tahmin sayısı: 1289

\- Toplam yanlış tahmin: 2495

\- 0.90 ve üzeri confidence ile yapılan yanlış tahmin: 554



&#x20;Validation Mismatched Sonuçları



\- Ortalama confidence: 0.8390

\- Doğru tahminlerin ortalaması: 0.8747

\- Yanlış tahminlerin ortalaması: 0.7286

\- 0.60 altında kalan tahmin sayısı: 1251

\- Toplam yanlış tahmin: 2405

\- 0.90 ve üzeri confidence ile yapılan yanlış tahmin: 557



&#x20;İnceleme



Sonuçlarda doğru tahminlerin confidence ortalamasının yanlış tahminlerden daha yüksek olduğu görüldü. Bu durum modelin doğru cevaplarda genel olarak daha emin olduğunu gösteriyor.



En düşük confidence değerine sahip yanlış tahminler yaklaşık 0.34 ile 0.36 arasındadır. Üç sınıflı bir problemde bu değerler modelin kararsız kaldığını göstermektedir.



Bazı yanlış tahminlerde confidence değerinin 0.99 seviyesine yaklaştığı da görüldü. Bu nedenle yüksek confidence değeri her zaman tahminin doğru olduğu anlamına gelmemektedir.



Özellikle matched veri setinde 554, mismatched veri setinde ise 557 yanlış tahminin confidence değeri 0.90 veya üzerindedir. Bu örneklerin daha sonra ayrı olarak incelenmesi faydalı olacaktır.



&#x20;Sonuç



Modelin confidence değerlerini hesaplayan sistem başarıyla çalıştı. Confidence bilgileri hem hata dosyalarına hem de değerlendirme raporuna eklendi.



Analiz sonucunda doğru tahminlerin daha yüksek confidence değerine sahip olduğu, ancak modelin bazı yanlış tahminlerde de oldukça emin davrandığı görüldü.

