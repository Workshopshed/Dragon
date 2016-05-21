from time import sleep

from libsoc import gpio
from libsoc import GPIO

# GPIO.set_debug(True)

gpio_out = gpio.GPIO(GPIO.gpio_id("GPIO-B"), gpio.DIRECTION_OUTPUT)

with gpio.request_gpios(gpio_out):
	while True:
	    gpio_out.set_high()
	    sleep(1)
	    gpio_out.set_low()
	    sleep(1)
