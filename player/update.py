# Author: Joonas Sarapalo, 014585951

import socket
import configparser
from client_functions import receive_tcp, send_tcp, checksum
from time import sleep

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
    print(repr(size))
    if status == False or size[:3] != "len":
        print("Didn't receive update size")
        return False

    size = int(size[3:])
    print(size)

    # request updates
    status = send_tcp(connection, "2", 10.0)
    if status == False:
        print("Couldn't reach the server")
        return False
    dl_sum = handle_downloading(connection, size)

    print(dl_sum, " updates downloaded")
    return True

# TODO: fix receiving multiple packets & implement requesting for specific chunks
def handle_downloading(connection, size):
    print("handle_downloading")
    buffer, missed = [], []
    while True:
        buffer, missed = download_chunks(connection, size, buffer)
        if len(missed) == 0:
            break
    # sort buffer...
    return len(buffer)

def download_chunks(connection, size, buffer):
    print('download_chunks')
    bytes_downloaded, seq, missed_seqs = 0, 0, []
    while bytes_downloaded < size:
        chunk_seq, msg, check = receive_and_parse_chunks(connection)
        print(chunk_seq, check)
        if chunk_seq == -1 or chunk_seq != seq or checksum(msg) != check:
            print('missed')
            missed_seqs.append(seq)
        else:
            buffer.append(msg.replace('0',''))
        bytes_downloaded += 1024
        seq += 1

    return buffer, missed_seqs

def receive_and_parse_chunks(connection):
    try:
        connection.settimeout(5.0)
        chunk = connection.recv(1024)
        seq = int(chunk[:6].decode('ascii'))
        msg = chunk[6:1021].decode('ascii')
        check = int(chunk[1021:].decode('ascii'))
        return seq, msg, check
    except:
        return -1, "", 0 # seq = -1 -> fail