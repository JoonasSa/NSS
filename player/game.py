# Author: Joonas Sarapalo, 014585951

import socket
import configparser
from client_functions import receive_tcp, send_tcp
from time import sleep, time
from game_loop import loop

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['GAME'])
host = 'localhost'

def play(session_token):
    print("Connecting to match...")

    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect((host, port))

    server_id = match_connect(tcp_client, session_token)
    if server_id == None:
        return

    tcp_client.close()

    loop(session_token, server_id)
    
    print('Disconnecting from match...')

def match_connect(connection, session_token):
    for _ in range(3):
        sent = send_tcp(connection, '1' + session_token)
        if sent == True:
            received, response = receive_tcp(connection, 32)
            if received == True:
                if handle_server_response(response):
                    return response
        sleep(2.0)

    print("Cannot connect to match server")
    return None

def handle_server_response(response):
    if len(response) != 32:
        return False
    else:
        return True if response[0] == '1' else False
