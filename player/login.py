# Author: Joonas Sarapalo, 014585951

import socket
import configparser
from client_functions import receive_tcp, send_tcp

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['LOGIN'])
host = 'localhost'

def login():
    print("Login to server")
    while True:
        username = input("username: ")
        password = input("password: ")
        if len(username) == 0 or len(password) == 0:
            print("Please enter both username and password")
        # a space is used to separate username and password
        elif " " in username or " " in password:
            print("Username and password can't contain spaces")
        # message length must fit into 3 characters, 998 = 999 - space character
        elif len(username) + len(password) > 998:
            print("Combined username and password length can't be over 998")
        else:
            session_token, error_msg = try_login(username, password)
            if error_msg == None:
                return session_token
            print(error_msg)
        print("Please try again\n")

def try_login(username, password):
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    credentials, msg_length = credentials_and_length(username, password)
    session_token, error_msg = send_and_receive(tcp_client, credentials, msg_length)
    tcp_client.close()
    return session_token, error_msg

def credentials_and_length(username, password):
    credentials = "log" + username + " " + password
    msg_length = str(len(credentials))
    while len(msg_length) < 3:
        msg_length = "0" + msg_length
    msg_length = "len" + msg_length
    return credentials, msg_length

def send_and_receive(tcp_client, credentials, msg_length):
    try:
        tcp_client.settimeout(2.0)
        tcp_client.connect((host, port))
    except:
        return "", "Connection refused"

    # TODO: tcp with triple redundancy is fucking retarded
    # try connecting for three times
    success = False
    for _ in range(3):
        if send_tcp(tcp_client, msg_length):
            if send_tcp(tcp_client, credentials):
                success = True
                break

    if success == False:
        return "", "Login attempt timed out"

    status, data = receive_tcp(tcp_client, token_length + 1) # success bit + session token
    if len(data) == 0:
        return "", "Login server timed out"
    if data[0] == "0":
        return "", data[2:data.find("'",2)] # extract error message, format is 0'errormessage'00...
    if status == False:
        return "", "Login server timed out"
    return data[1:], None # login successful