__author__ = "f-162a7v"

import socket, sys, traceback, threading, inputimeout, struct
from hashlib import sha256
from vigenere import vigencrypt, vigdecrypt
from datetime import datetime, timezone

stopcond = False
prev_key = ''
current_key = ''
glock = threading.Lock()

def create_first_key():
    global current_key
    time = datetime.now(timezone.utc).isoformat()
    time = time[:-19]
    hourly_code = sha256(time.encode('utf-8')).hexdigest()
    time = vigencrypt(time, hourly_code)
    hourly_code = sha256(time.vigencrypt('utf-8')).hexdigest()
    hourly_code = vigencrypt(hourly_code,hourly_code[:4])
    return hourly_code

def craft_msg(inpt,prevkey):
    if not prevkey:
        prevkey = sha256((inpt.encode)).hexdigest()
    key = sha256(inpt.encode()).hexdigest()
    key = key[:10]
    length = len(inpt) + len(key) + 2
    length = struct.pack('i',length)
    return length + f"|{vigencrypt(inpt,prevkey)}|{vigencrypt(key,prevkey)}".encode()


def send_function(sock,firstkey):
    global hosting
    while not stopcond:
        try:
            glock.acquire()
            typee = inputimeout.inputimeout("Press '1' to enter a message.. --> 2",)
            if typee == "1":
                content = input("Enter message contents...")


        except inputimeout.TimeoutOccurred:
            pass

def recv_function(sock,firstkey):
    key = firstkey

def handle_conn(sock,mytype):
    global current_key
    threads = []
    initial_key = create_first_key()
    current_key = initial_key
    t1 = threading.Thread(target=send_function,args=(sock,initial_key))
    t2 = threading.Thread(target=recv_function,args=(sock,initial_key))
    threads.append(t1)
    threads.append(t2)
    t1.start()
    t2.start()
    while not stopcond:
        pass
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
        handle_conn(you,0)
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
        handle_conn(cli,1)




if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("insufficient arguments, please enter desired arguments:")
        ipad = input('\nArgument 1: IP address: ')
        port = int(input('\nArgument 2: Port: '))
        main(ipad,port)
    else:
        main(sys.argv[1],sys.argv[2])