from libsoc_zero.GPIO import LED
from time import sleep

gpio_red = LED('GPIO-B')
gpio_green = LED('GPIO-C')
gpio_blue = LED('GPIO-D')

gpio_red.off()
gpio_green.off()	
gpio_blue.off()	
sleep(1)

while True:
    print("Red")
    gpio_red.on()
    sleep(2)
    gpio_red.off()

    print("Green")
    gpio_green.on()
    sleep(2)
    gpio_green.off()

    print("Blue")
    gpio_blue.on()
    sleep(2)
    gpio_blue.off()
