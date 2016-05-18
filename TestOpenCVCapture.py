import cv2
import datetime

cap = cv2.VideoCapture(0)
# Capture single frame
ret, frame = cap.read()
cap.release()

if ret:
    newFileName = "CaptureOutput" + datetime.datetime.now().isoformat().replace(":", "") + ".jpg"
    cv2.imwrite(newFileName, frame)
else:
    print "Capture failed"

