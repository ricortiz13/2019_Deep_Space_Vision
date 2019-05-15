import numpy as np
import cv2
import FalconEyeMap

# Creates a capture from the specified camera or file
cap = cv2.VideoCapture(1)

while 1:
    _, frame = cap.read()
    
    # Converts frame to grayscale
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Converts grayscale to binary image
    _, thresh = cv2.threshold(grayscale, FalconEyeMap.LOWER_BRIGHTNESS, FalconEyeMap.UPPER_BRIGHTNESS, 0)
   
    # Finds the contours of everything within the brightness threshold
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # First check: ensures there are at least two contours
    contoursLen = len(contours)
    i = 0
    if len(contours) >= 2:
        while i < contoursLen:
            currContour = contours[i]
            if cv2.contourArea(currContour) < FalconEyeMap.CONTOUR_SIZE_THRESHOLD:
                del contours[i]
                i-=1
                contoursLen-=1
            else:
                rect = cv2.minAreaRect(currContour)
                print(rect[1])
            i+=1

    cv2.imshow("frame", frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()