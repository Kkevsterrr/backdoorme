class Connection:
	def __init__(self, intro, conn):
		self.open = False
		self.type = intro
		self.connection = conn
	  	self.listening = 1
	def __str__(self):
		string = ""
		if(self.open):
			string += "Open\n"
		string += self.type + "\n"
		#string += self.connection + "\n"
		return string
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