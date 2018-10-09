## udp-py
[![pipeline status](https://gitlab.com/christianTragesser/udp-py/badges/master/pipeline.svg)](https://gitlab.com/christianTragesser/udp-py/commits/master)

Infrastructure verification tool for UDP network traffic.

Networks for distributed applications utilizing UDP can be tricky to implement and troubleshoot. udp-py supplies mechanisms for sending and receiving UDP traffic when testing network and load balancing infrastructure.

### Receiver
receive.py is a service which listens for UDP packets on(currently only) port 5000.  Any string typed binary data sent to receive.py will be printed to STDOUT.

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
1) Create a receiver instance named `receiver` on a docker network named `test`:
```
$ docker network create test
 ......
$ docker run -d --net test --name receiver registry.gitlab.com/christiantragesser/udp-py
 ......
$ docker ps
CONTAINER ID    IMAGE        COMMAND                  CREATED           STATUS          PORTS       NAMES
b91847e7cb14    udp-py       "/bin/sh -c 'python …"   43 seconds ago    Up 42 seconds   5000/udp   receiver
```

2) Send test UDP messages to the receiver instance:
```
$ docker run --rm -it --net test registry.gitlab.com/christiantragesser/udp-py send receiver

UDP target IP: receiver
UDP target port: 5000
Sending: Interval 0
Sending: Interval 1
Sending: Interval 2
Sending: Interval 3
Sending: Interval 4
```

3) The receiver logs the corresponding received message:
```
$ docker logs receiver
2018-10-09 02:54:06.315081 - INFO: UDP Receiver Started
2018-10-09 02:54:06.315149 Received message: Interval 0
2018-10-09 02:57:15.939344 Received message: Interval 1
2018-10-09 02:57:16.944167 Received message: Interval 2
2018-10-09 02:57:17.953034 Received message: Interval 3
2018-10-09 02:57:18.956739 Received message: Interval 4
```

#### Example: Test an exposed UDP service on Kubernetes
1) Deploy the udp-py receiver with 2 replicas and expose with `LoadBalancer` service:
```
$ kubectl run udp-py --image=registry.gitlab.com/christiantragesser/udp-py --port=5000 --replicas=2
deployment "udp-py" created

$ kubectl expose deployment udp-py --type=LoadBalancer --protocol=UDP
service "udp-py" exposed
```
2) Verify two available udp-py pods and the external IP of the udp-py service:
```
$ kubectl get po --selector run=udp-py
NAME                      READY     STATUS    RESTARTS   AGE
udp-py-67f8fbfbcc-kfjrw   1/1       Running   0          3m
udp-py-67f8fbfbcc-sqg6w   1/1       Running   0          3m

$ kubectl get svc udp-py
NAME      TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)          AGE
udp-py    LoadBalancer   10.107.239.201   192.168.22.12   5000:32364/UDP   2m
```

3) Send test messages to the exposed udp-py service:
```
$ docker run --rm -it registry.gitlab.com/christiantragesser/udp-py send 192.168.22.12

UDP target IP: 192.168.22.12
UDP target port: 5000
Sending: Interval 0
Sending: Interval 1
Sending: Interval 2
Sending: Interval 3
Sending: Interval 4
Sending: Interval 5
```
4) Verify UDP traffic has been distributed amoungst the deployed pods:
```
$ kubectl logs udp-py-67f8fbfbcc-sqg6w
2018-10-09 12:45:43.238795 - INFO: UDP Receiver Started
2018-10-09 12:45:43.238871 Received message: Interval 0
2018-10-09 12:51:14.209789 Received message: Interval 2
2018-10-09 12:51:16.213692 Received message: Interval 3
2018-10-09 12:51:17.216947 Received message: Interval 5

$ kubectl logs udp-py-67f8fbfbcc-kfjrw
2018-10-09 12:45:44.389040 - INFO: UDP Receiver Started
2018-10-09 12:45:44.389149 Received message: Interval 1
2018-10-09 12:51:15.212153 Received message: Interval 4
```