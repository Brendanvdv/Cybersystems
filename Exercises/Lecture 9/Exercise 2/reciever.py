# This is client.py file

import socket


port = 9999

# get local machine name
host = socket.gethostname()   

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:

    

                            

    # connection to hostname on the port.
    s.connect((host, port))

        
    # receive no more than 1024 bytes
    msg = s.recv(1024)

    print(msg.decode('ascii'))
    s.close()
