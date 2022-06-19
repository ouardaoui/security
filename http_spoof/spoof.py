#!/usr/bin/env

from netfilterqueue import NetfilterQueue
import scapy.all as scapy

ack_list = []
def print_and_accept(pkt):
    scapy_packet = scapy.IP(pkt.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        try : 
            if scapy_packet[scapy.TCP].dport == 80:
                print("HTTP request")
                if "gzip" in str(scapy_packet[scapy.Raw].load) :
                    print("[+] gzip request")
                    ack_list.append(scapy_packet[scapy.TCP].ack)
                    print(scapy_packet.show())
            elif scapy_packet[scapy.TCP].sport ==80:
                if scapy_packet[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("HTTP response")
                    print(scapy_packet.show())
        except IndexError : 
            pass
    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('something went wrong')

nfqueue.unbind()
