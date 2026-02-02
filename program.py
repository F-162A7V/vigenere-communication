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
    hourly_code = sha256(time.encode()).hexdigest()
    time = vigencrypt(time, hourly_code)
    hourly_code = sha256(time.encode()).hexdigest()
    hourly_code = vigencrypt(hourly_code,hourly_code[:4])
    return hourly_code

def craft_msg(inpt):
    glock.acquire()
    global prev_key
    global current_key
    if not prev_key:
        prev_key = sha256(inpt.encode()).hexdigest()
    key = sha256(inpt.encode()).hexdigest()
    key = key[:10]
    prev_key = current_key
    current_key = key
    length = len(inpt) + len(key) + 2
    length = struct.pack('i',length)
    glock.release()
    return length + f"|{vigencrypt(inpt,prev_key)}|{vigencrypt(key,prev_key)}".encode()


def send_function(sock,notuple):
    global stopcond
    while not stopcond:
        try:
            typeInpt = inputimeout.inputimeout("Press '1' to enter a message.. -->   ",1)
            if typeInpt == "1":
                glock.acquire()
                content = input("Enter message contents... -->   ")
                tosend = craft_msg(content)
                sock.send(tosend)
                glock.release()
        except inputimeout.TimeoutOccurred:
                glock.acquire()
                sys.stdout.write('\x1b[1A')
                print("\r                                                                         ")
                glock.release()

def recv_function(sock,notuple):
    sock = sock[0]
    global current_key
    global stopcond
    while not stopcond:
        sock.settimeout(None)
        data = sock.recv(4)
        glock.acquire()
        if data == b'':
            stopcond = True
            print("Other side has disconnected.")
            break
        len = struct.unpack("i",data)[0]
        data = ""
        if len > 8192:
            while len > 0:
                data += sock.recv(8192)
                len -= 8192
        else:
            data += sock.recv(len)

        glock.release()




def handle_conn(sock,mytype):
    global current_key
    threads = []
    initial_key = create_first_key()
    current_key = initial_key
    t1 = threading.Thread(target=send_function,args=(sock,"aa"))
    t2 = threading.Thread(target=recv_function,args=(sock,"aa"))
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
        #ipad = input('\nArgument 1: IP address: ')
        #port = int(input('\nArgument 2: Port: '))
        ipad = socket.gethostbyname(socket.gethostname())
        port = 11111
        main(ipad,int(port))
    else:
        main(sys.argv[1],int(sys.argv[2]))