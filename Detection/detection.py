
import cv2
import numpy as np
from Detection.cameraoverlay import showPiano_runInference
# import mediapipe


#two options

#1 keep single self.img and change it we will

class Detector():

    def __init__(self) :
        self.img = None #we won't use a single img as Detectors object to use multi threading in future if req
            #thus we w
        self.detectbool = False


    def runDetection(self,feed):
        # self.detectbool  = currDetbul

        image = self.img #does not handles main img for inferencing

        if feed :
            # pass
            showPiano_runInference(image)
                
        else:
            print('start video feed')


