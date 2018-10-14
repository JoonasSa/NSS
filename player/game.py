# Author: Joonas Sarapalo, 014585951

import socket
import configparser
from client_functions import receive_tcp, send_tcp

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['GAME'])
host = 'localhost'

def play():
    print("Connection game server...")
    
