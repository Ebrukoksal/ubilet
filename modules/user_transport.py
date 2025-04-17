import json
import random
import args
from modules.payment import process_payment
from utils import display_user_tickets

class Transport:
    def __init__(self, transport_type):
        self.transport_type = transport_type
        filename = args.TRANSPORT_TYPE2FILENAME.get(transport_type)
        self.data_file = "data/" + filename
        self.service_name = transport_type

    def display_table(self, departure, arrival, date):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                transports = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No {self.transport_type}s found.")
            return None

        if not transports:
            print(f"No {self.transport_type}s found.")
            return None

        # Filter transports based on user criteria
        matching_transports = {
            id: transport for id, transport in transports.items()
            if transport['departure'].lower() == departure.lower() and
               transport['arrival'].lower() == arrival.lower() or
               transport['date'] == date
        }  

        if not matching_transports:
            print(f"\nNo {self.transport_type}s found for the route from {departure} to {arrival} on {date}")
            return None

        # Table header
        print(f"\nAvailable {self.service_name}s:")
        print("-" * 100)
        print(f"{'No.':<5} {'Voyage Number':<15} {'Company':<10} {'From':<15} {'To':<15} {'Date':<12} {'Time':<8} {'Price':<10}")
        print("-" * 100)

        # Table rows with numbered listing
        transport_options = list(matching_transports.values())
        for idx, transport in enumerate(transport_options, 1):
            company_name = transport.get('company', 'N/A')
            print(f"{idx:<5} "
                  f"{transport['voyage_number']:<15} "
                  f"{company_name:<10} "
                  f"{transport['departure']:<15} "
                  f"{transport['arrival']:<15} "
                  f"{transport['date']:<12} "
                  f"{transport['time']:<8} "
                  f"{transport['price']:<10}")
        print("-" * 100)
        print()
        
        return transport_options

    def search(self, user):
        departure = input("From : ")
        arrival = input("To : ")
        date = input("Date : ")
        transport_options = self.display_table(departure, arrival, date)
        
        if transport_options:
            print(f"\nWould you like to book a {self.transport_type}?")
            choice = input(f"Enter {self.transport_type} number to book or 'N' to return to main menu: ")
            if choice.lower() != 'n':
                try:
                    selected_index = int(choice)
                    if 1 <= selected_index <= len(transport_options):
                        selected_transport = transport_options[selected_index - 1]
                        self.booking(selected_transport, user)
                    else:
                        print(f"Invalid {self.transport_type} number!")
                except ValueError:
                    print("Invalid input! Please enter a valid number or 'N'.")

    def booking(self, selected_transport, user):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                transports = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error accessing {self.transport_type} data.")
            return

        transport_key = None
        for key, transport in transports.items():
            if transport['voyage_number'] == selected_transport['voyage_number']:
                transport_key = key
                break

        if transport_key is None:
            print(f"{self.service_name} not found in the system.")
            return

        if 'seat_available' not in transports[transport_key]:
            transports[transport_key]['seat_available'] = 50
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(transports, f, ensure_ascii=False, indent=2)

        if transports[transport_key]['seat_available'] <= 0:
            print(f"Sorry, this {self.transport_type} is fully booked. No seats available.")
            return

        seat_number = random.randint(1, transports[transport_key]['seat_available'])

        print(f"\n{self.service_name} Details:")
        print(f"Voyage Number: {selected_transport['voyage_number']}")
        print(f"Company: {selected_transport['company']}")
        print(f"From: {selected_transport['departure']}")
        print(f"To: {selected_transport['arrival']}")
        print(f"Date: {selected_transport['date']}")
        print(f"Time: {selected_transport['time']}")
        print(f"Price: {selected_transport['price']}")
        print(f"Available Seats: {transports[transport_key]['seat_available']}")
        print(f"Your Seat Number: {seat_number}")

        confirm = input("\nWould you like to proceed with the booking? (Y/N): ")
        if confirm.lower() != 'y':
            print("Booking cancelled.")
            return

        transports[transport_key]['seat_available'] -= 1

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(transports, f, ensure_ascii=False, indent=2)

        booking_id = f"{self.transport_type.upper()}_{selected_transport['voyage_number']}_{user}"
        
        print(f"\nBooking successful! Your {self.transport_type} has been booked.")
        print(f"Booking ID: {booking_id}")
        print(f"Your Seat Number: {seat_number}")
        
        process_payment(booking_id, selected_transport['price'], self.transport_type, {
            "type": self.transport_type,
            "user": user,
            "voyage_number": selected_transport['voyage_number'],
            "company": selected_transport['company'],
            "departure": selected_transport['departure'],
            "arrival": selected_transport['arrival'],
            "date": selected_transport['date'],
            "time": selected_transport['time'],
            "seat_number": seat_number
        })
        
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
            if (payment['service_type'] == self.transport_type and
                payment['status'] == 'completed'):
                
                if 'booking_details' in payment:
                    booking_details = payment['booking_details']
                    user_bookings.append({
                        'payment_id': payment_id,
                        'booking_id': payment['booking_id'],
                        'voyage_number': booking_details['voyage_number'],
                        'company': booking_details['company'],
                        'departure': booking_details['departure'],
                        'arrival': booking_details['arrival'],
                        'date': booking_details['date'],
                        'time': booking_details['time'],
                        'seat_number': booking_details.get('seat_number', 'N/A')
                    })
                else:
                    parts = payment['booking_id'].split('_')
                    if len(parts) >= 3:
                        voyage_number = parts[1]
                        try:
                            with open(self.data_file, "r", encoding="utf-8") as f:
                                transports = json.load(f)
                                for transport in transports.values():
                                    if transport['voyage_number'] == voyage_number:
                                        user_bookings.append({
                                            'payment_id': payment_id,
                                            'booking_id': payment['booking_id'],
                                            'voyage_number': voyage_number,
                                            'company': transport['company'],
                                            'departure': transport['departure'],
                                            'arrival': transport['arrival'],
                                            'date': transport['date'],
                                            'time': transport['time'],
                                            'seat_number': 'N/A'
                                        })
                                        break
                        except (FileNotFoundError, json.JSONDecodeError):
                            print(f"Warning: Could not find {self.transport_type} details for booking {payment['booking_id']}")
                            continue

        if not user_bookings:
            print(f"You have no active {self.transport_type} bookings to cancel.")
            return

        print(f"\nYour {self.service_name} Bookings:")
        print("-" * 100)
        print(f"{'No.':<5} {'Voyage Number':<15} {'Company':<10} {'From':<15} {'To':<15} {'Date':<12} {'Time':<8} {'Seat':<8}")
        print("-" * 100)

        for idx, booking in enumerate(user_bookings, 1):
            print(f"{idx:<5} "
                  f"{booking['voyage_number']:<15} "
                  f"{booking['company']:<10} "
                  f"{booking['departure']:<15} "
                  f"{booking['arrival']:<15} "
                  f"{booking['date']:<12} "
                  f"{booking['time']:<8} "
                  f"{booking['seat_number']:<8}")
        print("-" * 100)

        try:
            choice = int(input("\nEnter the number of the booking you want to cancel (0 to go back): "))
            if choice == 0:
                return
            if not 1 <= choice <= len(user_bookings):
                print("Invalid booking number!")
                return
        except ValueError:
            print("Invalid input! Please enter a number.")
            return

        selected_booking = user_bookings[choice - 1]

        confirm = input(f"\nAre you sure you want to cancel your {self.transport_type} from {selected_booking['departure']} to {selected_booking['arrival']} on {selected_booking['date']}? (Y/N): ")
        if confirm.lower() != 'y':
            print("Cancellation cancelled.")
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                transports = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error accessing {self.transport_type} data.")
            return

        transport_updated = False
        for transport in transports.values():
            if transport['voyage_number'] == selected_booking['voyage_number']:
                transport['seat_available'] += 1
                transport_updated = True
                break

        if not transport_updated:
            print(f"Error: {self.service_name} not found in the system.")
            return

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(transports, f, ensure_ascii=False, indent=2)

        payments[selected_booking['payment_id']]['status'] = 'cancelled'

        with open("data/payments.json", "w", encoding="utf-8") as f:
            json.dump(payments, f, ensure_ascii=False, indent=2)

        print(f"\n{self.service_name} booking cancelled successfully!")
        print(f"Booking ID: {selected_booking['booking_id']}")
        print(f"Voyage Number: {selected_booking['voyage_number']}")
        print(f"Company: {selected_booking['company']}")
        print(f"From: {selected_booking['departure']}")
        print(f"To: {selected_booking['arrival']}")
        print(f"Date: {selected_booking['date']}")
        print(f"Time: {selected_booking['time']}")
        print(f"Seat Number: {selected_booking['seat_number']}")

    def arrangement(self, user):
        choice = False
        while not choice:
            choice = input(f"1 - Search for a {self.transport_type} \n"
                         f"2 - Cancel a {self.transport_type} \n"
                         f"3 - View my tickets \n"
                         f"4 - Go back \n")
            if choice == "1":
                self.search(user)
            elif choice == "2":
                self.cancel(user)
            elif choice == "3":
                display_user_tickets(user, self.transport_type)
            elif choice == "4":
                choice = True
            else:
                print("Invalid input! Please select an operation.")

    def display_voyages(self, departure, arrival, date=None):
        # Load transports from the JSON file
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                transports = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No {self.transport_type}s found.")
            return None

        if not transports:
            print(f"No {self.transport_type}s found.")
            return None

        # Filter transports based on user criteria
        relevant_transports = [
            transport for transport in transports.values()
            if transport['departure'].lower() == departure.lower() and
               transport['arrival'].lower() == arrival.lower()
        ]

        # If a date is provided, further filter the transports
        if date:
            relevant_transports = [
                transport for transport in relevant_transports
                if transport['date'] == date
            ]

        # Display the relevant transports
        if relevant_transports:
            print(f"\nAvailable {self.service_name}s:")
            print("-" * 100)
            print(f"{'No.':<5} {'Voyage Number':<15} {'Company':<10} {'From':<15} {'To':<15} {'Date':<12} {'Time':<8} {'Price':<10}")
            print("-" * 100)

            for idx, transport in enumerate(relevant_transports, 1):
                company_name = transport.get('company', 'N/A')
                print(f"{idx:<5} "
                      f"{transport['voyage_number']:<15} "
                      f"{company_name:<10} "
                      f"{transport['departure']:<15} "
                      f"{transport['arrival']:<15} "
                      f"{transport['date']:<12} "
                      f"{transport['time']:<8} "
                      f"{transport['price']:<10}")
            print("-" * 100)
            print()
            
            return relevant_transports
        else:
            print("No transports found for the given criteria.")
            return None
