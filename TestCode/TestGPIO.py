from libsoc_zero.GPIO import LED
from time import sleep

gpio_red = LED('GPIO-B')

while (True): 
    gpio_red.on()
    sleep(0.5)
    gpio_red.off()
    sleep(0.5)

    
