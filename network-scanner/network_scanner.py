#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 23:39:34 2019

@author: ahmedkhaled
"""

import scapy.all as scapy

def scan(ip):
    arp_req_packet = scapy.ARP()
    arp_req_packet.pdst=ip
    arp_req_packet.show()
    broadcast_packet = scapy.Ether()
    broadcast_packet.dst = "ff:ff:ff:ff:ff:ff"
    broadcast_packet.show()
    bc_arpreq_packet = broadcast_packet/arp_req_packet
    bc_arpreq_packet.show()
    
scan("<ip>")