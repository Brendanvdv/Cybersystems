import os 
import time
import machine


#CODE FROM VIDEO. Gets temperature.
#################################################################
tempSens = machine.I2C(scl=machine.Pin(17), sda = machine.Pin(21))

address = 24
temp_reg = 5
res_reg =8

data = tempSens.readfrom_mem(address, temp_reg, 2)



def temp_c(data):
    value = (data[0] << 8) | data[1]
    temp = (value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp

#####################################################################

#Initialize LEDs
p15R = machine.Pin(15,machine.Pin.OUT)#Red
p32Y = machine.Pin(32,machine.Pin.OUT)#Yellow
p14G = machine.Pin(14,machine.Pin.OUT)#Green




while True:

    data = tempSens.readfrom_mem(address, temp_reg, 2)
    print(temp_c(data))

    if temp_c(data) <= 26:
        p14G.value(1)
        p32Y.value(0)
        p15R.value(0)

    if temp_c(data) > 26 and temp_c(data) <= 28:
        p14G.value(0)
        p32Y.value(1)
        p15R.value(0)

    if temp_c(data) > 28:

        p14G.value(0)
        p32Y.value(0)
        p15R.value(1)


#Questions
#1) Do we need time sleeps?
#2) Can we copy the code from the video?
#3) import machine