#!/usr/bin/env python3
# Part 1 - UDP Pinger with No Delay and No Loss

import time
from statistics import mean
from datetime import datetime
from socket import socket, timeout, AF_INET, SOCK_DGRAM

serverName = 'localhost'
serverPort = 12000

TOTAL_PINGS = 10
n_timeout = 0
rtt_list = []

for n_ping in range(1, TOTAL_PINGS+1):
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    # Sets timeout value to 1 second
    clientSocket.settimeout(1)

    # Stores the time when the client sends the message
    start_time = time.time()

    # Send ping message using UDP to server
    message = f'Jason {n_ping} {datetime.now().ctime()}'
    clientSocket.sendto(message.encode(), (serverName, serverPort))

    print(f'Jason {n_ping}: ', end='')

    try:
        receivedMessage, _ = clientSocket.recvfrom(1024)

        # Calculates and converts the RTT from seconds to milliseconds
        rtt_list.append((time.time() - start_time) * 1000)

        # Prints the response message from the server
        # Retreives the latest ping's RTT (i.e., top of stack)
        print(f'server reply: {receivedMessage.decode()}, RTT = {rtt_list[-1]:.2f} ms')
    except timeout:
        n_timeout += 1
        print('Request timed out')

    clientSocket.close()

# Summary of all pings
print(f'Min RTT = {min(rtt_list):.2f} ms',
      f'Max RTT = {max(rtt_list):.2f} ms',
      f'Avg RTT = {mean(rtt_list):.2f} ms',
      f'Packet lost = {n_timeout / TOTAL_PINGS:.2%}', sep='\n')
