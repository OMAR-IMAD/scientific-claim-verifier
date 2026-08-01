&#x20;NLI Model Hata Analizi



Analiz Tarihi: 2 Ağustos 2026



&#x20;1. Çalışmanın Amacı



Bu çalışmanın amacı, geliştirilmiş RoBERTa tabanlı NLI modelinin yanlış sınıflandırdığı örnekleri çıkarmak ve temel hata türlerini incelemektir.



Analiz kapsamında aşağıdaki üç sınıf arasındaki yanlış tahminler değerlendirilmiştir:



\- ENTAILMENT

\- NEUTRAL

\- CONTRADICTION



Özellikle önceki değerlendirmede en fazla karışıklığın görüldüğü `NEUTRAL` ve `CONTRADICTION` sınıflarına odaklanılmıştır.



&#x20;2. Hata Çıkarma Sisteminin Eklenmesi



Model değerlendirme dosyası:



src/model/evaluate\_full.py



Değerlendirme koduna, yanlış tahmin edilen satırları otomatik olarak CSV dosyalarına kaydeden yeni bir yapı eklendi.



Her yanlış tahmin için aşağıdaki bilgiler kaydedilmektedir:



\- Premise metni

\- Hypothesis metni

\- Genre

\- Gerçek label ID

\- Gerçek sınıf adı

\- Tahmin edilen label ID

\- Tahmin edilen sınıf adı



Oluşturulan hata dosyaları:



\- reports/error\_analysis/validation\_matched\_misclassified.csv`

\- reports/error\_analysis/validation\_mismatched\_misclassified.csv`



&#x20;3. Dosya Kontrolü



Kod değişikliğinden sonra Python syntax kontrolü gerçekleştirildi.



Kullanılan komut:



powershell

.\\.venv\\Scripts\\python.exe -m py\_compile src\\model\\evaluate\_full.py



Komut herhangi bir hata mesajı vermeden tamamlandı.



Bu sonuç, değerlendirme dosyasında syntax hatası bulunmadığını doğrulamıştır.



4\. Değerlendirmenin Yeniden Çalıştırılması

Güncellenen değerlendirme kodu aşağıdaki komut ile çalıştırıldı:



.\\.venv\\Scripts\\python.exe src\\model\\evaluate\_full.py



Her iki resmi validation veri seti yeniden değerlendirildi ve yanlış sınıflandırılan örnekler CSV dosyalarına kaydedildi.



5\. Yanlış Tahmin Sayıları

Validation Matched



Toplam örnek sayısı:



9815



Yanlış tahmin edilen örnek sayısı:



2495



Yanlış tahmin edilen örnek sayısı:



2495



Yaklaşık hata oranı:



25.42%



Accuracy:



74.58%



Macro F1-score:



74.37%



Validation Mismatched



Toplam örnek sayısı:



9832



Yanlış tahmin edilen örnek sayısı:



2405



Yaklaşık hata oranı:



24.46%



Accuracy:



75.54%



Macro F1-score:



75.34%



CSV dosyalarında bulunan satır sayıları, değerlendirme sırasında terminalde gösterilen yanlış tahmin sayılarıyla tam olarak eşleşmiştir.



6\. Validation Matched Hata Dağılımı



| Gerçek Sınıf  | Tahmin Edilen Sınıf | Hata Sayısı |

| ------------- | ------------------- | ----------: |

| NEUTRAL       | CONTRADICTION       |         587 |

| CONTRADICTION | NEUTRAL             |         439 |

| ENTAILMENT    | NEUTRAL             |         430 |

| NEUTRAL       | ENTAILMENT          |         387 |

| CONTRADICTION | ENTAILMENT          |         382 |

| ENTAILMENT    | CONTRADICTION       |         270 |



Bu veri setindeki en sık hata:



NEUTRAL → CONTRADICTION



Hata sayısı:



587



Bu sonuç, modelin desteklenmeyen ancak açıkça çelişmeyen bazı ifadeleri doğrudan contradiction olarak değerlendirebildiğini göstermektedir.



7\. Validation Mismatched Hata Dağılımı



| Gerçek Sınıf  | Tahmin Edilen Sınıf | Hata Sayısı |

| ------------- | ------------------- | ----------: |

| CONTRADICTION | NEUTRAL             |         493 |

| NEUTRAL       | CONTRADICTION       |         491 |

| NEUTRAL       | ENTAILMENT          |         444 |

| ENTAILMENT    | NEUTRAL             |         417 |

| CONTRADICTION | ENTAILMENT          |         342 |

| ENTAILMENT    | CONTRADICTION       |         218 |



CONTRADICTION → NEUTRAL



Hata sayısı:



493



Buna çok yakın olan diğer hata:



NEUTRAL → CONTRADICTION



Hata sayısı:



491



Bu sonuçlar, NEUTRAL ve CONTRADICTION sınıfları arasındaki ayrımın modelin en önemli hata alanı olduğunu doğrulamaktadır.



8\. Validation Matched Genre Analizi



En sık görülen NEUTRAL → CONTRADICTION hatasının genre dağılımı:

| Genre      | Hata Sayısı |

| ---------- | ----------: |

| slate      |         143 |

| travel     |         136 |

| telephone  |         113 |

| government |          98 |

| fiction    |          97 |



Bu hata türü en fazla slate verilerinde görülmüştür.



İkinci sırada travel, üçüncü sırada ise telephone bulunmaktadır.



slate ve telephone örneklerinde konuşma dili, dolaylı anlatım, eksik bağlam veya düzensiz cümle yapıları modelin kararını zorlaştırabilir.



9\. Validation Mismatched Genre Analizi



En sık görülen CONTRADICTION → NEUTRAL hatasının genre dağılımı:

| Genre      | Hata Sayısı |

| ---------- | ----------: |

| facetoface |         122 |

| verbatim   |         104 |

| oup        |          97 |

| nineeleven |          88 |

| letters    |          82 |



Bu hata türü en fazla facetoface verilerinde görülmüştür.



İkinci sırada verbatim, üçüncü sırada ise oup bulunmaktadır.



Özellikle konuşma diline dayalı facetoface ve verbatim metinlerinde dolaylı ifadeler ve bağlama bağlı anlamlar modelin contradiction ilişkisini fark etmesini zorlaştırabilir.



10\. Metin Bazlı Örnek İncelemesi

10.1 NEUTRAL → CONTRADICTION Örnekleri



validation\_matched dosyasından ilk beş örnek incelendi.



İncelenen örneklerde aşağıdaki durumlar gözlemlendi:

Hypothesis içinde premise tarafından açıkça doğrulanmayan ek bilgiler bulunması

Niyet, duygu veya sonuç bildiren ifadelerin premise içinde yer almaması

Soru biçimindeki cümlelerin yanlış yorumlanması

Konuşma dilindeki eksik veya düzensiz cümlelerin bulunması

Modelin kanıt eksikliğini contradiction olarak değerlendirmesi



Bir örnekte premise yalnızca Missouri'nin planlama çalışmalarına devam etmesinin istendiğini belirtmektedir.



Hypothesis ise Missouri'nin bu çalışmalara devam etmekten mutlu olduğunu söylemektedir.



Mutluluk bilgisi premise tarafından ne doğrulanmakta ne de reddedilmektedir.



Bu nedenle gerçek sınıf NEUTRAL olmasına rağmen model CONTRADICTION tahmini üretmiştir.



10.2 CONTRADICTION → NEUTRAL Örnekleri



validation\_mismatched dosyasından ilk beş örnek incelendi.



İncelenen örneklerde aşağıdaki durumlar gözlemlendi:



Zıt anlamın doğrudan değil dolaylı biçimde verilmesi

Miktar ifadeleri arasındaki çelişkiler

Zaman veya durum değişikliği içeren ifadeler

Sebep ve sonuç bilgisinin değiştirilmesi

Soru biçimindeki metinlerde rollerin veya kişilerin değiştirilmesi



Bir örnekte premise, perakendecilerin tahmin yaparken karşılaştığı zorlukların arttığını belirtmektedir.



Hypothesis ise tahmin yapmanın daha kolay hale geldiğini söylemektedir.



Bu iki ifade anlam olarak çelişmesine rağmen model sonucu NEUTRAL olarak tahmin etmiştir.



Başka bir örnekte premise yalnızca bir tanrısal kadın figüründen söz ederken hypothesis birçok tanrıça bulunduğunu belirtmektedir.



Burada miktar açısından açık bir contradiction bulunmasına rağmen model bunu neutral olarak değerlendirmiştir.



11\. Belirlenen Temel Hata Türleri



İncelenen örneklere göre temel hata türleri aşağıdaki şekilde sınıflandırılmıştır:



Kanıt Eksikliği ve Çelişki Karışıklığı



Model, premise içinde bulunmayan bazı bilgileri NEUTRAL yerine CONTRADICTION olarak değerlendirmektedir.



Dolaylı Anlam Çelişkileri

Anlam karşıtlığı doğrudan zıt kelimelerle ifade edilmediğinde model contradiction ilişkisini kaçırabilmektedir.



Miktar ve Sayı İfadeleri



only one, many, all, none ve benzeri miktar ifadeleri arasındaki çelişkiler her zaman doğru algılanmamaktadır.



Duygu ve Niyet Bilgisi



Hypothesis içinde eklenen mutluluk, istek, ilgi veya amaç gibi bilgiler model tarafından yanlış yorumlanabilmektedir.



Konuşma Dili ve Eksik Cümleler



telephone, facetoface ve verbatim türlerinde bulunan konuşma dili, tekrarlar ve eksik cümle yapıları sınıflandırmayı zorlaştırmaktadır.



Soru Cümleleri



Soru biçimindeki premise ve hypothesis çiftlerinde kişi, zaman ve olay ilişkileri model tarafından karıştırılabilmektedir.



12\. Teknik Kazanımlar



Bugünkü çalışma sonucunda:



Yanlış tahminler otomatik olarak dışa aktarılabilir hale getirildi.

Her validation seti için ayrı CSV dosyası oluşturuldu.

Gerçek ve tahmin edilen sınıf adları dosyalara eklendi.

Hata sayıları otomatik olarak değerlendirme metriklerine eklendi.

Hata dosyasının konumu terminal çıktısında gösterildi.

CSV satır sayıları kontrol edildi.

Hata geçişlerinin dağılımı hesaplandı.

Genre bazlı hata dağılımları incelendi.

Metin bazlı örnek analizi başlatıldı.



13\. Modeli İyileştirme Önerileri



Analiz sonucunda aşağıdaki geliştirmeler önerilmektedir:



NEUTRAL ve CONTRADICTION sınıflarına ait zor örneklerle ek eğitim yapmak

Dolaylı contradiction örneklerinin eğitim verisindeki oranını artırmak

Miktar, sayı ve olumsuzluk ifadelerine sahip örnekleri ayrı incelemek

Konuşma dili içeren genre türleri için veri temizleme yöntemleri uygulamak

Düşük confidence değerine sahip tahminleri ayrı analiz etmek

Yanlış tahminlere model confidence score değerlerini eklemek

Metin uzunluğu ile hata oranı arasındaki ilişkiyi incelemek

Her hata türü için örneklerden oluşan ayrı bir veri seti hazırlamak

14\. Analizin Sınırları



Metin bazlı yorumlar, terminal üzerinden görüntülenen sınırlı sayıdaki örneğe dayanmaktadır.



Bu nedenle belirlenen hata türleri ilk bulgular olarak değerlendirilmelidir.



Daha kesin sonuçlar için daha fazla yanlış tahmin örneğinin sistematik olarak incelenmesi gerekmektedir.



15\. Sonuç



Geliştirilmiş NLI modelinin yanlış tahminleri başarıyla ayrı CSV dosyalarına çıkarılmıştır.



validation\_matched veri setinde 2495, validation\_mismatched veri setinde ise 2405 yanlış tahmin kaydedilmiştir.



Analiz sonucunda modelin temel zayıflığının NEUTRAL ve CONTRADICTION sınıfları arasındaki ayrım olduğu doğrulanmıştır.



Özellikle dolaylı çelişkiler, miktar ifadeleri, duygu ve niyet bilgileri, soru cümleleri ve konuşma dili içeren örneklerin model için daha zor olduğu görülmüştür.



Sonraki çalışmada hata analizinin otomatik özetlenmesi ve örneklerin hata türlerine göre sınıflandırılması planlanmaktadır.





