import cv2  
import datetime  
from subprocess import call  

capture = "CaptureInput" + datetime.datetime.now().isoformat().replace(":", "") + ".jpeg"  
cmdline = "streamer -c /dev/video0 -b 32 -f jpeg -o " + capture  

call(cmdline, shell=True)  

img = cv2.imread(capture)  
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
newFileName = "CaptureOutput" + datetime.datetime.now().isoformat().replace(":", "") + ".jpg"  
cv2.imwrite(newFileName, gray)  


