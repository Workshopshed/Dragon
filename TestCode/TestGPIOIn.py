from libsoc_zero.GPIO import Button
from libsoc_zero.GPIO import LED
from time import sleep

sensor = Button('GPIO-A')

gpio_red = LED('GPIO-B')

gpio_red.off()
sleep(2)

while True:
    if sensor.is_pressed():
        gpio_red.on()
        sleep(0.5)
    else:
        gpio_red.off()
        sleep(0.5)

