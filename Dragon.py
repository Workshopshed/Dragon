from StringIO import StringIO
import pycurl
import signal, sys
import cv2
import datetime
from subprocess import call
from time import sleep
from libsoc import gpio
from libsoc import GPIO


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


def notify(numDragons,key):
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
    gpio_in = gpio.GPIO(GPIO.gpio_id("GPIO-A"), gpio.DIRECTION_INPUT)
    with gpio.request_gpios(gpio_in):
        in_val = gpio_in.is_high()
    return in_val


def activated():
    gpio_red = gpio.GPIO(GPIO.gpio_id("GPIO-B"), gpio.DIRECTION_OUTPUT)
    gpio_green = gpio.GPIO(GPIO.gpio_id("GPIO-C"), gpio.DIRECTION_OUTPUT)
    gpio_blue = gpio.GPIO(GPIO.gpio_id("GPIO-D"), gpio.DIRECTION_OUTPUT)

    with gpio.request_gpios((gpio_red, gpio_green, gpio_blue)):
        gpio_green.set_low()
        gpio_blue.set_low()
        gpio_blue.set_high()


def activate_defences():
    gpio_red = gpio.GPIO(GPIO.gpio_id("GPIO-B"), gpio.DIRECTION_OUTPUT)
    gpio_green = gpio.GPIO(GPIO.gpio_id("GPIO-C"), gpio.DIRECTION_OUTPUT)
    gpio_blue = gpio.GPIO(GPIO.gpio_id("GPIO-D"), gpio.DIRECTION_OUTPUT)

    counter = 10;

    with gpio.request_gpios((gpio_red, gpio_green, gpio_blue)):
        gpio_green.set_low()
        gpio_blue.set_low()
        while counter > 0:
            gpio_red.set_high()
            sleep(0.5)
            gpio_red.set_low()
            sleep(0.5)
	    counter = counter - 1	


def deactivate_defences():
        gpio_red = gpio.GPIO(GPIO.gpio_id("GPIO-B"), gpio.DIRECTION_OUTPUT)
        gpio_green = gpio.GPIO(GPIO.gpio_id("GPIO-C"), gpio.DIRECTION_OUTPUT)
        gpio_blue = gpio.GPIO(GPIO.gpio_id("GPIO-D"), gpio.DIRECTION_OUTPUT)

        with gpio.request_gpios((gpio_red,gpio_green,gpio_blue)):
            gpio_green.set_low()
            gpio_red.set_low()
            gpio_blue.set_low()


# Handle exit and kill from OS
def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)


def on_exit(sig, func=None):
    print "exit handler triggered"
    sys.exit(1)


def main():
    while True:
        deactivate_defences()
	sleep(10) # Avoid rapid retriggering
        while not sensor_activated():
            sleep(1)
        activated()
        image = capture()
        dragons = detect(image)
        if dragons > 0:
            sleep(3)
            notify(dragons,get_key())
            activate_defences()
        


# Run program
if __name__ == '__main__':
    set_exit_handler(on_exit)
    sys.exit(main())
