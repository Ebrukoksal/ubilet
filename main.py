from modules.auth import login, signup
from modules.admin import admin
from modules.user import user_loggedin


def user_login():
    choice = input("Press 1 to sign up / Press 2 to admin login / Press 3 to user login / Press 4 to exit \n")

    if choice == "1":
        signup()
    elif choice =="2":
        user = login("admin")
        if not user:
            print("Credentials are wrong for admin login.")
        else:
            logout = False
            while not logout:
                admin(user["username"])
                wanna_logout = input("Do you want to logout? If so press x \n")
                if wanna_logout.lower() == "x":
                    logout = True
    elif choice == "3":
        user = login("user")
        if not user:
            print("Credentials are wrong for user login.")
        else:
            logout = False
            while not logout:
                user_loggedin(user["username"])
                wanna_logout = input("Do you want to logout? If so press x \n")
                if wanna_logout.lower() == "x":
                    logout = True
    elif choice == "4":
        exited = True
    else:
        print("Invalid option!")
    return choice=="4"
    
    
exited = False
user_id = None
while not exited:
    exited = user_login()

        
