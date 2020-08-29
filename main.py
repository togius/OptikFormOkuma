from kosetespit import KoseTespit
from cevaplariBul import CevaplariBul
import cv2


def Isaretliler(resim):
    koseTespit = KoseTespit(resim)
    yamuk = koseTespit.kirp()
    cb = CevaplariBul(yamuk)
    return cb.cevaplariListele(esikAyar=100, bulanikFirca=19)

if __name__ == '__main__':
    print(Isaretliler('resimler/c3.jpg'))

cv2.waitKey(0)
cv2.destroyAllWindows()


