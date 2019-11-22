#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 18:44:25 2019

@author: Ahmed Khaled
"""

import subprocess

interface = input("interface > ")
new_mac = input("mac > ")

subprocess.call("ifconfig " + interface + " down", shell=True)
subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
subprocess.call("ifconfig " + interface + " up ", shell=True)


