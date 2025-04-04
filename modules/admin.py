from modules.bus import bus_arrangement
from modules.car import car_arrangement
from modules.flight import flight_arrangement
from modules.hotel import hotel_arrangement
from modules.train import train_arrangement
from modules.logger import get_admin_logs


def admin(username):
    print(f"Welcome to Ubilet! How can I assist you {username}")
    exited = False
    while not exited:
        print("Select the operation you want to proceed by entering the operation number \n")
        print("1 - Manage Flights (Add/Remove/Update) \n"
            "2 - Manage Buses (Add/Remove/Update) \n"
            "3 - Manage Trains (Add/Remove/Update) \n"
            "4 - Manage Hotels (Add/Remove/Update) \n"
            "5 - Manage Cars (Add/Remove/Update) \n"
            "6 - Display Admin Logs \n"
            "7 - Logout Admin Panel \n")
        selected_operation = input("Operation number : ")
        if selected_operation =="1":
            flight_arrangement(username)
        elif selected_operation == "2":
            bus_arrangement(username)
        elif selected_operation == "3":
            train_arrangement(username)
        elif selected_operation == "4":
            hotel_arrangement(username)
        elif selected_operation == "5":
            car_arrangement(username)
        elif selected_operation == "6":
            display_admin_logs()
        elif selected_operation == "7":
            exited = True
        else:
            print("Invalid input! Please select an operation.")
    return exited

def display_admin_logs():
    logs = get_admin_logs()
    if not logs:
        print("No admin logs found.")
        return
    
    print("\nAdmin Action Logs:")
    print("-" * 50)
    for timestamp, log in logs.items():
        print(f"Timestamp: {log['timestamp']}")
        print(f"Admin: {log['admin_username']}")
        print(f"Action: {log['action_type']} {log['service_type']}")
        print("Details:")
        for key, value in log['details'].items():
            print(f"  {key}: {value}")
        print("-" * 50)





