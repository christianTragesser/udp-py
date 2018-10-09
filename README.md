## udp-py
[![pipeline status](https://gitlab.com/christianTragesser/udp-py/badges/master/pipeline.svg)](https://gitlab.com/christianTragesser/udp-py/commits/master)
Verification tool for UDP network traffic.

Networks for distributed applications utilizing UDP can be tricky to implement and troubleshoot. udp-py provides UDP packet sending and receiving capabilities for testing network and load balancing infrastructure.

### Receiver
receive.py is a service which listens for UDP packets on(currently only) port 5000.  Any string typed data sent to receive.py will be printed to STDOUT.

### Sender
send.py sends string typed binary messages to a UDP target provided as command argument; `send <host> -p <port>`. send.py will send UDP packets to the target host for 5 minutes unless keyboard interupt.
send.py is provided as an executable in the udp-py docker image:
```
$ docker run --rm -it registry.gitlab.com/christiantragesser/udp-py send -h
usage: sender.py [-h] [-p PORT] host

positional arguments:
  host                  UDP host target

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  UDP port target(default 5000)
```

#### Example: Test docker network UDP connectivity
Create a receiver instance named `receiver` on a docker network named `test`:
```
$ docker network create test
 ......
$ docker run -d --net test --name receiver registry.gitlab.com/christiantragesser/udp-py
 ......
$ docker ps
CONTAINER ID    IMAGE        COMMAND                  CREATED           STATUS          PORTS       NAMES
b91847e7cb14    udp-py       "/bin/sh -c 'python …"   43 seconds ago    Up 42 seconds   5000/udp   receiver
```

Send test UDP messages to the receiver instance:
```
$ docker run --rm -it --net test registry.gitlab.com/christiantragesser/udp-py send receiver

UDP target IP: receiver
UDP target port: 5000
Sending: Interval 0
Sending: Interval 1
Sending: Interval 2
Sending: Interval 3
Sending: Interval 4
Sending: Interval 5
Sending: Interval 6
Sending: Interval 7
Sending: Interval 8
Sending: Interval 9
```

The receiver container logs the corresponding received message:
```
$ docker logs receiver
2018-10-09 02:54:06.315081 - INFO: UDP Receiver Started
2018-10-09 02:54:06.315149 Received message: Interval 0
2018-10-09 02:57:15.939344 Received message: Interval 1
2018-10-09 02:57:16.944167 Received message: Interval 2
2018-10-09 02:57:17.953034 Received message: Interval 3
2018-10-09 02:57:18.956739 Received message: Interval 4
2018-10-09 02:57:19.960469 Received message: Interval 5
2018-10-09 02:57:20.964983 Received message: Interval 6
2018-10-09 02:57:21.970179 Received message: Interval 7
2018-10-09 02:57:22.975974 Received message: Interval 8
2018-10-09 02:57:23.946175 Received message: Interval 9
```