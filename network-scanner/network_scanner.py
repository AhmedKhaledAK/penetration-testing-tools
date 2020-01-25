#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 23:39:34 2019
"""

import scapy.all as scapy

def scan(ip):
    # the next two lines creates a packet that asks for a specific ip
    arp_req_packet = scapy.ARP()
    arp_req_packet.pdst=ip
    arp_req_packet.show()
    # creating the broadcast MAC address packet
    broadcast_packet = scapy.Ether()
    broadcast_packet.dst = "ff:ff:ff:ff:ff:ff"
    broadcast_packet.show()
    # combining packets
    bc_arpreq_packet = broadcast_packet/arp_req_packet
    bc_arpreq_packet.show()
    ans, unans = scapy.srp(bc_arpreq_packet)
    ans.show()
    unans.show()
    
    
scan("<ip>")