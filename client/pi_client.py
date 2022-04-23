#!/usr/bin/env python3

import socket

# HOST = '192.168.86.200'  # The server's hostname or IP address
HOST = socket.gethostbyname(socket.gethostname())
PORT = 2049        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))
