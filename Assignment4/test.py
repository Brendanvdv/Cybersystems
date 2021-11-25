import machine
import neopixel

NPpins = [neopixel.NeoPixel(machine.Pin(4), 8)]

col = (5,10,15)
NPpins[0][0] = col
NPpins[0][1] = col
NPpins[0].write()

print(NPpins)
print(str(NPpins))
print(str(NPpins[0][0]))
print(NPpins[0])