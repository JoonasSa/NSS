# Author: Joonas Sarapalo, 014585951

import socket
from sys import getsizeof
from functools import reduce
import string
import secrets

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

def generate_secret(n):
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(n)) 

def zero_padding(data, n, front=True):
    return (n - len(data)) * "0" + data if front else data + (n - len(data)) * "0"

def checksum(data):
    return sum(data, 0) % 255