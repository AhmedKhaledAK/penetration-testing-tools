#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import urllib as crawler
import queue
import _thread
import os

threads = 10

target = "https:/www.example.com" # your target website here
directory = "/home/ahmedkhaled/Downloads/Wordpress/latest/wordpress"

os.chdir(directory)

paths = queue.Queue()

for root, dirs, files in os.walk("."):
    for file in files:
        path = "%s/%s" % (root, file)
        if path.startswith("."):
            path = path[1:]
        paths.put(path)