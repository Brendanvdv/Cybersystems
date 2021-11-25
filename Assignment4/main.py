import json
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
P = ["Poteniometer"]
#4: Neopixels
#12: Button
#14: Green LED
#15: RED LED
#32: YELLOW LED
#17,21: Temp Sens
#39: ADC/potentiometer

#Values for table Task2
NPpins = [neopixel.NeoPixel(machine.Pin(4), 8)]
Bpins = [machine.Pin(12,machine.Pin.IN,machine.Pin.PULL_UP)]
Lpins = [machine.Pin(i, machine.Pin.OUT) for i in (14,15,32)]
TSpins = [machine.I2C(scl=machine.Pin(17), sda = machine.Pin(21))]
Ppins = [machine.ADC(machine.Pin(39))]

#LED stuff
#############################################################
Lpins[0].value(1)
Lpins[1].value(1)
Lpins[2].value(1)
#############################################################

#Neopixel stuff
#############################################################
col = (5,10,15)
NPpins[0][0] = col
NPpins[0][1] = col
NPpins[0].write()
#############################################################

#Potentiometer stuff
#############################################################
# set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
Ppins[0].atten(machine.ADC.ATTN_11DB)

# set 9 bit return values (returned range 0-511)
Ppins[0].width(machine.ADC.WIDTH_9BIT)
#############################################################

#Getting the Temperature
################################################### 
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
###################################################   





#Json for Pins
#############################################################
Pins = {


    "Pin 4": "Neopixel",
    "Pin 12": "Button",
    "Pin 14": "Green LED",
    "Pin 15": "RED LED",
    "Pin 32": "YELLOW LED",
    "Pin 17,21": "Temperature Sensor",
    "Pin 39": "Potentiometer"
}

# # Get a JSON formatted string
Pins_JSON = json.dumps(Pins)

#############################################################

#Json for sensors
#############################################################
Sensors = {

    "Pin 17": "Temperature Sensor",
    "Pin 21": "Temperature Sensor",
    "Pin 12": "Button",
    "Pin 39": "Potentiometer"

}
Sens_JSON =json.dumps(Sensors)
#############################################################

#Json for values. User can check for these.
#############################################################
Values = {

    "Pin4": str(NPpins[0][0]),
    "Pin12": str(Bpins[0].value()),
    "Pin14": str(Lpins[0].value()),
    "Pin15": str(Lpins[1].value()),
    "Pin32": str(Lpins[2].value()),
    "Pin17": str(temp_c(data)),
    "Pin21": str(temp_c(data)),
    "Pin39": str(Ppins[0].read())

    
}

#Val =json.dumps(Values)






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

<a href="/pins"><button>Pins</button></a>
<a href="/sensors"><button>Sensors</button></a>


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



###############################################
rows = ['<tr><td>%s</td><td>%s</td><td>%d</td></tr>' % (n, str(p), p.value())  for p,n in zip(Lpins,LEDs)] 
rows += ['<tr><td>%s</td><td>%s</td><td>%d</td></tr>' % (n, str(p), p.value())  for p,n in zip(Bpins,Button)]
rows += ['<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (n, "Pin(4)", str(p[0]))  for p,n in zip(NPpins,NeoPixels)]
rows += ['<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (n, "Pin(17), Pin(21)", str(temp_c(data)))  for n in TS]
rows += ['<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (n, "Pin(39)", str(Ppins[0].read()))  for n in P]
###############################################


while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        print(line)

        #Web API stuff
        ###############################################
        if (b'GET / HTTP/1.1\r\n') in line:
            response = html % '\n'.join(rows)
        #if line == b'GET /pins HTTP/1.1\r\n':
        if (b'GET /pins HTTP/1.1\r\n') in line:
            response = Pins_JSON
        if (b'GET /sensors HTTP/1.1\r\n') in line:
            response = Sens_JSON
        # if (b'GET /pins/%s HTTP/1.1\r\n') % (Val.keys()) in line:
        #     response = Val.get(s)



        # if (b'GET /pins/%s HTTP/1.1\r\n') % ("Pin4") in line:
        #     print("AFFFFFFFFFFFFFFFFFFF")

        # for key in Val:
        #     st = 'GET /pins/%s HTTP/1.1\r\n' % (str(key))
        #     bs = st.encode('utf_8')
        #     if bs in line: 
        #         print("it WORRRRRRRKSSSSS")
        #         #response = json.dumps(Val[key]) 

         ###############################################    

        for key,value in Values.items():
            if (b'GET /pins/%s HTTP/1.1\r\n') %key in line:
                print("AHHHHHHHHHHH")
                response = json.dumps(value)

        if not line or line == b'\r\n':
            break

    cl.send(response)
    cl.close()

    
	
    
    

#QUESTIONS:
#git
#Bootstrap
#Task3, Json
#Task1, Original code or all code?


"""

import os
os.remove('main.py')

"""