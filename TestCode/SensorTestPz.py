import piconzero as pz, time
pz.init()
pz.setInputConfig(0, 0)   # request pullup on input
while True:
    switch = pz.readInput(0) # 0 = pressed, 1 = not pressed
    if (switch == 0):
        print "Switch Pressed", switch
    else:
        print "Switch Released", switch
    time.sleep(1)