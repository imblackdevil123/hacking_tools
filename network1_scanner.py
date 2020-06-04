#!/usr/bin/env python
import scapy.all as scapy#1 download this to implement this 
# first need to creat packet asking who has this ip and broadcasting it using broadcast address dest mac=broadcast mac
# use arp to do
import argparse#same as optparse but successor of optparse so use argparse simply replace arg=opt and argument=option
def get_arguments():#13 
    parser=argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="target IP/IP range")
    # (options,arguments)=parser.parse_args()#13 argparse only return options so
    options = parser.parse_args()
    return options

def scan(ip):
    # first creaate packet using scapy
    arp_request=scapy.ARP(pdst=ip)#2 ,6 for setting pdst
    # arp_request.show()# to get more info than summary do after set pdst
    # arp_request.pdst=ip#5 to set for particular ip rather than 0.0.0.0 in 3 ie summary but alternet way to set is in 2 ie when obj created
    # print(arp_request.summary())#3 give summary of
    # scapy.ls(scapy.ARP())#4 used to list values which can be used to set them eg pdst in list to ip
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")#7 for setting broadcast address in packet which require ethernet frame
    # broadcast.show()# do after set dst
    # print(broadcast.summary())#7 similar for arp obj
    # scapy.ls(scapy.Ether())#7 similar for arp obj ,set dest
    # broadcast.dst="ff:ff:ff:ff:ff:ff"#8 or direct set in obj look up set broadcast address
    # print(broadcast.summary())#8 get value for mac os source and dest as broadcast
    arp_request_broadcast=broadcast/arp_request#combine 2 packet to form one packet to send containing both ip and broadcast mac
    # arp_request_broadcast.show()#9
    answered_list,unanswered_list=scapy.srp(arp_request_broadcast,timeout=1)#10 for send the packetand receive the outcome as ans and unans
    #here ether address is broadcast so it go to righ direction of same subnet devices
    #if you have used different mac and config some value in ls than it would have gone to that device and received response for other purpose
    #timeout is no of sec so program dont go death waiting outcome or response in same line and not proceeding
    #there is also sr function but srp is used to send packet with customn ether part  
    # two response answered and unanswered packet  use ans ,unans contain more data print and look
    # print(answered_list.summary())

    #error due to verbose not used as in arp spoof py script
    print("IP\t\t\tMAC Address\n...........................................")
    for element in answered_list:
        print(element[1].psrc + "\t\t" + element[1].hwsrc)
        
options=get_arguments()        
scan(options.target)

# run like ./network1_scanner.py -t 10.0.2.3/24
# pip3 install scapy-python3