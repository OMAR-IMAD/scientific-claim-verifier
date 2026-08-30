41\. Gün - Dashboard İstatistikleri İçin CRUD Geliştirmesi



2026-08-31



Bugün Dashboard bölümünde kullanılacak analiz istatistikleri üzerinde çalıştım.



Öncelikle crud.py dosyasına get\_analysis\_stats\_by\_user fonksiyonu eklendi. Bu fonksiyon belirli bir kullanıcının toplam analiz sayısını ve ENTAILMENT, CONTRADICTION ve NEUTRAL sonuçlarının sayılarını hesaplayacak şekilde geliştirildi.



İstatistik hesaplamalarında SQLAlchemy func.count ve group\_by yapıları kullanıldı. Daha sonra yeni fonksiyon için test\_crud.py dosyasına yeni bir test eklendi.



Test içerisinde dört farklı analiz oluşturuldu. Sonuçların ikisi ENTAILMENT, biri NEUTRAL ve biri CONTRADICTION olarak ayarlandı. Fonksiyonun toplam analiz sayısını 4 ve her sınıfın sayısını doğru döndürdüğü kontrol edildi.



Yeni test tek başına başarılı geçti. test\_crud.py dosyasındaki tüm testler çalıştırıldığında 5 test başarılı oldu. Projenin tamamında ise toplam 81 test başarılı geçti. git diff --check kontrolünde herhangi bir biçimlendirme hatası bulunmadı.



Sonuç:

Dashboard için ilk istatistik fonksiyonu oluşturuldu.

Kullanıcının toplam analiz sayısı hesaplanabiliyor.

ENTAILMENT, CONTRADICTION ve NEUTRAL dağılımları hesaplanabiliyor.

Yeni CRUD testi başarıyla tamamlandı.

Projenin tamamında 81 test başarılı geçti.



Sonraki Gün İçin Plan



Dashboard istatistiklerini API üzerinden erişilebilir hale getirmek.

