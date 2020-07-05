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
cnt = 0
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
        print("here1")
        req = crawler.Request(url)
        print("req:", req.get_full_url())
        try:
            print("here")
            response = crawler.urlopen(req)
            print("here2")
            content = response.read()
            
            print("response content:")
            print(content)
            print("response code:", response.code)
            print("response path:", path)
            response.close()
        except cerr.HTTPError as err:
            cnt += 1
            print("failed crawling; error code:")
            pass

def main():
    target = "https://www.example.com" # your target website here
    directory = "/home/ahmedkhaled/Downloads/Wordpress/latest/wordpress"
    
    os.chdir(directory)
    
    paths = get_paths()
    
    for i in range(threads):
        print("thread #:", i)
        t = threading.Thread(target=test_path, args=(paths, target))
        t.start()     
    
    print(cnt)
main()