# Author: Joonas Sarapalo, 014585951

import socket
import configparser
from client_functions import receive_udp, send_udp
import sys
import select
import tty
import termios
from time import time, sleep

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['GAME'])
host = 'localhost'

def loop(session_token, server_id):
    print("Entering match...")
    game_state = init_game_state()
    address = (host, port)
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    last_response = time()

    # https://stackoverflow.com/questions/2408560/python-nonblocking-console-input

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        while True:
            if is_data():
                c = sys.stdin.read(1)
                parsed = handle_input(c)
                if parsed == "end":
                    break
                elif parsed == "":
                    continue
                else:
                    send_udp(udp_client, address, session_token + ":" + parsed)
            status, state = receive_udp(udp_client, 2, 0.2)
            if status == True:
                last_response = time()
                game_state = state
                print(state)
            elif time() - last_response > 5.0:
                print('Disconnected from server')
                break

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    print('Leaving match...')

def is_data():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def handle_input(c):
    if c == '\x1b': # x1b is ESC
        return "end"
    elif c == "w":
        return "UP"
    elif c == "s":
        return "DN"
    elif c == "a":
        return "LT"
    elif c == "d":
        return "RT"
    else:
        return ""

def init_game_state():
    game_state = {
        'score': 0,
        'alive': True
    }
    return game_state