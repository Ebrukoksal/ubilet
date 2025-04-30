import json
import args
import random
from utils import get_valid_input, get_hash
from modules.logger import log_admin_action

class Rental:
    def __init__(self, rental_type):
        self.rental_type = rental_type
        filename = args.RENTAL_TYPE2FILENAME.get(rental_type)
        self.data_file = "data/" + filename
        self.service_name = rental_type

    def add(self, admin_username=None):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                rentals = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            rentals = {}

        if self.rental_type == 'car':
            brand = get_valid_input("Brand: ")
            location = get_valid_input("Location: ")
            cars_available = get_valid_input("Number of Available Cars: ", is_price=True)
            price = get_valid_input("Price per Day: ", is_price=True)
            
            # Handle car plate validation
            while True:
                car_plate = input("Car Plate (2 letters + 3 digits): ").strip().upper()
                if len(car_plate) == 5 and car_plate[:2].isalpha() and car_plate[2:].isdigit():
                    break
                print("Invalid car plate format. Please enter 2 letters followed by 3 digits.")

            # Generate hashed ID
            hashed_car_id = get_hash(brand, car_plate)

            rentals[hashed_car_id] = {
                "brand": brand,
                "location": location,
                "cars_available": int(cars_available),
                "price": int(price),
                "car_plate": car_plate
            }
        else:  # hotel
            hotel_name = get_valid_input("Hotel Name: ")
            location = get_valid_input("Location: ")
            rooms_available = get_valid_input("Rooms Available: ", is_price=True)
            adult_price = get_valid_input("Adult Price: ", is_price=True)
            child_price = get_valid_input("Child Price: ", is_price=True)

            # Generate hotel ID: first 3 letters of hotel name + first 2 letters of location + random 3 digits
            hotel_id = hotel_name[:3].upper() + location[:2].upper() + str(random.randint(100, 999))
            hashed_hotel_id = get_hash(hotel_name, adult_price)

            rentals[hashed_hotel_id] = {
                "hotel_id": hotel_id,
                "hotel_name": hotel_name,
                "location": location,
                "rooms_available": int(rooms_available),
                "adult_price": int(adult_price),
                "child_price": int(child_price)
            }

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(rentals, f, ensure_ascii=False, indent=2)
        
        if admin_username:
            log_admin_action(
                admin_username=admin_username,
                action_type="add",
                service_type=self.rental_type,
                details=rentals[hashed_hotel_id if self.rental_type == 'hotel' else hashed_car_id]
            )
        print("Changes saved!")

    def display_table(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                rentals = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No {self.rental_type}s found.")
            return

        if not rentals:
            print(f"No {self.rental_type}s found.")
            return

        if self.rental_type == 'car':
            print("\nExisting Cars:")
            print("-" * 100)
            print(f"{'Car Plate':<15} {'Brand':<10} {'Location':<15} {'Cars Available':<15} {'Price/Day':<10}")
            print("-" * 100)

            for car in rentals.values():
                print(f"{car['car_plate']:<15} "
                      f"{car['brand']:<10} "
                      f"{car['location']:<15} "
                      f"{car['cars_available']:<15} "
                      f"{car['price']:<10}")
        else:  # hotel
            print("\nExisting Hotels:")
            print("-" * 100)
            print(f"{'Hotel ID':<15} {'Name':<20} {'Location':<15} {'Rooms':<10} {'Adult Price':<15} {'Child Price':<15}")
            print("-" * 100)

            for hotel in rentals.values():
                print(f"{hotel['hotel_id']:<15} "
                      f"{hotel['hotel_name']:<20} "
                      f"{hotel['location']:<15} "
                      f"{hotel['rooms_available']:<10} "
                      f"{hotel['adult_price']:<15} "
                      f"{hotel['child_price']:<15}")
        
        print("-" * 100)
        print()

    def remove(self, admin_username=None):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                rentals = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No {self.rental_type}s found.")
            return
        
        self.display_table()
        
        if self.rental_type == 'car':
            print("Please enter the car plate of the car you want to remove")
            identifier = get_valid_input("Car Plate: ").upper()
            # Find the car by plate
            key_to_remove = None
            for key, car in rentals.items():
                if car['car_plate'] == identifier:
                    key_to_remove = key
                    break
        else:  # hotel
            print(f"Please enter the hotel ID of the {self.rental_type} you want to remove")
            identifier = get_valid_input("Hotel ID: ")
            key_to_remove = identifier
        
        if key_to_remove in rentals:
            rental_details = rentals[key_to_remove]
            del rentals[key_to_remove]
            if admin_username:
                log_admin_action(
                    admin_username=admin_username,
                    action_type="remove",
                    service_type=self.rental_type,
                    details=rental_details
                )
            print(f"{self.rental_type.capitalize()} removed successfully!")
        else:
            print(f"No {self.rental_type}s were found matching the information entered.")
        
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(rentals, f, ensure_ascii=False, indent=2)

    def update(self, admin_username=None):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                rentals = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No {self.rental_type}s found.")
            return
        
        self.display_table()
        
        if self.rental_type == 'car':
            print("Please enter the car plate of the car you want to update")
            identifier = get_valid_input("Car Plate: ").upper()
            # Find the car by plate
            key_to_update = None
            for key, car in rentals.items():
                if car['car_plate'] == identifier:
                    key_to_update = key
                    break
        else:  # hotel
            print(f"Please enter the hotel ID of the {self.rental_type} you want to update")
            identifier = get_valid_input("Hotel ID: ")
            key_to_update = identifier
        
        if key_to_update in rentals:
            old_details = rentals[key_to_update].copy()
            
            if self.rental_type == 'car':
                fields = ['brand', 'location', 'cars_available', 'price', 'car_plate']
            else:  # hotel
                fields = ['hotel_name', 'location', 'rooms_available', 'adult_price', 'child_price']
            
            print(f"\nAvailable fields to update: {', '.join(fields)}")
            field_to_update = input("Enter the field you want to change: ").lower()
            
            if field_to_update in fields:
                if field_to_update == 'car_plate':
                    while True:
                        new_value = input(f"Enter the new {field_to_update}: ").strip().upper()
                        if len(new_value) == 5 and new_value[:2].isalpha() and new_value[2:].isdigit():
                            break
                        print("Invalid car plate format. Please enter 2 letters followed by 3 digits.")
                elif field_to_update in ['price', 'cars_available', 'rooms_available', 'adult_price', 'child_price']:
                    new_value = input(f"Enter the new {field_to_update}: ")
                    rentals[key_to_update][field_to_update] = int(new_value)
                else:
                    new_value = input(f"Enter the new {field_to_update}: ")
                    rentals[key_to_update][field_to_update] = new_value

                if admin_username:
                    log_admin_action(
                        admin_username=admin_username,
                        action_type="update",
                        service_type=self.rental_type,
                        details={
                            "old_details": old_details,
                            "new_details": rentals[key_to_update],
                            "changed_field": field_to_update
                        }
                    )
                print("Changes saved!")
            else:
                print("Invalid field!")
        else:
            print(f"No {self.rental_type}s were found matching the information entered.")

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(rentals, f, ensure_ascii=False, indent=2)

    def arrangement(self, admin_username=None):
        choice = False
        while not choice:
            print(f"\n{self.rental_type.capitalize()} Management Menu:")
            print(f"1. Add a {self.rental_type}")
            print(f"2. Remove a {self.rental_type}")
            print(f"3. Update {self.rental_type} information")
            print(f"4. Display {self.rental_type}s")
            print(f"5. Go back to previous screen")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == "1":
                self.add(admin_username)
            elif choice == "2":
                self.remove(admin_username)
            elif choice == "3":
                self.update(admin_username)
            elif choice == "4":
                self.display_table()
            elif choice == "5":
                choice = True
            else:
                print("Invalid input! Please enter a number between 1 and 5.")
                choice = False
