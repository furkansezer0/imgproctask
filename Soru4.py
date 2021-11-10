import cv2
import numpy as np


cap = cv2.VideoCapture('denizanası1.mp4')

lower_bluewhite = np.array([0,0,75])
upper_bluewhite = np.array([179,255,255])

biggestCon = 0
biggestConIndex = 0

if (cap.isOpened()== False): 
  print("Error opening video stream or file")

while(cap.isOpened()):

  ret, frame = cap.read()
  if ret == True:
      
    gauss = cv2.GaussianBlur(frame, (3,3), 0)
    hsvFrame = cv2.cvtColor(gauss, cv2.COLOR_BGR2HSV)
    maskFrame = cv2.inRange(hsvFrame, lower_bluewhite, upper_bluewhite)
    
    resFrame = cv2.bitwise_and(gauss, gauss, mask= maskFrame)

    contours, hierarchy = cv2.findContours(maskFrame, cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_NONE)
    
    contour = max(contours, key = cv2.contourArea)
    
    
    cv2.drawContours(resFrame, contour,-1, (0,255,0),2)
    
    cv2.imshow('Result Frame', resFrame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
      break


  else: 
    break

cap.release()

cv2.destroyAllWindows()