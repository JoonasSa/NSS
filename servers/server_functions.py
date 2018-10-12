# Author: Joonas Sarapalo, 014585951

import socket
import sys

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

def message_to_chunks(msg, n):
    magic = n // 2 # magic number to get exactly 100 bytes
    chunks = []
    for i in range(0, len(msg), magic):
        chunk = msg[i : i + magic]
        if sys.getsizeof(chunk) < n:
            padding = n - sys.getsizeof(chunk)
            chunk = chunk + padding * '0'
        chunks.append(chunk)
    return chunks

def checksum(data):
    i=0
    checksum = 0
    while i < len(data):
        checksum = checksum ^ ord(data[i])
        i+=1
    return hex(checksum)