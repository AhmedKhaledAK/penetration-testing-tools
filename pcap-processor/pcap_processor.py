#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import re
import zlib
import scapy.all as scapy

images_dir = "/home/Documets/Kali-Linux/penetration-testing-tools/pcap-processor/images"
pcap_file = "arp_spoofer.pcap"

def find_http(pcap_file):
    images = 0
    packets = scapy.rdpcap(pcap_file)
    sessions = packets.sessions()
    var = 0
    for sess in sessions:
        payload = ""
        for packet in sessions[sess]:
            try:
                if 'TCP' in packet:
                    print("TCP FOUND")
                    var += 1
                    #print(packet['TCP'])
                if packet['TCP'].dport == 80 or packet['TCP'].sport == 80:
                    payload += str(packet['TCP'].payload)
            except:
                pass
            
            
    print("var:",var)


def main():
    find_http(pcap_file)

main()