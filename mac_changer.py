#!/usr/bin/env python
# this py script automate the process to change mac address in one step for linux system
import subprocess#used to run command of cli in py code automating sequential command to type in one step
import optparse#allow the user argument to parse and use in code eg -- or -help ,--interface wlan0 etc rather using input
import re
def get_arguments():
    parser=optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Set new MAC address to change")
    # argument contains --interface and --mac so not used
    # dest to assign value with respective name so we can use it later
    (options,arguments)=parser.parse_args()#option contain new mac and interface 
    if not options.interface:
        # parser.error gives error message if user dont specify reqd arguments and exit the program
        parser.error("[-] Please specify the interface use --help for more information.")
    elif not options.new_mac:
        parser.error("[-] Please specify the mac use --help for more information.")
    return options    
 
# use another subprocess.call command as it is not secure
# lets user to use any command in interface and execute it eg wlan0;ls;which is linux 
# way to execute another command after

# interface=input("input interface >")
# new_mac=input("input MAC >")
def change_mac(interface,new_mac):
    print("[+] Changing MAC address for " + interface +" to " + new_mac)
    # this subprocess command hijack the command
    # subprocess.call("ifconfig " + interface + " down", shell=True)
    # subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
    # subprocess.call("ifconfig " + interface + " up", shell=True)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    # new step to check and validate that the mac address actually changed
    # to verify we should get the o/p of ifconfig interface in commandline  after changing mac
    # use regx for filtering mac from o/p then compare with user specified new_mac
    # go to pythex.org for generating the expression
    ifconfig_result=subprocess.check_output(["ifconfig", interface])
    # print(ifconfig_result)
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
        # group 0 to get 0 index value if many selected . in this case one selected.
    else:
        print("[-] cannot read mac address.")

options=get_arguments()
 

current_mac=get_current_mac(options.interface)
print("current mac =" + str(current_mac))
change_mac(options.interface, options.new_mac)  
current_mac=get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Mac address has successfully changed to " + current_mac)
else:
    print("[-] unable to change mac address to " + str(options.new_mac))    



