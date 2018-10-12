# Author: Joonas Sarapalo, 014585951

import socket
import configparser

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['HUB'])
host = 'localhost'

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    while True:
        connection, _ = server.accept()

        print("client connected...")
        session_token = receive_session_token(connection)
        if is_valid_session_token(session_token):
            while True:
                # handle different requests
                break
        else:
            # fuck u
            return

        print("connection closed...")
        connection.close()

def receive_session_token(connection):
    connection.settimeout(2.0)
    encoded_token = connection.recv(token_length)
    decoded_token = encoded_token.decode('ascii')
    return decoded_token

def is_valid_session_token(session_token):
    # secret formula
    return True

if __name__ == "__main__":
    main()