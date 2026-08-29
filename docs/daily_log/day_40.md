40\. Gün - Analiz Geçmişi Sıralama Testlerinin Geliştirilmesi



2026-08-30



Bugün analiz geçmişindeki sıralama özelliğinin testlerini geliştirdim.



Öncelikle get\_analyses\_by\_user fonksiyonunun oldest sıralama seçeneği için yeni bir CRUD testi eklendi. Test içerisinde iki farklı analiz oluşturuldu ve sort\_order="oldest" kullanıldığında ilk oluşturulan analizin önce döndüğü kontrol edildi.



Yeni test tek başına çalıştırıldı ve başarılı geçti. Daha sonra test\_crud.py dosyasındaki tüm testler çalıştırıldı ve toplam 4 test başarılı oldu.



Son olarak projenin tüm testleri tekrar çalıştırıldı. Yeni eklenen test ile birlikte toplam test sayısı 80'e çıktı ve tüm testler başarılı geçti. git diff --check kontrolünde herhangi bir biçimlendirme hatası bulunmadı.



Sonuç:

oldest sıralama davranışı CRUD seviyesinde test edildi.

Yeni sıralama testi başarıyla tamamlandı.

test\_crud.py içerisindeki 4 test başarılı geçti.

Projenin tamamında toplam 80 test başarılı oldu.



Sonraki Gün İçin Plan



Analiz geçmişi özelliklerinin test kapsamını geliştirmeye devam etmek.

