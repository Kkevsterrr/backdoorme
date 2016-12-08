import os

os.system('apt-get install -y python3-pip')
os.system('pip install scp')
os.system('pip install ecdsa')
os.system('rm /usr/local/lib/python2.7/dist-packages/paramiko/transport.py')
os.system('cp paramiko/transport.py /usr/local/lib/python2.7/dist-packages/paramiko')
os.system('apt-get install -y nmap')
os.system('apt-get install -y python-tk')
os.system('pip install rpyc')
os.system('pip install colorama')
os.system('pip install pefile')
os.system('pip install paramiko')
os.system('git clone https://github.com/n1nj4sec/pupy')
