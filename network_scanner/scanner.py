#!/usr/bin/env python 

import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="target",help="enter range of your IPs")
    arguments = parser.parse_args()
    return arguments

def scan(ip) : 
    arp = scapy.ARP(pdst=ip)
    #arp.show()
    boardcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #boardcast.show()
    arp_boardcast = boardcast/arp
    #arp_boardcast.show()
    answered_list = scapy.srp(arp_boardcast,timeout=1,verbose=False)[0] #return 2 list but we use first list
    client_list = []
    for element in answered_list : 
        ele = {"ip":element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(ele)
    return client_list

def print_client(list_client) :
    print("IP\t\t\tMAC address")
    print("-----------------------------------------------------------")
    for element in list_client : 
        print(element["ip"]+"\t\t"+element["mac"])

arguments = get_arguments() 
result_client = scan(arguments.target)
print_client(result_client)
