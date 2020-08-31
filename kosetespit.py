import cv2
import imutils
import numpy as np

class KoseTespit:
    def __init__(self, resim=""):
        self.img = cv2.imread(resim)
        self.img = imutils.resize(self.img, height=800, width=600)
        pass

    def __koseleriSirala(self, pts):
        '''
        koordinatları sıralamalıyız
        nokta1: sol üst, nokta2: sag ust, nokta3:sag alt, nokta4: sol alt
        '''
        rect = np.zeros((4, 2), dtype="float32")
        # sol ust toplaması en küçük olandır. sag alt ise en buyuk olandir.
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        # fark değeri en küçük olan sag ust, en buyuk olan sag alttir
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    def __ayarlanmis(self, img, corners):
        pts = np.array([list([int(x), int(y)]) for x, y in corners])
        rect = self.__koseleriSirala(pts)

        # np.arra().ravel() foksiyonu bize x,y diye iki değer döndürüyor daha doğrusu dizi elemanlarını ayrı ayrı
        xEnBuyuk, yEnBuyuk = np.max(pts, axis=0).ravel()
        xEnKucuk, yEnKucuk = np.min(pts, axis=0).ravel()

        persGenislik = xEnBuyuk - xEnKucuk
        persYukseklik = xEnBuyuk - xEnKucuk

        dst = np.array([
            [0, 0],
            [persGenislik - 1, 0],
            [persGenislik - 1, persYukseklik - 1],
            [0, persYukseklik - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(img, M, (persGenislik, persYukseklik))
        return warped

    def __konturBul(self):
        blur = cv2.GaussianBlur(self.img, (17, 17), 0)
        gri = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        _,kenar = cv2.threshold(gri,100,255,cv2.THRESH_BINARY_INV)
        # kenar = cv2.Canny(gri, 25, 100)
        # kenar = cv2.Canny(gri, 25, 150)

        kernel = np.ones((11, 11), np.uint8) / 255
        genisleme = cv2.erode(kenar, kernel, iterations=1)

        konturlar, hiyerarsi = cv2.findContours(genisleme.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        konturlar = sorted(konturlar, key=cv2.contourArea, reverse=True)
        return konturlar

    def kirp(self):
        konturlar = self.__konturBul()
        koseler = []

        if len(konturlar) >= 4:
            konturlar = konturlar[0:4]
            #kontur kare seklindeyse
            for kontur in konturlar:
                (x, y), yariCap = cv2.minEnclosingCircle(kontur)
                cv2.circle(self.img, (int(x), int(y)), radius=int(yariCap), color=(0, 255, 0), thickness=2)

                koseler.append((x, y))
            # corners = np.array(koseler, dtype="float32")
            yamuk = self.__ayarlanmis(self.img, koseler)
            yamuk = imutils.resize(yamuk,width=500,height=500)
            return yamuk
        else:
            print(len(konturlar))