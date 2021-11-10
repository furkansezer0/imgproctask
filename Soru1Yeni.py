import cv2
import numpy as np
from matplotlib import pyplot as plt

resim = cv2.imread("resim1.jpg")

griresim = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(resim, cv2.COLOR_BGR2HSV)

kernel = np.ones((3,3), np.uint8)

lower_orange = np.array([0,180,100])
upper_orange = np.array([22,255,255])

lower_white = np.array([20, 0, 204])
upper_white = np.array([128, 126, 255])



mask1 = cv2.inRange(hsv, lower_orange, upper_orange)
opening = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel, iterations=4)
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=8)
mask1= closing


mask2 = cv2.inRange(hsv, lower_white, upper_white)
erosion2 = cv2.erode(mask2, kernel, iterations=4)
dilation2 = cv2.dilate(erosion2, kernel, iterations=16)
closing2 = cv2.morphologyEx(dilation2, cv2.MORPH_CLOSE, kernel, iterations=16)
mask2= closing2
mask = cv2.bitwise_or(mask1, mask2)
    
res = cv2.bitwise_and(resim,resim, mask= mask)

contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_NONE)

firstFish = sorted(contours, key=cv2.contourArea, reverse=True)[0]
print(f"First Fish Area: {firstFish.size}")

secondFish = sorted(contours, key=cv2.contourArea, reverse=True)[1]
print(f"Second Fish Area: {secondFish.size}")


cv2.drawContours(res, firstFish,-1, (0,255,0),2)
cv2.drawContours(res, secondFish,-1, (0,255,0),2)

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