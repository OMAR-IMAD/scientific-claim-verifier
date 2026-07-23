Day 01
 22 July 2026 8:00 - 15:00

 1. Gün – Ortam Kurulumu, Veri Setinin Hazırlanması, Model Eğitimi ve Backend Başlatma

Tarih: 22 Temmuz 2026

 Günün Amacı

Projenin geliştirme ortamını hazırlamak, üniversite tarafından sağlanan MultiNLI veri setini incelemek, ilk NLI modellerini eğitmek ve web uygulamasının backend altyapısını oluşturmaya başlamak.

 Yapılan Çalışmalar

 1. Proje Gereksinimlerinin İncelenmesi

Üniversite tarafından gönderilen proje yönergesi ayrıntılı olarak incelendi. Projenin temel amacı; bir premise ve hypothesis arasındaki anlamsal ilişkiyi aşağıdaki üç sınıftan biriyle belirleyen bir sistem geliştirmektir:

- Entailment
- Neutral
- Contradiction

Hazır GPT, Gemini veya Claude API’lerinin temel sınıflandırma işlemi için kullanılamayacağı dikkate alındı. Bu nedenle verilen veri seti kullanılarak kendi NLI modelimizin eğitilmesine karar verildi.

 2. Geliştirme Ortamının Hazırlanması

Windows 11 üzerinde proje için gerekli geliştirme ortamı oluşturuldu.

Kullanılan temel araçlar:

- Python 3.12.4
- Git
- Visual Studio Code yerine ilk aşamada Notepad ve PowerShell
- Python sanal ortamı .venv
- NVIDIA GeForce GTX 1660 Ti, 6 GB GPU belleği

PyTorch CUDA desteğiyle kuruldu ve ekran kartının başarıyla algılandığı doğrulandı.

Kurulan temel Python kütüphaneleri:

- PyTorch
- Transformers
- Datasets
- Evaluate
- Accelerate
- Scikit-learn
- Pandas
- NumPy
- FastAPI
- Uvicorn

 3. Veri Setinin İncelenmesi

Üniversite tarafından sağlanan aşağıdaki üç CSV dosyası proje klasörüne eklendi:

- multinli_train.csv
- multinli_validation_matched.csv
- multinli_validation_mismatched.csv

Veri seti üzerinde otomatik inceleme yapıldı.

Dosya boyutları:

- Eğitim verisi: 392.702 kayıt
- Matched validation verisi: 9.815 kayıt
- Mismatched validation verisi: 9.832 kayıt

Etiket eşlemesi şu şekilde belirlendi:

- 0: Entailment
- 1: Neutral
- 2: Contradiction

Eğitim veri setinde sınıfların neredeyse tamamen dengeli olduğu görüldü.

 4. Veri Temizleme

Eğitim veri setinde aşağıdaki sorunlar tespit edildi:

- Hypothesis değeri eksik olan 40 kayıt
- Tamamen tekrar eden 22 kayıt

Bu kayıtlar eğitim verisinden çıkarıldı.

Temizleme sonucunda:

- Orijinal eğitim kaydı: 392.702
- Temizlenen eğitim kaydı: 392.640

Resmî validation dosyaları değiştirilmeden korundu.

 5. İlk Baseline Modelin Eğitilmesi

İlk olarak eğitim sisteminin doğru çalıştığını doğrulamak amacıyla küçük bir baseline model hazırlandı.

Kullanılan ayarlar:

- Model: distilbert-base-uncased
- Eğitim örneği: 3.000
- Validation örneği: 600
- Epoch: 1
- Maksimum token uzunluğu: 128

Baseline model başarıyla eğitildi.

Elde edilen yaklaşık sonuçlar:

- Accuracy: %59,67
- Macro F1: %59,64

Bu modelin amacı yüksek doğruluk elde etmekten çok, veri okuma, tokenization, eğitim, değerlendirme ve model kaydetme süreçlerinin eksiksiz çalıştığını doğrulamaktı.

 6. Geliştirilmiş Modelin Eğitilmesi

Baseline modelin performansını artırmak için ikinci bir model eğitildi.

Kullanılan ayarlar:

- Model: `distilroberta-base`
- Eğitim örneği: 15.000
- Validation örneği: 1.500
- Epoch: 2
- Maksimum token uzunluğu: 128
- GPU hızlandırması ve FP16 kullanımı

Eğitim yaklaşık 50 dakika sürdü.

İlk değerlendirme sonucu:

- Accuracy: yaklaşık %72
- Macro F1: yaklaşık %71,90

Geliştirilmiş model, baseline modele göre belirgin şekilde daha başarılı sonuç verdi.

 7. Modelin Örnek Cümlelerle Test Edilmesi

Model farklı premise ve hypothesis örnekleriyle test edildi.

Örnek:

Premise:

The door is open.

Hypothesis:

The door is closed.

Model sonucu:

- Prediction: Contradiction
- Confidence: %95,70

Başka bir örnekte, premise içinde belirtilmeyen bir kıyafet bilgisi için model doğru şekilde Neutral sınıfını tahmin etti.

 8. Resmî Validation Dosyaları Üzerinde Tam Değerlendirme

Geliştirilmiş model, üniversite tarafından sağlanan iki validation dosyasının tamamı üzerinde test edildi.

 Validation Matched

- Kayıt sayısı: 9.815
- Accuracy: %74,58
- Macro F1: %74,37

 Validation Mismatched

- Kayıt sayısı: 9.832
- Accuracy: %75,54
- Macro F1: %75,34

Ayrıca confusion matrix, sınıf bazlı sonuçlar ve genre bazlı performans değerleri raporlandı.

 9. Git ve GitHub Kurulumu

Proje için yerel bir Git deposu oluşturuldu.

Yapılan işlemler:

- Git deposu başlatıldı.
- İlk commit oluşturuldu.
- Ana branch adı `main` olarak ayarlandı.
- GitHub üzerinde `scientific-claim-verifier` adlı repository oluşturuldu.
- Proje dosyaları GitHub’a başarıyla gönderildi.

Büyük veri dosyaları, model dosyaları ve sanal ortam `.gitignore` ile GitHub dışında bırakıldı.

 10. FastAPI Backend Başlangıcı

Web uygulamasının backend bölümü için FastAPI kullanılarak temel yapı oluşturuldu.

Oluşturulan ilk endpointler:

- GET /
- GET /health
- POST /predict

POST /predict endpointi, kullanıcıdan premise ve hypothesis alarak eğitilmiş NLI modelini çalıştıracak şekilde hazırlandı.

Backend’in modeli CUDA üzerinden başarıyla yüklediği doğrulandı.

Swagger API dokümantasyonu aşağıdaki adreste başarıyla açıldı:

http://127.0.0.1:8000/docs

 Karşılaşılan Zorluklar

- Veri setinin büyük olması nedeniyle veri işleme işlemlerinin dikkatli yapılması gerekti.
- Baseline model bazı basit çelişki örneklerinde yanlış tahmin yaptı.
- Model performansını artırmak için daha iyi bir temel model, daha fazla eğitim verisi ve daha fazla epoch kullanılması gerekti.
- Geliştirilmiş modelin eğitimi yaklaşık 50 dakika sürdü.
- GPU belleğinin 6 GB olması nedeniyle batch size ve maksimum token uzunluğu kontrollü seçildi.

 Alınan Kararlar

- Temel NLI sınıflandırma görevi için hazır LLM API’leri kullanılmayacak.
- Model eğitiminde Hugging Face Transformers ve PyTorch kullanılacak.
- Backend için FastAPI kullanılacak.
- Frontend daha sonraki aşamada React ile geliştirilecek.
- Veritabanı olarak PostgreSQL kullanılması planlanıyor.
- Modelin ilk başarılı sürümü daha sonraki geliştirmeler için korunacak.
- Tüm geliştirme süreci Git ve GitHub üzerinden düzenli olarak takip edilecek.

 Gün Sonu Sonucu

Projenin geliştirme ortamı başarıyla hazırlandı. Veri seti incelendi ve temizlendi. Baseline ve geliştirilmiş olmak üzere iki farklı NLI modeli eğitildi. Geliştirilmiş model resmî validation dosyalarında yaklaşık %75 doğruluk elde etti. GitHub repository oluşturuldu ve FastAPI backend altyapısına başlandı.

 Sonraki Gün İçin Plan

- POST /predict endpointini Swagger üzerinden test etmek
- Backend için request ve response şemalarını geliştirmek
- Hata yönetimini iyileştirmek
- Veritabanı yapısını planlamak
- Kullanıcı kayıt ve giriş sistemine başlamak