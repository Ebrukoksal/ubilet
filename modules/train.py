import json
from utils import get_hash
from utils import get_hash_with_kwargs
from utils import get_valid_input
from modules.logger import log_admin_action

def train_arrangement(admin_username=None):
    choice = False
    while not choice:
        train_arrangement = input(" Press 1 to add a train service \n Press 2 to remove a train service \n Press 3 to update train service informations \n Press 4 to display trains \n Press 5 to go back previous screen \n")
        if train_arrangement == "1":
            add_train(admin_username)
        elif train_arrangement == "2":
            remove_train(admin_username)
        elif train_arrangement == "3":
            update_train(admin_username)
        elif train_arrangement == "4":
            display_trains_table()
        elif train_arrangement == "5":
            choice = True
        else:
            print("Invalid input")

def get_train_voyage_number(company, departure, arrival, date, time):
    voyage_number = company[0].upper() + departure[0].upper() + arrival[0].upper()
    voyage_number += date.replace("/", "")
    voyage_number += time.replace(":", "")
    
    return voyage_number


def add_train(admin_username=None):
    with open("data/trains.json", "r", encoding="utf-8") as f:
        trains = json.load(f)

    company = get_valid_input("Company: ").lower()
    departure = get_valid_input("Departure: ").lower()
    arrival = get_valid_input("Arrival: ").lower()
    date = get_valid_input("Date: ")
    time = get_valid_input("Time: ")
    seats_available = get_valid_input("Seats Available: ")
    price = get_valid_input("Price: ", is_price=True)

    hashed_train_id = get_hash(company, departure, arrival, date, time, price)
    voyage_number = get_train_voyage_number(company, departure, arrival, date, time)


    trains[hashed_train_id] = {
        "voyage_number": voyage_number,
        "company": company,
        "departure": departure,
        "arrival": arrival,
        "date": date,
        "time": time,
        "price": int(price),
        "seats_available": int(seats_available)
    }
    with open("data/trains.json", "w", encoding="utf-8") as f:
        json.dump(trains, f, ensure_ascii=False, indent=2)
    
    if admin_username:
        log_admin_action(
            admin_username=admin_username,
            action_type="add",
            service_type="train",
            details={
                "voyage_number": voyage_number,
                "company": company,
                "departure": departure,
                "arrival": arrival,
                "date": date,
                "time": time,
                "price": int(price),
                "seats_available": int(seats_available)
            }
        )
    print("Changes saved!")
    
def display_trains_table():
    """
    Display all trains in a formatted table.
    """
    try:
        with open("data/trains.json", "r", encoding="utf-8") as f:
            trains = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No trains found.")
        return

    if not trains:
        print("No trains found.")
        return

    # Table header
    print("\nExisting Trains:")
    print("-" * 100)
    print(f"{'Voyage Number':<15} {'Company':<10} {'From':<15} {'To':<15} {'Date':<12} {'Time':<8} {'Price':<10} {'Seats Available':<10}")
    print("-" * 100)

    # Table rows
    for train in trains.values():
        print(f"{train['voyage_number']:<15} "
              f"{train['company']:<10} "
              f"{train['departure']:<15} "
              f"{train['arrival']:<15} "
              f"{train['date']:<12} "
              f"{train['time']:<8} "
              f"{train['price']:<10} "
              f"{train['seats_available']:<10}")
    print("-" * 100)
    print()


def remove_train(admin_username=None):
    with open("data/trains.json", "r", encoding="utf-8") as f:
        trains = json.load(f)
    
    display_trains_table()
    print("Please enter the voyage number of the train you want to remove ")
    voyage_number = get_valid_input("Voyage Number: ")
    key_to_remove = None
    train_details = None
    for key, train in trains.items():
        if train["voyage_number"] == voyage_number:
            key_to_remove = key
            train_details = train
            break
    if key_to_remove in trains.keys():
        del trains[key_to_remove]
        if admin_username and train_details:
            log_admin_action(
                admin_username=admin_username,
                action_type="remove",
                service_type="train",
                details=train_details
            )
    else:
        print("No trains were found matching the information entered. \n")
    
    with open("data/trains.json", "w", encoding="utf-8") as f:
        json.dump(trains, f, ensure_ascii=False, indent=2)


def update_train(admin_username=None):
    with open("data/trains.json", "r", encoding="utf-8") as f:
        trains = json.load(f)
    
    display_trains_table()
    print("Please enter the voyage number of the train you want to update \n")
    voyage_number = get_valid_input("Voyage Number: ")
    key_to_updating_train = None
    for key, train in trains.items():
        if train["voyage_number"] == voyage_number:
            key_to_updating_train = key
            break

    if key_to_updating_train in trains:
        old_train_details = trains[key_to_updating_train].copy()
        key_to_update = input("Enter the detail you want to change (company/departure/arrival/date/time/price/seats_available): ").lower()
        new_value = input(f"Enter the new {key_to_update}: ")
        
        if key_to_update == "price" or key_to_update == "seats_available":
            trains[key_to_updating_train][key_to_update] = int(new_value) 
            trains[key_to_updating_train]["seats_available"] = int(new_value)
        else:
            trains[key_to_updating_train][key_to_update] = new_value.lower()

        updated_voyage_number = get_train_voyage_number(
            trains[key_to_updating_train]["company"],
            trains[key_to_updating_train]["departure"],
            trains[key_to_updating_train]["arrival"],
            trains[key_to_updating_train]["date"],
            trains[key_to_updating_train]["time"]
        )

        new_key_updated_train = get_hash_with_kwargs(**trains[key_to_updating_train])

        kwargs = {
            "voyage_number": updated_voyage_number
        }

        kwargs[key_to_update] = trains[key_to_updating_train][key_to_update]

        new_key_updated_train = get_hash_with_kwargs(**kwargs)
        trains[new_key_updated_train] = trains[key_to_updating_train].copy()
        trains[new_key_updated_train]["voyage_number"] = updated_voyage_number
        del trains[key_to_updating_train]

        if admin_username:
            log_admin_action(
                admin_username=admin_username,
                action_type="update",
                service_type="train",
                details={
                    "old_details": old_train_details,
                    "new_details": trains[new_key_updated_train],
                    "changed_field": key_to_update
                }
            )

        print("Changes saved!")
    else:
        print("No buses were found matching the information entered. \n")

    with open("data/trains.json", "w", encoding="utf-8") as f:
        json.dump(trains, f, ensure_ascii=False, indent=2)




