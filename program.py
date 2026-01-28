__author__ = "f-162a7v"

import socket, sys, traceback, threading
from hashlib import sha256
from vigenere import encode, decode, find_stdispNmod
from datetime import datetime, timezone

stopcond = False
prev_key = ''
current_key = ''
hosting = False


def create_first_key():
    global current_key
    time = datetime.now(timezone.utc).isoformat()
    time = time[:-19]
    hourly_code = sha256(time.encode('utf-8')).hexdigest()
    time = encode(time, hourly_code)
    hourly_code = sha256(time.encode('utf-8')).hexdigest()
    hourly_code = encode(hourly_code,hourly_code[:4])
    return hourly_code


def send_function(sock,firstkey):
    global hosting
    key = firstkey

def recv_function(sock,firstkey):
    global hosting
    key = firstkey


def handle_conn(sock):
    threads = []
    initial_key = create_first_key()
    t1 = threading.Thread(target=send_function,args=(sock,initial_key))
    t2 = threading.Thread(target=recv_function,args=(sock,initial_key))
    threads.append(t1)
    threads.append(t2)
    t1.start()
    t2.start()

    for t in threads:
        t.join()


def main(ip, port):
    you = socket.socket()
    global hosting
    try:
        print(f"Attempting to connect to {ip} on port {port}....")
        you.settimeout(1)
        you.connect((ip, port))
        print(f"Connection established with {ip}")
        handle_conn(you)
    except socket.timeout:
        myname = socket.gethostname()
        myip = socket.gethostbyname(myname)
        print(f"Connection attempt failed, hosting and listening on {myip}, {port}....")
        you = socket.socket()
        you.bind((myip,port))
        you.listen(1)
        cli = you.accept()
        print(f"Connection established with {ip}")
        hosting = True
        handle_conn(cli)




if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("insufficient arguments, please enter desired arguments:")
        ipad = input('\nArgument 1: IP address: ')
        port = int(input('\nArgument 2: Port: '))
        main(ipad,port)
    else:
        main(sys.argv[1],sys.argv[2])