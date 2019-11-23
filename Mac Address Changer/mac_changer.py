#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 18:44:25 2019

@author: Ahmed Khaled
"""

import subprocess

# use raw_input() instead of input() to run on python2.7
interface = input("interface > ")
new_mac = input("mac > ")

# this way of calling the call method is more secure so that a hacker can't hijack the system
# by using for example: ;ls; because python will treat this whole list as a single command and not
# as multiple commands
subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
subprocess.call(["ifconfig", interface, "up"])
