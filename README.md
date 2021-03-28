# OptikFormOkuma
26 Soruluk Test Kağıdını Okuma.

Proje çalışma basamakları:
1. Test kağıdı üzerindeki 4 tane karenin referans alınarak kırpılması.
2. Bu (kare) referans noktalarının merkezlerini kullanarak kağıdın perspektifinin oluşturuşması ve kağıdın 500x500 boyutlarına getirilmesi.
3. Roi (Region Of Interest) şeklinde (500 px / 13 satır) şeklinde karelere böldüm. 
4. 2. sütunda roileri alırken 5. kareden sonrasında 215pikselden başlattım ki 2. sutun cevaplarını alsın
5. Alınan her roide kontur taraması yaptım ve kontur alanını max kontur alanına göre soru işaretli mi değil mi belirledim.
6. Pandas ile işaretli olanları sıraladım.

Not: Yuvarlaklar tam dolacak şekilde işaretlenirse sistem gayet başarılı okuyor.

