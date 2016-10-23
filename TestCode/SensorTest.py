#! /usr/bin/env python

# GNU GPL V3
# Test code for 4tronix Picon Zero

import piconzero as pz, time
from libsoc import gpio
from libsoc import GPIO
from time import sleep

def sensor_activated():
    gpio_in = gpio.GPIO(GPIO.gpio_id("GPIO-A"), gpio.DIRECTION_INPUT)
    with gpio.request_gpios(gpio_in):
        in_val = gpio_in.is_high()
    return in_val

pz.init()
pz.setOutputConfig(0, 2)  # set output 0 to Servo
pz.setOutputConfig(1, 1)  # set output 1 to PWM
pz.setOutputConfig(2, 1)  # set output 2 to PWM
pz.setOutputConfig(3, 1)  # set output 3 to PWM

rev = pz.getRevision()
print rev[0], rev[1]
try:
    while True:
        while not sensor_activated():
            sleep(1)
        for x in range(0, 50):
            pz.setOutput(1, x)
            time.sleep(0.04)
        pz.setOutput(1, 0)
        sleep(3)
except KeyboardInterrupt:
    print
finally:
    pz.cleanup()
