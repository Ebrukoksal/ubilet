from modules.auth import login, signup

def user_login():
    choice = input("Press 1 to sign up / Press 2 to login / Press 3 to exit")

    if choice == "1":
        signup()
    elif choice =="2":
        login()
    elif choice == "3":
        print("by")
    else:
        print("Invalid option!")
    return choice=="3"
    
exited = False
while not exited:
    exited = user_login()
        
