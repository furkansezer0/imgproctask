import cv2
import numpy as np

cap = cv2.VideoCapture('sarıbalık1.mp4')

kernel= np.ones((3,3), np.uint8)

lower_yellow = np.array([20,75,0])
upper_yellow = np.array([72,255,255])

lower_blue = np.array([97,50,126])
upper_blue = np.array([125,147,222])

if (cap.isOpened()== False): 
  print("Error opening video stream or file")

while(cap.isOpened()):

  ret, frame = cap.read()
  if ret == True:
      
    gauss = cv2.GaussianBlur(frame, (3,3), 0)
    hsvFrame = cv2.cvtColor(gauss, cv2.COLOR_BGR2HSV)
    maskYellow = cv2.inRange(hsvFrame, lower_yellow, upper_yellow)    
    maskYellow = cv2.dilate(maskYellow, kernel, iterations=4)
    
    
    maskBlue = cv2.inRange(hsvFrame, lower_blue, upper_blue)
    maskBlue = cv2.erode(maskBlue, kernel, iterations=4)
    maskBlue = cv2.dilate(maskBlue, kernel, iterations=12)
    
    
    maskFrame = cv2.bitwise_or(maskYellow, maskBlue)
    
    resFrame = cv2.bitwise_and(gauss, gauss, mask= maskFrame)

    contours, hierarchy = cv2.findContours(maskFrame, cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_NONE)
    
    # En büyük kontürün tespiti
    contour = max(contours, key = cv2.contourArea)
    
    cv2.drawContours(resFrame, contours,-1, (0,255,0),2)
    
    cv2.imshow('Result Frame', resFrame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  else: 
    break

cap.release()

cv2.destroyAllWindows()
