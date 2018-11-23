"""
Face recognition pipeline

"""

import os
import cv2
import imutils
import cv2
import argparse
import sys
from glob import glob
from opencv_face_recognition import face_recognition

# Load the face detector
face_recogniser = face_recognition()

# Create a list of training images and labels
labels = []
images = glob('./my_photos/*/*', recursive=True)
for filename in images:
    labels.append(filename.split(os.path.sep)[-2].title())

# Train using this dataset
face_recogniser.train(images, labels)

# Now start video feed
print('Checking for camera...')
cam = cv2.VideoCapture(0)
if ( not cam.isOpened() ):
    print ("no cam!")
    sys.exit()
print ("cam: ok.")

cv2.namedWindow('Face Recognition', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Face Recognition', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cam.read()
    labelled_frame = face_recogniser.recognise(frame)

    cv2.imshow('Face Recognition', labelled_frame)

















