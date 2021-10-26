import os, time
import machine
import neopixel


tempSens = machine.I2C(scl=machine.Pin(17), sda = machine.Pin(21))

#tempSens.scan()

address = 24
temp_reg = 5
res_reg =8

#tempSens.readfrom_mem(address,temp_reg,2)

data = tempSens.readfrom_mem(address, temp_reg, 2)



def temp_c(data):
    value = (data[0] << 8) | data[1]
    temp = (value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp

temp_c(data)

###############################################


np = neopixel.NeoPixel(machine.Pin(4), 8)

GREEN = (255,0,0)
RED = (0,255,0)
BLUE = (0,0,255)
ORANGE = (128,255,0)
PINK = (0,255,128)


# np[0] = (ORANGE) # set to red, full brightness
# np.write()



while True:

    data = tempSens.readfrom_mem(address, temp_reg, 2)
    print(temp_c(data))

    if temp_c(data) <= 26:
       np[0] = (GREEN)
       np[1] = (GREEN)
       np.write()

    if temp_c(data) > 26 and temp_c(data) <= 28:
       np[0] = (ORANGE)
       np[1] = (ORANGE)
       np.write()

    if temp_c(data) > 28:
        np[0] = (RED)
        np[1] = (RED)
        np.write()
        