#!/usr/bin/env python
import scapy.all as scapy#download this to implement this 
def scan(ip):
    scapy.arping(ip)
scan("192.168.1.1/24")


# echo 1 > /proc/sys/net/ipv4/ip_forward command for  ip forwarding to router in arp spoof attack ie mimf
