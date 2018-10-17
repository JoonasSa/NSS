# Author: Joonas Sarapalo, 014585951

import socketserver
import configparser
from time import time, sleep

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['GAME'])
host = 'localhost'

class UDPGameServer(socketserver.BaseRequestHandler):
	def handle(self):
		print("client connected...")
		self.timer = time()

		print("connection closed...")

if __name__ == "__main__":
	print("UDP Game server started...\n")
	server = socketserver.UDPServer((host, port), UDPGameServer)
	server.serve_forever()