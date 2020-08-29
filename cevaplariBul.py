import cv2
import numpy as np
import pandas as pd


class CevaplariBul:
    def __init__(self, img):
        self.img = img
        self.cevapAlani = self.img[40:470, 70:460]

    def cevaplariListele(self, esikAyar=100, bulanikFirca=19):
        blur = cv2.GaussianBlur(self.cevapAlani, (bulanikFirca, bulanikFirca), 0)
        gri = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        esik = cv2.threshold(gri, esikAyar, 255, cv2.THRESH_BINARY_INV)[-1]
        cevapRects = self.__cevaplariBol(esik, satirSayisi=13, sutunSayisi=10)
        return cevapRects

    def __cevaplariBol(self, esikCevapAlani, satirSayisi, sutunSayisi):
        h, w = esikCevapAlani.shape
        parca = int(h / satirSayisi)
        soruNumarasi = 0
        cevapKoordinatlari = []
        s = 0
        for j in range(0, satirSayisi):
            for i in range(0, sutunSayisi):
                s = s + 1
                if i >= 5:
                    basX = 215 + (i % 5) * parca
                    soruNumarasi = (j + 1) + satirSayisi
                else:
                    soruNumarasi = (j + 1)
                    basX = i * parca

                basY = j * parca
                bitX = basX + parca
                bitY = basY + parca
                pt1 = (basX, basY)
                pt2 = (bitX, bitY)
                cevap = self.__cevapHarf(i)
                roi = esikCevapAlani[basY:bitY, basX:bitX]

                isaretli = self.__cevapKontrolEt(roi)
                # print(s, (basY, bitY), (basX, bitX))
                cevapKoordinatlari.append(
                    {"koordinat": (pt1, pt2), "sorunumarasi": soruNumarasi, "isaretli": isaretli, "cevap": cevap})

                if isaretli == True:
                    cv2.rectangle(self.cevapAlani, pt1, pt2, (255, 255, 255), 2)

                ############### Test İşlemleri İçin ######################
                # self.__testContour(s,24,roi,pt1,pt2)

        cv2.imshow("resim", self.cevapAlani)

        c = pd.DataFrame(cevapKoordinatlari)
        return c.query("isaretli == True").sort_values(by=['sorunumarasi'])

    def __cevapKontrolEt(self, roi):

        sonuc = False
        contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # ne olur ne olmaz diye konturleri siralayip en buyuk olani bulalim
        if len(contours) > 0:
            kontorler = sorted(contours, key=cv2.contourArea, reverse=True)
            kontur = kontorler[0]  # alani en buyuk kontor
            if (cv2.contourArea(kontur) > 130):
                sonuc = True
        else:
            sonuc = False
        return sonuc

    def __cevapHarf(self, sayi):
        cevaplar = ["a", "b", "c", "d", "e"]
        return cevaplar[sayi % 5]

    def __resimAydinlat(self, orjResim, value=10):
        hsv = cv2.cvtColor(orjResim, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        final_hsv = cv2.merge((h, s, v))
        return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    def __testContour(self, sira,numara, roi, pt1, pt2):
        if sira == numara:
            # cv2.rectangle(self.cevapAlani, pt1, pt2, (255, 255, 255), 2)
            contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                kontorler = sorted(contours, key=cv2.contourArea, reverse=True)
                kontur = kontorler[0]  # alani en buyuk kontor
                print(cv2.contourArea(kontur))

            cv2.imshow("roi", roi)
