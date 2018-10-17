# Author: Joonas Sarapalo, 014585951

import socketserver
import configparser
from time import time, sleep

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['GAME'])
host = 'localhost'

# save players -> send state to all -> remove if inactive for 5 sec
active_players = set() # (time, token, socket, address)
game_state = {}

class UDPGameServer(socketserver.BaseRequestHandler):
	def handle(self):
		parts = self.request[0].decode('ascii').split(":")
		session_token, command = parts[0], parts[1]
		print(session_token, command)
		active_players.add((time(), session_token, self.request[1], self.client_address))

	def handle_command(self):
		return ''

	# send 
	def service_actions(self):
		print('service_actions')
		for player in active_players:
			print(player)
			time, _, socket, address = player
			if time() - time > 5.0:
				active_players.remove(player)
			else:
				socket.sendto(bytes('test', 'ascii'), address)

if __name__ == "__main__":
	print("UDP Game server started...\n")
	server = socketserver.UDPServer((host, port), UDPGameServer)
	server.serve_forever()