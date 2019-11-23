#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 18:44:25 2019

@author: Ahmed Khaled
"""

import subprocess
import optparse

# creating an instance from OptionParser
parser = optparse.OptionParser()
# adding arguments to the command-line arguments
parser.add_option("-i", "--interface", dest="interface", 
                  help="The Interface that you want to change its MAC address")
parser.add_option("-m", "--mac", dest="new_mac", help="The new MAC address of the interface chosen")
# parsing the arguments passed to add_option method above and 
# stored the return value (which is a tuple of the Values and list of the arguments)
values = parser.parse_args()

# use raw_input() instead of input() to run on python2.7
interface = values[0].interface
new_mac = values[0].new_mac

# this way of calling the call method is more secure so that a hacker can't hijack the system
# by using for example: ;ls; because python will treat this whole list as a single command and not
# as multiple commands
if interface is None and new_mac is None:
    print("no interface and mac address specified, exiting...")
elif interface is None:
    print("no interface specified, exiting...")
elif new_mac is None:
    print("no mac address specified, exiting...")
else:
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
