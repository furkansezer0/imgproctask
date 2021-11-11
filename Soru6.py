import cv2
import numpy as np

cap = cv2.VideoCapture('kaplumbaga1.mp4')

kernel = np.ones((3,3), np.uint8)

lower_bluewhite = np.array([25,85,89])
upper_bluewhite = np.array([179,255,255])

if (cap.isOpened()== False): 
  print("Error opening video stream or file")

while(cap.isOpened()):
    
  ret, frame = cap.read()
  if ret == True:
      
    gauss = cv2.GaussianBlur(frame, (3,3), 0)
    hsvFrame = cv2.cvtColor(gauss, cv2.COLOR_BGR2HSV)
    maskFrame = cv2.inRange(hsvFrame, lower_bluewhite, upper_bluewhite)
    # bitwise_not() işlemi ile yapılabilecek işlemin threshold ile yapılması
    ret,thresh = cv2.threshold(maskFrame,127,255,cv2.THRESH_BINARY_INV)
    maskFrame = thresh
    maskFrame = cv2.dilate(maskFrame, kernel, iterations=4)
    
    resFrame = cv2.bitwise_and(gauss, gauss, mask= maskFrame)

    contours, hierarchy = cv2.findContours(maskFrame, cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_NONE)
    
    contour = max(contours, key = cv2.contourArea)
    
    print(contour)
    
    cv2.drawContours(resFrame, contour,-1, (0,255,0),2)    

    cv2.imshow('Result Frame', resFrame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  else: 
    break

cap.release()

cv2.destroyAllWindows()
