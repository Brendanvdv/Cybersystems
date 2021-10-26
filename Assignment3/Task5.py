import machine
import time
import os
import neopixel

#Initialize potentiometer
adc = machine.ADC(machine.Pin(39))

# set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
adc.atten(machine.ADC.ATTN_11DB)

# set 9 bit return values (returned range 0-511)
adc.width(machine.ADC.WIDTH_9BIT)

#Initialize neopixel
np = neopixel.NeoPixel(machine.Pin(4), 8)



while True:

    #Takes value from pontiometer and divides by 3 so that it fits the range 0-255
    value = int(adc.read()/3)
    GREEN = (value,0,0)
    print(value)

    np[0]= GREEN
    np[1] = GREEN
    np.write()