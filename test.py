#!/usr/bin/env python
import subprocess 
import re 
 
command="netsh wlan show profile"
networks=subprocess.check_output(command,shell=True) 
network_names = re.findall("Profile", networks)
print( network_names.group(0))