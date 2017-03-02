#!/usr/bin/python

import socket
import subprocess
import sys
import threading

def interact(sock, address):
	while True:
		print(" >>>"),
		command = raw_input()

		sock.sendto(command, address)

		try:
			response, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
			print(response)

		except KeyboardInterrupt:
			pass


if(len(sys.argv) < 2):
	print("Usage: ./udpclient <recv_port>")
	exit(1)

#read requests, send data, receive data, print data.

recv_ip = "0.0.0.0" 
recv_port = int(sys.argv[1])

#send_ip = sys.argv[2] #127.0.0.1
#send_port = int(sys.argv[3]) #5006

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((recv_ip, recv_port))

#sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP



while True:
	i = 0
	identifier, addr = sock.recvfrom(1024)
	if(identifier == "Begin Connection id: 3242"):
		i += 1
		print("Connection " + str(i) + " received")
		interact(sock, addr)
		#thread = threading.Thread(target = interact, args = (sock, addr))
		#thread.start()
		
