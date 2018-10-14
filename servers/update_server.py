# Author: Joonas Sarapalo, 014585951

import socketserver
import configparser
from time import time, sleep
from server_functions import checksum, zero_padding
from sys import getsizeof

config = configparser.ConfigParser()
config.read('conf.ini')

token_length = int(config['DEFAULT']['TOKEN_LENGTH'])
port = int(config['PORTS']['UPDATE'])
host = 'localhost'

def message_to_1020_byte_chunks(data):
    magic = 952 # magic number to get 1015 bytes from string
    b_data = bytearray(data, 'ascii')
    chunks = []
    i = 0 
    while i < len(b_data):
        chunk = b_data[i : i + magic]
        if getsizeof(chunk) < 1020:
            padding = 1020 - getsizeof(chunk)
            chunk = chunk + bytes(padding * '0', 'ascii')
        chunks.append(chunk)
        i += magic
    return chunks

with open("update_data.txt") as text_file:
    update_data = text_file.read()
data_chunks = message_to_1020_byte_chunks(update_data)
update_size = "len" + zero_padding(str(len(data_chunks)), 5)

class UpdateServer(socketserver.BaseRequestHandler):
	def handle(self):
		print("client connected...")
		self.timer = time()
		while True:
			self.request.settimeout(2.0)
			try:
				self.request_type = self.request.recv(1).decode('ascii')
				self.handle_request()
			except:
				print('timeout...')
				self.request.close()				
				break
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

		else:
			print('Unknown request type')

	# TODO: add some beef here
	def updates_available(self):
		return True

	def send_updates(self):
		for i in range(len(data_chunks)):
			chunk = data_chunks[i] # data
			check = zero_padding(str(checksum(chunk)), 3) # checksum + padding
			chunk = chunk + bytes(check + '}', 'ascii') # '}' is end of chunk character 
			self.request.send(chunk)

		print('sent', len(data_chunks), 'chunks')

if __name__ == "__main__":
	print("Update server started...\n")
	server = socketserver.TCPServer((host, port), UpdateServer)
	server.serve_forever()