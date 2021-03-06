import machine
import network
import socket
import neopixel

ap = network.WLAN (network.AP_IF)
ap.active (True)
ap.config (essid = 'The Lord of the Pings')
ap.config (authmode = 3, password = 'Pablo-password')

names = ["Temp sens", "Temp Sens","Potentiometer"]
LEDs = ["Green LED", "Red LED", "Yellow LED"]
NeoPixels = ["Neopixel"]
Button = ["Button"]
TS = ["Temp sens"]
#4: Neopixels
#12: Button
#14: Green LED
#15: RED LED
#32: YELLOW LED
#17,21: Temp Sens
#39: ADC/potentiometer


NPpins = [neopixel.NeoPixel(machine.Pin(4), 8)]
Bpins = [machine.Pin(12,machine.Pin.IN,machine.Pin.PULL_UP)]
Lpins = [machine.Pin(i, machine.Pin.IN) for i in (14,15,32)]
TSpins = [machine.I2C(scl=machine.Pin(17), sda = machine.Pin(21))]
pins = [machine.Pin(i, machine.Pin.OUT) for i in (14,15,32)]

#############################################################
Lpins[0].value(1)
Lpins[1].value(1)
Lpins[2].value(1)
#############################################################
col = (84,60,20)
NPpins[0][0] = col
NPpins[0][1] = col
NPpins[0].write()
#############################################################
address = 24
temp_reg = 5
res_reg =8

data = TSpins[0].readfrom_mem(address, temp_reg, 2)

def temp_c(data):
    value = (data[0] << 8) | data[1]
    temp = (value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp
#############################################################




html = """
<!DOCTYPE html>
<html>
<head>
<title>
ESP32 Pins
</title>
<style>
table {
	border-collapse: collapse;
    font-family: Tahoma, Geneva, sans-serif;
}
table td {
	padding: 15px;
}
table thead td {
	background-color: #54585d;
	color: #ffffff;
	font-weight: bold;
	font-size: 13px;
	border: 1px solid #54585d;
}
table tbody td {
	color: #636363;
	border: 1px solid #dddfe1;
}
table tbody tr {
	background-color: #f9fafb;
}
table tbody tr:nth-child(odd) {
	background-color: #ffffff;
}
</style>
</head>

<body style = "background-color: rgb(28, 139, 212);">
<h1> ESP32 Pins </h1>
<table>
	<thead>
		<tr>
			<td>Name</td>
			<td>Pin</td>
			<td>Value</td>
		</tr>
	</thead>
	<tbody>
        %s
	</tbody>
</table>
</body>

</html>
""" 

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        print(line)
        if not line or line == b'\r\n':
            break
	rows = ['<tr><td>%s</td><td>%s</td><td>%d</td></tr>' % (n, str(p), p.value())  for p,n in zip(Lpins,LEDs)] 
	rows += ['<tr><td>%s</td><td>%s</td><td>%d</td></tr>' % (n, str(p), p.value())  for p,n in zip(Bpins,Button)]
	rows += ['<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (n, "Pin(4)", str(p[0]))  for p,n in zip(NPpins,NeoPixels)]
	rows += ['<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (n, "Pin(17), Pin(21)", str(temp_c(data)))  for n in TS]
	
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()

#QUESTIONS:
#How to turn off LEDs
#Git
#wifi name