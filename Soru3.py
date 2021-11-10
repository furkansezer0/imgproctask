import cv2
import numpy as np

resim3 = cv2.imread("resim3.jpg")
resim4 = cv2.imread("resim4.jpg")

lower_orange = np.array([0,132,0])
upper_orange = np.array([22,255,255])

lower_white = np.array([0, 0, 130])
upper_white = np.array([69, 255, 255])

lower_brown = np.array([0, 86, 0])
upper_brown = np.array([22, 255, 123])

def checkCoralColor(resim):
    
    
    status = ['Saglikli', 'Agarmis', 'Olmus']
    
    hsv = cv2.cvtColor(resim , cv2.COLOR_BGR2HSV)

    height = resim.shape[0]
    width = resim.shape[1]

    halfLeftHSV = hsv[0:int(height), 0:int(width/2)]
    
    halfRightHSV = hsv[0:int(height), int(width/2 +10): width]
    
    LeftOrangeMask = cv2.inRange(halfLeftHSV, lower_orange, upper_orange)
    LeftOrangePixel = np.sum(LeftOrangeMask == 255)    
    LeftWhiteMask = cv2.inRange(halfLeftHSV, lower_white, upper_white)
    LeftWhitePixel = np.sum(LeftWhiteMask == 255)
    LeftBrownMask = cv2.inRange(halfLeftHSV, lower_brown, upper_brown)
    LeftBrownPixel = np.sum(LeftBrownMask == 255)
    if LeftOrangePixel > LeftWhitePixel and LeftOrangePixel > LeftBrownPixel:
        print("Soldaki Mercan Kolonisi Sağlıklı")
        cv2.putText(resim, status[0], (int(width/4),int(50)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
    elif LeftWhitePixel > LeftBrownPixel:
        print("Soldaki Mercan Kolonisi Ağarmış")
        cv2.putText(resim, status[1], (int(width/4),int(50)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        print("Soldaki Mercan Kolonisi Ölmüş")
        cv2.putText(resim, status[2], (int(width/4),int(50)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
    
    
    RightOrangeMask = cv2.inRange(halfRightHSV, lower_orange, upper_orange)
    RightOrangePixel = np.sum(RightOrangeMask == 255)   
    RightWhiteMask = cv2.inRange(halfRightHSV, lower_white, upper_white)
    RightWhitePixel = np.sum(RightWhiteMask == 255)
    RightBrownMask = cv2.inRange(halfRightHSV, lower_brown, upper_brown)
    RightBrownPixel = np.sum(RightBrownMask == 255)
    if LeftOrangePixel > RightOrangePixel and RightWhitePixel > RightOrangePixel and RightWhitePixel > RightBrownPixel:
        print("Sağdaki Mercan Kolonisi Ağarmış")
        cv2.putText(resim, status[1], (int(3*width/4),int(50)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
    elif RightBrownPixel > RightWhitePixel:
        print("Sağdaki Mercan Kolonisi Ölmüş")
        cv2.putText(resim, status[2], (int(3*width/4),int(50)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        print("Sağdaki Mercan Kolonisi Sağlıklı")
        cv2.putText(resim, status[0], (int(3*width/4),int(50)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
    
    cv2.imshow(f"{resim}", resim)

    

checkCoralColor(resim3)
checkCoralColor(resim4)


k = cv2.waitKey(0)

if k == ord('q'):
    print("Kapatıldı")
    
cv2.destroyAllWindows()
    
