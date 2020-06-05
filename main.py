# Evan Zhang
# Martin Lopez
# Gonzalo Arana


import cv2 as cv
import sys
import numpy as np


face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')


cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #x,y,w,h are the face positions
    for (x,y,w,h) in faces:
        frame = cv.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
    gray_face = gray[y:y+h, x:x+w] # cut the gray face frame out
    face = frame[y:y+h, x:x+w] # cut the face frame out
    eyes = eye_cascade.detectMultiScale(gray_face)
    #ex,ey,ew,eh are the eye positions
    for (ex,ey,ew,eh) in eyes: 
        cv.rectangle(frame,(ex,ey),(ex+ew,ey+eh),(0,225,255),2) 
    
    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

