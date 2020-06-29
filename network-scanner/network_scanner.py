#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 23:39:34 2019

Description: scan connected devices on the same network.

run this script from terminal using: python network_scanner.py -i <ip>
"""

import scapy.all as scapy
import argparse
#from IPy import IP


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", dest="ip", help="The IP address/subnet you want to send the packet to")
    values = parser.parse_args()
    return values.ip

def scan(ip):
    # the next two lines creates a packet that asks for a specific ip
    arp_req_packet = scapy.ARP()
    arp_req_packet.pdst=ip
    # creating the broadcast MAC address packet
    broadcast_packet = scapy.Ether()
    broadcast_packet.dst = "ff:ff:ff:ff:ff:ff"
    # combining packets
    bc_arpreq_packet = broadcast_packet/arp_req_packet
    # sending and receiving packets, the answered ones and the unanswered. The timeout is necessary.  
    ans_list = scapy.srp(bc_arpreq_packet, timeout=1)[0]
    for el in ans_list:
        print(el[1].psrc, el[1].hwsrc)
    
    
ip = parse_command_line()
if ip is None:
    print("IP address is required")
else:
    try:
        #IP(ip,make_net=True)
        scan(ip)
    except ValueError:
        print("Not a valid IP address")
        
