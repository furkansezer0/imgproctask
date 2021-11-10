import cv2
import numpy as np

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('sarıbalık1.mp4')

kernel= np.ones((3,3), np.uint8)

lower_yellow = np.array([20,75,0])
upper_yellow = np.array([72,255,255])

lower_blue = np.array([97,50,126])
upper_blue = np.array([125,147,222])

biggestCon = 0
biggestConIndex = 0

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
      
    gauss = cv2.GaussianBlur(frame, (3,3), 0)
    hsvFrame = cv2.cvtColor(gauss, cv2.COLOR_BGR2HSV)
    maskYellow = cv2.inRange(hsvFrame, lower_yellow, upper_yellow)    
    #maskYellow = cv2.morphologyEx(maskYellow, cv2.MORPH_OPEN, kernel, iterations=2)
    maskYellow = cv2.dilate(maskYellow, kernel, iterations=4)
    
    
    maskBlue = cv2.inRange(hsvFrame, lower_blue, upper_blue)
    #maskBlue = cv2.morphologyEx(maskBlue, cv2.MORPH_OPEN, kernel, iterations=8)
    maskBlue = cv2.erode(maskBlue, kernel, iterations=4)
    maskBlue = cv2.dilate(maskBlue, kernel, iterations=12)
    
    
    
    maskFrame = cv2.bitwise_or(maskYellow, maskBlue)
    
    resFrame = cv2.bitwise_and(gauss, gauss, mask= maskFrame)

    contours, hierarchy = cv2.findContours(maskFrame, cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_NONE)
    
    contour = max(contours, key = cv2.contourArea)
    
    print(contour)
    
    cv2.drawContours(resFrame, contours,-1, (0,255,0),2)
    
    # Display the resulting frame
    cv2.imshow('Result Frame', resFrame)

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  # Break the loop
  else: 
    break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
