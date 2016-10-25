import time
from Queue import Queue
from threading import Thread

# A test to see if we can process through two queues full of timed tasks
# Ref https://www.troyfawkes.com/learn-python-multithreading-queues-basics/
#     https://docs.python.org/2/library/queue.html


class ServoTask:
    def __init__(self, angle,delay):
        self.angle = angle
        self.delay = delay

    def run(self):
        # Todo: Swap with call to piconzero
        print self.angle
        time.sleep(self.delay)


class LEDTask:
    def __init__(self, rgb,delay):
        self.rgb = rgb
        self.delay = delay

    def run(self):
        # Todo: Swap with call to piconzero
        print self.rgb.red, self.rgb.green, self.rgb.blue
        time.sleep(self.delay)


class RGB:
    def __init__(self, red,green,blue):
        self.red = red
        self.green = green
        self.blue = blue


def processq(q):
    while True:
        task = q.get()
        task.run()
        q.task_done()


qLED = Queue(maxsize=0)
qServo = Queue(maxsize=0)

workerLED = Thread(target=processq,args=(qLED,))
workerLED.setDaemon(True)
workerLED.start()

workerServo = Thread(target=processq,args=(qServo,))
workerServo.setDaemon(True)
workerServo.start()

qLED.put(LEDTask(RGB(10,5,2),2))
qLED.put(LEDTask(RGB(0,10,0),2))
qLED.put(LEDTask(RGB(10,5,2),2))
qLED.put(LEDTask(RGB(0,10,0),2))
qLED.put(LEDTask(RGB(10,5,2),2))
qLED.put(LEDTask(RGB(0,10,0),2))

for i in range(120,10,-1):
    qServo.put(ServoTask(i,0.2))


# Wait till both queues are empty
qLED.join()
qServo.join()

print "done"
