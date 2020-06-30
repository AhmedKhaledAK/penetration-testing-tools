#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import re
import zlib
import scapy.all as scapy

images_dir = "/home/Documets/Kali-Linux/penetration-testing-tools/pcap-processor/images"
pcap_file = "dummy_data.pcapng"

def get_headers(payload):
    headers = dict()
    try:
        headers_raw = payload[:payload.index("\r\n\r\n")+2]
        headers = dict(re.findall(r"([a-zA-Z-]*): ([a-zA-z-/0-9]*)",headers_raw))
    except:
        return None
    
    if "Content-Type" not in headers:
        return None
    
    return headers

def extract_image(headers, payload):
    image = None
    image_type = None
    
    try:
        if "image" in headers['Content-Type']:
            image_type = headers['Content-Type'].split("/")[1]
            image = payload[payload.index("\r\n\r\n") + 4:]
    except:
        return None, None
    
    return image, image_type
            

def write_to_file(image, image_type):
    

def find_http(pcap_file):
    images = 0
    packets = scapy.rdpcap(pcap_file)
    sessions = packets.sessions()
    var = 0     # for testing purposes
    for sess in sessions:
        payload = ""
        for packet in sessions[sess]:
            try:
                if 'TCP' in packet:
                    print("TCP FOUND")
                    var += 1
                    #print(packet['TCP'])
                if packet['TCP'].dport == 80 or packet['TCP'].sport == 80:
                    print("PORT 80 FOUND")
                    payload += str(packet['TCP'].payload)
            except:
                pass
        #for testing purposes
        print("payload")
        print(payload)
        
        headers = get_headers(payload)
        print("headers:")
        print(headers)
        
        if headers is None:
            continue
        
        image, image_type = extract_image(headers, payload)
        
        print("image:")
        print(image)
        print("\niamge type:")
        print(image_type)
        
        if image is not None and image_type is not None:
            wrte_to_file(image, image_type)
        
    # for testing purposes         
    print("var:",var)


def main():
    find_http(pcap_file)

main()