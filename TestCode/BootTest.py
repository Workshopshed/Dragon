#! /usr/bin/env python

# GNU GPL V3
# Test code to see boot time

import piconzero as pz, time


pz.init()
pz.setOutputConfig(0, 2)  # set output 0 to Servo
pz.setOutputConfig(1, 1)  # set output 1 to PWM
pz.setOutputConfig(2, 1)  # set output 2 to PWM
pz.setOutputConfig(3, 1)  # set output 3 to PWM

rev = pz.getRevision()
print rev[0], rev[1]
try:
    while True:
        for x in range(0, 50):
	    pz.setOutput(1, x)
            time.sleep(0.04)

except KeyboardInterrupt:
    print
finally:
    pz.cleanup()
