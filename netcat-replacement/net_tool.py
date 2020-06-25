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

def parse_args():
    if len(sys.argv[1:]) == 0:
        return None

    opts_args = None
    
    try:
        opts_args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print(str(err))
        opts_args = None
    
    #print("opts:",opts_args[0])
    #print("args:",opts_args[1])

    if opts_args == None:
        return None
    return opts_args[0]


def main():
    global listen
    global shell_cmd
    global upload 
    global execute_cmd
    global target
    global upload_dest
    global port

    parsed_line = parse_args()
    #set_variables()
    print(parsed_line)

main()