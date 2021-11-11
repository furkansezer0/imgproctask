import cv2
import numpy as np
from matplotlib import pyplot as plt

lower_yellow = np.array([0,42,0])
upper_yellow = np.array([30,255,255])

lower_blue = np.array([43,231,0])
upper_blue = np.array([135,255,255])

# reverse değişkeni 2 ayrı renk tespiti için kullanılmıştır. 
# Eğer reverse = False ise fonksiyon sarı renkleri tespit edecektir.
# Eğer reverse = True ise fonksiyon mavi rengi tespit edip tersini alacaktır.
def YellowFishFinder(lower_thresh, upper_thresh, reverse):
    
    resim = cv2.imread("resim2.jpg")

    hsv = cv2.cvtColor(resim, cv2.COLOR_BGR2HSV)

    kernel = np.ones((3,3), np.uint8)
    
    if reverse == False:
        mask = cv2.inRange(hsv, lower_thresh, upper_thresh)
        mask = cv2.dilate(mask, kernel, iterations=2)
        method = "1. Yöntem"
    else:
        mask = cv2.inRange(hsv, lower_thresh, upper_thresh)
        mask = cv2.bitwise_not(mask)
        method = "2. Yöntem"

    res = cv2.bitwise_and(resim,resim, mask= mask)
    
    # Maskelerdeki beyaz ve siyah renklerin pixel miktarı
    number_of_white_pix = np.sum(mask == 255)
    number_of_black_pix = np.sum(mask == 0)
    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(resim, contours, -1, (0,255,0),2,)

    

    # beyaz piksel / toplam piksel oranı işlemi ile tespit edilen rengin oranı
    
    print(f"{method} \n Sarı piksel sayısı: {number_of_white_pix}",
          f"\n Toplam piksel sayısı: {number_of_white_pix + number_of_black_pix}", 
          f"\n Sarı renk piksel oranı: {number_of_white_pix/(number_of_white_pix+number_of_black_pix)}",
          f"\n Toplam sarı balık sayısı: {len(contours)}")


    outputs= [resim, mask, res]

    plt.figure(method)
    for i in range(len(outputs)):
        plt.subplot(1,len(outputs),i+1)
        if i != 1:
            plt.imshow(outputs[i][:,:,::-1])
        else:
            plt.imshow(outputs[i], cmap='gray')
        plt.xticks([]), plt.yticks([])

YellowFishFinder(lower_yellow, upper_yellow, reverse=False)
YellowFishFinder(lower_blue, upper_blue, reverse=True)


k = cv2.waitKey(0)
if k == ord("s"):
    print("Kapatıldı")     
    
cv2.destroyAllWindows()


