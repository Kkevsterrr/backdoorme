import os

if __name__ == "__main__":
	if os.getuid() != 0:
		print("Please run this installation script as root!")
	else:	
		print("Installing Pip for Python.")
		os.system('apt-get install -y python3-pip >> /dev/null')
		os.system('apt-get install -y python-pip >> /dev/null')
		os.system("pip install --upgrade pip")
		print("Installing development Python version.")
		os.system('apt-get install -y build-essential libssl-dev libffi-dev python-dev >> /dev/null')
		print("Installing Nmap.")
		os.system('apt-get install -y nmap >> /dev/null')
		os.system('apt-get install -y python-tk >> /dev/null')
		print("Installing essential python packages.")
		os.system('pip install -r requirements.txt >> /dev/null')
		print("Downloading additional backdoors.")
		os.system('git clone https://github.com/n1nj4sec/pupy >> /dev/null')
