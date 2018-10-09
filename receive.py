import socket
import datetime
 
UDP_IP = "0.0.0.0"
UDP_PORT = 5000

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
start = datetime.datetime.now()
print('{0} - INFO: UDP Receiver Started'.format(start))
while True:
    now = datetime.datetime.now() 
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print('{0} Received message: {1:s}'.format(now, data.decode()))