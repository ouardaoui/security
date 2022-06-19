#!/usr/bin 
sudo iptables --flush
sudo iptables -I INPUT -j NFQUEUE --queue-num 1
sudo iptables -I OUTPUT -j NFQUEUE --queue-num 1
sudo python3 spoof.py
