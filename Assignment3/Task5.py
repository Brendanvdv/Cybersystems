import machine
import time
import os
import neopixel


adc = machine.ADC(machine.Pin(39))
adc.atten(machine.ADC.ATTN_11DB)
adc.width(machine.ADC.WIDTH_9BIT)

np = neopixel.NeoPixel(machine.Pin(4), 8)



while True:
    value = int(adc.read()/3)
    GREEN = (value,0,0)
    print(value)
    np[0]= GREEN
    np[1] = GREEN
    np.write()