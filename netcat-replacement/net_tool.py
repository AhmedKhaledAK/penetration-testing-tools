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

def set_variables(options):

    global listen
    global shell_cmd
    global upload 
    global execute_cmd
    global target
    global upload_dest
    global port

    for opt, arg in options:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-l", "--listen"):
            listen = True
        elif opt in ("-e", "--execute"):
            execute_cmd = arg
        elif opt in ("-c", "--command"):
            shell_cmd = True
        elif opt in ("-u", "--upload"):
            upload_dest = arg
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        else:
            return False

    return True

def client():

    buffer = sys.stdin.read()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((target, port))

        if len(buffer) > 0:
            client_socket.send(buffer)

        while True:
            recv_len = 1
            response = ""
            while recv_len != 0:
                data = client_socket.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break
            
            print("response:")
            print(response)

            buffer = input()
            buffer += "\n"

            client_socket.send(buffer)

    except:
        print("EXCEPTION, closing connection")
        client_socket.close()


def server():
    global target

    if not len(target):
        target = "0.0.0.0"

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((target, port))
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()

        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def client_handler(client_socket):
    global upload
    global execute_cmd
    global shell_cmd

    if len(upload_dest):
        file_buffer = ""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data

        try:
            file_desc = open(upload_dest, "wb")
            file_desc.write(file_buffer)
            file_desc.close()

            client_socket.send("Saved file to:", upload_dest)
        except:
            client_socket.send("Failed to save file to:", upload_dest)


    if len(execute_cmd):
        op = run_command(execute_cmd)
        client_socket.send(op)

    if len(shell_cmd):
        while True:
            client_socket.send("SHELL<>: ")

            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            response = run_command(cmd_buffer)
            client_socket.send(response)


def run_command(cmd):
    #trimming the newline
    cmd = cmd.rstrip()

    try:
        op = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except:
        op = "Failed to execute command\r\n"

    return op

def main():
    global listen
    global shell_cmd
    global upload 
    global execute_cmd
    global target
    global upload_dest
    global port

    options = parse_args()

    if options == None:
        print("Undefined usage")
        sys.exit(0)

    boolean = set_variables(options)

    if boolean == False:
        print("Undefined usage")
        sys.exit(0)

    if not listen and len(target) != 0 and port > 0:
        client()

    if listen:
        server()

main()