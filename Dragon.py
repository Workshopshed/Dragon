from StringIO import StringIO
import pycurl
import signal, sys
import cv2
import datetime
from subprocess import call
from time import sleep
import piconzero as pz
from Queue import Queue
from threading import Thread


# Ref https://www.troyfawkes.com/learn-python-multithreading-queues-basics/
#     https://docs.python.org/2/library/queue.html

class ServoTask:
    def __init__(self, angle, delay):
        self.angle = angle
        self.delay = delay

    def run(self):
        print self.angle
        pz.setOutput(0, self.angle)
        sleep(self.delay)


class LEDTask:
    def __init__(self, rgb, delay):
        self.rgb = rgb
        self.delay = delay

    def run(self):
        print self.rgb.red, self.rgb.green, self.rgb.blue
        pz.setOutput(1, self.rgb.red)
        pz.setOutput(2, self.rgb.green)
        pz.setOutput(3, self.rgb.blue)
        sleep(self.delay)


class RGB:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue


def processq(q):
    while True:
        task = q.get()
        task.run()
        q.task_done()


def call_api(url):
    r = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.CONNECTTIMEOUT, 10)
    c.setopt(c.TIMEOUT, 60)
    c.setopt(c.WRITEFUNCTION, r.write)
    c.perform()
    c.close()
    return r.getvalue()


def get_key():
    with open('IFTTTKey.conf', 'r') as f:
        key = f.readline()
    f.close()
    return key


def notify(numDragons, key):
    url = "https://maker.ifttt.com/trigger/DragonDetected/with/key/" + key + "?value1=" + str(numDragons)
    r = call_api(url)
    print r


def capture():
    filename = "CaptureInput" + datetime.datetime.now().isoformat().replace(":", "") + ".jpeg"
    cmdline = "streamer -c /dev/video0 -b 32 -f jpeg -o " + filename
    call(cmdline, shell=True)
    return cv2.imread(filename)


def detect(img):
    dclassifier = cv2.CascadeClassifier('DragonClassifier50x50-5v2.xml')

    detected = 0

    dragons = dclassifier.detectMultiScale(img)
    for (x, y, w, h) in dragons:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        detected += 1

    if detected > 0:
        newFileName = "Detected" + datetime.datetime.now().isoformat().replace(":", "") + ".jpg"
        cv2.imwrite(newFileName, img)

    print(str(detected) + " dragons")
    return detected


def sensor_activated():
    return pz.readInput(0)


def waitforaction():
    # Wait till both queues are empty
    qLED.join()
    qServo.join()


def deactivate_defences():
    qLED.put(LEDTask(RGB(0, 50, 0), 0.5))
    waitforaction()


def activated():
    # Flash blue
    qServo.put(ServoTask(120, 0.2))
    qLED.put(LEDTask(RGB(0, 0, 50), 0.5))
    qLED.put(LEDTask(RGB(0, 0, 0), 0.5))
    qLED.put(LEDTask(RGB(0, 0, 50), 0.5))
    qLED.put(LEDTask(RGB(0, 0, 0), 0.5))
    qLED.put(LEDTask(RGB(0, 0, 50), 0.5))
    waitforaction()


def activate_defences():
    # Three sword blows
    for f in range(1, 4, 1):
        qServo.put(ServoTask(30, 0.5))
        for i in range(30, 120, 2):
            qServo.put(ServoTask(i, 0.01))

    greenlim = 30
    for f in range(1, 8, 1):
        qLED.put(LEDTask(RGB(80, greenlim, 0), 0.5))
        for i in range(greenlim, 0, -1):
            qLED.put(LEDTask(RGB(80, i, 0), 0.01))
        for i in range(0, greenlim, 1):
            qLED.put(LEDTask(RGB(80, i, 0), 0.01))
    # And back to red
    for i in range(greenlim, 0, -1):
        qLED.put(LEDTask(RGB(80, i, 0), 0.01))

    waitforaction()


# Handle exit and kill from OS
def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)


def on_exit(sig, func=None):
    print "Exiting DragonDetector"
    pz.cleanup()
    sys.exit(1)


def initialise():
    # Setup
    pz.init()
    pz.setOutputConfig(0, 2)  # set output 0 to Servo
    pz.setOutputConfig(1, 1)  # set output 1 to PWM
    pz.setOutputConfig(2, 1)  # set output 2 to PWM
    pz.setOutputConfig(3, 1)  # set output 3 to PWM
    pz.setInputConfig(0, 0)  # set input 1 to digital

    # Setup Action queues
    global qLED
    qLED = Queue(maxsize=0)
    global qServo
    qServo = Queue(maxsize=0)

    workerLED = Thread(target=processq, args=(qLED,))
    workerLED.setDaemon(True)
    workerLED.start()

    workerServo = Thread(target=processq, args=(qServo,))
    workerServo.setDaemon(True)
    workerServo.start()


def main():
    try:
        initialise()
        while True:
            deactivate_defences()
            sleep(10)  # Avoid rapid retriggering
            while not sensor_activated():
                sleep(1)
            activated()
            image = capture()
            dragons = detect(image)
            if dragons > 0:
                sleep(3)
                notify(dragons, get_key())
                activate_defences()
    except KeyboardInterrupt:
        print 'Finished'


# Run program
if __name__ == '__main__':
    set_exit_handler(on_exit)
    sys.exit(main())
