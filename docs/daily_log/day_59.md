59\. Gün - Dashboard İstatistikleri



2026-09-18



Bugün Frontend tarafına Dashboard bölümü eklendi.



Backend üzerinde bulunan /dashboard/stats endpointi kontrol edildi. Bu endpointin giriş yapan kullanıcıya ait toplam analiz sayısını ve Entailment, Neutral ve Contradiction istatistiklerini döndürdüğü doğrulandı.



api.js dosyasına getDashboardStats fonksiyonu eklendi. Bu fonksiyon access token kullanarak Dashboard verilerini Backend üzerinden aldı.



App.jsx dosyasına dashboardStats, dashboardLoading ve dashboardError durumları eklendi.



Kullanıcı giriş yaptıktan sonra Dashboard istatistiklerinin otomatik olarak yüklenmesi sağlandı.



Dashboard üzerinde Total Analyses, Entailment, Neutral ve Contradiction bilgileri kartlar halinde gösterildi. Her kategori için analiz sayısı ve yüzde değeri gösterildi.



App.css dosyasına Dashboard kartları için yeni stiller eklendi ve mobil ekranlar için responsive yapı oluşturuldu.



Yeni bir analiz yapıldığında Dashboard istatistiklerinin sayfa yenilenmeden otomatik olarak güncellenmesi sağlandı.



Frontend kodu ESLint ile kontrol edildi ve hata bulunmadı. Production build testi başarıyla tamamlandı.



Backend ve Frontend birlikte çalıştırılarak özellik tarayıcı üzerinde test edildi. Yeni analiz sonrasında toplam analiz sayısının ve kategori istatistiklerinin doğru şekilde güncellendiği doğrulandı.



Sonuç:

Dashboard istatistik bölümü başarıyla eklendi.

Toplam analiz sayısı gösterildi.

Entailment, Neutral ve Contradiction sayıları ve yüzdeleri gösterildi.

Yeni analiz sonrası Dashboard otomatik olarak güncellendi.

ESLint ve production build testleri başarıyla geçti.



Sonraki Gün İçin Plan



Dashboard bölümünü geliştirmeye ve kullanıcı için ek istatistik ve yönetim özellikleri eklemeye devam etmek.
