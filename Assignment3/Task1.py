
import os
import time
import machine

button = machine.Pin(12,machine.Pin.IN,machine.Pin.PULL_UP)
p15 = machine.Pin(15,machine.Pin.OUT)

while True:
	if button.value() == 0:
		p15.value(1)
		time.sleep(0.5)
		p15.value(0)
		time.sleep(0.5)	


