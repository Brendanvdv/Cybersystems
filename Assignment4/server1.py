import machine
import network
import socket

ap = network.WLAN (network.AP_IF)
ap.active (True)
ap.config (essid = 'Lord of the Ping')
ap.config (authmode = 3, password = 'Pablo-password')

#4: Neopixels
#12: Button
#14: Green LED
#15: RED LED
#32: YELLOW LED
#17,21: Temp Sens
#39: ADC/potentiometer
pins = [machine.Pin(i, machine.Pin.IN) for i in (4,12,14,15,17,21,32,39)]

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

<body>
<h1> ESP32 Pins </h1>
<table>
	<thead>
		<tr>
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
        #print(line)
        if not line or line == b'\r\n':
            break
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()
