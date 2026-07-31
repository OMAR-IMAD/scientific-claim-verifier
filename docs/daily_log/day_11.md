11\. Gün – NLI Model Değerlendirme Sonuçlarının İncelenmesi



Tarih: 1 Ağustos 2026



&#x20;Günün Amacı



Bugün geliştirilmiş NLI modelinin resmi validation veri setlerindeki performans sonuçlarını incelemek amaçlandı.



Modelin genel başarı metrikleri, sınıf bazlı sonuçları, confusion matrix değerleri ve genre bazlı performansı analiz edildi.



Değerlendirme Dosyalarının İncelenmesi



İlk olarak proje içindeki değerlendirme dosyaları arandı.



Aşağıdaki önemli dosyalar bulundu:



\- reports/full\_evaluation\_results.json

\- reports/full\_evaluation\_summary.txt

\- src/model/evaluate\_full.py



reports/full\_evaluation\_summary.txt dosyası PowerShell üzerinden açılarak mevcut değerlendirme sonuçları incelendi.



&#x20;Kullanılan Model ve Veriler



Değerlendirme kodu incelendiğinde kullanılan model dizininin aşağıdaki konum olduğu görüldü:



models/improved\_test/final\_model



Modelin config.json dosyası kontrol edildi.



Model tipi:



RoBERTa



Sınıf eşlemesi:



\- 0 = ENTAILMENT

\- 1 = NEUTRAL

\- 2 = CONTRADICTION



Değerlendirmede kullanılan resmi MultiNLI validation dosyaları:



\- data/raw/multinli\_validation\_matched.csv

\- data/raw/multinli\_validation\_mismatched.csv



Değerlendirme ayarları:



\- Batch Size: 32

\- Maximum Sequence Length: 128

\- Sınıf Sayısı: 3



&#x20;Genel Performans Sonuçları



&#x20;Validation Matched



Toplam örnek sayısı:



9815



Elde edilen sonuçlar:



\- Accuracy: 74.58%

\- Macro Precision: 74.38%

\- Macro Recall: 74.38%

\- Macro F1-score: 74.37%



&#x20;Validation Mismatched



Toplam örnek sayısı:



9832



Elde edilen sonuçlar:



\- Accuracy: 75.54%

\- Macro Precision: 75.39%

\- Macro Recall: 75.34%

\- Macro F1-score: 75.34%



validation\_mismatched veri setinde accuracy ve Macro F1-score değerlerinin küçük bir farkla daha yüksek olduğu görüldü.



&#x20;Validation Matched Sınıf Sonuçları



ENTAILMENT



\- Precision: 78.33%

\- Recall: 79.88%

\- F1-score: 79.09%

\- Support: 3479



&#x20;NEUTRAL



\- Precision: 71.21%

\- Recall: 68.81%

\- F1-score: 69.99%

\- Support: 3123



&#x20;CONTRADICTION



\- Precision: 73.62%

\- Recall: 74.45%

\- F1-score: 74.03%

\- Support: 3213



Bu veri setinde en başarılı sınıf ENTAILMENT, en düşük performansa sahip sınıf ise NEUTRAL olmuştur.



&#x20;Validation Mismatched Sınıf Sonuçları



&#x20;ENTAILMENT



\- Precision: 78.25%

\- Recall: 81.66%

\- F1-score: 79.92%

\- Support: 3463



&#x20;NEUTRAL



\- Precision: 70.68%

\- Recall: 70.12%

\- F1-score: 70.40%

\- Support: 3129



&#x20;CONTRADICTION



\- Precision: 77.23%

\- Recall: 74.23%

\- F1-score: 75.70%

\- Support: 3240



Bu veri setinde de en başarılı sınıf ENTAILMENT, en düşük performansa sahip sınıf ise NEUTRAL olmuştur.



&#x20;Confusion Matrix Analizi



&#x20;Validation Matched



Confusion matrix değerleri:



| Gerçek Sınıf | Predicted ENTAILMENT | Predicted NEUTRAL | Predicted CONTRADICTION |

|---|---:|---:|---:|

| ENTAILMENT | 2779 | 430 | 270 |

| NEUTRAL | 387 | 2149 | 587 |

| CONTRADICTION | 382 | 439 | 2392 |



Bu veri setindeki en yüksek yanlış sınıflandırma:



NEUTRAL → CONTRADICTION: 587



Validation Mismatched



Confusion matrix değerleri:



| Gerçek Sınıf | Predicted ENTAILMENT | Predicted NEUTRAL | Predicted CONTRADICTION |

|---|---:|---:|---:|

| ENTAILMENT | 2828 | 417 | 218 |

| NEUTRAL | 444 | 2194 | 491 |

| CONTRADICTION | 342 | 493 | 2405 |



Bu veri setindeki en yüksek yanlış sınıflandırma:



CONTRADICTION → NEUTRAL: 493



Buna çok yakın olan diğer hata:



NEUTRAL → CONTRADICTION: 491



&#x20;Genre Bazlı Sonuçlar



Validation matched veri setinde en yüksek başarı government türünde elde edildi:



\- Accuracy: 79.74%

\- F1-score: 79.39%



En düşük sonuç slate türünde görüldü:



\- Accuracy: 70.59%

\- F1-score: 70.49%



Validation mismatched veri setinde en yüksek başarı letters türünde elde edildi:



\- Accuracy: 78.55%

\- F1-score: 78.17%



En düşük F1-score değeri facetoface türünde görüldü:



\- Accuracy: 73.61%

\- F1-score: 73.39%



&#x20;Teknik Analiz Dosyasının Oluşturulması



İncelenen tüm sonuçları düzenli biçimde belgelemek için aşağıdaki dosya oluşturuldu:



reports/model\_evaluation\_analysis.md



Bu dosyaya aşağıdaki bilgiler eklendi:



\- Kullanılan model ve validation verileri

\- Genel performans metrikleri

\- Sınıf bazlı Precision, Recall ve F1-score değerleri

\- Confusion matrix analizi

\- Genre bazlı sonuçlar

\- Modelin güçlü ve zayıf yönleri

\- Gelecek iyileştirme önerileri



&#x20;Gün Sonu Sonucu



Geliştirilmiş RoBERTa tabanlı NLI modelinin iki resmi validation veri setindeki sonuçları ayrıntılı olarak incelendi.



Modelin genel accuracy ve Macro F1-score değerlerinin yaklaşık %75` seviyesinde olduğu görüldü.



Her iki veri setinde de en güçlü sınıfın ENTAILMENT, en zayıf sınıfın ise NEUTRAL olduğu belirlendi.



Modelin temel hata alanının NEUTRAL ve CONTRADICTION sınıfları arasındaki karışıklık olduğu tespit edildi.



Tüm sonuçlar bağımsız bir teknik analiz dosyasında belgelendi.



Sonraki Gün İçin Plan



\- Yanlış tahmin edilen örnekleri veri setinden çıkarmak

\- NEUTRAL ve CONTRADICTION hatalarını metin bazlı incelemek

\- En sık görülen hata türlerini sınıflandırmak

\- Model hata analizi raporu hazırlamak

