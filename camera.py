'''
Camera Example
==============

This example demonstrates a simple use of the camera. It shows a window with
a buttoned labelled 'play' to turn the camera on and off. Note that
not finding a camera, perhaps because gstreamer is not installed, will
throw an exception during the kv language processing.

'''

# Uncomment these lines to see all the messages
# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

import cv2
import numpy as np
from PIL import Image

from datetime import datetime

from Detection.detection import Detector

Builder.load_string('''
<CameraClick>:
    orientation: 'horizontal'
    Camera:
        id: camera
        resolution: (1920, 1080)
        play: False
    ToggleButton:
        text: 'Play/Stop'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
    Button:
        text: 'Run Detection'
        size_hint_y: None
        height: '48dp'
        on_press: root.detector.runDetection()
    
''')


def get_frame(cameraObject):
    texture = cameraObject.texture
    size=texture.size
    pixels = texture.pixels

    #cv2 format 
    mat = cv2.cv.CreateMatFromData(pixels.width, pixels.height, cv2.cv.CV_8UC4, pixels.data)
    array = np.asarray(mat)

    return array 

    #pil format
    pil_image=Image.frombytes(mode='RGBA', size=size,data=pixels)
    # return pil_image

class CameraClick(BoxLayout):

    detector = Detector()

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        print(type(camera))
        camera.export_to_png("/anywhere-piano/Images/IMG_{}.png".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
        print("Captured")




class TestCamera(App):

    def build(self):
        return CameraClick()
    

    



TestCamera().run()