#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import urllib as crawler
import queue
import thread
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
    while not paths.empty():
        path = paths.get()
        url = "%s%s" % (target, path)
        req = crawler.request.Request(url)
        try:
            response = crawler.request.urlopen(req)
            content = response.read()
            
            print("response content:")
            print(content)
            print("response code:", response.code)
            print("response path:", path)
            response.close()
        except crawler.request.HTTPError as err:
            print("failed crawling; error code:", err.code)
            pass

def main():
    target = "https:/www.example.com" # your target website here
    directory = "/home/ahmedkhaled/Downloads/Wordpress/latest/wordpress"
    
    os.chdir(directory)
    
    paths = get_paths()
    
    for i in range(threads):
        print("thread #:", i)
        thread.start_new_thread(test_path, (paths, target))     
    
main()