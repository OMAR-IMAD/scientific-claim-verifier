&#x20;WEX 428 – Proje Raporu



Scientific Claim Verifier: NLI-Based Fact-Checking Platform



Öğrenci Adı : OMAR IMAD ISMAEL AL-HADEETHI

Öğrenci NO : 220206919 

Bölüm : Bilgisayar Mühendisliği

Ders: WEX 428 – İş Yeri Deneyimi III  

Proje Türü: LLM / Natural Language Inference (NLI)  

Tarih: 2026-09-29



---
1. Proje Özeti



Bu projede, verilen bir önerme (hypothesis) ile kanıt metni (premise) arasındaki anlamsal ilişkiyi belirleyen web tabanlı bir doğrulama sistemi geliştirilmiştir.



Sistem, Natural Language Inference (NLI) yaklaşımını kullanarak metin çiftlerini üç farklı sınıfa ayırmaktadır:



- Entailment

- Neutral

- Contradiction



Proje kapsamında NLI modeli eğitilmiş ve geliştirilen web uygulamasına entegre edilmiştir. Kullanıcılar sisteme kayıt olabilir, giriş yapabilir, yeni analiz oluşturabilir, tahmin sonuçlarını ve güven skorlarını görüntüleyebilir.



Ayrıca kullanıcıların geçmiş analizlerini görüntüleyebilmesi, arama ve filtreleme yapabilmesi, analizleri silebilmesi ve genel analiz istatistiklerini dashboard üzerinden takip edebilmesi sağlanmıştır.



Backend tarafında FastAPI, frontend tarafında React kullanılmıştır. Kullanıcı ve analiz verileri ilişkisel bir veritabanında saklanmaktadır. Uygulamanın çalıştırılması ve dağıtıma hazırlanması için Docker desteği de eklenmiştir.



2. Projenin Amacı ve Hedefleri



Bu projenin temel amacı, kullanıcıların bilimsel veya genel iddiaları verilen kanıt metinleri ile karşılaştırarak doğrulayabilmesini sağlayan tam kapsamlı bir web uygulaması geliştirmektir.



Proje kapsamında aşağıdaki hedefler belirlenmiştir:



- Premise ve hypothesis çiftlerini analiz eden bir Natural Language Inference (NLI) modeli geliştirmek ve sisteme entegre etmek.

- Metin çiftlerini Entailment, Neutral veya Contradiction sınıflarından biriyle sınıflandırmak.

- Her tahmin için güven skorlarını kullanıcıya göstermek.

- Güvenli kullanıcı kayıt ve giriş sistemi oluşturmak.

- JWT tabanlı kimlik doğrulama mekanizması kullanmak.

- Kullanıcıların önceki analizlerini görüntüleyebileceği bir geçmiş sistemi geliştirmek.

- Analiz geçmişinde arama, filtreleme, detay görüntüleme ve silme işlemlerini desteklemek.

- Kullanıcıların analiz istatistiklerini görebileceği bir dashboard hazırlamak.

- Backend ve frontend arasında REST API üzerinden iletişim sağlamak.

- Uygulamayı Docker kullanarak çalıştırılabilir ve dağıtıma uygun hale getirmek.



Bu hedefler doğrultusunda proje; yapay zeka modeli, backend, frontend, veritabanı ve kullanıcı yönetimi bileşenlerinin birlikte çalıştığı tam kapsamlı bir sistem olarak geliştirilmiştir.



3. Kullanılan Veri Seti ve Veri Hazırlama



Projede ders kapsamında sağlanan veri seti kullanılmıştır. Veri seti; premise, hypothesis ve bunlar arasındaki anlamsal ilişkiyi gösteren etiketlerden oluşmaktadır.



Kullanılan etiket eşlemesi aşağıdaki gibidir:



- 0 = Entailment

- 1 = Neutral

- 2 = Contradiction



\### 3.1. Eğitim Verisi



Eğitim veri seti `multi\_nli\_train.csv` dosyasından alınmıştır.



Toplam eğitim örneği sayısı:



392.702



Sınıf dağılımı:



- Entailment: 130.899

- Neutral: 130.900

- Contradiction: 130.903



Bu dağılım, eğitim verisinin sınıflar açısından dengeli olduğunu göstermektedir.



Veri kontrolü sırasında:



- Geçersiz etiket bulunmamıştır.

- 22 adet tamamen aynı üçlü kayıt tespit edilmiştir.

- 40 adet hypothesis alanının eksik olduğu görülmüştür.



3.2. Validation Verileri



Model değerlendirmesinde iki farklı validation veri seti kullanılmıştır:



Validation Matched\*\*

- Toplam örnek: 9.815

- Entailment: 3.479

- Neutral: 3.123

- Contradiction: 3.213



Validation Mismatched\*\*

- Toplam örnek: 9.832

- Entailment: 3.463

- Neutral: 3.129

- Contradiction: 3.240



Her iki validation veri setinde de geçersiz etiket bulunmamıştır.



3.3. Veri Hazırlama Süreci



Model eğitiminden önce veri seti analiz edilmiş ve gerekli kontroller yapılmıştır. Premise, hypothesis ve label alanlarının yapısı incelenmiş, eksik veriler, tekrar eden kayıtlar ve sınıf dağılımları kontrol edilmiştir.



Verilerin modele uygun hale getirilmesi için metin çiftleri tokenizer ile işlenmiş ve NLI modelinin kullanabileceği giriş formatına dönüştürülmüştür.



Bu işlemler için proje içerisinde veri hazırlama ve veri kontrolü amacıyla `prepare\_dataset.py` ve `audit\_dataset.py` dosyaları kullanılmıştır.



4. NLI Modelinin Eğitimi ve Geliştirilmesi



Projede premise ve hypothesis arasındaki anlamsal ilişkiyi belirlemek amacıyla RoBERTa tabanlı bir Natural Language Inference modeli kullanılmıştır.



Model, üç sınıflı bir sequence classification problemi için yapılandırılmıştır:



- Entailment

- Neutral

- Contradiction



Model yapılandırmasına göre kullanılan mimari `RobertaForSequenceClassification` yapısındadır. Modelin temel özellikleri aşağıdaki gibidir:



- Model türü: RoBERTa

- Hidden size: 768

- Hidden layer sayısı: 6

- Attention head sayısı: 12

- Vocabulary size: 50.265

- Maksimum position embedding: 514

- Sınıf sayısı: 3



Etiket eşlemesi aşağıdaki şekilde kullanılmıştır:



- 0 = Entailment

- 1 = Neutral

- 2 = Contradiction



4.1. Baseline Model



İlk aşamada bir baseline model eğitilmiştir. Baseline model, eğitim sürecinin başlangıç performansını görmek ve daha sonraki geliştirmeler için karşılaştırma noktası oluşturmak amacıyla kullanılmıştır.



Baseline model test sonuçları:



- Accuracy: %59,67

- Precision (Macro): %60,50

- Recall (Macro): %59,67

- F1-Score (Macro): %59,64

- Evaluation Loss: 0,890



Baseline eğitim süreci 1 epoch üzerinden gerçekleştirilmiştir.



4.2. Improved Model



Baseline modelden elde edilen sonuçlar analiz edildikten sonra eğitim süreci geliştirilmiş ve ikinci bir model oluşturulmuştur.



Improved model test sonuçları:



- Accuracy: %72,00

- Precision (Macro): %71,91

- Recall (Macro): %72,00

- F1-Score (Macro): %71,90

- Evaluation Loss: 0,693



Improved model 2 epoch boyunca eğitilmiştir.



Baseline ve improved model karşılaştırıldığında accuracy değerinde yaklaşık 12,33 yüzde puanlık bir artış elde edilmiştir. Aynı zamanda F1-Score değeri de yaklaşık 12,26 yüzde puan artmış ve evaluation loss değeri azalmıştır.



Bu sonuçlar doğrultusunda improved model, uygulamada kullanılacak nihai NLI modeli olarak seçilmiştir.



4.3. Modelin Kaydedilmesi



Eğitim tamamlandıktan sonra model ve tokenizer dosyaları proje içerisinde saklanmıştır.



Nihai model klasöründe aşağıdaki dosyalar bulunmaktadır:



- `config.json`

- `model.safetensors`

- `tokenizer.json`

- `tokenizer\_config.json`

- `training\_args.bin`



Bu yapı sayesinde eğitilmiş model yeniden eğitim yapılmadan backend tarafından yüklenebilmekte ve kullanıcıların gönderdiği premise-hypothesis çiftleri üzerinde tahmin işlemi gerçekleştirebilmektedir.



5. Model Değerlendirme Sonuçları ve Hata Analizi



Nihai modelin performansını daha ayrıntılı değerlendirmek için iki farklı validation veri seti kullanılmıştır:



- Validation Matched

- Validation Mismatched



Bu değerlendirme sürecinde Accuracy, Precision, Recall ve F1-Score metrikleri kullanılmıştır. Ayrıca sınıf bazlı sonuçlar, confusion matrix değerleri ve yanlış sınıflandırılan örnekler analiz edilmiştir.



5.1. Validation Matched Sonuçları



Validation Matched veri setinde toplam 9.815 örnek bulunmaktadır.



Genel sonuçlar:



- Accuracy: %74,58

- Precision (Macro): %74,38

- Recall (Macro): %74,38

- F1-Score (Macro): %74,37



Sınıf bazlı F1-Score sonuçları:



- Entailment: %79,09

- Neutral: %69,99

- Contradiction: %74,03



Bu sonuçlara göre modelin en yüksek performansı Entailment sınıfında gösterdiği, Neutral sınıfında ise diğer sınıflara göre daha düşük performans elde ettiği görülmüştür.



5.2. Validation Mismatched Sonuçları



Validation Mismatched veri setinde toplam 9.832 örnek bulunmaktadır.



Genel sonuçlar:



- Accuracy: %75,54

- Precision (Macro): %75,39

- Recall (Macro): %75,54

- F1-Score (Macro): %75,34



Sınıf bazlı F1-Score sonuçları:



- Entailment: %79,92

- Neutral: %70,40

- Contradiction: %75,70



Validation Mismatched sonuçlarının Validation Matched sonuçlarına oldukça yakın olması, modelin farklı metin türleri üzerinde benzer bir performans gösterebildiğini ortaya koymuştur.



5.3. Hata Analizi



Model değerlendirme sürecinde yanlış sınıflandırılan örnekler ayrıca analiz edilmiştir.



Validation Matched veri setinde 2.495 örnek yanlış sınıflandırılmıştır.



Modelin:



- Doğru tahminlerde ortalama confidence değeri yaklaşık 0,87

- Yanlış tahminlerde ortalama confidence değeri yaklaşık 0,73



olarak ölçülmüştür.



Ayrıca confidence threshold değeri 0,60 olarak kullanılmış ve düşük güvenli tahminler ayrı olarak incelenmiştir.



Hata analizi için proje içerisinde aşağıdaki raporlar oluşturulmuştur:



- model\_error\_analysis.md

- model\_confidence\_analysis.md

- automatic\_error\_summary.md`

- validation\_matched\_misclassified.csv

- validation\_mismatched\_misclassified.csv



Bu analizler sayesinde modelin hangi durumlarda daha fazla hata yaptığı ve tahmin güven skorlarının doğru ve yanlış tahminlerde nasıl değiştiği incelenmiştir.



6. Backend Mimarisi ve API Yapısı



Uygulamanın backend tarafı Python ve FastAPI kullanılarak geliştirilmiştir. Backend, kullanıcı işlemleri, kimlik doğrulama, NLI modelinin çalıştırılması, analiz geçmişinin yönetilmesi, dosya yükleme işlemleri ve dashboard istatistiklerinin oluşturulmasından sorumludur.



API yapısı RESTful prensiplere uygun şekilde hazırlanmıştır.



Backend içerisinde Pydantic şemaları kullanılarak gelen ve dönen verilerin doğrulaması yapılmıştır. Veritabanı işlemleri için SQLAlchemy kullanılmış, veritabanı yapısının yönetimi için Alembic migration desteği eklenmiştir.



6.1. Temel API Endpointleri



Projede kullanılan temel endpointler aşağıdaki gibidir:



- GET /health  

&#x20; Backend servisinin ve NLI modelinin çalışma durumunu kontrol eder.



- POST /register 

&#x20; Yeni kullanıcı kaydı oluşturur.



- POST /login 

&#x20; Kullanıcı giriş işlemini gerçekleştirir ve başarılı giriş sonrasında JWT access token döndürür.



- GET /me 

&#x20; Giriş yapmış kullanıcının profil bilgilerini döndürür.



- POST /predict  

&#x20; Premise ve hypothesis çiftini NLI modeline gönderir. Tahmin sınıfını, confidence değerini ve üç sınıfa ait skorları döndürür.



- GET /history

&#x20; Kullanıcının önceki analizlerini listeler.



- DELETE /history/{id} 

&#x20; Belirtilen analiz kaydını siler.



- GET /dashboard/stats

&#x20; Kullanıcının analiz istatistiklerini ve sınıf dağılımlarını döndürür.



- POST /upload  

&#x20; Dosya üzerinden premise ve hypothesis verilerinin işlenmesini sağlar.



6.2. Kimlik Doğrulama



Uygulamada JWT tabanlı kimlik doğrulama sistemi kullanılmıştır.



Kullanıcı giriş yaptıktan sonra oluşturulan access token, korumalı endpointlere yapılan isteklerde kullanılmaktadır.



Bu yapı sayesinde kullanıcıya ait profil, analiz geçmişi, tahmin sonuçları ve dashboard verileri yetkilendirilmiş şekilde yönetilmektedir.



6.3. Model Entegrasyonu



Eğitilen NLI modeli backend içerisine entegre edilmiştir.



Kullanıcı bir premise-hypothesis çifti gönderdiğinde backend modeli çalıştırarak aşağıdaki sonuçları üretmektedir:



- Prediction class

- Entailment score

- Neutral score

- Contradiction score

- Confidence score



Model servisi backend ile kullanıcı arayüzü arasında doğrudan bağlantı sağlayarak tahmin sonuçlarının web uygulamasında gösterilmesini mümkün hale getirmektedir.



6.4. API Testleri



Backend için otomatik testler hazırlanmıştır.



Projenin son kontrol aşamasında test paketi çalıştırılmış ve:



84 test başarıyla tamamlanmıştır.



Ayrıca Docker ortamında health, register, login, profile, prediction, history, dashboard ve delete işlemleri manuel olarak test edilmiştir.



7. Veritabanı Tasarımı ve Veri Yönetimi



Projede kullanıcı bilgileri ve analiz geçmişinin saklanması için ilişkisel veritabanı kullanılmıştır.



Geliştirme aşamasında SQLite tercih edilmiştir. Veritabanı işlemleri SQLAlchemy ORM kullanılarak gerçekleştirilmiş, şema değişikliklerinin yönetimi için Alembic migration sistemi kullanılmıştır.



7.1. Temel Tablolar



Veritabanında temel olarak iki ana yapı bulunmaktadır:



- users

- analyses



users tablosu kullanıcı hesap bilgilerinin saklanmasından sorumludur.



analyses tablosu ise kullanıcıların gerçekleştirdiği NLI analizlerini saklamak için kullanılmaktadır.



Bu yapı sayesinde her analiz ilgili kullanıcı ile ilişkilendirilebilmekte ve kullanıcı yalnızca kendi analiz geçmişini görüntüleyebilmektedir.



7.2. Saklanan Veriler



Sistemde aşağıdaki bilgiler veritabanında saklanmaktadır:



- Kullanıcı bilgileri

- Kimlik doğrulama için gerekli kullanıcı verileri

- Premise metni

- Hypothesis metni

- Tahmin sonucu

- Confidence bilgisi

- Analiz tarihi ve zamanı

- Kullanıcıya ait analiz geçmişi



7.3. CRUD İşlemleri



Veritabanı katmanında kullanıcı ve analiz kayıtlarını yönetmek için CRUD işlemleri geliştirilmiştir.



Temel işlemler:



- Yeni kullanıcı oluşturma

- Kullanıcıyı e-posta adresine göre bulma

- Yeni analiz kaydı oluşturma

- Kullanıcıya ait analizleri listeleme

- Analiz kaydını silme



Analiz geçmişi backend API ile entegre edilerek frontend üzerinden görüntülenebilir hale getirilmiştir.



7.4. Veritabanı Yönetimi



SQLAlchemy kullanımı sayesinde Python nesneleri ile veritabanı tabloları arasında ORM tabanlı bir yapı oluşturulmuştur.



Alembic kullanılarak veritabanı şemasındaki değişikliklerin kontrollü şekilde uygulanması sağlanmıştır.



Bu yapı, uygulamanın veritabanı tarafının daha düzenli ve sürdürülebilir şekilde geliştirilmesine yardımcı olmuştur.





8. Frontend ve Kullanıcı Arayüzü



Uygulamanın frontend tarafı React kullanılarak geliştirilmiştir. Kullanıcı arayüzü, backend servisleri ile REST API üzerinden iletişim kurmaktadır.



Arayüz, kullanıcıların sisteme kolay şekilde erişebilmesi ve analiz işlemlerini basit adımlarla gerçekleştirebilmesi amacıyla hazırlanmıştır.



8.1. Kullanıcı İşlemleri



Frontend üzerinden aşağıdaki kullanıcı işlemleri desteklenmektedir:



- Yeni kullanıcı kaydı

- Kullanıcı girişi

- Kullanıcı profili görüntüleme

- Oturum kapatma



Giriş işlemi sonrasında alınan JWT access token, korumalı API isteklerinde kullanılmaktadır.



8.2. Claim Verification



Kullanıcılar premise ve hypothesis alanlarını manuel olarak girerek analiz başlatabilmektedir.



Analiz tamamlandıktan sonra sistem kullanıcıya aşağıdaki bilgileri göstermektedir:



- Prediction sonucu

- Confidence değeri

- Entailment skoru

- Neutral skoru

- Contradiction skoru

- Girilen premise ve hypothesis metinleri



Form doğrulaması sayesinde premise veya hypothesis alanlarından biri boş bırakıldığında kullanıcıya uyarı gösterilmektedir.



8.3. Dosya Yükleme



Uygulamada dosya yükleme özelliği bulunmaktadır.



Kullanıcılar uygun formatta hazırlanan dosyaları sisteme yükleyerek premise ve hypothesis verilerini işleyebilmektedir.



Bu özellik backend tarafındaki `/upload` endpointi ile entegre edilmiştir.



8.4. Analysis History



Kullanıcıların geçmiş analizlerini görüntüleyebilmesi için Analysis History bölümü geliştirilmiştir.



Bu bölümde kullanıcılar:



- Önceki analizlerini görüntüleyebilir

- Arama yapabilir

- Filtreleme yapabilir

- Sıralama yapabilir

- Analiz detaylarını görüntüleyebilir

- Analiz kayıtlarını silebilir



8.5. Dashboard



Dashboard bölümünde kullanıcıya ait analiz istatistikleri gösterilmektedir.



Dashboard içerisinde aşağıdaki bilgiler sunulmaktadır:



- Toplam analiz sayısı

- Entailment sayısı

- Neutral sayısı

- Contradiction sayısı

- Sınıfların yüzdelik dağılımları

- Günlük analiz sayıları

- Son 7 günlük analiz bilgileri

- En sık tahmin edilen sınıf



Bu yapı sayesinde kullanıcı kendi analiz geçmişini ve genel kullanım istatistiklerini görsel olarak takip edebilmektedir.



8.6. Responsive ve Kullanıcı Dostu Tasarım



Frontend tasarımında kullanıcı dostu ve anlaşılır bir yapı oluşturulmasına dikkat edilmiştir.



Sayfalar arasında kolay geçiş, form doğrulaması, hata mesajları ve sonuçların açık şekilde gösterilmesi sağlanmıştır.



Frontend production build işlemi proje sonunda test edilmiş ve başarılı şekilde tamamlanmıştır.





9. Docker, Deployment ve Sistem Testleri



Projenin çalıştırılabilir ve dağıtıma uygun bir yapıya sahip olması amacıyla Docker kullanılmıştır.



Backend uygulaması için Docker image oluşturulmuş ve uygulama container içerisinde çalıştırılarak test edilmiştir.



9.1. Docker Yapısı



Backend uygulaması Docker ortamında çalıştırılabilmektedir.



Proje için oluşturulan backend image:



`scientific-claim-verifier-backend:latest`



Docker container çalıştırıldığında backend servisi dışarıya port yönlendirmesi ile erişilebilir hale gelmektedir.



Docker ortamında NLI modelinin başarıyla yüklendiği ve CPU üzerinde tahmin yapabildiği doğrulanmıştır.



9.2. Backend Testleri



Backend tarafında otomatik testler hazırlanmıştır.



Projenin son kontrol aşamasında test paketi çalıştırılmış ve:



84 test başarıyla geçmiştir.



Testler; API davranışları, veri doğrulama işlemleri ve temel backend fonksiyonlarının doğru çalışmasını kontrol etmek amacıyla kullanılmıştır.



9.3. Docker Ortamında Manuel API Testleri



Backend Docker container içerisinde çalıştırıldıktan sonra aşağıdaki işlemler manuel olarak test edilmiştir:



- Health kontrolü

- Kullanıcı kaydı

- Kullanıcı girişi

- JWT token oluşturulması

- Kullanıcı profilinin görüntülenmesi

- NLI prediction işlemi

- Analysis history görüntüleme

- Dashboard istatistikleri

- Analysis silme işlemi



/health endpointi üzerinden sistemin durumu kontrol edilmiş ve NLI modelinin hazır durumda olduğu doğrulanmıştır.



9.4. Frontend Production Build



Frontend uygulamasının production build işlemi gerçekleştirilmiştir.



Vite kullanılarak yapılan build işlemi hata olmadan tamamlanmış ve production için gerekli `dist` dosyaları başarıyla oluşturulmuştur.



Bu kontrol sayesinde frontend uygulamasının production build aşamasında herhangi bir hata vermediği doğrulanmıştır.



9.5. Son Sistem Kontrolü



Projenin son aşamasında backend testleri, frontend build işlemi ve Docker çalışma durumu yeniden kontrol edilmiştir.



Backend, frontend, NLI modeli, authentication sistemi, veritabanı ve kullanıcı arayüzünün birlikte çalıştığı doğrulanmıştır.



Proje Docker kullanılarak çalıştırılabilir durumda hazırlanmıştır. Bu proje kapsamında ayrıca bir cloud platformuna deployment yapılmamıştır.





10. Proje Sonuçları ve Genel Değerlendirme



Bu proje kapsamında, bilimsel veya genel iddiaların verilen kanıt metinleri ile karşılaştırılmasını sağlayan tam kapsamlı bir NLI tabanlı web uygulaması geliştirilmiştir.



Projenin başlangıcında veri seti analiz edilmiş, eğitim ve validation verileri kontrol edilmiş ve üç sınıflı NLI problemi için gerekli veri hazırlama işlemleri gerçekleştirilmiştir.



İlk olarak baseline model eğitilmiş ve daha sonra eğitim süreci geliştirilerek improved model oluşturulmuştur. Improved model, baseline modele göre daha yüksek performans göstermiştir.



Baseline modelin test accuracy değeri %59,67 iken improved modelin test accuracy değeri %72,00 seviyesine yükselmiştir.



Ayrıntılı validation değerlendirmelerinde ise:



- Validation Matched Accuracy: %74,58

- Validation Mismatched Accuracy: %75,54



sonuçları elde edilmiştir.



Model yalnızca ayrı bir makine öğrenmesi bileşeni olarak bırakılmamış, geliştirilen FastAPI backend içerisine entegre edilmiştir. Böylece kullanıcıların web arayüzü üzerinden premise ve hypothesis göndererek gerçek zamanlı tahmin sonucu alabilmesi sağlanmıştır.



Proje kapsamında ayrıca:



- Kullanıcı kayıt ve giriş sistemi

- JWT tabanlı kimlik doğrulama

- Kullanıcı profili

- NLI claim verification

- Confidence score gösterimi

- Analysis history

- Arama, filtreleme ve sıralama

- Analiz detaylarını görüntüleme

- Analiz silme

- Dashboard ve istatistikler

- Dosya yükleme

- İlişkisel veritabanı

- Docker desteği

- Backend otomatik testleri

- Frontend production build



başarıyla uygulanmıştır.



Projenin son kontrol aşamasında backend üzerinde 84 otomatik test başarıyla tamamlanmış, frontend production build işlemi hata olmadan gerçekleştirilmiş ve backend Docker ortamında çalıştırılarak temel API fonksiyonları manuel olarak doğrulanmıştır.



Sonuç olarak proje; veri hazırlama, model eğitimi, model değerlendirme, backend, frontend, veritabanı, authentication, dashboard ve Docker bileşenlerinin birlikte çalıştığı tam kapsamlı bir sistem haline getirilmiştir.



Bu proje sayesinde Natural Language Inference, transformer tabanlı modeller, REST API geliştirme, kullanıcı kimlik doğrulama, ilişkisel veritabanı yönetimi, frontend-backend entegrasyonu, test süreçleri ve Docker kullanımı konularında uygulamalı deneyim kazanılmıştır.





11. GitHub Repository ve Kaynak Kod



Projenin kaynak kodları GitHub üzerinde tutulmaktadır.



GitHub Repository:



https://github.com/OMAR-IMAD/scientific-claim-verifier



Repository içerisinde aşağıdaki temel proje bileşenleri bulunmaktadır:



- Backend kaynak kodları

- Frontend kaynak kodları

- NLI model eğitim ve değerlendirme dosyaları

- Veritabanı ve migration dosyaları

- Test dosyaları

- Docker yapılandırmaları

- Model değerlendirme raporları

- Günlük çalışma kayıtları



Proje geliştirme süreci boyunca yapılan değişiklikler Git üzerinden takip edilmiş ve düzenli olarak GitHub repository içerisine gönderilmiştir.
