import json
from utils import get_hash
from utils import get_hash_with_kwargs
from utils import get_valid_input
from modules.logger import log_admin_action

def bus_arrangement(admin_username=None):
    choice = False
    while not choice:
        bus_arrangement = input(" Press 1 to add a bus service \n Press 2 to remove a bus service \n Press 3 to update bus service informations \n Press 4 to display buses \n Press 5 to go back previous screen \n")
        if bus_arrangement == "1":
            add_bus(admin_username)
        elif bus_arrangement == "2":
            remove_bus(admin_username)
        elif bus_arrangement == "3":
            update_bus(admin_username)
        elif bus_arrangement == "4":
            display_buses_table()
        elif bus_arrangement == "5":
            choice = True
        else:
            print("Invalid input")

def get_bus_voyage_number(company, departure, arrival, date, time):
    voyage_number = company[0].upper() + departure[0].upper() + arrival[0].upper()
    voyage_number += date.replace("/", "")
    voyage_number += time.replace(":", "")
    
    return voyage_number


def add_bus(admin_username=None):
    with open("data/buses.json", "r", encoding="utf-8") as f:
        buses = json.load(f)

    company = get_valid_input("Company: ").lower()
    departure = get_valid_input("Departure: ").lower()
    arrival = get_valid_input("Arrival: ").lower()
    date = get_valid_input("Date: ")
    time = get_valid_input("Time: ")
    seat_available = get_valid_input("Seat Available: ", is_price=True)
    price = get_valid_input("Price: ", is_price=True)

    hashed_bus_id = get_hash(company, departure, arrival, date, time, price)
    voyage_number = get_bus_voyage_number(company, departure, arrival, date, time)


    buses[hashed_bus_id] = {
        "voyage_number": voyage_number,
        "company": company,
        "departure": departure,
        "arrival": arrival,
        "date": date,
        "time": time,
        "seat_available": int(seat_available),
        "price": int(price)
    }
    with open("data/buses.json", "w", encoding="utf-8") as f:
        json.dump(buses, f, ensure_ascii=False, indent=2)
    
    if admin_username:
        log_admin_action(
            admin_username=admin_username,
            action_type="add",
            service_type="bus",
            details={
                "voyage_number": voyage_number,
                "company": company,
                "departure": departure,
                "arrival": arrival,
                "date": date,
                "time": time,
                "seat_available": int(seat_available),
                "price": int(price)
            }
        )
    print("Changes saved!")
    
def display_buses_table():
    """
    Display all buses in a formatted table.
    """
    try:
        with open("data/buses.json", "r", encoding="utf-8") as f:
            buses = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No buses found.")
        return

    if not buses:
        print("No buses found.")
        return

    # Table header
    print("\nExisting Buses:")
    print("-" * 100)
    print(f"{'Voyage Number':<15} {'Company':<10} {'From':<15} {'To':<15} {'Date':<12} {'Time':<8} {'Seat Available':<10} {'Price':<10}")
    print("-" * 100)

    # Table rows
    for bus in buses.values():
        print(f"{bus['voyage_number']:<15} "
              f"{bus['company']:<10} "
              f"{bus['departure']:<15} "
              f"{bus['arrival']:<15} "
              f"{bus['date']:<12} "
              f"{bus['time']:<8} "
              f"{bus['seat_available']:<10} "
              f"{bus['price']:<10}")
    print("-" * 100)
    print()


def remove_bus(admin_username=None):
    with open("data/buses.json", "r", encoding="utf-8") as f:
        buses = json.load(f)
    
    display_buses_table()
    print("Please enter the voyage number of the bus you want to remove ")
    voyage_number = get_valid_input("Voyage Number: ")
    key_to_remove = None
    bus_details = None
    for key, bus in buses.items():
        if bus["voyage_number"] == voyage_number:
            key_to_remove = key
            bus_details = bus
            break
    if key_to_remove in buses.keys():
        del buses[key_to_remove]
        if admin_username and bus_details:
            log_admin_action(
                admin_username=admin_username,
                action_type="remove",
                service_type="bus",
                details=bus_details
            )
    else:
        print("No buses were found matching the information entered. \n")
    
    with open("data/buses.json", "w", encoding="utf-8") as f:
        json.dump(buses, f, ensure_ascii=False, indent=2)


def update_bus(admin_username=None):
    with open("data/buses.json", "r", encoding="utf-8") as f:
        buses = json.load(f)
    
    display_buses_table()
    print("Please enter the voyage number of the bus you want to update \n")
    voyage_number = get_valid_input("Voyage Number: ")
    key_to_updating_bus = None
    for key, bus in buses.items():
        if bus["voyage_number"] == voyage_number:
            key_to_updating_bus = key
            break

    if key_to_updating_bus in buses:
        old_bus_details = buses[key_to_updating_bus].copy()
        key_to_update = input("Enter the detail you want to change (company/departure/arrival/date/time/seat_available/price): ").lower()
        new_value = input(f"Enter the new {key_to_update}: ")
        
        if key_to_update == "price" or key_to_update == "seat_available":
            buses[key_to_updating_bus][key_to_update] = int(new_value)
            buses[key_to_updating_bus]["seat_available"] = int(new_value)
        else:
            buses[key_to_updating_bus][key_to_update] = new_value.lower()

        updated_voyage_number = get_bus_voyage_number(
            buses[key_to_updating_bus]["company"],
            buses[key_to_updating_bus]["departure"],
            buses[key_to_updating_bus]["arrival"],
            buses[key_to_updating_bus]["date"],
            buses[key_to_updating_bus]["time"]
        )

        new_key_updated_bus = get_hash_with_kwargs(**buses[key_to_updating_bus])

        kwargs = {
            "voyage_number": updated_voyage_number
        }

        kwargs[key_to_update] = buses[key_to_updating_bus][key_to_update]

        new_key_updated_bus = get_hash_with_kwargs(**kwargs)
        buses[new_key_updated_bus] = buses[key_to_updating_bus].copy()
        buses[new_key_updated_bus]["voyage_number"] = updated_voyage_number
        del buses[key_to_updating_bus]

        if admin_username:
            log_admin_action(
                admin_username=admin_username,
                action_type="update",
                service_type="bus",
                details={
                    "old_details": old_bus_details,
                    "new_details": buses[new_key_updated_bus],
                    "changed_field": key_to_update
                }
            )

        print("Changes saved!")
    else:
        print("No buses were found matching the information entered. \n")

    with open("data/buses.json", "w", encoding="utf-8") as f:
        json.dump(buses, f, ensure_ascii=False, indent=2)




