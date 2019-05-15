""" @file: falconthreads.py
    @class: FalconThreads
    @description:
    
"""
import threading
import cv2

from imagedata import ImageData 
from imageprocessor import ImageProcessor
from imageprocessing import BasicAlgorithm
from imageprocessing import AdvancedAlgorithm

import FalconEyeMap

""" @class: FalconThreads
    @description:
    
"""
class FalconThreads(threading.Thread):
    def setSharedData(self, sharedData):
            self.sharedData = sharedData
    def endThread(self):
        self.keepRunning = False
    def run(self):
        raise NotImplementedError

""" List all threads that will be used
    in the FalconEye application
"""
class TCPDataOut(FalconThreads):
    def run(self):
        pass

class TCPDataIn(FalconThreads):
    def run(self):
        pass

class MJPEGServer(FalconThreads):
    def run(self):
        pass

class DebugVideoFeed(FalconThreads):
    def run(self):
        self.keepRunning = True

        while self.keepRunning:
            time.sleep(1/30)# TODO Debug only: FalconEyeMap.SHOW_IMAGE_FREQ
            cv2.imshow("Frame", self.sharedData.frame)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
        cv2.destroyAllWindows()

class RetrieveImage(FalconThreads):
    def run(self):
        self.keepRunning = True

        while self.keepRunning:
            time.sleep(1/60) #TODO Debug only
            e1 = cv2.getTickCount()
            self.sharedData.getFrame()
            e2 = cv2.getTickCount()
            t = (e2-e1)/cv2.getTickFrequency()
            #print(t) TODO: Debug only

class ProcessImage(FalconThreads):
    def run(self):
        self.keepRunning = True
        self.worstTime = 0.0
        self.meanTime = 0.0
        self.counter = 0

        """ Image Processor is the context for the image processing
            algorithms we are developing. We can plug and play with
            any of the implemented algorithms by dorpping them into
            the Image Processor constructor or using the setAlgorithm
            method.
        """
        self.imgProcessor = ImageProcessor(BasicAlgorithm(self.sharedData))
        while self.keepRunning:
            e1 = cv2.getTickCount()
            self.imgProcessor.processImage()
            e2 = cv2.getTickCount()
            t = (e2-e1)/cv2.getTickFrequency()
            self.meanTime+=t
            self.counter+=1
            if t>self.worstTime:
                self.worstTime = t
        print("Worst img processsing time took: " +str(self.worstTime)) #TODO Debugging only
        print("Mean img processsing time took: " +str(self.meanTime/self.counter)) 

class MainThread(FalconThreads):
    """ Setup all threads
    """
    def setupThreads(self):
        # Shared data to connect all image services
        self.imData = ImageData(FalconEyeMap.VID_1)

        # Retireve image thread
        self.recvImg = RetrieveImage()
        self.recvImg.setSharedData(self.imData)

        # Processing image thread
        self.imgProcess = ProcessImage()
        self.imgProcess.setSharedData(self.imData)

        # Show the video window (Debbugging only)
        self.debugFeed = DebugVideoFeed()
        self.debugFeed.setSharedData(self.imData)

    """ Start all threads
    """
    def startThreads(self):
        self.recvImg.start()
        self.imgProcess.start()

        self.debugFeed.start()

    """ Kill all threads when main ends
    """
    def endThread(self):
        self.keepRunning = False

        self.recvImg.endThread()
        self.recvImg.join()

        self.imgProcess.endThread()
        self.imgProcess.join()

        self.debugFeed.endThread()
        self.debugFeed.join()

    def run(self):
        """ Setup all threads
        """
        self.setupThreads()

        """ Start all threads
        """
        self.startThreads()

        self.keepRunning = True
        while self.keepRunning:
            time.sleep(1)

        """ End all threads
        """
        self.endThread()
        


if __name__=='__main__':
    import time
    main = MainThread()
    main.start()
    time.sleep(15)
    main.endThread()
    main.join()
