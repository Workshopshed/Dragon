#! /usr/bin/env python

# GNU GPL V3
# Test code for 4tronix Picon Zero

import piconzero as pz, time

lastPix = 0
numpixels = 8

pz.init()
pz.setOutputConfig(0, 2)  # set output 0 to Servo
pz.setOutputConfig(1, 1)  # set output 1 to PWM
pz.setOutputConfig(2, 1)  # set output 2 to PWM
pz.setOutputConfig(3, 1)  # set output 3 to PWM

rev = pz.getRevision()
print rev[0], rev[1]
try:
    while True:
        for channel in range(1, 4):
            for x in range(0, 50):
                pz.setOutput(channel, x)
                time.sleep(0.04)
            pz.setOutput(channel, 0)
except KeyboardInterrupt:
    print
finally:
    pz.cleanup()
