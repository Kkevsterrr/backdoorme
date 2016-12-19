import socket
import time
import sys
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = sys.argv[1]
s.bind(("0.0.0.0", int(port)))
s.listen(5)

def interact(sock):
    command=''
    print("Accepted Connection!")
    time.sleep(.25)
    #print(sock[0].recv(0x10000)),
    while(command != 'exit'):
     	command = raw_input()
     	#print "hi"
        sock[0].send(command + '\n')
        time.sleep(.25)
        data = sock[0].recv(0x10000)
        print data,
        #os.system("echo \"Sent " + command + "\" >> asdf.asdf")
        #os.system("echo \"Received " + data + "\" >> asdf.asdf")
    return

interact(s.accept()) 	

