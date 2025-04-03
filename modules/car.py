import json
from utils import get_hash
from utils import get_hash_with_kwargs
from utils import get_valid_input
from modules.logger import log_admin_action

def car_arrangement(admin_username=None):
    choice = False
    while not choice:
        car_arrangement = input("Press 1 to add a car service \n Press 2 to remove a car service \n Press 3 to update car service informations \n Press 4 to go back previous screen \n")
        if car_arrangement == "1":
            add_car(admin_username)
        elif car_arrangement == "2":
            remove_car(admin_username)
        elif car_arrangement == "3":
            update_car(admin_username)
        elif car_arrangement == "4":
            choice = True
        else:
            print("Invalid input")

def get_car_id(brand, rental_date, return_date):
    car_id = brand[0].upper()
    car_id += rental_date.replace("/", "").upper()
    car_id += return_date.replace("/", "").upper()
    
    return car_id


def add_car(admin_username=None):
    with open("data/cars.json", "r", encoding="utf-8") as f:
        cars = json.load(f)

    brand = get_valid_input("Brand: ").lower()
    rental_date = get_valid_input("Rental Date: ")
    return_date = get_valid_input("Return Date: ")
    price = get_valid_input("Price: ", is_price=True)

    hashed_car_id = get_hash(brand, rental_date, return_date, price)
    car_id = get_car_id(brand, rental_date, return_date)


    cars[hashed_car_id] = {
        "car_id": car_id,
        "brand": brand,
        "rental_date": rental_date,
        "return_date": return_date,
        "price": int(price)
    }
    with open("data/cars.json", "w", encoding="utf-8") as f:
        json.dump(cars, f, ensure_ascii=False, indent=2)
    
    if admin_username:
        log_admin_action(
            admin_username=admin_username,
            action_type="add",
            service_type="car",
            details={
                "car_id": car_id,
                "brand": brand,
                "rental_date": rental_date,
                "return_date": return_date,
                "price": int(price)
            }
        )
    print("Değişiklikler kaydedildi.")

def display_cars_table():
    """
    Display all cars in a formatted table.
    """
    try:
        with open("data/cars.json", "r", encoding="utf-8") as f:
            cars = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No cars found.")
        return

    if not cars:
        print("No cars found.")
        return

    # Table header
    print("\nExisting Cars:")
    print("-" * 100)
    print(f"{'Voyage Number':<15} {'Brand':<10} {'Rental Date':<15} {'Return Date':<15} {'Price':<10}")
    print("-" * 100)

    # Table rows
    for car in cars.values():
        print(f"{car['car_id']:<15} "
              f"{car['brand']:<10} "
              f"{car['rental_date']:<15} "
              f"{car['return_date']:<15} "
              f"{car['price']:<10}")
    print("-" * 100)
    print()


def remove_car(admin_username=None):
    with open("data/cars.json", "r", encoding="utf-8") as f:
        cars = json.load(f)
    
    display_cars_table()
    print("Please enter the car id of the car you want to remove ")
    car_id = get_valid_input("Car ID: ")
    key_to_remove = None
    car_details = None
    for key, car in cars.items():
        if car["car_id"] == car_id:
            key_to_remove = key
            car_details = car
            break
    if key_to_remove in cars.keys():
        del cars[key_to_remove]
        if admin_username and car_details:
            log_admin_action(
                admin_username=admin_username,
                action_type="remove",
                service_type="car",
                details=car_details
            )
    else:
        print("No cars were found matching the information entered. \n")
    
    with open("data/cars.json", "w", encoding="utf-8") as f:
        json.dump(cars, f, ensure_ascii=False, indent=2)

def update_car(admin_username=None):
    with open("data/cars.json", "r", encoding="utf-8") as f:
        cars = json.load(f)
    
    display_cars_table()
    print("Please enter the car id of the car you want to update \n")
    car_id = get_valid_input("Car ID: ")
    key_to_updating_car = None
    for key, car in cars.items():
        if car["car_id"] == car_id:
            key_to_updating_car = key
            break

    if key_to_updating_car in cars:
        old_car_details = cars[key_to_updating_car].copy()
        key_to_update = input("Enter the detail you want to change (brand/rental_date/return_date/price): ").lower()
        new_value = input(f"Enter the new {key_to_update}: ")
        
        if key_to_update == "price":
            cars[key_to_updating_car][key_to_update] = int(new_value)
        else:
            cars[key_to_updating_car][key_to_update] = new_value.lower()

        updated_car_id = get_car_id(
            cars[key_to_updating_car]["brand"],
            cars[key_to_updating_car]["rental_date"],
            cars[key_to_updating_car]["return_date"]
        )

        new_key_updated_car = get_hash_with_kwargs(**cars[key_to_updating_car])

        kwargs = {
            "car_id": updated_car_id
        }

        kwargs[key_to_update] = cars[key_to_updating_car][key_to_update]

        new_key_updated_car = get_hash_with_kwargs(**kwargs)
        cars[new_key_updated_car] = cars[key_to_updating_car].copy()
        cars[new_key_updated_car]["car_id"] = updated_car_id
        del cars[key_to_updating_car]

        if admin_username:
            log_admin_action(
                admin_username=admin_username,
                action_type="update",
                service_type="car",
                details={
                    "old_details": old_car_details,
                    "new_details": cars[new_key_updated_car],
                    "changed_field": key_to_update
                }
            )

        print("Changes saved!")
    else:
        print("No cars were found matching the information entered. \n")

    with open("data/cars.json", "w", encoding="utf-8") as f:
        json.dump(cars, f, ensure_ascii=False, indent=2)

