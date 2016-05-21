from libsoc_zero.GPIO import Button
from libsoc_zero.GPIO import LED
from time import sleep

sensor = Button('GPIO-A')

gpio_red = LED('GPIO-B')
gpio_green = LED('GPIO-C')
gpio_blue = LED('GPIO-D')

gpio_red.off()
gpio_green.off()	
gpio_blue.off()	
sleep(2)

while True:
    if sensor.is_pressed():
        gpio_red.on()
        gpio_green.on()	
        gpio_blue.on()	
        sleep(0.5)
    else:
        gpio_red.off()
        gpio_green.off()	
        gpio_blue.off()	
        sleep(0.5)

