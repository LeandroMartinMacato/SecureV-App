import os
import cv2

import tensorflow as tf

model = r"E:\Programming\Python\~PROJECTS\College~\secureV\Tools\yolov4-custom-functions\checkpoints\custom-416\saved_model.pb"
webcam = cv2.VideoCapture(0)

def main():
    while webcam.isOpened():
            ret , frame = webcam.read()
            # cv2.imshow("SecureV ", frame) # Open Cam
    pass

if __name__ == '__main__':
    main()