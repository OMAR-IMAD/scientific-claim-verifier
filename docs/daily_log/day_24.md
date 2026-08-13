24\. Gün – ErrorResponse Testlerinin Geliştirilmesi



2026-08-14



Bugün backend tarafında kullanılan `ErrorResponse` yapısının testlerini geliştirdim.



İlk olarak `ErrorResponse` sınıfının yapısını inceledim. Bu yapının API hata mesajlarını göstermek için `detail` isimli bir alan kullandığını kontrol ettim.



Daha sonra hata mesajının doğru şekilde saklanıp saklanmadığını kontrol eden bir test ekledim. Test içinde `Premise cannot be empty.` mesajını kullanarak oluşturulan `ErrorResponse` nesnesinin `detail` alanını doğruladım.



İkinci testte ise `detail` alanının zorunlu olup olmadığını kontrol ettim. `detail` verilmeden bir `ErrorResponse` oluşturmaya çalıştım ve Pydantic'in bu durumu `ValidationError` ile doğru şekilde reddettiğini doğruladım.



Eklediğim iki testi önce ayrı ayrı çalıştırdım ve ikisi de başarılı oldu. Daha sonra `test\_schemas.py` dosyasındaki bütün schema testlerini birlikte çalıştırdım.



Son olarak projedeki tüm testleri tekrar çalıştırarak yeni testlerin mevcut backend yapısını etkilemediğini kontrol ettim. Backend smoke testini de çalıştırdım ve gerçek model ile tahmin işlemi başarılı şekilde tamamlandı.



Sonuç:



\- 2 yeni `ErrorResponse` testi eklendi.

\- 7 schema testi başarılı.

\- Toplam 38 proje testi başarılı.

\- Backend smoke test başarılı.

\- Predict endpoint başarılı çalıştı.

\- Gerçek model CUDA üzerinde çalıştı.

\- `git diff --check` kontrolünde hata bulunmadı.



&#x20;Sonraki Gün İçin Plan



Backend schema testlerini geliştirmeye ve farklı doğrulama durumlarını kontrol etmeye devam etmek.

