import socket
import time

UDP_IP = '127.0.0.1'
UDP_PORT = 5000

interval = 0
print('\nUDP target IP:', UDP_IP)
print('UDP target port:', UDP_PORT)
while interval <= 300:
    MESSAGE = 'Interval '+str(interval)
    print('Sending:', MESSAGE)

    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes(MESSAGE, 'utf-8'), (UDP_IP, UDP_PORT))
    interval += 1
    time.sleep(1)