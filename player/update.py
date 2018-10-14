# Author: Joonas Sarapalo, 014585951

import socket
import configparser
from client_functions import receive_tcp, send_tcp, checksum
from time import sleep
from sys import getsizeof 

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['UPDATE'])
host = 'localhost'

def update():
    print("Checking for updates...")
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect((host, port))

    # ask the server if there are any new updates
    updates = send_tcp(tcp_client, "0", 5.0)
    up_to_date = not updates
    if updates:
        up_to_date = download_update(tcp_client)

    print("close...")
    tcp_client.close()
    return up_to_date

def download_update(connection):
    print("Downloading updates...")

    # request update size
    status = send_tcp(connection, "1", 5.0)
    if status == False:
        print("Couldn't reach the server")
        return False

    # receive update size
    sleep(0.5)
    status, size = receive_tcp(connection, 9, 5.0)
    if status == False or size[:3] != "len":
        print("Didn't receive update size")
        return False
    size = int(size[3:])

    # request updates
    status = send_tcp(connection, "2", 10.0)
    if status == False:
        print("Couldn't reach the server")
        return False
    
    dl_sum = handle_downloading(connection, size)

    print(dl_sum, "chunks received")
    return True

def handle_downloading(connection, size):
    print("handle_downloading")
    downloaded_chunks, missed_seqs = [], []
    received = download_chunks(connection, size)
    chunks = split_chunks(received)
    for seq in range(len(chunks)):
        msg, check = parse_chunk(chunks[seq])
        if checksum(msg) != check:
            missed_seqs.append(seq)
        else:
            downloaded_chunks.append((seq, msg.replace('0','')))
    return len(downloaded_chunks)

def download_chunks(connection, size):
    print('download_chunks')
    received, seq = [], 0
    while seq < size:
        status, chunk = receive_tcp(connection, 1024)
        if status == True:
            received.append(chunk)
        else:
            print('connection problems...')
        seq += 1
    return received

def split_chunks(received):
    buffer = ""
    chunks = []
    for r in received:
        buffer += r
        if '}' in buffer:
            eoc = buffer.index('}') # end of chunk
            chunk, buffer = buffer[:eoc], buffer[eoc + 1:]
            chunks.append(chunk)
    return chunks

def parse_chunk(chunk):
    msg = chunk[:-3] # actual data
    check = chunk[-4:] # checksum
    return msg, int(check)