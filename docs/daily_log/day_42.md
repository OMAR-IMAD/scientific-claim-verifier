42\. Gün - Dashboard İstatistikleri API Endpoint Geliştirmesi



2026-09-01



Bugün Dashboard bölümünde kullanılacak analiz istatistiklerini API üzerinden erişilebilir hale getirdim.



Öncelikle schemas.py dosyasına DashboardStatsResponse modeli eklendi. Bu model toplam analiz sayısı ile ENTAILMENT, CONTRADICTION ve NEUTRAL sonuçlarının sayılarını döndürecek şekilde hazırlandı.



Daha sonra main.py dosyasına /dashboard/stats endpointi eklendi. Endpoint sadece giriş yapmış kullanıcının istatistiklerini döndürecek şekilde get\_current\_user ile koruma altına alındı. Day 41'de oluşturulan get\_analysis\_stats\_by\_user fonksiyonu bu endpoint ile kullanıldı.



Yeni endpoint için test\_api.py dosyasına bir API testi eklendi. Testte doğru kullanıcı id değerinin kullanıldığı, HTTP 200 cevabı döndüğü ve istatistiklerin doğru şekilde geldiği kontrol edildi.



Yeni test tek başına başarılı geçti. test\_api.py içerisindeki toplam 43 test başarılı oldu. Projenin tamamında ise toplam 82 test başarılı geçti. Ayrıca git diff --check kontrolünde herhangi bir biçimlendirme hatası bulunmadı.



Sonuç:

Dashboard istatistikleri için yeni API endpointi oluşturuldu.

Endpoint kullanıcı bazlı ve güvenli hale getirildi.

DashboardStatsResponse modeli eklendi.

Yeni API testi başarılı tamamlandı.

Projenin tamamında 82 test başarılı geçti.



Sonraki Gün İçin Plan



Dashboard istatistikleri ve API testlerini geliştirmeye devam etmek.

