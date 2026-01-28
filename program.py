__author__ = "yoav"

import socket, sys, traceback, threading
from hashlib import sha256
from vigenere import encode, decode, find_stdispNmod
from datetime import datetime, timezone


stopcond = False
prev_key = ''
current_key = ''

def create_code():
    global current_key
    time = datetime.now(timezone.utc).isoformat()
    time = time[:-19]
    hourly_code = sha256(time.encode('utf-8')).hexdigest()
    time = encode(time, hourly_code)
    hourly_code = sha256(time.encode('utf-8')).hexdigest()
    hourly_code = encode(hourly_code,hourly_code[:4])
    return hourly_code

def craft_msg():
    pass

def parse_resp():
    pass


def handle_conn(sock):
    sock = sock[0]
    sock.send()


def main(type, ip, port):
    you = socket.socket()
    if (type):
        you.bind((ip, port))
        you.listen(1)
        client = you.accept()
        handle_conn(client)
    else:
        you.connect((ip, port))









if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("insufficient arguments, please enter desired arguments:")
        type = int(input('\nArgument 1: Socket type - 1 for server, 0 for client'))
        ipad = input('\nArgument 2: IP address: ')
        port = int(input('\nArgument 3: Port: '))
        main(type,ipad,port)
    else:
        if (sys.argv[1] != "1" or sys.argv[1] != '0'):
            print("Error: Socket type must be either 1 (Server) or 0 (Client)")
        else:
            main(sys.argv[1],sys.argv[2],sys.argv[3])