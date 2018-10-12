# Author: Joonas Sarapalo, 014585951

import socketserver
import configparser
from time import time
from server_functions import message_to_chunks, checksum

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['UPDATE'])
host = 'localhost'

with open("update_data.txt") as text_file:
    update_data = text_file.read()
data_chunks = message_to_chunks(update_data, 1024)
update_size = str(len(data_chunks))
while len(update_size) < 6:
	update_size = "0" + update_size
update_size = "len" + update_size

class UpdateServer(socketserver.BaseRequestHandler):
	def handle(self):
		print("client connected...")
		while True:
			self.request.settimeout(2.0)
			self.request_type = self.request.recv(1).decode('ascii')
			print(self.request_type)
			# is there available update
			if (self.request_type == '0'):
				self.request.settimeout(2.0)
				self.request.send(bytes(self.updates_available()))
			# size of the update in chunks
			elif (self.request_type == '1'):
				print('update_size: ', update_size)
				self.request.send(update_size.encode('ascii'))
			# the update
			elif (self.request_type == '2'):
				self.send_updates()
			# specific chunk of the update
			elif (self.request_type == '3'):
				# needs to receive the chunk number
				print('Client is requesting a specific part of the update')
			else:
				print('Unknown request type')
				break
		print("connection closed...")

	# TODO: add some beef here
	def updates_available(self):
		return True

	def send_updates(self):
		for chunk in data_chunks:
			#asd = checksum(chunk)
			#print(asd)
			# sequencing and checksum to chunk
			self.request.sendall(chunk)

if __name__ == "__main__":
	print("Update server started...\n")
	server = socketserver.TCPServer((host, port), UpdateServer)
	server.serve_forever()