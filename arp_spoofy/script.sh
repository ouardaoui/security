#!/usr/bin

echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
sudo python3 *.py

