39\. Gün - Analiz Geçmişi Sıralama Özelliği



2026-08-29



Bugün analiz geçmişi için sıralama özelliği üzerinde çalıştım.



Öncelikle get\_analyses\_by\_user fonksiyonuna sort\_order parametresi eklendi. Kullanıcının analiz geçmişini en yeniden en eskiye veya en eskiden en yeniye sıralayabilmesi sağlandı.



Daha sonra /history endpointine sort\_order parametresi eklendi. Bu parametre için newest ve oldest değerleri desteklendi ve varsayılan değer newest olarak belirlendi.



Mevcut API testleri yeni sort\_order parametresine uyumlu hale getirildi. Testlerde kullanılan sahte get\_analyses\_by\_user fonksiyonları güncellendi ve oluşan parametre uyumsuzlukları giderildi.



Kontroller sonucunda test\_api.py dosyasındaki 42 test başarılı geçti. Projenin tamamında ise toplam 79 test başarılı oldu. git diff --check kontrolünde herhangi bir biçimlendirme hatası bulunmadı.



Sonuç:

Analiz geçmişine sıralama desteği eklendi.

newest ve oldest sıralama seçenekleri oluşturuldu.

API testleri yeni parametreye göre güncellendi.

Toplam 79 proje testi başarılı geçti.



Sonraki Gün İçin Plan



Analiz geçmişi özelliklerini geliştirmeye devam etmek.

