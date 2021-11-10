import cv2
import numpy as np
from matplotlib import pyplot as plt

resim = cv2.imread("resim2.jpg")

height = resim.shape[0]
width = resim.shape[1]

hsv = cv2.cvtColor(resim, cv2.COLOR_BGR2HSV)


kernel = np.ones((3,3), np.uint8)

lower_yellow = np.array([0,44,120])
upper_yellow = np.array([30,255,255])

mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
dilation = cv2.dilate(mask, kernel, iterations=2)
mask = dilation

res = cv2.bitwise_and(resim,resim, mask= mask)

number_of_white_pix = np.sum(mask == 255)
number_of_black_pix = np.sum(mask == 0)

print("Sarı renk piksel oranı: ",number_of_white_pix/(number_of_white_pix+number_of_black_pix))

contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_NONE)



print("Toplam sarı balık sayısı: ",len(contours))

outputs= [resim, mask, res]


for i in range(len(outputs)):
    plt.subplot(1,len(outputs),i+1)
    if i != 1:
        plt.imshow(outputs[i][:,:,::-1])
    else:
        plt.imshow(outputs[i], cmap='gray')
    plt.xticks([]), plt.yticks([])


k = cv2.waitKey(0)
if k == ord("s"):
    print("Kapatıldı")     
    
cv2.destroyAllWindows()