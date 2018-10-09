#!/usr/local/bin/python3
import socket
import time
from argparse import ArgumentParser

def sendPackets(host, port):
    interval = 0
    print('\nUDP target IP:', host)
    print('UDP target port:', int(port))
    while interval <= 300:
        MESSAGE = 'Interval '+str(interval)
        print('Sending:', MESSAGE)
    
        sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
        sock.sendto(bytes(MESSAGE, 'utf-8'), (host, int(port)))
        interval += 1
        time.sleep(1)

def main():
    parser = ArgumentParser(prog='sender.py')
    parser.add_argument('host', type=str,
                        help='UDP host target')
    parser.add_argument('-p', '--port', type=int,
                        help='UDP port target(default 5000)', default=5000)
    args = parser.parse_args()
    sendPackets(args.host, args.port)

if __name__ == '__main__':
    main()