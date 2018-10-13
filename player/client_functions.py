# Author: Joonas Sarapalo, 014585951

import socket
from random import random
from string import printable

def receive_tcp(connection, size, timeout=2.0, encoding='ascii'):
    try:
        connection.settimeout(timeout)
        encoded_msg = connection.recv(size)
        decoded_msg = encoded_msg.decode(encoding)
        decoded_msg = filter(lambda x: x in printable, decoded_msg) # remove control characters
        return True, "".join(list(decoded_msg))
    except:
        return False, ""

def send_tcp(connection, msg, timeout=2.0, encoding='ascii'):
    # if random() < 0.25:
    #    return False, ""
    try:
        connection.settimeout(timeout)
        encoded_msg = msg.encode(encoding)
        connection.sendall(encoded_msg)
        return True
    except:
        return False

def checksum(data):
    return sum(bytearray(data, 'ascii'), 0) % 255