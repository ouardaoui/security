#!/usr/bin

sudo service apache2 start
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
sudo python3 *.py
sudo service apache2 stop
