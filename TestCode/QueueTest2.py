import time
from Queue import Queue
from threading import Thread
import piconzero as pz


# A test to see if we can process through two queues full of timed tasks
# Ref https://www.troyfawkes.com/learn-python-multithreading-queues-basics/
#     https://docs.python.org/2/library/queue.html


class ServoTask:
    def __init__(self, angle, delay):
        self.angle = angle
        self.delay = delay

    def run(self):
        print self.angle
        pz.setOutput(0, self.angle)
        time.sleep(self.delay)


class LEDTask:
    def __init__(self, rgb, delay):
        self.rgb = rgb
        self.delay = delay

    def run(self):
        print self.rgb.red, self.rgb.green, self.rgb.blue
        pz.setOutput(1, self.rgb.red)
        pz.setOutput(2, self.rgb.green)
        pz.setOutput(3, self.rgb.blue)
        time.sleep(self.delay)


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


def deactivate_defences():
    qLED.put(LEDTask(RGB(0, 50, 0), 0.5))


def activated():
    qServo.put(ServoTask(120, 0.2))
    qLED.put(LEDTask(RGB(0, 0, 50), 0.5))
    qLED.put(LEDTask(RGB(0, 0, 0), 0.5))
    qLED.put(LEDTask(RGB(0, 0, 50), 0.5))
    qLED.put(LEDTask(RGB(0, 0, 0), 0.5))
    qLED.put(LEDTask(RGB(0, 0, 50), 0.5))


def activate_defences():
    # Three sword blows
    for f in range(1, 4, 1):
        qServo.put(ServoTask(30, 0.5))
        for i in range(30, 120, 2):
            qServo.put(ServoTask(i, 0.01))

    greenlim = 30
    for f in range(1, 8, 1):
        qLED.put(LEDTask(RGB(80,greenlim, 0), 0.5))
        for i in range(greenlim, 0, -1):
                qLED.put(LEDTask(RGB(80, i, 0), 0.01))
        for i in range(0, greenlim, 1):
                qLED.put(LEDTask(RGB(80, i, 0), 0.01))
    #And back to red
    for i in range(greenlim, 0, -1):
        qLED.put(LEDTask(RGB(80, i, 0), 0.01))

# Setup
pz.init()
pz.setOutputConfig(0, 2)  # set output 0 to Servo
pz.setOutputConfig(1, 1)  # set output 1 to PWM
pz.setOutputConfig(2, 1)  # set output 2 to PWM
pz.setOutputConfig(3, 1)  # set output 3 to PWM

qLED = Queue(maxsize=0)
qServo = Queue(maxsize=0)

workerLED = Thread(target=processq, args=(qLED,))
workerLED.setDaemon(True)
workerLED.start()

workerServo = Thread(target=processq, args=(qServo,))
workerServo.setDaemon(True)
workerServo.start()

# main loop
try:
    while True:
        val = raw_input("Enter 1,2,3")
        print val
        if val == "1":
            deactivate_defences()
        if val == "2":
            activated()
        if val == "3":
            activate_defences()

        # Wait till both queues are empty
        qLED.join()
        qServo.join()

except KeyboardInterrupt:
    print

finally:
    pz.cleanup()
