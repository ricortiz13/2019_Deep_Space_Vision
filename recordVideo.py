import cv2
import numpy
import os

cap = cv2.VideoCapture(0)

# Get the default resolutions of the frame
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Create a VideoWriter
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

while(1):
    _, frame = cap.read()

    # Write the frame into the file 'output.avi'
    out.write(frame)

    # Display the frame
    cv2.imshow('frame', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
out.release()

cv2.destroyAllWindows()