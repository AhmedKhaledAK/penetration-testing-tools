#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 23:39:34 2019

@author: ahmedkhaled
"""

import scapy.all as scapy

def scan(ip):
    arp_req = scapy.ARP()
    arp_req.pdst=ip
    arp_req.show()
    broadcast = scapy.Ether()
    broadcast.dst = "ff:ff:ff:ff:ff:ff"
    broadcast.show()
    bc_arpreq = broadcast/arp_req
    bc_arpreq.show()
    
scan("<ip>")