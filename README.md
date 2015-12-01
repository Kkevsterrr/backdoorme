# backdoorme [![Build Status](https://travis-ci.org/Kkevsterrr/backdoorme.png)](https://travis-ci.org/Kkevsterrr/backdoorme)

 Backdoorme is a powerful utility capable of backdooring Unix machines with a slew of backdoors.  
 
 Backdoorme relies on having an existing SSH connection or credentials to the victim, through which it will transfer and deploy any backdoors.  In the future, this reliance will be removed as the tool is expanded. https://help.ubuntu.com/community/SSH/OpenSSH/Configuring
 
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
### Functionality  
Currently enabled backdoors include:
 
 - Bash
 - Netcat
 - Netcat-traditional
 - Metasploit
 - Perl
 - Pupy
 - Python
  
## Contributing
Backdoorme is still very much in its infancy! Feel free to contribute to the project - simply fork it, make your changes, and issue a pull request. 
