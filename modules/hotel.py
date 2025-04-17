import json
from utils import get_hash
from utils import get_hash_with_kwargs
from utils import get_valid_input
from modules.logger import log_admin_action
import random

def hotel_arrangement(admin_username=None):
    choice = False
    while not choice:
        hotel_arrangement = input(" Press 1 to add a hotel service \n Press 2 to remove a hotel service \n Press 3 to update hotel service informations \n Press 4 to display hotels \n Press 5 to go back previous screen \n")
        if hotel_arrangement == "1":
            add_hotel(admin_username)
        elif hotel_arrangement == "2":
            remove_hotel(admin_username)
        elif hotel_arrangement == "3":
            update_hotel(admin_username)
        elif hotel_arrangement == "4":
            display_hotels_table()
        elif hotel_arrangement == "5":
            choice = True
        else:
            print("Invalid input")

def get_hotel_id(hotel_name, location):
    # Use the first three letters of the hotel name
    hotel_id = hotel_name[:3].upper()
    
    # Add the first two letters of the location
    hotel_id += location[:2].upper()
    
    # Add a random number to make it unique
    hotel_id += str(random.randint(100, 999))
    
    return hotel_id

def add_hotel(admin_username=None):
    with open("data/hotels.json", "r", encoding="utf-8") as f:
        hotels = json.load(f)

    hotel_name = get_valid_input("Hotel Name: ").lower()
    location = get_valid_input("Location: ").lower()
    rooms_available = get_valid_input("Rooms Available: ", is_price=True)
    adult_price = get_valid_input("Price per adult per day: ", is_price=True)
    child_price = get_valid_input("Price per child per day: ", is_price=True)

    hashed_hotel_id = get_hash(hotel_name, adult_price)
    hotel_id = get_hotel_id(hotel_name, location)

    hotels[hashed_hotel_id] = {
        "hotel_id": hotel_id,
        "hotel_name": hotel_name,
        "location": location,
        "rooms_available": int(rooms_available),
        "adult_price": int(adult_price),
        "child_price": int(child_price)
    }
    with open("data/hotels.json", "w", encoding="utf-8") as f:
        json.dump(hotels, f, ensure_ascii=False, indent=2)
    
    if admin_username:
        log_admin_action(
            admin_username=admin_username,
            action_type="add",
            service_type="hotel",
            details={
                "hotel_id": hotel_id,
                "hotel_name": hotel_name,
                "location": location,
                "rooms_available": int(rooms_available),
                "adult_price": int(adult_price),
                "child_price": int(child_price)
            }
        )
    print("Changes saved!")

def display_hotels_table():
    """
    Display all hotels in a formatted table.
    """
    try:
        with open("data/hotels.json", "r", encoding="utf-8") as f:
            hotels = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No hotels found.")
        return

    if not hotels:
        print("No hotels found.")
        return

    # Table header
    print("\nExisting Hotels:")
    print("-" * 120)
    print(f"{'Hotel ID':<15} {'Hotel Name':<15} {'location':<15} {'Rooms Available':<15} {'Adult Price/Day':<15} {'Child Price/Day':<15}")
    print("-" * 120)

    # Table rows
    for hotel in hotels.values():
        print(f"{hotel['hotel_id']:<15} "
              f"{hotel['hotel_name']:<15} "
              f"{hotel['location']:<15} "
              f"{hotel['rooms_available']:<15} "
              f"{hotel['adult_price']:<15} "
              f"{hotel['child_price']:<15}")
    print("-" * 120)
    print()

def remove_hotel(admin_username=None):
    with open("data/hotels.json", "r", encoding="utf-8") as f:
        hotels = json.load(f)
    
    display_hotels_table()
    print("Please enter the hotel id of the hotel you want to remove ")
    hotel_id = get_valid_input("Hotel ID: ")
    key_to_remove = None
    hotel_details = None
    for key, hotel in hotels.items():
        if hotel["hotel_id"] == hotel_id:
            key_to_remove = key
            hotel_details = hotel
            break
    if key_to_remove in hotels.keys():
        del hotels[key_to_remove]
        if admin_username and hotel_details:
            log_admin_action(
                admin_username=admin_username,
                action_type="remove",
                service_type="hotel",
                details=hotel_details
            )
    else:
        print("No hotels were found matching the information entered. \n")
    
    with open("data/hotels.json", "w", encoding="utf-8") as f:
        json.dump(hotels, f, ensure_ascii=False, indent=2)

def update_hotel(admin_username=None):
    with open("data/hotels.json", "r", encoding="utf-8") as f:
        hotels = json.load(f)
    
    display_hotels_table()
    print("Please enter the hotel id of the hotel you want to update \n")
    hotel_id = get_valid_input("Hotel ID: ")
    key_to_updating_hotel = None
    for key, hotel in hotels.items():
        if hotel["hotel_id"] == hotel_id:
            key_to_updating_hotel = key
            break

    if key_to_updating_hotel in hotels:
        old_hotel_details = hotels[key_to_updating_hotel].copy()
        key_to_update = input("Enter the detail you want to change (hotel_name/location/rooms_available/adult_price/child_price): ").lower()
        
        if key_to_update == "adult_price" or key_to_update == "child_price" or key_to_update == "rooms_available":
            new_value = input(f"Enter the new {key_to_update}: ")
            hotels[key_to_updating_hotel][key_to_update] = int(new_value)
        else:
            new_value = input(f"Enter the new {key_to_update}: ")
            hotels[key_to_updating_hotel][key_to_update] = new_value.lower()

        updated_hotel_id = get_hotel_id(
            hotels[key_to_updating_hotel]["hotel_name"],
            hotels[key_to_updating_hotel]["location"]
        )

        new_key_updated_hotel = get_hash_with_kwargs(**hotels[key_to_updating_hotel])

        kwargs = {
            "hotel_id": updated_hotel_id
        }

        kwargs[key_to_update] = hotels[key_to_updating_hotel][key_to_update]

        new_key_updated_hotel = get_hash_with_kwargs(**kwargs)
        hotels[new_key_updated_hotel] = hotels[key_to_updating_hotel].copy()
        hotels[new_key_updated_hotel]["hotel_id"] = updated_hotel_id
        del hotels[key_to_updating_hotel]

        if admin_username:
            log_admin_action(
                admin_username=admin_username,
                action_type="update",
                service_type="hotel",
                details={
                    "old_details": old_hotel_details,
                    "new_details": hotels[new_key_updated_hotel],
                    "changed_field": key_to_update
                }
            )

        print("Changes saved!")
    else:
        print("No hotels were found matching the information entered. \n")

    with open("data/hotels.json", "w", encoding="utf-8") as f:
        json.dump(hotels, f, ensure_ascii=False, indent=2)

