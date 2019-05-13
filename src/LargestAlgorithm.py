import numpy as np
import cv2
import FalconEyeMap
import time

# Creates a capture from the specified camera or file
cap = cv2.VideoCapture('../target_samples/field_panel_2_rocket.avi')

distance = None

while(1):
    # Slows video to 10 fps
    time.sleep(0.1)

    _, frame = cap.read()

    tickCount1 = cv2.getTickCount()

    # Converts frame to grayscale, then to a binary image
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(grayscale, FalconEyeMap.LOWER_BRIGHTNESS, FalconEyeMap.UPPER_BRIGHTNESS, 0)

    # Stores the number of rows and columns in thresh
    rows = thresh.shape[0]
    cols = thresh.shape[1]

    # Finds the contours within the brightness threshold
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filters out contours with small areas
    i = 0
    contoursLen = len(contours)
    while i < contoursLen:
        currContour = contours[i]
        if cv2.contourArea(currContour) < FalconEyeMap.CONTOUR_SIZE_THRESHOLD:
            del contours[i]
            i-=1
            contoursLen-=1
        i+=1

    if len(contours) >= 2:
        # Sorts contours from largest to smallest
        sortedContours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        # Stores the two largest contours
        largestTarget = sortedContours[0]
        secondLargestTarget = sortedContours[1]

        # Draws the two largest targets
        largestRect = cv2.minAreaRect(largestTarget)
        largestBox = cv2.boxPoints(largestRect)
        largestBox = np.int0(largestBox)
        secondLargestRect = cv2.minAreaRect(secondLargestTarget)
        secondLargestBox = cv2.boxPoints(secondLargestRect)
        secondLargestBox = np.int0(secondLargestBox)
        cv2.drawContours(frame, [largestBox], 0, (0,0,255), 2)
        cv2.drawContours(frame, [secondLargestBox], 0, (0,0,255), 2)

        # Stores centers of targets and center of frame
        largestRectCX = largestRect[0][0]
        largestRectCY = largestRect[0][1]
        secondLargestRectCX = secondLargestRect[0][0]
        secondLargestRectCY = secondLargestRect[0][1]
        frameCenterX = int(cols / 2)

        # Calculates midpoint of targets and distance between midpoint and center of frame
        midpointX = int((largestRectCX + secondLargestRectCX) / 2)
        midpointY = int((largestRectCY + secondLargestRectCY) / 2)
        distance = abs(int(frameCenterX - midpointX))

        # Draws a line from midpoint to center of frame
        cv2.line(frame, (midpointX, midpointY), (frameCenterX, midpointY), (0,0,255), 3)

    # Draws a vertical line in the center of frame
    cv2.line(frame, (frameCenterX, 0), (frameCenterX, rows), (0,255,0), 3)

    tickCount2 = cv2.getTickCount()
    timeElapsed = (tickCount2 - tickCount1) / cv2.getTickFrequency()
    print(timeElapsed)

    # Displays frame and thresh
    cv2.imshow("frame", frame)
    cv2.imshow("thresh", thresh)

    # Closes the program if Esc is pressed
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()