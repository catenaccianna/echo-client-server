#!/usr/bin/env python3

import socket
import struct
import time

# HOST = '192.168.86.200'  # Standard loopback interface address (localhost)

# for two programs on the same computer on the same network:
# HOST = socket.gethostbyname(socket.gethostname())

# for two programs on different devices:
# HOST = socket.gethostname()
HOSTS = ['192.168.1.39', '192.168.1.40', '192.168.1.41', '192.168.1.42']
HOST_INDEX = 0
HOST = HOSTS[HOST_INDEX]
PORT = 2049        # Port to listen on (non-privileged ports are > 1023)

# prolly read in from a generic file I create, as the message doesn't matter
# as much as the time of transmission in this case. HOWEVER, it does
# seem like longer files may take longer to send?
message = open('KB_0.txt')
identifier = message.read(1)

# cast to multiple local ips in sequence for multicast & broadcast
# since I know unicast works
# I think this would be like the range of ips thing that anik was talking about

# UNICAST (TCP)
if identifier == 0:
    print("BEGIN: "+str(time.time())+"\n")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
    print("END: "+str(time.time())+"\n")

# MULTICAST (UDP)
if identifier == 1:
    IS_ALL_GROUPS = True

    receivers = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if IS_ALL_GROUPS:
        # on this port, receives ALL multicast groups
        sock.bind(('', PORT))
    else:
        # on this port, listen ONLY to HOST
        sock.bind((HOST, PORT))
    mreq = struct.pack("4sl", socket.inet_aton(HOST), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        # For Python 3, change next line to "print(sock.recv(10240))"
        print(sock.recv(1024))

# BROADCAST (UDP)
if identifier == 2:
    IS_ALL_GROUPS = True

    receivers = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # this is where we bind to all ports that are running right now
    sock.bind(('', PORT))
    mreq = struct.pack("4sl", socket.inet_aton(HOST), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        # For Python 3, change next line to "print(sock.recv(10240))"
        print(sock.recv(1024))


# source for UDP methods: https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python

# how is this going to work if only one pi is connected to either the ethernet or a computer?
# like if we're finding this by ip address?

# also how to write a list of ip addresses to ping
