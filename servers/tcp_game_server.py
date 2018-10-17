# Author: Joonas Sarapalo, 014585951

import socketserver
import configparser
from server_functions import generate_secret

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['GAME'])
host = 'localhost'

class TCPGameServer(socketserver.BaseRequestHandler):
	def handle(self):
		print("client connected...")
		raw = self.request.recv(token_length).decode('ascii')
		option, session_token = raw[0], raw[1:]
		print(option, session_token, option == '1', len(session_token))
        # join match
		if option == '1':
			if len(session_token) == 31:
				self.request.send(bytes('1' + generate_secret(token_length), 'ascii'))
			else:
				print('Bad session token')
				self.request.send(bytes('0' * 32, 'ascii'))
		# leave match
		elif option == '0':
			self.request.send(bytes('L' * 32))
		else:
			print('Bad request')
			self.request.send(bytes('0' * 32, 'ascii'))
		print('client disconnected...')
	
	# TODO: remove
	def handle_error(self, request, client_address):
		print('hurr?')
	
	# TODO: remove
	def handle_timeout(self):
		print('timeout')

if __name__ == "__main__":
	print("TCP Game server started...\n")
	server = socketserver.TCPServer((host, port), TCPGameServer)
	server.timeout = 1.0
	server.serve_forever()