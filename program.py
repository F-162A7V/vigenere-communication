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

def craft_resp():
    pass

def parse_resp():
    pass


def handle_conn(sock):
    sock = sock[0]
    sock.send()


def main(serip,serport):
    serversock = socket.socket()
    serversock.bind((serip,serport))
    serversock.listen(1000000000)
    threads = []
    while not stopcond:
        connection, address = serversock.accept()
        t1 = threading.Thread(target=handle_conn, args=(connection,))
        threads.append(t1)
        t1.start()
    for t in threads:
        t.join()









if __name__ == '__main__':
    if len(sys.argv) < 3:
        main("127.0.0.1",16000)
    else:
        main(sys.argv[1],sys.argv[2])