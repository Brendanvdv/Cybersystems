import machine
import neopixel

np = neopixel.NeoPixel(machine.Pin(4), 8)

GREEN = (0,0,0)

np[0] = (GREEN)
np[1] = (GREEN)
np.write()