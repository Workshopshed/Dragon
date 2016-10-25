#!/usr/bin/python

from libsoc import I2C

# This test is intended to be run with the PiconZero on I2C bus 0.
# Note this is not currently working
I2C_BUS = 0
I2C_ADDR = 0x22
RETRIES = 10   # max number of retries for I2C calls

def main():
    I2C.set_debug(1)
    with I2C(I2C_BUS, I2C_ADDR) as bus:
        # initialize LCD
	for i in range(RETRIES):
        	try:
        	    rval = bus.read(1)
		    type = rval%256	
        	    revison = rval/256
        	except:
        	    print "Error in getRevision(), retrying"


	print "Board Type:", type 	
	print "Firmware version:", revison 


if __name__ == '__main__':
    main()


