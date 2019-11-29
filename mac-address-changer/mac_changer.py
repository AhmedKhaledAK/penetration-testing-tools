#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 18:44:25 2019

@author: Ahmed Khaled
"""

import subprocess
import optparse
import re


def change_mac(interface, new_mac):
    # this way of calling the call method is more secure so that a hacker can't hijack the system
    # by using for example: ;ls; because python will treat this whole list as a single command and not
    # as multiple commands
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    
    print_current_address(interface)

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
        print("no interface and mac address specified, exiting...")
        err=2
    elif values[0].interface is None:
        print("no interface specified, exiting...")
        err=1
    elif values[0].new_mac is None:
        print("no mac address specified, exiting...")
        err=1
    return (parser.parse_args(),err)

values = parse_command_line()
if values[1]==0:
    change_mac(values[0][0].interface, values[0][0].new_mac)
else:
    print("errors: ", values[1])



