&#x20;21. Gün – Input Doğrulama Düzenlemesi



2026-08-11



Bugün API tarafındaki input işlemlerini düzenledim.



`PredictionRequest` içine `field\\\_validator` ekleyerek premise ve hypothesis alanlarındaki gereksiz boşlukların otomatik olarak temizlenmesini sağladım.



Daha sonra `main.py` içindeki tekrar eden `.strip()` işlemlerini kaldırdım ve kontrolü schema tarafına taşıdım.



Bu işlem için yeni bir API testi ekledim. Test başarılı oldu.



Sonuç:



\- 21 API testi başarılı.

\- Toplam 31 test başarılı.

\- Backend smoke test başarılı.

\- Gerçek model CUDA üzerinde çalıştı.

\- `git diff --check` kontrolünde hata bulunmadı.



&#x20;Sonraki Gün İçin Plan



Backend yapısını geliştirmeye devam etmek.

