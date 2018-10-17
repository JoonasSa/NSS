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

    end_result = play(session_token)
    print(end_result)

if __name__ == "__main__":
    main()