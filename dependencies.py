import os

os.system('git clone https://github.com/paramiko/paramiko')
os.system('easy_install ./')
os.system('apt-get install python-pip')
os.system('pip install scp')
os.system('pip install ecdsa')
os.system('rm /usr/local/lib/python2.7/dist-packages/paramiko/transport.py')
os.system('cp paramiko/transport.py /usr/local/lib/python2.7/dist-packages/paramiko')
os.system('apt-get install nmap')
os.system('apt-get install python-tk')
os.system('pip install rpyc')
os.system('pip install pefile')

