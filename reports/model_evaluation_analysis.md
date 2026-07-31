&#x20;NLI Model Değerlendirme Analizi



Analiz Tarihi: 1 Ağustos 2026



1\. Değerlendirmenin Amacı



Bu çalışmanın amacı, geliştirilen NLI modelinin resmi validation veri setleri üzerindeki performansını incelemektir.



Model; premise ve hypothesis arasındaki ilişkiyi aşağıdaki üç sınıftan biri olarak tahmin etmektedir:



\- `ENTAILMENT`

\- `NEUTRAL`

\- `CONTRADICTION`



Değerlendirme sırasında genel başarı metrikleri, sınıf bazlı sonuçlar, confusion matrix değerleri ve veri türlerine göre performans sonuçları incelenmiştir.



&#x20;2. Kullanılan Model



Değerlendirilen model dizini:



`models/improved\_test/final\_model`



Model tipi:



`RoBERTa`



Model sınıf eşlemesi:



| Label ID | Sınıf |

|---|---|

| 0 | ENTAILMENT |

| 1 | NEUTRAL |

| 2 | CONTRADICTION |



&#x20;3. Kullanılan Validation Verileri



Değerlendirmede aşağıdaki resmi MultiNLI validation dosyaları kullanılmıştır:



\- `data/raw/multinli\_validation\_matched.csv`

\- `data/raw/multinli\_validation\_mismatched.csv`



`validation\_matched`, eğitim verileriyle benzer genre türlerinden oluşmaktadır.



`validation\_mismatched` ise eğitim verilerinde bulunmayan veya farklı genre türlerinden oluşmaktadır.



&#x20;4. Değerlendirme Ayarları



Değerlendirme dosyası:



`src/model/evaluate\_full.py`



Kullanılan temel ayarlar:



| Ayar | Değer |

|---|---:|

| Batch Size | 32 |

| Maximum Sequence Length | 128 |

| Sınıf Sayısı | 3 |



Değerlendirme sonuçları aşağıdaki dosyalardan incelenmiştir:



\- `reports/full\_evaluation\_results.json`

\- `reports/full\_evaluation\_summary.txt`



5\. Genel Performans Sonuçları



&#x20;5.1 Validation Matched



Toplam örnek sayısı:



`9815`



| Metrik | Sonuç |

|---|---:|

| Accuracy | 74.58% |

| Macro Precision | 74.38% |

| Macro Recall | 74.38% |

| Macro F1-score | 74.37% |



\### 5.2 Validation Mismatched



Toplam örnek sayısı:



`9832`



| Metrik | Sonuç |

|---|---:|

| Accuracy | 75.54% |

| Macro Precision | 75.39% |

| Macro Recall | 75.34% |

| Macro F1-score | 75.34% |



&#x20;6. Genel Sonuçların Karşılaştırılması



`validation\_mismatched` veri setinde elde edilen accuracy değeri, `validation\_matched` veri setinden `0.96` puan daha yüksektir.



Macro F1-score açısından fark:



`75.34% - 74.37% = 0.97%`



Model, farklı genre türlerinden oluşan mismatched veri setinde küçük bir farkla daha başarılı sonuç vermiştir.



İki veri setindeki sonuçların birbirine yakın olması, modelin farklı metin türlerine karşı genel olarak dengeli bir performans gösterdiğini düşündürmektedir.



7\. Sınıf Bazlı Sonuçlar



&#x20;7.1 Validation Matched Sınıf Sonuçları



| Sınıf | Precision | Recall | F1-score | Support |

|---|---:|---:|---:|---:|

| ENTAILMENT | 78.33% | 79.88% | 79.09% | 3479 |

| NEUTRAL | 71.21% | 68.81% | 69.99% | 3123 |

| CONTRADICTION | 73.62% | 74.45% | 74.03% | 3213 |



Bu veri setinde en yüksek F1-score değeri `ENTAILMENT` sınıfında elde edilmiştir.



En düşük F1-score değeri ise `NEUTRAL` sınıfında görülmüştür.



&#x20;7.2 Validation Mismatched Sınıf Sonuçları



| Sınıf | Precision | Recall | F1-score | Support |

|---|---:|---:|---:|---:|

| ENTAILMENT | 78.25% | 81.66% | 79.92% | 3463 |

| NEUTRAL | 70.68% | 70.12% | 70.40% | 3129 |

| CONTRADICTION | 77.23% | 74.23% | 75.70% | 3240 |



Bu veri setinde de en güçlü sınıf `ENTAILMENT` olmuştur.



En düşük F1-score yeniden `NEUTRAL` sınıfında görülmüştür.



&#x20;8. Confusion Matrix Analizi



Confusion matrix satırları gerçek sınıfları, sütunları ise model tarafından tahmin edilen sınıfları göstermektedir.



Sınıf sırası:



1\. ENTAILMENT

2\. NEUTRAL

3\. CONTRADICTION



&#x20;8.1 Validation Matched Confusion Matrix



| Gerçek Sınıf | Predicted ENTAILMENT | Predicted NEUTRAL | Predicted CONTRADICTION |

|---|---:|---:|---:|

| ENTAILMENT | 2779 | 430 | 270 |

| NEUTRAL | 387 | 2149 | 587 |

| CONTRADICTION | 382 | 439 | 2392 |



Bu veri setindeki en yüksek yanlış sınıflandırma:



`NEUTRAL → CONTRADICTION: 587`



Diğer önemli yanlış sınıflandırmalar:



\- `CONTRADICTION → NEUTRAL: 439`

\- `ENTAILMENT → NEUTRAL: 430`

\- `NEUTRAL → ENTAILMENT: 387`

\- `CONTRADICTION → ENTAILMENT: 382`



&#x20;8.2 Validation Mismatched Confusion Matrix



| Gerçek Sınıf | Predicted ENTAILMENT | Predicted NEUTRAL | Predicted CONTRADICTION |

|---|---:|---:|---:|

| ENTAILMENT | 2828 | 417 | 218 |

| NEUTRAL | 444 | 2194 | 491 |

| CONTRADICTION | 342 | 493 | 2405 |



Bu veri setindeki en yüksek yanlış sınıflandırma:



`CONTRADICTION → NEUTRAL: 493`



Buna çok yakın olan diğer hata:



`NEUTRAL → CONTRADICTION: 491`



&#x20;9. Sınıfların Performans Yorumu



&#x20;ENTAILMENT



`ENTAILMENT`, iki validation veri setinde de en yüksek F1-score değerine sahip sınıftır.



Model, doğrudan desteklenen premise-hypothesis ilişkilerini diğer sınıflara göre daha başarılı ayırt etmektedir.



&#x20;NEUTRAL



`NEUTRAL`, her iki veri setinde de en düşük F1-score değerine sahip sınıftır.



Model özellikle `NEUTRAL` ve `CONTRADICTION` sınıflarını birbirinden ayırırken daha fazla hata yapmaktadır.



Neutral bir hypothesis, premise tarafından açıkça desteklenmediğinde veya çürütülmediğinde bu sınıfa ait olmalıdır. Ancak bazı örneklerde model, destek bulunmamasını doğrudan contradiction olarak değerlendirebilmektedir.



&#x20;CONTRADICTION



`CONTRADICTION` sınıfı, `ENTAILMENT` sınıfından daha düşük ancak `NEUTRAL` sınıfından daha yüksek bir performans göstermiştir.



En önemli hata türlerinden biri contradiction örneklerinin neutral olarak tahmin edilmesidir.



&#x20;10. Genre Bazlı Sonuçlar



&#x20;Validation Matched



| Genre | Satır Sayısı | Accuracy | F1-score |

|---|---:|---:|---:|

| fiction | 1973 | 73.14% | 72.93% |

| government | 1945 | 79.74% | 79.39% |

| slate | 1955 | 70.59% | 70.49% |

| telephone | 1966 | 74.47% | 74.35% |

| travel | 1976 | 75.00% | 74.76% |



En yüksek başarı `government` türünde elde edilmiştir.



En düşük başarı `slate` türünde görülmüştür.



&#x20;Validation Mismatched



| Genre | Satır Sayısı | Accuracy | F1-score |

|---|---:|---:|---:|

| facetoface | 1974 | 73.61% | 73.39% |

| letters | 1977 | 78.55% | 78.17% |

| nineeleven | 1974 | 75.53% | 75.16% |

| oup | 1961 | 76.54% | 76.41% |

| verbatim | 1946 | 73.43% | 73.40% |



En yüksek başarı `letters` türünde elde edilmiştir.



En düşük F1-score değeri `facetoface` türünde görülmüştür.



&#x20;11. Temel Bulgular



\- Modelin genel accuracy değeri yaklaşık `%75` seviyesindedir.

\- İki validation veri setindeki sonuçlar birbirine yakındır.

\- En başarılı sınıf `ENTAILMENT` sınıfıdır.

\- En zayıf sınıf `NEUTRAL` sınıfıdır.

\- En fazla karışıklık `NEUTRAL` ve `CONTRADICTION` sınıfları arasında oluşmaktadır.

\- Genre türü model performansını etkilemektedir.

\- `government` ve `letters` türlerinde daha yüksek sonuçlar elde edilmiştir.

\- `slate`, `facetoface` ve `verbatim` türlerinde daha düşük sonuçlar görülmüştür.



&#x20;12. İyileştirme Önerileri



Model performansını geliştirmek için aşağıdaki çalışmalar yapılabilir:



\- NEUTRAL ve CONTRADICTION örneklerinin hata analizini gerçekleştirmek

\- Yanlış tahmin edilen örnekleri ayrı bir raporda toplamak

\- Sınıf dağılımını ve zor örnekleri incelemek

\- Daha uzun sequence length değerlerini test etmek

\- Learning rate ve batch size ayarlarını karşılaştırmak

\- Neutral sınıfına ait daha zor örneklerle ek eğitim yapmak

\- Genre bazlı performans farklarını ayrıntılı incelemek

\- Confidence score değerleri düşük olan tahminleri analiz etmek



13\. Sonuç



RoBERTa tabanlı geliştirilmiş NLI modeli, resmi validation veri setlerinde yaklaşık `%75` accuracy ve Macro F1-score elde etmiştir.



Model, `ENTAILMENT` ilişkilerini güçlü şekilde ayırt edebilmiştir.



Bununla birlikte `NEUTRAL` ve `CONTRADICTION` sınıflarının birbirinden ayrılması modelin temel geliştirme alanı olarak belirlenmiştir.



Sonraki çalışmalarda yanlış tahmin edilen örneklerin metin bazlı hata analizi yapılacaktır.

