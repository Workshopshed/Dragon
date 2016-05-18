# A simple test file for OpenCV

import numpy as np
import cv2
import datetime


def detect(img_color):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    detected = 0
    gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    # Now we find the faces in the image. If faces are found, it returns the positions of detected faces as Rect(x,y,w,h).
    # Once we get these locations, we can create a ROI for the face and apply eye detection on this ROI (since eyes are always on the face !!! ).
    faces = face_cascade.detectMultiScale(gray)
    for (x, y, w, h) in faces:
        cv2.rectangle(img_color, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img_color[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) > 0:
            detected = detected + 1
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    print(str(detected) + " people")
    return detected

img = cv2.imread('TestPicture.JPG')

if detect(img) > 0:
    newFileName = "TestOutput" + datetime.datetime.now().isoformat().replace(":","") + ".jpg"
    cv2.imwrite(newFileName, img);
