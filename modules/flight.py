import json
from utils import get_hash
from utils import get_hash_with_kwargs
from utils import get_valid_input
from modules.logger import log_admin_action


def flight_arrangement(admin_username=None):
    choice = False
    while not choice:
        flight_arrangement = input(" Press 1 to add a flight \n Press 2 to remove a flight \n Press 3 to update flight informations \n Press 4 to display flights \n Press 5 to go back previous screen \n")
        if flight_arrangement == "1":
            add_flight(admin_username)
        elif flight_arrangement == "2":
            remove_flight(admin_username)
        elif flight_arrangement == "3":
            update_flight(admin_username)
        elif flight_arrangement == "4":
            display_flights_table()
        elif flight_arrangement == "5":
            choice = True
        else:
            print("Invalid input")

def get_flight_voyage_number(company, departure, arrival, date, time):
    voyage_number = company[0].upper() + departure[0].upper() + arrival[0].upper()
    voyage_number += date.replace("/", "")
    voyage_number += time.replace(":", "")
    
    return voyage_number


def add_flight(admin_username=None):
    with open("data/flights.json", "r", encoding="utf-8") as f:
        flights = json.load(f)

    company = get_valid_input("Company: ").lower()
    departure = get_valid_input("Departure: ").lower()
    arrival = get_valid_input("Arrival: ").lower()
    date = get_valid_input("Date: ")
    time_ = get_valid_input("Time: ")
    seat_available = get_valid_input("Seat Available: ", is_price=True)
    price = get_valid_input("Price: ", is_price=True)
    hashed_flight_id = get_hash(company, departure, arrival, date, time_, price)
    voyage_number = get_flight_voyage_number(company, departure, arrival, date, time_)

    flights[hashed_flight_id] = {
        "voyage_number": voyage_number,
        "company": company,
        "departure": departure,
        "arrival": arrival,
        "date": date,
        "time": time_,
        "seat_available": int(seat_available),
        "price": int(price)
    }
    with open("data/flights.json", "w", encoding="utf-8") as f:
        json.dump(flights, f, ensure_ascii=False, indent=2)
    
    if admin_username:
        log_admin_action(
            admin_username=admin_username,
            action_type="add",
            service_type="flight",
            details={
                "voyage_number": voyage_number,
                "company": company,
                "departure": departure,
                "arrival": arrival,
                "date": date,
                "time": time_,
                "seat_available": int(seat_available), 
                "price": int(price)
            }
        )
    print("Changes saved!")

def display_flights_table():
    """
    Display all flights in a formatted table.
    """
    try:
        with open("data/flights.json", "r", encoding="utf-8") as f:
            flights = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No flights found.")
        return

    if not flights:
        print("No flights found.")
        return

    # Table header
    print("\nExisting Flights:")
    print("-" * 100)
    print(f"{'Voyage Number':<15} {'Company':<10} {'From':<15} {'To':<15} {'Date':<12} {'Time':<8} {'Seat Available':<10} {'Price':<10}")
    print("-" * 100)

    # Table rows
    for flight in flights.values():
        print(f"{flight['voyage_number']:<15} "
              f"{flight['company']:<10} "
              f"{flight['departure']:<15} "
              f"{flight['arrival']:<15} "
              f"{flight['date']:<12} "
              f"{flight['time']:<8} "
              f"{flight['seat_available']:<10} "
              f"{flight['price']:<10}")
    print("-" * 100)
    print()

def remove_flight(admin_username=None):
    with open("data/flights.json", "r", encoding="utf-8") as f:
        flights = json.load(f)
    
    display_flights_table()
    print("Please enter the voyage number of the flight you want to remove ")
    voyage_number = get_valid_input("Voyage Number: ")
    key_to_remove = None
    flight_details = None
    for key, flight in flights.items():
        if flight["voyage_number"] == voyage_number:
            key_to_remove = key
            flight_details = flight
            break
    if key_to_remove in flights.keys():
        del flights[key_to_remove]
        if admin_username and flight_details:
            log_admin_action(
                admin_username=admin_username,
                action_type="remove",
                service_type="flight",
                details=flight_details
            )
    else:
        print("No flights were found matching the information entered. \n")
    
    with open("data/flights.json", "w", encoding="utf-8") as f:
        json.dump(flights, f, ensure_ascii=False, indent=2)

def update_flight(admin_username=None):
    with open("data/flights.json", "r", encoding="utf-8") as f:
        flights = json.load(f)
    
    display_flights_table()
    print("Please enter the voyage number of the flight you want to update \n")
    voyage_number = get_valid_input("Voyage Number: ")
    key_to_updating_flight = None
    for key, flight in flights.items():
        if flight["voyage_number"] == voyage_number:
            key_to_updating_flight = key
            break

    if key_to_updating_flight in flights:
        old_flight_details = flights[key_to_updating_flight].copy()
        key_to_update = input("Enter the detail you want to change (company/departure/arrival/date/time/seat_available/price): ").lower()
        new_value = input(f"Enter the new {key_to_update}: ")
        
        if key_to_update == "price" or key_to_update == "seat_available":
            flights[key_to_updating_flight][key_to_update] = int(new_value)
            flights[key_to_updating_flight]["seat_available"] = int(new_value)
        else:
            flights[key_to_updating_flight][key_to_update] = new_value.lower()

        updated_voyage_number = get_flight_voyage_number(
            flights[key_to_updating_flight]["company"],
            flights[key_to_updating_flight]["departure"],
            flights[key_to_updating_flight]["arrival"],
            flights[key_to_updating_flight]["date"],
            flights[key_to_updating_flight]["time"]
        )

        new_key_updated_flight = get_hash_with_kwargs(**flights[key_to_updating_flight])

        kwargs = {
            "voyage_number": updated_voyage_number
        }

        kwargs[key_to_update] = flights[key_to_updating_flight][key_to_update]

        new_key_updated_flight = get_hash_with_kwargs(**kwargs)
        flights[new_key_updated_flight] = flights[key_to_updating_flight].copy()
        flights[new_key_updated_flight]["voyage_number"] = updated_voyage_number
        del flights[key_to_updating_flight]

        if admin_username:
            log_admin_action(
                admin_username=admin_username,
                action_type="update",
                service_type="flight",
                details={
                    "old_details": old_flight_details,
                    "new_details": flights[new_key_updated_flight],
                    "changed_field": key_to_update
                }
            )

        print("Changes saved!")
    else:
        print("No flights were found matching the information entered. \n")

    with open("data/flights.json", "w", encoding="utf-8") as f:
        json.dump(flights, f, ensure_ascii=False, indent=2)
