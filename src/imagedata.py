""" @file: imagedata.py
"""

import cv2
import FalconEyeMap

class ImageData(object):
    def __init__(self, cameraPort=0):
        self.camera = cv2.VideoCapture(cameraPort)
        self.frame = None
        self.thresh = None
        self.contours = []
        self.targetX = 0
        self.targetY = 0
    
    def __del__(self):
        self.camera.release()

    def getFrame(self):
        _, self.frame = self.camera.read()
        grayscale = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        _, self.thresh = cv2.threshold(grayscale, FalconEyeMap.LOWER_BRIGHTNESS, FalconEyeMap.UPPER_BRIGHTNESS, 0)

if __name__ == '__main__':
    import time

    imData = ImageData(0)
    imData.getFrame()

    time.sleep(5)

    exit()

    