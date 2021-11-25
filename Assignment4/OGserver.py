import machine
import network
import socket

#Create a WLAN network interface object
ap = network.WLAN (network.AP_IF)
#Activates Network
ap.active (True)
#Set Genereal Network Paramters
ap.config (essid = 'The Lord of The Pings')
ap.config (authmode = 3, password = 'Pablo-password')

#List concatenation for the pins
pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]

#THe Html code that describes the look of the server/website
html = """<!DOCTYPE html>
<html>
    <head> <title>ESP32 Pins</title> </head>
    <body> <h1>ESP32 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

#Gets the Ip address from tuple 
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

#Creates Socket
s = socket.socket()
#Binds the Ip adress to the socket
s.bind(addr)
#'Activate' the socket 
s.listen(1)

print('listening on', addr)


while True:
    #A new socket representing the connection (cl) and the address (addr)
    cl, addr = s.accept()
    print('client connected from', addr)
    #an Input/Output stream connected to the socket
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        print(line)
        #break when it reaches the end of the file
        if not line or line == b'\r\n':
            break
    #Creates the rows for the table in the html
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    #Inserts the rows line by line into the html
    response = html % '\n'.join(rows)
    #Sends the response to server
    cl.send(response)
    #Closes the connection to the server
    cl.close()
