# A simple test file for OpenCV

import numpy as np
import cv2
import datetime

def detect(img_color):
    dclassifier = cv2.CascadeClassifier('DragonClassifier50x50-5v2.xml')

    detected = 0

    # Now we find the faces in the image. If faces are found, it returns the positions of detected faces as Rect(x,y,w,h).
    # Once we get these locations, we can create a ROI for the face and apply eye detection on this ROI (since eyes are always on the face !!! ).
    dragons = dclassifier.detectMultiScale(img_color)
    for (x, y, w, h) in dragons:
        cv2.rectangle(img_color, (x, y), (x + w, y + h), (255, 0, 0), 2)
        detected += 1

    print(str(detected) + " dragons")
    return detected

img = cv2.imread('TestDragons1.jpg')

if detect(img) > 0:
    newFileName = "TestOutput" + datetime.datetime.now().isoformat().replace(":","") + ".jpg"
    cv2.imwrite(newFileName, img);
