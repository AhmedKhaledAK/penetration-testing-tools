#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import urllib.request as crawler
import urllib.error as cerr
import queue
import threading
import os

threads = 10

def get_paths():
    paths = queue.Queue()
    for root, dirs, files in os.walk("."):
        for file in files:
            path = "%s/%s" % (root, file)
            if path.startswith("."):
                path = path[1:]
            paths.put(path)    
    return paths


def test_path(paths, target):
    global cnt
    while not paths.empty():
        path = paths.get()
        url = "%s%s" % (target, path)
        req = crawler.Request(url)
        try:
            response = crawler.urlopen(req)
            content = response.read()
            
            print("response content:")
            print(content)
            print("response code:", response.code)
            print("response path:", path)
            response.close()
        except cerr.HTTPError as err:
            print("failed crawling; error code:", err)
            pass

def main():
    target = "https://www.example.com" # your target website here
    directory = "/home/ahmedkhaled/Downloads/Wordpress/latest/wordpress"
    
    os.chdir(directory)
    
    paths = get_paths()
    
    for i in range(threads):
        print("thread #:", i)
        thread = threading.Thread(target=test_path, args=(paths, target))
        thread.start()     
    
main()