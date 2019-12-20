#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 23:39:34 2019

@author: ahmedkhaled
"""

import scapy.all as scapy

def scan(ip):
    arp_req = scapy.ARP(pdst=ip)
    print(arp_req.summary())
    scapy.ls(scapy.ARP())
    
scan("<your_ip>")