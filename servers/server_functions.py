# Author: Joonas Sarapalo, 014585951

import socket
from sys import getsizeof
from functools import reduce

def receive_tcp(connection, size, timeout=2.0, encoding='ascii'):
    try:
        connection.settimeout(timeout)
        encoded_msg = connection.recv(size)
        decoded_msg = encoded_msg.decode(encoding)
        return True, decoded_msg
    except:
        return False, ""

def send_tcp(connection, msg, timeout=2.0, encoding='ascii'):
    try:
        connection.settimeout(timeout)
        encoded_msg = msg.encode('ascii')
        connection.sendall(encoded_msg)
        return True
    except:
        return False

# TODO: works?
def message_to_chunks(data, n):
    b_data = bytearray(data, 'ascii')
    chunks = []
    i = 0 
    while i < len(b_data):
        chunk = b_data[i : i + n].decode('ascii')
        print("shiit", getsizeof(chunk))
        if getsizeof(chunk) < n:
            padding = n - getsizeof(chunk)
            chunk = chunk + padding * '0'
        chunks.append(chunk)
        i += n
    return chunks

def zero_padding(data, n, front=True):
    return (n - len(data)) * "0" + data if front else data + (n - len(data)) * "0"

def checksum(data):
    return sum(bytearray(data, 'ascii'), 0) % 255