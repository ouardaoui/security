#!/usr/bin 
sudo iptables --flush
sudo iptables -I FORWARD -j NFQUEUE --queue-num 1

sudo python3 spoof.py
