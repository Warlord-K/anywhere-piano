import cv2
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from piano import Piano
import numpy as np
import time

import mediapipe as mp
model_path = 'anywhere-piano\hand_landmarker.task'

mp_hands = mp.solutions.hands
points = [point for point in mp_hands.HandLandmark]
finger_points = [(3,2), 
                 (7,5),
                 (11,9),
                 (15,13),
                 (19,17)]
# ro set the hands function which will hold the landmarks points
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
pressed = [False] * 5

# to set up the drawing function of hands landmarks on the image
mp_drawing = mp.solutions.drawing_utils

def overlay_image_alpha(img, img_overlay, x, y, alpha_mask):
    """Overlay `img_overlay` onto `img` at (x, y) and blend using `alpha_mask`.

    `alpha_mask` must have same HxW as `img_overlay` and values in range [0, 1].
    """
    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    # Blend overlay within the determined ranges
    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
    alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis]
    alpha_inv = 1.0 - alpha

    img_crop[:] = alpha * img_overlay_crop + alpha_inv * img_crop

class MyApp(App):
    def build(self):

        self.image = Image()
        self.piano_img = cv2.imread('piano_keys.jpg')
        self.piano = Piano()
        # Starting the OpenCV capture in a separate thread
        Clock.schedule_once(self.start_opencv_capture, 0)

        #for fps
        self.frames = 0 
        self.start_time = time.time()

        return self.image

    def update_frame(self, dt):
        ret, frame = self.cap.read()
        if ret:
            
            #we need to flip updown as coordinate axis in kivy is downleft while in open cv it is topleft
            #left right for user convenience , taken care in

            frame = cv2.flip(frame, 1)
            fpsframe = self.update_fps(frame)
            flipped_frame = cv2.flip(fpsframe, -1)
            


                # Process the frame
            
            results = hands.process(cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB))

            image_height, image_width, _ = flipped_frame.shape
        
            img_copy = flipped_frame

            if results.multi_hand_landmarks:

                for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    
                    mp_drawing.draw_landmarks(image = img_copy, landmark_list = hand_landmarks,
                                            connections = mp_hands.HAND_CONNECTIONS )
                    for i,press in enumerate(pressed):
                        if not press:
                            if hand_landmarks.landmark[points[finger_points[i][0]]].y > hand_landmarks.landmark[points[finger_points[i][1]]].y: 
                                pressed[i] = True
                                print(i, "armed")
                        else:
                            if hand_landmarks.landmark[points[finger_points[i][0]]].y < hand_landmarks.landmark[points[finger_points[i][1]]].y:
                                print(i, "disarmed")
                                pressed[i] = False
                                normalizedLandmark = hand_landmarks.landmark[points[finger_points[i][1]+1]]
                                pos = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, image_width, image_height)
                                self.piano.play(pos, image_height, image_width)

            # img_copy = overlay_image_alpha(img_copy, self.piano_img, 0, 0, np.array(self.piano_img)/255 * 0.8)
            # img_copy =  cv2.addWeighted(img_copy[:self.piano_img.shape[1]][:self.piano_img.shape[0]], 1, self.piano_img, 0.8,0)
            processed_frame = img_copy

            

            # Update the Kivy Image with the processed frame
            texture = self.convert_frame_to_texture(processed_frame)
            self.image.texture = texture

    def start_opencv_capture(self, dt):
    # OpenCV capture code
        self.cap = cv2.VideoCapture(1)  # Capture from the default camera (index 0)

        Clock.schedule_interval(self.update_frame, 1 / 30)  # Update at 30 FPS

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
            # print("FPS:", fps)
            

            
            self.frames = 0
            self.start_time = time.time()

        return frame

if __name__ == '__main__':
    MyApp().run()
