# This is client.py file

import socket


port = 9999

# get local machine name
host = socket.gethostname()   


while True:                           

    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 

    # connection to hostname on the port.
    s.connect((host, port))

    # receive no more than 1024 bytes
    msg = s.recv(1024)
    print(msg.decode('ascii'))

    msg2 = input('Message: ')

    s.send(msg2.encode('ascii'))
    s.close()

    
