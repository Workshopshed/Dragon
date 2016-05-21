import time

from libsoc_zero.GPIO import LED
from time import sleep

gpio_red = LED('GPIO-B')
gpio_green = LED('GPIO-C')
gpio_blue = LED('GPIO-D')

while (True): 
    gpio_red.on()
    gpio_green.on()	
    gpio_blue.on()	
    sleep(0.5)
    gpio_red.off()
    gpio_green.off()	
    gpio_blue.off()	
    sleep(0.5)

    
