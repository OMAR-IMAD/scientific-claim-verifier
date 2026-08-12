23\. Gün – PredictionResponse Testlerinin Geliştirilmesi



2026-08-13



Bugün backend tarafında kullanılan `PredictionResponse` yapısının testlerini geliştirdim.



İlk olarak response içinde bulunan `prediction` alanını kontrol ettim. Bu alanın sadece `ENTAILMENT`, `NEUTRAL` ve `CONTRADICTION` değerlerini kabul etmesi gerekiyor. Bu nedenle geçersiz bir değer olan `UNKNOWN` ile test yaptım ve Pydantic tarafından doğru şekilde reddedildiğini doğruladım.



Daha sonra `confidence` alanı için test ekledim. Bu değerin 0.0 ile 1.0 arasında olması gerektiği için 1.20 değerini kullanarak geçersiz bir durum oluşturdum. Sistem bu değeri de doğru şekilde reddetti.



Eklediğim iki testi önce ayrı ayrı çalıştırdım ve ikisi de başarılı oldu. Daha sonra `test\_schemas.py` dosyasındaki bütün schema testlerini birlikte çalıştırdım.



Son olarak proje içerisindeki tüm testleri tekrar çalıştırarak yeni eklenen testlerin mevcut sistem üzerinde herhangi bir probleme neden olmadığını kontrol ettim. Backend smoke testini de tekrar çalıştırdım ve gerçek model ile tahmin işlemi başarılı şekilde tamamlandı.



Sonuç:



\* 2 yeni `PredictionResponse` testi eklendi.

\* 5 schema testi başarılı.

\* Toplam 36 proje testi başarılı.

\* Backend smoke test başarılı.

\* Predict endpoint başarılı çalıştı.

\* Gerçek model CUDA üzerinde çalıştı.

\* `git diff --check` kontrolünde hata bulunmadı.



&#x20;Sonraki Gün İçin Plan



Schema ve backend testlerini geliştirmeye devam etmek ve response yapısının farklı durumlarını kontrol etmek.



