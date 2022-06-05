#!/usr/bin/env python 

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface for change mac addres")
    parser.add_option("-m", "--mac", dest="mac", help="mac address")
    (options,arguments) = parser.parse_args()
    if not options.interface: 
        parser.error("[-] provide interface --help for more info")
    elif not options.mac: 
        parser.error("[-] provide MAC address --help for more info")
    return options

def change_mac(interface,new_MAC):
        subprocess.call(["sudo", "ifconfig", interface, "down"])
        rc = subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_MAC])
        subprocess.call(["sudo", "ifconfig", interface, "up"])
        if not rc : 
            print("[+] changing mac address for "+ interface + " to " + new_MAC)
        else :
            print("[-] cant change address")

def get_current_mac(interface):
    try : 
        ifconfig_result= subprocess.check_output(["sudo","ifconfig",interface],encoding='utf-8')
        mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_result)
        return mac_result.group(0)
    except subprocess.CalledProcessError as e:
        print("[-] no readable mac address")

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC : " + str(current_mac))
change_mac(options.interface,options.mac)
