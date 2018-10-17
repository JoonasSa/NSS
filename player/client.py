# Author: Joonas Sarapalo, 014585951

from login import login
from update import update
from game import play

def main():

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

    #session_token = "9M47TN6YQJVZ4Y4IO2AJYSK93IWEEJ0Q"
    play(session_token)

    print("                                   ")
    print("***********************************")
    print("* Thank you for playing FPS game! *")
    print("***********************************")
    print("                                   ")

if __name__ == "__main__":
    main()