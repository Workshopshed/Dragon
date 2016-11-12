from StringIO import StringIO
import pycurl
import signal, sys
import cv2
from subprocess import call
import piconzero as pz
from Queue import Queue
from threading import Thread
import datetime, time
import dropbox, os


# Ref https://www.troyfawkes.com/learn-python-multithreading-queues-basics/
#     https://docs.python.org/2/library/queue.html

class ServoTask:
    def __init__(self, angle, delay):
        self.angle = angle
        self.delay = delay

    def run(self):
        # print self.angle
        pz.setOutput(0, self.angle)
        sleep(self.delay)


class LEDTask:
    def __init__(self, rgb, delay):
        self.rgb = rgb
        self.delay = delay

    def run(self):
        # print self.rgb.red, self.rgb.green, self.rgb.blue
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


def get_IFTTTkey():
    with open('IFTTTKey.conf', 'r') as f:
        key = f.readline()
    f.close()
    return key


# Have created a Dropbox App folder with the DropBox Developer console
# https://www.dropbox.com/developers/apps
# Get the access token from a file, as created by above console
def get_dropboxkey():
    with open('DropBoxKey.conf', 'r') as f:
        key = f.readline()
    f.close()
    return key


def notify(numDragons, key):
    url = "https://maker.ifttt.com/trigger/DragonDetected/with/key/" + key + "?value1=" + str(numDragons)
    r = call_api(url)
    print r


# Simplified upload from the updown.py example
# https://github.com/dropbox/dropbox-sdk-python/blob/master/example/updown.py
def upload(sourcefile, destfile, overwrite=False):
    """Upload a file.

    Return the request response, or None in case of error.
    """
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    mtime = os.path.getmtime(sourcefile)
    with open(sourcefile, 'rb') as f:
        data = f.read()
    try:
        res = dbx.files_upload(
            data, destfile, mode,
            client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
            mute=True)
    except dropbox.exceptions.ApiError as err:
        print('*** API error', err)
        return None
    print 'Uploaded', res.name.encode('utf8')
    return res


def purge_old_files(daystokeep):
    files = 0
    print 'Deleting dropbox files older than {} days'.format(daystokeep)
    now = datetime.datetime.now()
    for entry in dbx.files_list_folder('').entries:
        delta = now - entry.server_modified
        if delta.days > daystokeep:
            files += 1
            print 'Deleting {} from {}'.format(entry.name, entry.server_modified)
            try:
                dbx.files_delete('/' + entry.name)
            except dropbox.exceptions.ApiError as err:
                print('*** API error', err)
                return None
    if files > 0:
        print 'Deleted {} files'.format(files)


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

    newfilename = ""
    if detected > 0:
        newfilename = "Detected" + datetime.datetime.now().isoformat().replace(":", "") + ".jpg"
        cv2.imwrite(newfilename, img)

    print(str(detected) + " dragons")
    print ""
    return detected, newfilename


def sensor_activated():
    return pz.readInput(0)


def waitforaction():
    # Wait till both queues are empty
    qLED.join()
    qServo.join()


def deactivate_defences():
    print "Looking for Dragons"
    qLED.put(LEDTask(RGB(0, 50, 0), 0.5))
    waitforaction()


def activated():
    # Flash blue
    print "Motion detected"
    qServo.put(ServoTask(120, 0.2))
    qLED.put(LEDTask(RGB(0, 0, 50), 0.5))
    qLED.put(LEDTask(RGB(0, 0, 0), 0.5))
    qLED.put(LEDTask(RGB(0, 0, 50), 0.5))
    qLED.put(LEDTask(RGB(0, 0, 0), 0.5))
    qLED.put(LEDTask(RGB(0, 0, 50), 0.5))
    waitforaction()


def activate_defences():
    print "Dragon detected"
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

    # Initialise dropbox
    global dbx;
    dbx = dropbox.Dropbox(get_dropboxkey())


def main():
    try:
        initialise()
        while True:
            deactivate_defences()
            time.sleep(10)  # Avoid rapid retriggering
            while not sensor_activated():
                time.sleep(0.2)
            activated()
            image = capture()
            dragons, outfile = detect(image)
            if dragons > 0:
                notify(dragons, get_IFTTTkey())
                upload(outfile, '/' + outfile, True)
                activate_defences()
                purge_old_files(30)  # Keep 30 days of history
    except KeyboardInterrupt:
        print 'Stopping...'
        on_exit(None)


# Run program
if __name__ == '__main__':
    set_exit_handler(on_exit)
    sys.exit(main())
