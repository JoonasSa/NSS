# Author: Joonas Sarapalo, 014585951

import socket

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