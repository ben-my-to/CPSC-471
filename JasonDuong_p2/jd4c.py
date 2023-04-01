#!/usr/bin/env python3
# Part 4 - UDP Heartbeat Monitor (Client)

import sys
import time
import random
from datetime import datetime
from socket import socket, AF_INET, SOCK_DGRAM

serverName = 'localhost'
serverPort = 12000

n_timeout = 0

# Used to identify a client process
client_id = sys.argv[1]

# Continuously sends message to the server
while True:
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    # Creates an arbitrary delay ranging between 2-25 seconds
    time.sleep(random.randint(2, 25))

    message = f'Jason client{client_id} heartbeat at {datetime.now().ctime()}'

    print(message)
    clientSocket.sendto(message.encode(), (serverName, serverPort))

    clientSocket.close()