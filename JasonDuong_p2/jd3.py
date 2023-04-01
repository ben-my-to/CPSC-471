#!/usr/bin/env python3
# Part 3 - UDP Pinger with Delays and Packet Losses

import time
import random
from socket import socket, AF_INET, SOCK_DGRAM

# Artifical Percentage of Packet Loss Occurrence
THRESHOLD = 10

# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('', 12000))

while True:
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)

    # Creates an arbitrary, random RTT delay ranging from 10-20 milliseconds
    time.sleep(random.randint(10, 20) / 1000)

    # Does not send original packet back if random value is within the first 10 integers
    if random.randrange(100) < THRESHOLD:
        continue

    # The server responds
    serverSocket.sendto(message, address)