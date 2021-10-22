import os, time
import machine
import neopixel

np = neopixel.NeoPixel(machine.Pin(4), 8)

np[0] = (255, 0, 0) # set to red, full brightness
