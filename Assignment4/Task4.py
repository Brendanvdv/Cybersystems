import os 
import time
import machine



#################################################################
tempSens = machine.I2C(scl=machine.Pin(17), sda = machine.Pin(21))

address = 24
temp_reg = 5
res_reg =8

def temp_c(data):
    value = (data[0] << 8) | data[1]
    temp = (value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp

#####################################################################

with open('temp.txt','w') as f:

    for i in range(30):

        data = tempSens.readfrom_mem(address, temp_reg, 2)

        print("The temperature is: " + str(temp_c(data)) + " c")

        f.write('%s,%s' % (i,temp_c(data)))
        f.write('\n')
        time.sleep(1)

    f.close()

   