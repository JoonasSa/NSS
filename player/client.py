# Author: Joonas Sarapalo, 014585951

import socket
from login import login
from time import sleep
from update import check_for_updates, update

def main():
    # udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("                            ")
    print("****************************")
    print("*Welcome to FPS game client*")
    print("****************************")
    print("                            ")

    # TODO: use session token 
    session_token = login()
    print("session token:", session_token)
    exit(0)
    if check_for_updates():
        print("Client needs to be updated")
        while True:
            status, msg = update()
            print(msg)
            if status == True:
                break
            # we need to try again until updating succeeds
            sleep(3)
    else:
        print("Client up to date")

    exit(0)

if __name__ == "__main__":
    main()