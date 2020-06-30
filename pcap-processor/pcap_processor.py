#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import re
#import zlib
import scapy.all as scapy

# change this according to your path
images_dir = "/home/ahmedkhaled/Documents/Kali-Linux/penetration-testing-tools/pcap-processor/images"
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
                

def write_to_file(image, image_type, images_cnt):
    filename = "%s-pcap_image-%d.%s"%(pcap_file, images_cnt, image_type)
    fd = open("%s/%s"%(images_dir,filename), "wb")
    fd.write(image)
    fd.close()

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
        
        #fd = open("/home/ahmedkhaled/Desktop/unrelated/IMG-20180809-WA0009.jpg", "rb")

        #image = fd.read()
        
            
        print("image:")
        print(image)
        print("\nimage type:")
        print(image_type)
        
        if image is not None and image_type is not None:
            write_to_file(image, image_type, images)
            
        images += 1
        
    # for testing purposes         
    print("var:",var)
    return images


def main():
    cnt = find_http(pcap_file)
    print(cnt)

main()