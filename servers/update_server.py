# Author: Joonas Sarapalo, 014585951

import socketserver
import configparser

class UpdateServer(socketserver.BaseRequestHandler):
	def handle(self):
		print("client connected...")
		# self.request is the TCP socket connected to the client
		self.data = self.request.recv(1024).strip()
		print("{} wrote:".format(self.client_address[0]))
		print(self.data)
		# just send back the same data, but upper-cased
		print("connection closed...")
		self.request.sendall(self.data.upper())

if __name__ == "__main__":
	config = configparser.ConfigParser()
	config.read('conf.ini')

	token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
	port = int(config['PORTS']['UPDATE'])
	host = "localhost"

	server = socketserver.TCPServer((host, port), UpdateServer)
	server.serve_forever()