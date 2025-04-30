import json
from utils import get_hash
from utils import get_hash_with_kwargs
from utils import get_valid_input
from modules.logger import log_admin_action

class Transport:
    def __init__(self, transport_type):
        self.transport_type = transport_type
        if transport_type == "bus":
            self.data_file = "data/buses.json"
        else:
            self.data_file = f"data/{transport_type}s.json"
        self.service_name = transport_type

    def get_voyage_number(self, company, departure, arrival, date, time):
        voyage_number = company[0].upper() + departure[0].upper() + arrival[0].upper()
        voyage_number += date.replace("/", "")
        voyage_number += time.replace(":", "")
        return voyage_number

    def add(self, admin_username=None):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                transports = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            transports = {}

        company = get_valid_input("Company: ").lower()
        departure = get_valid_input("Departure: ").lower()
        arrival = get_valid_input("Arrival: ").lower()
        date = get_valid_input("Date: ")
        time = get_valid_input("Time: ")
        seats_available = get_valid_input("Seats Available: ", is_price=True)
        price = get_valid_input("Price: ", is_price=True)

        hashed_id = get_hash(company, departure, arrival, date, time, price)
        voyage_number = self.get_voyage_number(company, departure, arrival, date, time)

        transports[hashed_id] = {
            "voyage_number": voyage_number,
            "company": company,
            "departure": departure,
            "arrival": arrival,
            "date": date,
            "time": time,
            "seats_available": int(seats_available),
            "price": int(price)
        }

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(transports, f, ensure_ascii=False, indent=2)
        
        if admin_username:
            log_admin_action(
                admin_username=admin_username,
                action_type="add",
                service_type=self.transport_type,
                details=transports[hashed_id]
            )
        print("Changes saved!")

    def display_table(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                transports = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No {self.transport_type}s found.")
            return

        if not transports:
            print(f"No {self.transport_type}s found.")
            return

        print(f"\nExisting {self.transport_type.capitalize()}s:")
        print("-" * 100)
        print(f"{'Voyage Number':<15} {'Company':<10} {'From':<15} {'To':<15} {'Date':<12} {'Time':<8} {'Seats Available':<10} {'Price':<10}")
        print("-" * 100)

        for transport in transports.values():
            # Handle both seat_available and seats_available field names
            seats = transport.get('seats_available', transport.get('seat_available', 0))
            print(f"{transport['voyage_number']:<15} "
                  f"{transport['company']:<10} "
                  f"{transport['departure']:<15} "
                  f"{transport['arrival']:<15} "
                  f"{transport['date']:<12} "
                  f"{transport['time']:<8} "
                  f"{seats:<10} "
                  f"{transport['price']:<10}")
        print("-" * 100)
        print()

    def remove(self, admin_username=None):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                transports = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No {self.transport_type}s found.")
            return
        
        self.display_table()
        print(f"Please enter the voyage number of the {self.transport_type} you want to remove")
        voyage_number = get_valid_input("Voyage Number: ")
        
        key_to_remove = None
        transport_details = None
        for key, transport in transports.items():
            if transport["voyage_number"] == voyage_number:
                key_to_remove = key
                transport_details = transport
                break

        if key_to_remove in transports:
            del transports[key_to_remove]
            if admin_username and transport_details:
                log_admin_action(
                    admin_username=admin_username,
                    action_type="remove",
                    service_type=self.transport_type,
                    details=transport_details
                )
            print(f"{self.transport_type.capitalize()} removed successfully!")
        else:
            print(f"No {self.transport_type}s were found matching the information entered.")
        
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(transports, f, ensure_ascii=False, indent=2)

    def update(self, admin_username=None):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                transports = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No {self.transport_type}s found.")
            return
        
        self.display_table()
        print(f"Please enter the voyage number of the {self.transport_type} you want to update")
        voyage_number = get_valid_input("Voyage Number: ")
        
        key_to_update = None
        for key, transport in transports.items():
            if transport["voyage_number"] == voyage_number:
                key_to_update = key
                break

        if key_to_update in transports:
            old_details = transports[key_to_update].copy()
            field_to_update = input("Enter the detail you want to change (company/departure/arrival/date/time/seats_available/price): ").lower()
            new_value = input(f"Enter the new {field_to_update}: ")
            
            if field_to_update in ["price", "seats_available"]:
                transports[key_to_update][field_to_update] = int(new_value)
            else:
                transports[key_to_update][field_to_update] = new_value.lower()

            updated_voyage_number = self.get_voyage_number(
                transports[key_to_update]["company"],
                transports[key_to_update]["departure"],
                transports[key_to_update]["arrival"],
                transports[key_to_update]["date"],
                transports[key_to_update]["time"]
            )

            new_key = get_hash_with_kwargs(**transports[key_to_update])
            transports[new_key] = transports[key_to_update].copy()
            transports[new_key]["voyage_number"] = updated_voyage_number
            del transports[key_to_update]

            if admin_username:
                log_admin_action(
                    admin_username=admin_username,
                    action_type="update",
                    service_type=self.transport_type,
                    details={
                        "old_details": old_details,
                        "new_details": transports[new_key],
                        "changed_field": field_to_update
                    }
                )
            print("Changes saved!")
        else:
            print(f"No {self.transport_type}s were found matching the information entered.")

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(transports, f, ensure_ascii=False, indent=2)

    def arrangement(self, admin_username=None):
        choice = False
        while not choice:
            print(f"\n{self.transport_type.capitalize()} Management Menu:")
            print(f"1. Add a {self.transport_type}")
            print(f"2. Remove a {self.transport_type}")
            print(f"3. Update {self.transport_type} information")
            print(f"4. Display {self.transport_type}s")
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
