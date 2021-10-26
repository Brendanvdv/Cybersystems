
import os
import time
import machine


#Initialize Pins
button = machine.Pin(12,machine.Pin.IN,machine.Pin.PULL_UP)
p15R = machine.Pin(15,machine.Pin.OUT)#Red
p32Y = machine.Pin(32,machine.Pin.OUT)#Yellow
p14G = machine.Pin(14,machine.Pin.OUT)#Green


p14G.value(1) #Turn green led on

i = 0


#Uses variable i to switch between leds
#Used time.sleep() to make sure do not enter two if statements at the same time
while True:

    if button.value() == 0 and i == 0:
        time.sleep(0.5)
        if button.value() == 1:

            p14G.value(0)
            time.sleep(0.5)
            p32Y.value(1)
            i = 1
        

    if button.value() == 0 and i == 1:
        time.sleep(0.5)

        if button.value() == 1:
            p32Y.value(0)
            time.sleep(0.5)
            p15R.value(1)
            i = 2

    if button.value() == 0 and i == 2:
        time.sleep(0.5)

        if button.value() == 1:
            p15R.value(0)
            time.sleep(0.5)
            p14G.value(1)
            i = 0

        