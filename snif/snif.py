#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http

def snif(interface): 
    scapy.sniff(iface=interface,store=False,prn=process_packet)

def process_packet(packet):
    if packet.haslayer(http.HTTPRequest) :
    #packet.haslayer(scapy.Raw):
            print(packet.show())        
snif("eth0")
