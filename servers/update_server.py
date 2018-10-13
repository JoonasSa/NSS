# Author: Joonas Sarapalo, 014585951

import socketserver
import configparser
from time import time, sleep
from server_functions import message_to_chunks, checksum, zero_padding

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['UPDATE'])
host = 'localhost'

with open("mini_update_data.txt") as text_file:
    update_data = text_file.read()
data_chunks = message_to_chunks(update_data, 1015) # 1024 - 6 (seq) - 3 (checksum)
update_size = "len" + zero_padding(str(len(data_chunks)), 5)
print(repr(update_size), len(update_size))

class UpdateServer(socketserver.BaseRequestHandler):
	def handle(self):
		print("client connected...")
		self.timer = time()
		while True:
			self.request.settimeout(2.0)
			self.request_type = self.request.recv(1).decode('ascii')

			# reset timeout timer if something was received
			if (len(self.request_type) > 0):
				self.timer = time()

			# check timeout timer if nothing was received
			else:
				if time() - self.timer > 5.0:
					print('timeout...')
					break
				sleep(0.5)

			self.handle_request()
		print("connection closed...")

	def handle_request(self):
		# is there available update
		if (self.request_type == '0'):
			self.request.settimeout(2.0)
			self.request.send(bytes(self.updates_available()))

		# size of the update in chunks
		elif (self.request_type == '1'):
			print('update_size: ', repr(update_size), len(update_size))
			self.request.settimeout(2.0)
			self.request.send(bytes(update_size, 'ascii'))

		# the update
		elif (self.request_type == '2'):
			self.send_updates()

		# specific chunk of the update
		elif (self.request_type == '3'):
			# needs to receive the chunk number
			print('Client is requesting a specific part of the update')

		else:
			print('Unknown request type')

	# TODO: add some beef here
	def updates_available(self):
		return True

	def send_updates(self):
		for i in range(len(data_chunks)):
			chunk = data_chunks[i] # data
			check = zero_padding(str(checksum(chunk)), 3) # checksum
			seq = zero_padding(str(i), 6) # seq
			chunk = seq + chunk + check
			print(chunk)
			self.request.sendall(bytes(chunk, 'ascii'))

if __name__ == "__main__":
	print("Update server started...\n")
	server = socketserver.TCPServer((host, port), UpdateServer)
	server.serve_forever()