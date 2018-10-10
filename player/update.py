# Author: Joonas Sarapalo, 014585951

import socket
import configparser
from client_functions import receive_tcp, send_tcp

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['UPDATE'])
host = socket.gethostname()

def check_for_updates():
    print("Checking for updates...")
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection = tcp_client.connect((port, host))
    # ask the server if there are any new updates
    updates, _ = send_tcp(connection, "0", 5.0)
    connection.close()
    return updates

def update():
    print("Downloading updates...")
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection = tcp_client.connect((port, host))
    # ask the server for new update size
    status, size = send_tcp(connection, "1", 5.0)
    if status == False:
        return False, "Couldn't reach the server"
    dl_sum = download_updates(connection, size)
    connection.close()
    return True, str(dl_sum) + " updates downloaded"

def download_updates(connection, size):
    bytes_downloaded = 0
    buffer = []
    while bytes_downloaded < size:
        status, data = receive_tcp(connection, 256, 30.0)
        if status == False:
            return False
    return True