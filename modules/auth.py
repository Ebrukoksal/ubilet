
# auth.py
import json
from modules.admin import admin
from utils import get_hash


def login(role):
    username = input("Name : ")
    password = input("Password : ")

    with open("data/users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

    hashed_password = get_hash(password)

    user_id = generate_user_id(username, hashed_password, role)

    return get_user(user_id)

def signup():
    username = input("Name : ")
    password = input("Password : ")
    role = input("Role : ")

    hashed_password = get_hash(password)
    user_id = generate_user_id(username, hashed_password, role)

    with open("data/users.json", "r", encoding="utf-8") as f:
        users = json.load(f) 

   
    user_presence = get_user(user_id)
    if not user_presence:
        
        users[user_id] = {
            "username" : username,
            "hashed_password" : hashed_password,
            "role" : role
        }
        with open("data/users.json", "w") as f:
            json.dump(users, f, indent=4)
        print("User added succesfully!")
    else:
        print("User already registered!")
    return None

    



def get_user(user_id):
    with open("data/users.json", "r", encoding="utf-8") as f:
        users = json.load(f) 
    
    return users.get(user_id)

def generate_user_id(username, hashed_password, role):
    return get_hash(username, hashed_password, role)


    