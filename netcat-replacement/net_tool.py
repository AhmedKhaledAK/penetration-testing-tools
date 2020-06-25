import sys
import socket
import getopt
import threading
import subprocess

# global variables
listen = False
shell_cmd = False
upload = False
execute_cmd = ""
target = ""
upload_dest = ""
port = 0

def usage():
    print("NET TOOL")
    print("Usage: net_tool.py -t target -p port")
    print("-l --listen              - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run - execute the given file upon receiving a connection")
    print("-c --command             - initialize a command shell")
    print("-u --upload=destination  - upon receiving connection upload a file and write to [destination]")
    print("Examples: ")
    print("net_tool.py -t 192.168.0.1 -p 5555 -l -c")
    print("net_tool.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("net_tool.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./net_tool.py -t 192.168.11.12 -p 135")
    sys.exit(0)