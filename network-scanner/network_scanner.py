#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 23:39:34 2019

@author: ahmedkhaled
"""

import scapy.all as scapy

def scan(ip):
    arp_req = scapy.ARP()
    print(arp_req.summary())
    
scan("192.168.1.1/24")