import os 
import time
import machine


#CODE FROM VIDEO. Gets temperature. https://www.youtube.com/watch?v=SJTk7V7iC1I&t=7s
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

f = open("temp.txt",'a')


for i in range(10):

    f.write(str(i),str(temp_c(data)))
    time.sleep(1)

f.close()