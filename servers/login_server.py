# Author: Joonas Sarapalo, 014585951

import socket
import secrets
import string
# from time import time
import configparser
from server_functions import receive_tcp, send_tcp, generate_secret

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['LOGIN'])
host = 'localhost'

mocks = [
    {'username': 'username', 'password': 'password'},
    {'username': 'joonas', 'password': 'sarapalo'},
    {'username': 'a', 'password': 'a'}
]

# TODO: make this do something
# active_tokens = set()

def main():
    print('Login server started...')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    while True:
        connection, _ = server.accept()

        print("client connected...")
        status = False
        for _ in range(3):
            status, credentials = receive_msg(connection)
            if status == True:
                print("login:", credentials)
                session_token = handle_msg(credentials)
                print('session_token', session_token)
                send_tcp(connection, session_token)
                break
        if status == False:
            send_tcp(connection, "0'No credentials received'0000000")
        print("connection closed...\n")
        connection.close()

def receive_msg(connection):
    length = 0
    status, decoded_length = receive_tcp(connection, 6)
    if status and decoded_length[:3] == "len":
        length = int(decoded_length[3:])
    else:
        return False, ""

    status, credentials = receive_tcp(connection, length)
    if status and credentials[:3] == "log":
        return True, credentials[3:].split(" ")
    return False, ""

def handle_msg(decoded_msg):
    if validate_username_password(decoded_msg):
        session_token = generate_secret(token_length)
        # TODO: make this do something
        # active_tokens.add({session_token, time()}) # token and current time
        return "1" + session_token # correct username & password
    else:
        return "0'Incorrect username & password'0"

def validate_username_password(decoded_msg):
    if not (len(decoded_msg)) == 2:
        return False

    username, password = decoded_msg[0], decoded_msg[1]
    # mock validation of the username and password
    if not {'username': username, 'password': password} in mocks:
        print("username", username, "password", password, "not in mocks")
        return False
    return True

if __name__ == "__main__":
    main()