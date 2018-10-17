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
    server_id = match_connect(tcp_client, session_token, '1')
    if server_id == None:
        return
    #tcp_client.close()
    #tcp_end = time()

    loop(session_token, server_id)

    # there needs to be atleast 3 seconds between the tcp requests
    #while True:
    #    if time() - tcp_end > 3:
    #        break

    #tcp_client.connect((host, port))
    response = match_connect(tcp_client, session_token, '0')
    tcp_client.close()
    if response == None:
        return
    
    print('Disconnecting from match...')

def match_connect(connection, session_token, option):
    for _ in range(3):
        print(option + session_token)
        sent = send_tcp(connection, option + session_token)
        print('sent', sent)
        if sent == True:
            received, response = receive_tcp(connection, 32)
            print('received', received)
            if received == True:
                if handle_server_response(response, option):
                    return response
        sleep(2.0)

    print("Cannot connect to match server")
    return None

def handle_server_response(response, option):
    print('handle_server_response', response, option)
    if len(response) != 32:
        return False
    if option == '1':
        return True if response[0] == '1' else False
    else:
        print('hello there')
        return True if response[0] == 'L' else False
