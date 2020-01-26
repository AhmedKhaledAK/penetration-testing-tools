#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 18:44:25 2019

run this from terminal using: python3 mac_changer.py -i <interface_name> -m <new_mac>
"""

import subprocess
import optparse
import re


def get_current_address(interface):
    call_result = subprocess.check_output(["ifconfig", interface])
    call_result = str(call_result, 'utf-8')
    search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", call_result)
    if search_result is not None:
        print("This is the current MAC address: " + search_result.group(0))
        return search_result.group(0)
    else:
        print("Could not find a MAC address for this interface")
        # returns NoneType

def change_mac(interface, new_mac):
    # this way of calling the call method is more secure so that a hacker can't hijack the system
    # by using for example: ;ls; because python will treat this whole list as a single command and not
    # as multiple commands
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def parse_command_line():
    # creating an instance from OptionParser
    parser = optparse.OptionParser()
    # adding arguments to the command-line arguments
    parser.add_option("-i", "--interface", dest="interface", 
                  help="The Interface that you want to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="The new MAC address of the interface chosen")
    # parsing the arguments passed to add_option method above and 
    # returned its return value (which is a tuple of the Values and list of the arguments)
    values = parser.parse_args()
    err =0
    if values[0].interface is None and values[0].new_mac is None:
        print("no interface and MAC address specified, exiting...")
        err=2
    elif values[0].interface is None:
        print("no interface specified, exiting...")
        err=1
    elif values[0].new_mac is None:
        print("no MAC address specified, exiting...")
        err=1
    return (parser.parse_args(),err)

values = parse_command_line()

if values[1]==0:
    mac = get_current_address(values[0][0].interface)
    if mac is None:
        print("no MAC address to change for this interface")
    else:
        change_mac(values[0][0].interface, values[0][0].new_mac)
        mac_new = get_current_address(values[0][0].interface)
        print("MAC address changed from: " + mac + " to: " + mac_new)
    
else:
    print("errors: ", values[1])



