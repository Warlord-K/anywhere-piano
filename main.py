import cv2
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from Utils.cvfpscalc import CvFpsCalc


import time

import mediapipe

class MyApp(App):
    def build(self):

        self.image = Image()

        # Starting the OpenCV capture in a separate thread
        Clock.schedule_once(self.start_opencv_capture, 0)

        #for fps
        self.frames = 0 
        self.start_time = time.time()

        return self.image

    def start_opencv_capture(self, dt):
    # OpenCV capture code
        cap = cv2.VideoCapture(0)  # Capture from the default camera (index 0)
       

        def update_frame(dt):
            ret, frame = cap.read()
            if ret:
               
                #we need to flip updown as coordinate axis in kivy is downleft while in open cv it is topleft
                #left right for user convenience , taken care in

                frame = cv2.flip(frame, 1)
                fpsframe = self.update_fps(frame)
                flipped_frame = cv2.flip(fpsframe, -1)
                


                 # Process the frame
                processed_frame = flipped_frame

                #put fps
                

                # Update the Kivy Image with the processed frame
                texture = self.convert_frame_to_texture(processed_frame)
                self.image.texture = texture

        Clock.schedule_interval(update_frame, 1 / 30)  # Update at 30 FPS

    def convert_frame_to_texture(self, frame):
    # Convert the frame to a Kivy texture
        frame = cv2.flip(frame, 1)
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(frame.flatten(), colorfmt='bgr', bufferfmt='ubyte')
        return texture
    
    def update_fps(self,frame):
        self.frames += 1

        elapsed_time = time.time() - self.start_time

        fps_text = "FPS: {:.2f}".format(self.frames / (time.time() - self.start_time))
        cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
    
        if elapsed_time > 1.0:
            fps = self.frames / elapsed_time
            print("FPS:", fps)
            

            
            self.frames = 0
            self.start_time = time.time()

        return frame

if __name__ == '__main__':
    MyApp().run()
