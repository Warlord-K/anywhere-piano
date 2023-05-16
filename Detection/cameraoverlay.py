import cv2
import numpy as np
import asyncio


    
def showPiano_runInference(img):
    
# Load the video capture
    cap = cv2.VideoCapture(0)

    # Load the piano keys image

    #this relative doesnt work in my case 
    # piano_path = 'anywhere-piano\piano_keys.png'

    piano_path = 'C:\\Users\\Sairaj Loke\\Desktop\\KivyDev\\anywhere-piano\\piano_keys.png'
    piano_keys = cv2.imread(piano_path, cv2.IMREAD_UNCHANGED)

        
    # if piano_keys is None:
    #     print('Wrong path:', piano_path)
    # else:
    while True:
        # Read a frame from the video capture
        
        ret, frame = cap.read()
        if not ret:
            break

        type(img)
        # Resize the frame to fit the piano keys image
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

        frame_height, frame_width = frame.shape[:2]
        piano_keys = cv2.resize(piano_keys, (frame_width, frame_height // 2))

        
        # Define the region of interest for overlaying piano keys
        roi_top = frame_height // 2  # Adjust the vertical position of the keys
        roi_bottom = frame_height
        roi_left = 0
        roi_right = frame_width

        # Extract the region of interest from the frame
        roi = frame[roi_top:roi_bottom, roi_left:roi_right]

        # Overlay the piano keys on the region of interest
        combined = cv2.addWeighted(roi, 1.0, piano_keys, 0.5, 0, dtype=cv2.CV_8U)

        # Replace the region of interest with the combined image
        frame[roi_top:roi_bottom, roi_left:roi_right] = combined

        #left right inversion(for user convenience)
        frame = cv2.flip(frame,1)

        # Display the frame in fullscreen mode
        cv2.namedWindow('Video with Piano Keys', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Video with Piano Keys', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Video with Piano Keys', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyWindow()


