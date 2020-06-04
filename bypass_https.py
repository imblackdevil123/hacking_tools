#!/usr/bin/env python
# data in http is send as plane text and we can read and modify if we are in middle of connection but for https it is encrypted using ssl or tls
# so we cannot adapt to change the html code as we do previously in code_injector.py file(for http)
# SSlstrip is used hacker device to downgrade https to http but dont work for HSTS implemented websites as they get hardcoded in browser itself to use https
# if hsts not implemented first request from client is always http unless they type url with https
# afterthat server response and insist to use https after https is used by both to communicate
# mimf can downgrade https to http changing req and res of client and server from start
# sslstrip basically downgrade https response from server to http and upgrade http request from target to https
# in this way target thinks server only knows http and server thinks target using https as it is upgraded to https at hacker device using sslstrip before sending to server
# here server is having both req and res as https and client is having both req and res as http.ie downgrade one side and upgrade other side 
# one exception for hsts
# sslstrip actually written in python by moxie #target to find moxie code and read and analyze it how it is implemented
# very useful command  if you use some proxy and want to redirest data to flow to that proxy

algorithm
# to runsslstrip and bypass https
# first flush iptable using command iptable --flush
# become middle using arp_spoof.py python script
# run sslstrip using command sslstrip
# sslstrip use port 1000 so need redirect any packet that come in p0rt 80 to 1000.do this redirection using iptable
# iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 1000#A implies appending rule and rule for tcp packet
# finally run the tool that you want to do ex sniffer.py ,dns_spoofer.py,code_injector.py ,replace_download.py work for https
# here for sniffer it works good with sslstrip but for other it dont work good
# the reason is both ssl strip and other code eg replace_download.py require to modify the packet content so there require some adjustment so they dont interfair with oneanother work
# here there are two iptable rule one for sslstrip(prerouting) and other for replace_download.py(forward chain)
# prerouting rule redirect all packet of port 80 to 1000 for sslstrip so there will nothing stored in forward chain
# so replace rule of forward chain and use i/p and 0/p rule that we use when we tested locally
# so run three iptable command to work and change the replace_download.py code replace 80 in code with 1000 because packet are redirected to 1000
# hence this algo will be compatible for both http and https website check it
# small bugfix in png file

# to make work with code_injector.py to https similar as abve for replace_download.py 
# change 80 to 1000 in code 
# all same ie 3 iptable command
# but uncomment the line which replace http v1.1 to http v1.0 because 1.1 send response in chunks which dont have content length and we try to modify it
# but if we replace v1.1 with v1.0 in request side ,server thinks that browser only understand v1.0 and before sending its change its content and send in v1.1

