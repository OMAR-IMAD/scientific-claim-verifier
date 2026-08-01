12\. Gün – Model Hatalarının Çıkarılması ve İncelenmesi



Tarih: 2 Ağustos 2026



&#x20;Yapılan Çalışmalar



Bugün modelin yanlış tahmin ettiği örnekleri otomatik olarak kaydetmek için `src/model/evaluate\_full.py` dosyasında düzenleme yapıldı.



Değerlendirme sırasında gerçek label ile tahmin edilen label karşılaştırıldı. Birbirinden farklı olan satırlar yanlış tahmin olarak seçildi.



Yanlış tahminlerde aşağıdaki bilgiler kaydedildi:



\- Premise

\- Hypothesis

\- Genre

\- Gerçek sınıf

\- Tahmin edilen sınıf



Dosyaların kaydedilmesi için aşağıdaki klasör kullanıldı:



reports/error\_analysis



Oluşturulan dosyalar:



\- validation\_matched\_misclassified.csv

\- validation\_mismatched\_misclassified.csv



Kod değişikliğinden sonra syntax kontrolü yapıldı:



powershell

.\\.venv\\Scripts\\python.exe -m py\_compile src\\model\\evaluate\_full.py



Daha sonra değerlendirme yeniden çalıştırıldı:

.\\.venv\\Scripts\\python.exe src\\model\\evaluate\_full.py



Elde Edilen Sonuçlar



validation\_matched veri setinde:



Toplam satır: 9815

Yanlış tahmin: 2495

Accuracy: %74.58

Macro F1: %74.37



validation\_mismatched veri setinde:



Toplam satır: 9832

Yanlış tahmin: 2405

Accuracy: %75.54

Macro F1: %75.34



CSV dosyalarının satır sayıları kontrol edildi ve sonuçlarla uyumlu olduğu görüldü.



Hata Analizi



validation\_matched veri setindeki en sık hata:



NEUTRAL → CONTRADICTION: 587



Bu hata en fazla şu genre türlerinde görüldü:



slate: 143

travel: 136

telephone: 113



validation\_mismatched veri setindeki en sık hata:



CONTRADICTION → NEUTRAL: 493



Bu hata en fazla şu genre türlerinde görüldü:



facetoface: 122

verbatim: 104

oup: 97



Bazı yanlış tahmin örnekleri metin olarak incelendi. Modelin özellikle dolaylı çelişkilerde, soru cümlelerinde, miktar ifadelerinde ve konuşma dilinde zorlandığı görüldü



Gün Sonu Sonucu



Bugün yanlış tahminleri otomatik olarak CSV dosyalarına kaydeden sistem tamamlandı.



Modelin en çok NEUTRAL ve CONTRADICTION sınıflarını karıştırdığı görüldü.



Yapılan analizler aşağıdaki dosyada kaydedildi:



reports/error\_analysis/model\_error\_analysis.md



Sonraki Gün İçin Plan



Bir sonraki gün hata sonuçlarını otomatik olarak özetleyen bir Python dosyası hazırlanacak.

