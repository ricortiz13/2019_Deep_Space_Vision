import cv2
import numpy as np
import os
import FalconEyeMap

# Changes the camera settings
os.system("v4l2-ctl --set-ctrl=contrast=4")
os.system("v4l2-ctl --set-ctrl=brightness=4")
os.system("v4l2-ctl --set-ctrl=saturation=4")
os.system("v4l2-ctl --set-ctrl=gain=-4")

# Creates a capture from the specified camera or file
cap = cv2.VideoCapture(0)

# Variables for the brightness threshold
lower_brightness = 200
upper_brightness = 255

# Variables for the color threshold
# lower_color = numpy.array([30, 175, 69])
# upper_color = numpy.array([124, 255, 245])

# Color threshold for testing
lower_color = numpy.array([0, 0, 0])
upper_color = numpy.array([255, 255, 255])

while(1):
    _, frame = cap.read()

    # Converts BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Thresholds the HSV image
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # Converts frame to grayscale
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    # Sets the threshold for what brightness objects of interest must be
    _, thresh = cv2.threshold(gray, lower_brightness, upper_brightness, 0)
    # Finds the contours of everything within the brightness threshold
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(frame, contours, -1, (0,255,0), 3)

    # If there are any contours, finds the center of each and draws rectangles around them
    if(len(contours) > 0):
        for i in contours:
            if(cv2.contourArea(i) > 50):
                # Finds the center of the contour
                M = cv2.moments(i)
                cX = int(M['m10'] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Draws a dot in the center of the contour
                cv2.circle(frame, (cX,cY), 5, (0,0,255), -1)

                # Draws a rotated rectangle around the contour
                rect = cv2.minAreaRect(i)
                box = cv2.boxPoints(rect)
                box = numpy.int0(box)
                cv2.drawContours(frame, [box], 0, (0,0,255), 2)

    cv2.imshow("res", res)
    cv2.imshow("frame", frame)
    cv2.imshow("thresh", thresh)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()