# Author: Joonas Sarapalo, 014585951

import socket
import configparser
from random import random

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['GAME'])
host = 'localhost'

def main():
    print('UDP game server started...')
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.settimeout(0.3)
    server.bind((host, port))

    active_players = set() # (time, token, address)
    game_state = { 'score': 0, 'hp': 100 }

    # TODO: fix, needed to shutdown the server
    from time import time
    timer = time()

    while True:
        try:
            if (time() - timer) > 20.0:
                break
            raw, address = server.recvfrom(35)
            timer = time()
            parts = raw.decode('ascii').split(':')
            session_token, command = parts[0], parts[1]
            print('Received command:', command, "from:", session_token)
            active_players.add((time(), session_token, address))
        except:
            new_set = set()
            for player in active_players:
                last, _, address = player
                if time() - last < 5.0:
                    new_set.add(player)
                    game_state = mutated_game_state(game_state)
                    server.sendto(bytes(game_state_string(game_state), 'ascii'), address)
            active_players = new_set

def mutated_game_state(game_state):
    score_now = int(game_state.get('score'))
    hp_now = int(game_state.get('hp'))

    new_hp = hp_now + int(random() * 5) if random() > 0.55 else hp_now - int(random() * 5)
    new_score = '0' * (6 - len(str(score_now))) + str(score_now + int(random() * 5))

    new_game_state = { 'score': new_score, 'hp': new_hp }
    return new_game_state

def game_state_string(game_state):
    return str(game_state.get('score')) + ":" + str(game_state.get('hp'))

if __name__ == "__main__":
    main()