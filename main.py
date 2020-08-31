from kosetespit import KoseTespit
from cevaplariBul import CevaplariBul
import cv2
import time

def Isaretliler(resim):
    koseTespit = KoseTespit(resim)
    yamuk = koseTespit.kirp()
    cb = CevaplariBul(yamuk)
    return cb.cevaplariListele(esikAyar=100, bulanikFirca=19)

if __name__ == '__main__':
    bas = time.time()
    print(Isaretliler('resimler/c18.jpg'))
    bit = time.time()
    print(bit-bas)

cv2.waitKey(0)
cv2.destroyAllWindows()


