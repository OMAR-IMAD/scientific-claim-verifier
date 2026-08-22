32\. Gün - Kullanıcının Analiz Geçmişinin Görüntülenmesi



2026-08-22



Bugün kullanıcıların daha önce yaptığı analizleri görüntüleyebilmesi için analiz geçmişi özelliği üzerinde çalıştım.



Öncelikle AnalysisResponse şemasını ekledim. Bu şema analiz id, premise, hypothesis, prediction, confidence, sınıf skorları ve oluşturulma tarihini içeriyor.



Daha sonra /history endpointini oluşturdum. Endpoint JWT ile korundu ve sadece giriş yapan kullanıcının kendi analizlerini getirecek şekilde get\_analyses\_by\_user fonksiyonu ile ilişkilendirildi.



Analiz geçmişi için başarılı erişim ve token olmadan erişim senaryolarını test eden yeni API testleri ekledim.



Son olarak tüm proje testlerini çalıştırdım ve 68 test başarıyla geçti. git diff --check kontrolünde herhangi bir biçimlendirme hatası bulunmadı.



Sonuç:



/history endpointi oluşturuldu.

Analiz geçmişi kullanıcı hesabı ile ilişkilendirildi.

AnalysisResponse şeması eklendi.

JWT koruması doğrulandı.

Yeni history testleri başarıyla geçti.

Toplam 68 proje testi başarılı oldu.



Sonraki Gün İçin Plan



Analiz geçmişi üzerinde detay görüntüleme ve diğer geçmiş işlemleri için backend geliştirmelerine devam etmek.

