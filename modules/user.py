from modules.bus import bus_arrangement
from modules.car import car_arrangement
from modules.flight import flight_arrangement
from modules.hotel import hotel_arrangement
from modules.train import train_arrangement


def user_loggedin(username):
    print(f"Welcome to Ubilet! How can I assist you {username}")
    exited = False
    while not exited:
        print("1 - Uçak seferleri \n"
            "2 - Otobüs seferleri \n"
            "3 - Tren seferleri \n"
            "4 - Otel seferleri \n"
            "5 - Araç seferleri \n"
            "6 - Çıkış yap \n")
        selected_operation = input("Operation number : ")
        if selected_operation =="1":
            flight_arrangement()
        elif selected_operation == "2":
            bus_arrangement()
        elif selected_operation == "3":
            train_arrangement()
        elif selected_operation == "4":
            hotel_arrangement()
        elif selected_operation == "5":
            car_arrangement()
        elif selected_operation == "6":
            exited = True
            print("by")
        else:
            print("Invalid input! Please select an operation.")
    return exited





