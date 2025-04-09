from modules.user_bus import user_bus_arrangement
from modules.user_car import user_car_arrangement
from modules.user_flight import user_flight_arrangement
from modules.user_hotel import user_hotel_arrangement
from modules.user_train import user_train_arrangement
from utils import display_user_tickets

def user_loggedin(user):
    print(f"Welcome to Ubilet! How can I assist you {user}")
    exited = False
    while not exited:
        print("1 - Flights \n"
            "2 - Buses \n"
            "3 - Trains \n"
            "4 - Hotels \n"
            "5 - Cars \n"
            "6 - View my tickets \n"
            "7 - Logout \n")
        selected_operation = input("Operation number : ")
        if selected_operation =="1":
            user_flight_arrangement(user)
        elif selected_operation == "2":
            user_bus_arrangement(user)
        elif selected_operation == "3":
            user_train_arrangement(user)
        elif selected_operation == "4":
            user_hotel_arrangement(user)
        elif selected_operation == "5":
            user_car_arrangement(user)
        elif selected_operation == "6":
            display_user_tickets(user)
        elif selected_operation == "7":
            exited = True
        else:
            print("Invalid input! Please select an operation.")
    return exited





