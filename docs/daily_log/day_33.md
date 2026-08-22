33\. Gün - Analiz Detayının Görüntülenmesi



2026-08-23



Bugün analiz geçmişindeki belirli bir kaydın detaylarını görüntüleme özelliği üzerinde çalıştım.



Öncelikle get\_analysis\_by\_id\_for\_user fonksiyonunu ekledim. Bu fonksiyon analiz id ve kullanıcı id bilgilerini birlikte kontrol ederek sadece ilgili kullanıcıya ait analizi döndürüyor.



Daha sonra /history/{analysis\_id} endpointini oluşturdum. Endpoint JWT ile korundu ve giriş yapan kullanıcının sadece kendi analiz detaylarına erişebilmesi sağlandı.



İstenen analiz bulunamadığında veya kullanıcıya ait olmadığında 404 hata cevabı eklendi.



Analiz detayının başarılı şekilde getirilmesi ve bulunamayan analiz için 404 dönmesi senaryolarını test eden yeni API testleri ekledim.



Kod dosyalarının syntax kontrolü başarılı oldu. API testlerinde 33 test, tüm proje testlerinde ise 70 test başarıyla geçti. git diff --check kontrolünde herhangi bir biçimlendirme hatası bulunmadı.



Sonuç:



/history/{analysis\_id} endpointi oluşturuldu.

Kullanıcıya ait analiz detayları görüntülenebilir hale geldi.

Başka kullanıcıların analizlerine erişim engellendi.

404 hata kontrolü eklendi.

Yeni analiz detay testleri başarıyla geçti.

Toplam 70 proje testi başarılı oldu.



Sonraki Gün İçin Plan



Kullanıcının kendi analiz geçmişindeki bir kaydı silebilmesi için silme işlemi üzerinde çalışmaya başlamak.

