#!/usr/bin/env python3
# Part 4 - UDP Heartbeat Monitor (Server)

import time
from socket import socket, timeout, AF_INET, SOCK_DGRAM

# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('', 12000))

# Sets the timeout to 20 seconds
serverSocket.settimeout(20)

# Time difference is zero upon the first receive message from a client
delta_time = 0
last_heartbeat_time = {}

try:
    while True:
        # Receive the client packet along with the address it is coming from
        message, address = serverSocket.recvfrom(1024)

        time_recv = time.time()
        client_id = message[12:13]

        # The server calculate the time difference from the last heartbeat
        # (i.e., the time of the previous received message)
        if last_heartbeat_time.get(client_id):
            delta_time = int(time_recv - last_heartbeat_time[client_id])

        print(f'Server received: {message.decode()} Last heartbeat received {delta_time} seconds ago')

        # Update time difference from the last heartbeat request
        # If it was the first response from a client, the server initiates the time receive
        last_heartbeat_time[client_id] = time_recv

        # The server responds
        serverSocket.sendto(message, address)
except timeout:
    print('No heartbeat after 20 seconds. Server quits. Server stops.')
    serverSocket.close()
