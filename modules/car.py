import json
from utils import get_hash
from utils import get_hash_with_kwargs
from utils import get_valid_input
from modules.logger import log_admin_action

def car_arrangement(admin_username=None):
    choice = False
    while not choice:
        car_arrangement = input(" Press 1 to add a car service \n Press 2 to remove a car service \n Press 3 to update car service informations \n Press 4 to display cars \n Press 5 to go back previous screen \n")
        if car_arrangement == "1":
            add_car(admin_username)
        elif car_arrangement == "2":
            remove_car(admin_username)
        elif car_arrangement == "3":
            update_car(admin_username)
        elif car_arrangement == "4":
            display_cars_table()
        elif car_arrangement == "5":
            choice = True
        else:
            print("Invalid input")

def get_car_id(brand, car_plate):
    car_id = brand[0].upper() + car_plate.upper() 
    return car_id

def add_car(admin_username=None):
    with open("data/cars.json", "r", encoding="utf-8") as f:
        cars = json.load(f)

    brand = get_valid_input("Brand: ").lower()
    cars_available = get_valid_input("Number of Available Cars: ", is_price=True)
    price = get_valid_input("Price: ", is_price=True)
    car_plate = get_valid_input("Car Plate (2 letters + 3 digits): ", is_car_plate=True)

    hashed_car_id = get_hash(brand, car_plate)
    car_id = get_car_id(brand, car_plate)

    cars[hashed_car_id] = {
        "car_id": car_id,
        "brand": brand,
        "cars_available": int(cars_available),
        "price": int(price),
        "car_plate": car_plate.upper()
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
                "cars_available": int(cars_available),
                "price": int(price),
                "car_plate": car_plate.upper()
            }
        )
    print("Changes saved!")

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
    print(f"{'Car ID':<15} {'Brand':<10} {'Cars Available':<15} {'Price':<10} {'Car Plate':<10}")
    print("-" * 100)

    # Table rows
    for car in cars.values():
        print(f"{car['car_id']:<15} "
              f"{car['brand']:<10} "
              f"{car['cars_available']:<15} "
              f"{car['price']:<10} "
              f"{car['car_plate']:<10}")
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
        key_to_update = input("Enter the detail you want to change (brand/cars_available/price/car_plate): ").lower()
        
        if key_to_update == "car_plate":
            new_value = get_valid_input(f"Enter the new {key_to_update}: ", is_car_plate=True)
            cars[key_to_updating_car][key_to_update] = new_value.upper()
        elif key_to_update == "price" or key_to_update == "cars_available":
            new_value = input(f"Enter the new {key_to_update}: ")
            cars[key_to_updating_car][key_to_update] = int(new_value)
        else:
            new_value = input(f"Enter the new {key_to_update}: ")
            cars[key_to_updating_car][key_to_update] = new_value.lower()

        updated_car_id = get_car_id(
            cars[key_to_updating_car]["brand"],
            cars[key_to_updating_car]["car_plate"]
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

