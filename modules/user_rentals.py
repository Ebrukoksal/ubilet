import json
import args
from modules.payment import process_payment
from utils import display_user_tickets
from datetime import datetime

class Rental:
    def __init__(self, rental_type):
        self.rental_type = rental_type
        filename = args.RENTAL_TYPE2FILENAME.get(rental_type)
        self.data_file = "data/" + filename
        self.service_name = rental_type

    def display_table(self, location, date=None):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                rentals = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No {self.rental_type}s found.")
            return None

        if not rentals:
            print(f"No {self.rental_type}s found.")
            return None

        # Filter rentals based on criteria - date is ignored for cars
        if self.rental_type == 'car':
            matching_rentals = {
                id: rental for id, rental in rentals.items()
                if rental['location'].lower() == location.lower()
            }
        else:  # hotel
            matching_rentals = {
                id: rental for id, rental in rentals.items()
                if rental['location'].lower() == location.lower()
            }

        if not matching_rentals:
            print(f"\nNo {self.rental_type}s found in {location}")
            return None

        # Different display formats for car and hotel
        if self.rental_type == 'car':
            # Table header for cars
            print("\nAvailable Cars:")
            print("-" * 100)
            print(f"{'No.':<5} {'Car ID':<15} {'Brand':<10} {'Location':<15} {'Price/Day':<10}")
            print("-" * 100)

            # Table rows with numbered listing
            rental_options = list(matching_rentals.values())
            for idx, car in enumerate(rental_options, 1):
                print(f"{idx:<5} "
                      f"{car['car_id']:<15} "
                      f"{car['brand']:<10} "
                      f"{car['location']:<15} "
                      f"{car['price']:<10}")
        elif self.rental_type == 'hotel':
            # Table header for hotels
            print("\nAvailable Hotels:")
            print("-" * 100)
            print(f"{'No.':<5} {'Hotel ID':<15} {'Name':<20} {'Location':<15} {'Rooms':<10} {'Adult Price':<15} {'Child Price':<15}")
            print("-" * 100)

            # Table rows with numbered listing
            rental_options = list(matching_rentals.values())
            for idx, hotel in enumerate(rental_options, 1):
                print(f"{idx:<5} "
                      f"{hotel['hotel_id']:<15} "
                      f"{hotel['hotel_name']:<20} "
                      f"{hotel['location']:<15} "
                      f"{hotel['rooms_available']:<10} "
                      f"{hotel['adult_price']:<15} "
                      f"{hotel['child_price']:<15}")
        
        print("-" * 100)
        print()
        
        return rental_options

    def search(self, user):
        location = input("Location: ")
        
        # Only ask for date for hotels, not for cars
        date = None
        if self.rental_type == 'hotel':
            # For hotels, we don't need date as it's not in the data structure
            pass
            
        rental_options = self.display_table(location, date if date else None)
        
        if rental_options:
            print(f"\nWould you like to book a {self.rental_type}?")
            choice = input(f"Enter {self.rental_type} number to book or 'N' to return to main menu: ")
            if choice.lower() != 'n':
                try:
                    selected_index = int(choice)
                    if 1 <= selected_index <= len(rental_options):
                        selected_rental = rental_options[selected_index - 1]
                        self.booking(selected_rental, user)
                    else:
                        print(f"Invalid {self.rental_type} number!")
                except ValueError:
                    print("Invalid input! Please enter a valid number or 'N'.")

    def booking(self, selected_rental, user):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                rentals = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error accessing {self.rental_type} data.")
            return

        rental_key = None
        for key, rental in rentals.items():
            if rental[f'{self.rental_type}_id'] == selected_rental[f'{self.rental_type}_id']:
                rental_key = key
                break

        if rental_key is None:
            print(f"{self.service_name.capitalize()} not found in the system.")
            return

        # For cars, get rental and return dates
        rental_date = None
        return_date = None
        days = 1
        
        if self.rental_type == 'car':
            total_price = selected_rental['price']
            rental_date = input("Enter Rental Date (DD/MM/YYYY): ")
            return_date = input("Enter Return Date (DD/MM/YYYY): ")
            
            # Calculate the number of days between rental and return dates
            try:
                rental_datetime = datetime.strptime(rental_date, "%d/%m/%Y")
                return_datetime = datetime.strptime(return_date, "%d/%m/%Y")
                days = (return_datetime - rental_datetime).days
                if days <= 0:
                    print("Return date must be after rental date.")
                    return
                
                # Calculate total price based on number of days
                total_price = days * selected_rental['price']
            except ValueError:
                print("Invalid date format. Please use DD/MM/YYYY.")
                return
        elif self.rental_type == 'hotel':
            # For hotels, get number of adults and children to calculate price
            try:
                adults = int(input("Number of adults: "))
                children = int(input("Number of children: "))
                rooms = int(input("Number of rooms: "))
                
                if adults < 1 or rooms < 1 or rooms > int(selected_rental['rooms_available']):
                    print("Invalid number of adults or rooms.")
                    return
                
                # Calculate total price based on number of adults and children
                total_price = (adults * float(selected_rental['adult_price']) + 
                              children * float(selected_rental['child_price'])) * rooms
            except ValueError:
                print("Invalid input! Please enter valid numbers.")
                return

        # Display rental details based on type
        if self.rental_type == 'car':
            print(f"\nCar Details:")
            print(f"Brand: {selected_rental['brand']}")
            print(f"Location: {selected_rental['location']}")
            print(f"Rental Date: {rental_date}")
            print(f"Return Date: {return_date}")
            print(f"Number of Days: {days}")
            print(f"Price per Day: {selected_rental['price']}")
            print(f"Total Price: {total_price}")
        elif self.rental_type == 'hotel':
            print(f"\nHotel Details:")
            print(f"Name: {selected_rental['hotel_name']}")
            print(f"Location: {selected_rental['location']}")
            print(f"Rooms Available: {selected_rental['rooms_available']}")
            print(f"Adults: {adults}")
            print(f"Children: {children}")
            print(f"Rooms Booked: {rooms}")
            print(f"Adult Price: {selected_rental['adult_price']}")
            print(f"Child Price: {selected_rental['child_price']}")
            print(f"Total Price: {total_price}")

        confirm = input(f"\nWould you like to proceed with the booking? (Y/N): ")
        if confirm.lower() != 'y':
            print("Booking cancelled.")
            return
            
        # For hotels, collect guest information after confirmation
        if self.rental_type == 'hotel':
            print("\nPlease provide guest information:")
            adult_guests = []
            child_guests = []
            
            # Collect adult information
            print("\n--- Adult Guests ---")
            for i in range(adults):
                print(f"\nAdult #{i+1}:")
                name = input("Name: ")
                surname = input("Surname: ")
                id_number = input("Identification Number: ")
                adult_guests.append({
                    "name": name,
                    "surname": surname,
                    "id_number": id_number
                })
                
            # Collect child information
            if children > 0:
                print("\n--- Child Guests ---")
                for i in range(children):
                    print(f"\nChild #{i+1}:")
                    name = input("Name: ")
                    surname = input("Surname: ")
                    id_number = input("Identification Number: ")
                    child_guests.append({
                        "name": name,
                        "surname": surname,
                        "id_number": id_number
                    })
            
            # Store guest information in booking details
            booking_details = selected_rental.copy()
            booking_details["user"] = user
            booking_details["adults"] = adults
            booking_details["children"] = children
            booking_details["rooms_booked"] = rooms
            booking_details["total_price"] = total_price
            booking_details["adult_guests"] = adult_guests
            booking_details["child_guests"] = child_guests
        else:
            # For car rentals, just copy the existing data
            booking_details = selected_rental.copy()
            booking_details["user"] = user
            
            if self.rental_type == 'car':
                booking_details["rental_date"] = rental_date
                booking_details["return_date"] = return_date
                booking_details["days"] = days
                booking_details["total_price"] = total_price

        # Generate booking ID
        booking_id = f"{self.rental_type.upper()}_{selected_rental[f'{self.rental_type}_id']}_{user}"
        
        print(f"\nBooking successful! Your {self.rental_type} has been booked.")
        print(f"Booking ID: {booking_id}")
        
        # Process payment
        process_payment(booking_id, total_price, self.rental_type, booking_details)
        
        print("\nThank you for choosing our service!")

    def cancel(self, user):
        try:
            with open("data/payments.json", "r", encoding="utf-8") as f:
                payments = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error accessing payment data.")
            return

        user_bookings = []
        for payment_id, payment in payments.items():
            if (payment['service_type'] == self.rental_type and 
                payment['customer_name'] == user and 
                payment['status'] == 'completed'):
                
                if 'booking_details' in payment:
                    booking_details = payment['booking_details']
                    booking_entry = {
                        'payment_id': payment_id,
                        'booking_id': payment['booking_id'],
                        'rental_id': booking_details[f'{self.rental_type}_id'],
                        'location': booking_details['location'],
                        'price': payment['amount']
                    }
                    
                    if self.rental_type == 'car':
                        booking_entry['name'] = booking_details.get('brand', 'N/A')
                        booking_entry['rental_date'] = booking_details.get('rental_date', 'N/A')
                        booking_entry['return_date'] = booking_details.get('return_date', 'N/A')
                        booking_entry['days'] = booking_details.get('days', 1)
                    else: # hotel
                        booking_entry['name'] = booking_details.get('hotel_name', 'N/A')
                        booking_entry['adults'] = booking_details.get('adults', 'N/A')
                        booking_entry['children'] = booking_details.get('children', 'N/A')
                        booking_entry['rooms_booked'] = booking_details.get('rooms_booked', 'N/A')
                        booking_entry['rooms_available'] = booking_details.get('rooms_available', 'N/A')
                        booking_entry['adult_price'] = booking_details.get('adult_price', 'N/A')
                        booking_entry['child_price'] = booking_details.get('child_price', 'N/A')
                        # Copy guest information if available
                        if 'adult_guests' in booking_details:
                            booking_entry['adult_guests'] = booking_details['adult_guests']
                        if 'child_guests' in booking_details:
                            booking_entry['child_guests'] = booking_details['child_guests']
                    
                    user_bookings.append(booking_entry)

        if not user_bookings:
            print(f"You have no active {self.rental_type} bookings to cancel.")
            return

        # Display user's bookings
        print(f"\nYour {self.service_name.capitalize()} Bookings:")
        print("-" * 100)
        
        if self.rental_type == 'car':
            print(f"{'No.':<5} {'ID':<15} {'Brand':<15} {'Location':<15} {'Rental Date':<12} {'Return Date':<12} {'Days':<8} {'Total':<10}")
            print("-" * 100)
            for idx, booking in enumerate(user_bookings, 1):
                print(f"{idx:<5} "
                      f"{booking['rental_id']:<15} "
                      f"{booking['name']:<15} "
                      f"{booking['location']:<15} "
                      f"{booking['rental_date']:<12} "
                      f"{booking['return_date']:<12} "
                      f"{booking['days']:<8} "
                      f"{booking['price']:<10}")
        elif self.rental_type == 'hotel':
            print(f"{'No.':<5} {'ID':<15} {'Name':<20} {'Location':<15} {'Price':<10}")
            print("-" * 100)
            for idx, booking in enumerate(user_bookings, 1):
                print(f"{idx:<5} "
                      f"{booking['rental_id']:<15} "
                      f"{booking['name']:<20} "
                      f"{booking['location']:<15} "
                      f"{booking['price']:<10}")
        
        print("-" * 100)

        # Get user's choice
        try:
            choice = int(input(f"\nEnter the number of the {self.rental_type} booking you want to cancel (0 to go back): "))
            if choice == 0:
                return
            if not 1 <= choice <= len(user_bookings):
                print("Invalid booking number!")
                return
        except ValueError:
            print("Invalid input! Please enter a number.")
            return

        selected_booking = user_bookings[choice - 1]

        # Confirm cancellation
        confirm = input(f"\nAre you sure you want to cancel this {self.rental_type} booking? (Y/N): ")
        if confirm.lower() != 'y':
            print("Cancellation cancelled.")
            return

        # Update payment status
        payments[selected_booking['payment_id']]['status'] = 'cancelled'

        # Save updated payments data
        with open("data/payments.json", "w", encoding="utf-8") as f:
            json.dump(payments, f, ensure_ascii=False, indent=2)

        print(f"\n{self.service_name.capitalize()} booking cancelled successfully!")
        print(f"Booking ID: {selected_booking['booking_id']}")
        print(f"Rental ID: {selected_booking['rental_id']}")
        print(f"Name: {selected_booking['name']}")
        
        if self.rental_type == 'car':
            print(f"Location: {selected_booking['location']}")
            print(f"Rental Date: {selected_booking['rental_date']}")
            print(f"Return Date: {selected_booking['return_date']}")
            print(f"Number of Days: {selected_booking['days']}")
            print(f"Total Price: {selected_booking['price']}")
        else:
            print(f"Location: {selected_booking['location']}")
            print(f"Rooms Available: {selected_booking['rooms_available']}")
            print(f"Adults: {selected_booking.get('adults', 'N/A')}")
            print(f"Children: {selected_booking.get('children', 'N/A')}")
            print(f"Rooms Booked: {selected_booking.get('rooms_booked', 'N/A')}")
            print(f"Adult Price: {selected_booking.get('adult_price', 'N/A')}")
            print(f"Child Price: {selected_booking.get('child_price', 'N/A')}")
            
            # Display guest information if available
            if 'adult_guests' in selected_booking:
                print("\nAdult Guests:")
                for i, guest in enumerate(selected_booking['adult_guests'], 1):
                    print(f"  Adult #{i}: {guest.get('name', 'N/A')} {guest.get('surname', 'N/A')} - ID: {guest.get('id_number', 'N/A')}")
            
            if 'child_guests' in selected_booking and selected_booking['child_guests']:
                print("\nChild Guests:")
                for i, guest in enumerate(selected_booking['child_guests'], 1):
                    print(f"  Child #{i}: {guest.get('name', 'N/A')} {guest.get('surname', 'N/A')} - ID: {guest.get('id_number', 'N/A')}")

    def arrangement(self, user):
        choice = False
        while not choice:
            choice = input(f"1 - Search for a {self.rental_type} \n"
                         f"2 - Cancel a {self.rental_type} booking \n"
                         f"3 - View my tickets \n"
                         f"4 - Go back \n")
            if choice == "1":
                self.search(user)
            elif choice == "2":
                self.cancel(user)
            elif choice == "3":
                display_user_tickets(user, self.rental_type)
            elif choice == "4":
                choice = True
            else:
                print("Invalid input! Please select an operation.")



