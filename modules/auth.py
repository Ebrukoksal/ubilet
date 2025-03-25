
# auth.py
import json
import hashlib


def login():
    username = input("Kullanıcı Adı: ")
    password = input("Şifre: ")


    # Kullanıcıların saklandığı bir JSON dosyası ya da dictionary varsayılabilir
    with open("data/users.json", "r", encoding="utf-8") as f:
        users = json.load(f)


    hashed_password = hashlib.sha256(password.encode()).hexdigest()


    for user in users:
        if user["username"] == username and user["hashed_password"] == hashed_password:
            print("Giriş başarılı!")
            return user["role"]  # "admin" veya "user"


    print("Kullanıcı adı veya şifre hatalı!")
    return None

def signup():
    username = input("username= ")
    password = input("password= ")
    role = input("role= ")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()


    with open("data/users.json", "r", encoding="utf-8") as f:
        users = json.load(f) 

   
    user_presence = check_user(username, hashed_password, role)
    if user_presence == False:
        
        users.append(
            {
                "username" : username,
                "hashed_password": hashed_password,
                "role": role
            }
        )
        with open("data/users.json", "w") as f:
            json.dump(users, f)
        print("user added succesfully.")
    else:
        print("User already added.")
    return None

    



def check_user(username, hashed_password, role):
    with open("data/users.json", "r", encoding="utf-8") as f:
        users = json.load(f) 
    
    user_presence = False

    for user in users:
        if user["username"] == username and user["hashed_password"] == hashed_password and user["role"] == role:
            user_presence=True
            break
    return user_presence


    