import threading
import pexpect

class Connection:
	def __init__(self, intro, conn, numb):
		self.open = False
		self.type = intro
		self.connection = conn
		self.listening = 1
		self.number = int(numb) + 1
		self.thread = threading.Thread(target=self.wait)
		self.thread.start()
	def __str__(self):
		string = ""
		if(self.open):
			string += "Open\n"
		else:
			string += "Closed\n"
		string += self.type + "\n"
		#string += self.connection + "\n"
		return string

	def wait(self):
		try:
			self.connection.expect("Connection Received.")
			print("\nSession " + str(self.number) + " has recieved a connection. Type sessions -i " + str(self.number) + " to interact.")
			self.open = True
		except:
			self.open = False

	def interact(self):
		if self.connection.isalive():
			if self.listening == 0:
				self.connection.sendline()
				print("Press Control + ] to exit the shell."),

			else:
				self.listening = 0
				print("Press Control + ] to exit the shell.")
			self.connection.interact(escape_character='\x1d', input_filter=None, output_filter=None)
			self.open = True #at least for now
		else:
			print("The connection has been lost")