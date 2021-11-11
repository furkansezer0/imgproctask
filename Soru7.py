import cv2
import numpy as np


cap = cv2.VideoCapture("auv1.mp4")

lower_yellow = np.array([0,95,0])
upper_yellow = np.array([58,255,255])


# 8 ayrı yöne göre yön tespit fonksiyonu
def directionFinder(cx,cy, height, width):
    
    fx= width/2 
    fy= height/2
    
    # 20 değeri tolerans aralığı olarak belirlenmiştir
    if fy > cy and abs(cx - fx) <= 20:
        print("Kuzey")
    elif fy > cy and abs(cx - fx) > 20 and cx - fx > 0:
        print("Kuzeydoğu")
    elif cx > fx and abs(cy - fy) <= 20:
        print("Doğu")
    elif cy > fy and abs(cx - fx) > 20 and cx - fx > 0:
        print("Güneydoğu")
    elif cy > fy and abs(cx - fx) <= 20:
        print("Güney")
    elif cy > fy and abs(cx - fx) > 20 and fx - cx > 0:
        print("Güneybatı")
    elif fx > cx and abs(cy - fy) <= 20:
        print("Batı")
    elif fy > cy and abs(cx - fx) > 20 and fx - cx > 0:
        print("Kuzeybatı")
    else:
        print("Tanımlanmayan Yön")
    

if cap.isOpened()== False:
    print("Error opening video stream or file")

while cap.isOpened():
    
    ret, frame = cap.read()
    if ret == True:
        
        height = frame.shape[0]
        width = frame.shape[1]
             
        gauss = cv2.GaussianBlur(frame, (3,3), 0)
        hsvFrame = cv2.cvtColor(gauss, cv2.COLOR_BGR2HSV)
        maskFrame = cv2.inRange(hsvFrame, lower_yellow, upper_yellow)
        
        resFrame = cv2.bitwise_and(gauss, gauss, mask= maskFrame)
    
        contours, hierarchy = cv2.findContours(maskFrame, cv2.RETR_TREE, 
                                               cv2.CHAIN_APPROX_NONE)
        
        # En büyük kontür tespiti
        contour = max(contours, key = cv2.contourArea)
        
        cv2.drawContours(resFrame, contour,-1, (0,255,0),2)
        
        
        # Bulunan en büyük kontürün merkezinin tespiti ve merkeze nokta çizimi
        M = cv2.moments(contour)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(resFrame, (cx, cy), 7, (0, 0, 255), -1)              
        
        # Ekranın ortasına nokta çizimi
        cv2.circle(resFrame, (int(width/2),int(height/2)), radius=7, color=(0, 0, 255), thickness=-1)
        
        directionFinder(cx, cy, height, width)
        
        cv2.imshow('Result Frame', resFrame)
    
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    
    else: 
        break

cap.release()

cv2.destroyAllWindows()
    

