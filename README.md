# About
Every Operating System has a hosts file. For OSX, its located at ```/private/etc/hosts```.  
This file contains rules on which websites to not allow and redirection logic. 
We are using this file to redirect to a custom IP that can tell us the connection is 
insecure. Our python code shall modify this file automatically based on the 
network the system is connected to. 

# Requirements
1. Needs Python 3. Haven't tested on python 2.7 or earlier  
**Supports MacOS as of now, but can easily be configured for other OS too. Need to just change the hosts path**

# Setup
1. Copy original hosts file to project directory and rename it as original_hosts
2. Add the trusted public IPs in trusted_ips.json
3. Configure domains, redirect IP and hosts file path in blockade.py under the ```# Configure these``` comment
4. Configure WAIT_TIME in blockade_start.py

Note: The REDIRECT_IP currently used is the IP of example.com. You can run ```ping example.com to get the ip```

# Test
Run the command ```sudo python blockade_start.py```

# Install PM2 on MacOS
1. Open terminal
2. Run ```cat ~/.zshrc```. If you see any output, then you have this file (.zshrc). Elseif you get error that file not found, run ```touch ~/.zshrc```
3. Run ```curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash```. This will install nvm which is needed to install pm2
4. Run below commands:  
4.1 ```source ~/.zshrc```. If you are asked ```Ignore insecure directories and continue...```, type ```y``` and press enter.  
   4.2. ```nvm install 12.19.0```  
   4.3. ```npm install -g pm2```  
5. If you have reached till here, pm2 is successfully installed. 

# Start PM2 process
1. Open terminal and navigate to project root directory
2. Run ```pm2 kill```
3. Run ```sudo ./start.sh```
4. You can open the latest log file in logs folder to track the actions

# Useful PM2 Commands
1. To Check running processes: ```pm2 list```
2. Stop application: ```pm2 stop blockade```

# Stop and Reset Hosts file
Before running scripts, ensure you make the .sh (stop.sh, reset_hosts.sh) scripts executable. 
1. To directly stop pm2 process and reset hosts, run ```./stop.sh```
2. To just reset hosts (replaces hosts file with original one, this will allow the blocked websites), run ```./reset_hosts.sh```

# Setting as startup script
Once your application is successfully running, Run below commands to auto start 
1. ```pm2 save```
2. ```pm2 startup```

You can now restart and run ```pm2 list``` to see if application is running. 

# License
MIT License
