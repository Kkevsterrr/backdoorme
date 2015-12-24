# backdoorme [![Build Status](https://travis-ci.org/Kkevsterrr/backdoorme.png)](https://travis-ci.org/Kkevsterrr/backdoorme)

 Backdoorme is a powerful utility capable of backdooring Unix machines with a slew of backdoors.  
 
 Backdoorme relies on having an existing SSH connection or credentials to the victim, through which it will transfer and deploy any backdoors.  In the future, this reliance will be removed as the tool is expanded. 
 To set up SSH, please see here: https://help.ubuntu.com/community/SSH/OpenSSH/Configuring
 
 Please only use Backdoorme with explicit permission - please don't hack without asking.  
## Usage
To start backdoorme, first ensure that you have the required dependencies. 
```python
$ python dependencies.py
```
Launching backdoorme:
```
$ python master.py
   ___           __      __              __  ___
  / _ )___ _____/ /_____/ /__  ___  ____/  |/  /__
 / _  / _ `/ __/  '_/ _  / _ \/ _ \/ __/ /|_/ / -_)
/____/\_,_/\__/_/\_\\_,_/\___/\___/_/ /_/  /_/\__/
Welcome to BackdoorMe, a powerful backdooring utility. Type "help" to see the list of available commands.
Type "addtarget" to set a target, and "open" to open an SSH connection to that target.
Using local IP of 10.1.0.1.
>>
```
To add a target:
``` 
>> addtarget
Target Hostname: 10.1.0.2
Username: victim
Password: password123
 + Target 1 Set!
>>
 ```
## Functionality  
Backdoorme comes with a number of built-in backdoors and modules.  Backdoors are specific components to create and deploy a specific backdoor, such as a netcat backdoor or msfvenom backdoor.  Modules can be applied to any backdoor, and are used to make backdoors more potent, stealthy, or more readily tripped. 

### Backdoors
Currently enabled backdoors include:
 
 - Bash
 - Netcat
 - Netcat-traditional
 - Metasploit
 - Perl
 - Pupy
 - Python
 
### Modules
Currently enabled modules include:
 - Poison
  - Performs bin poisoning on the target computer - it compiles an executable to call a system utility and an existing backdoor.
  - For example, if the bin poisoning module is triggered with "ls", it would would compile and move a binary called "ls" that would run both an existing backdoor and the original "ls", thereby tripping a user to run an existing backdoor more frequently. 
 - Cron
  - Adds an existing backdoor to the root user's crontab to run with a given frequency.  
 
## Contributing
Backdoorme is still very much in its infancy! Feel free to contribute to the project - simply fork it, make your changes, and issue a pull request. 
