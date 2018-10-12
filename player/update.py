# Author: Joonas Sarapalo, 014585951

import socket
import configparser
from client_functions import receive_tcp, send_tcp

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
    print("Downloading updates...", connection)

    # request update size
    status = send_tcp(connection, "1", 5.0)
    if status == False:
        print("Couldn't reach the server")
        return False

    # receive update size
    status, size = receive_tcp(connection, 9, 5.0)
    if status == False or size[:3] != "len":
        print("Didn't receive update size", size)
        return False
    size = int(size[3:])

    # request updates
    status = send_tcp(connection, "2", 10.0)
    if status == False:
        print("Couldn't reach the server")
        return False
    dl_sum = handle_downloading(connection, size)

    print(dl_sum, " updates downloaded")
    return True

def handle_downloading(connection, size):
    buffer = []
    missed = []
    while True:
        buffer, missed = download_chunks(connection, size, buffer)
        #if len(missed) == 0:
        #    break
    # sort buffer...
    return len(buffer)

def download_chunks(connection, size, buffer):
    bytes_downloaded = 0
    missed = []
    seq = 0
    while bytes_downloaded < size:
        status, data = receive_tcp(connection, 1024, 30.0)
        if status == False:
            missed.append(seq)
        else:
            buffer.append(data)
        seq += 1
    return buffer, missed