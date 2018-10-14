# Author: Joonas Sarapalo, 014585951

import socket
from login import login
from time import sleep
from update import update
from game import play

def main():
    # udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("                              ")
    print("******************************")
    print("* Welcome to FPS game client *")
    print("******************************")
    print("                              ")

    # TODO: use session token 
    session_token = login()
    print("session token:", session_token)

    update()
    print("client updated!")

    play()
    exit(0)

if __name__ == "__main__":
    main()