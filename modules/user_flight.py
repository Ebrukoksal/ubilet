import json
import random
from modules.payment import process_payment
from utils import display_user_tickets

def user_flight_arrangement(user):
    choice = False
    while not choice:
        choice = input("1 - Search for a flight \n"
                       "2 - Cancel a flight \n"
                       "3 - View my tickets \n"
                       "4 - Go back \n")
        if choice == "1":
            user_flight_search(user)
        elif choice == "2":
            user_flight_cancel(user)
        elif choice == "3":
            display_user_tickets(user, service_type='flight')
        elif choice == "4":
            choice = True
        else:
            print("Invalid input! Please select an operation.")

def display_flights_table(departure, arrival, date):
    try:
        with open("data/flights.json", "r", encoding="utf-8") as f:
            flights = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No flights found.")
        return None

    if not flights:
        print("No flights found.")
        return None

    # Filter flights based on user criteria
    matching_flights = {
        id: flight for id, flight in flights.items()
        if flight['departure'].lower() == departure.lower() and
           flight['arrival'].lower() == arrival.lower() or
           flight['date'] == date
    }

    if not matching_flights:
        print(f"\nNo flights found for the route from {departure} to {arrival} on {date}")
        return None

    # Table header
    print("\nAvailable Flights:")
    print("-" * 100)
    print(f"{'No.':<5} {'Voyage Number':<15} {'Airline':<10} {'From':<15} {'To':<15} {'Date':<12} {'Time':<8} {'Price':<10}")
    print("-" * 100)

    # Table rows with numbered listing
    flight_options = list(matching_flights.values())
    for idx, flight in enumerate(flight_options, 1):
        print(f"{idx:<5} "
              f"{flight['voyage_number']:<15} "
              f"{flight['airline']:<10} "
              f"{flight['departure']:<15} "
              f"{flight['arrival']:<15} "
              f"{flight['date']:<12} "
              f"{flight['time']:<8} "
              f"{flight['price']:<10}")
    print("-" * 100)
    print()
    
    return flight_options

def user_flight_search(user):
    departure = input("From : ")
    arrival = input("To : ")
    date = input("Date : ")
    flight_options = display_flights_table(departure, arrival, date)
    
    if flight_options:
        print("\nWould you like to book a flight?")
        choice = input("Enter flight number to book or 'N' to return to main menu: ")
        if choice.lower() != 'n':
            try:
                selected_index = int(choice)
                if 1 <= selected_index <= len(flight_options):
                    selected_flight = flight_options[selected_index - 1]
                    user_flight_booking(selected_flight, user)
                else:
                    print("Invalid flight number!")
            except ValueError:
                print("Invalid input! Please enter a valid number or 'N'.")

def user_flight_booking(selected_flight, user):
    # Load the flights data
    try:
        with open("data/flights.json", "r", encoding="utf-8") as f:
            flights = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing flight data.")
        return

    # Find the flight in the flights data using voyage number
    flight_key = None
    for key, flight in flights.items():
        if flight['voyage_number'] == selected_flight['voyage_number']:
            flight_key = key
            break

    if flight_key is None:
        print("Flight not found in the system.")
        return

    # Add seat_available field if it doesn't exist
    if 'seat_available' not in flights[flight_key]:
        flights[flight_key]['seat_available'] = 50  # Default number of seats
        # Save the updated flights data with seat_available field
        with open("data/flights.json", "w", encoding="utf-8") as f:
            json.dump(flights, f, ensure_ascii=False, indent=2)

    # Check seat availability
    if flights[flight_key]['seat_available'] <= 0:
        print("Sorry, this flight is fully booked. No seats available.")
        return

    # Assign a random seat number
    seat_number = random.randint(1, flights[flight_key]['seat_available'])

    # Confirm booking with user
    print(f"\nFlight Details:")
    print(f"Voyage Number: {selected_flight['voyage_number']}")
    print(f"From: {selected_flight['departure']}")
    print(f"To: {selected_flight['arrival']}")
    print(f"Date: {selected_flight['date']}")
    print(f"Time: {selected_flight['time']}")
    print(f"Price: {selected_flight['price']}")
    print(f"Available Seats: {flights[flight_key]['seat_available']}")
    print(f"Your Seat Number: {seat_number}")

    confirm = input("\nWould you like to proceed with the booking? (Y/N): ")
    if confirm.lower() != 'y':
        print("Booking cancelled.")
        return

    # Update seat availability
    flights[flight_key]['seat_available'] -= 1

    # Save the updated flights data
    with open("data/flights.json", "w", encoding="utf-8") as f:
        json.dump(flights, f, ensure_ascii=False, indent=2)

    # Generate booking ID
    booking_id = f"FLIGHT_{selected_flight['voyage_number']}_{user}"
    
    print("\nBooking successful! Your flight has been booked.")
    print(f"Booking ID: {booking_id}")
    print(f"Your Seat Number: {seat_number}")
    
    # Process payment and store booking information
    process_payment(booking_id, selected_flight['price'], "flight", {
        "type": "flight",
        "user": user,
        "voyage_number": selected_flight['voyage_number'],
        "departure": selected_flight['departure'],
        "arrival": selected_flight['arrival'],
        "date": selected_flight['date'],
        "time": selected_flight['time'],
        "seat_number": seat_number
    })
    
    print("\nThank you for choosing our service!")

def user_flight_cancel(user):
    # Load the payments data
    try:
        with open("data/payments.json", "r", encoding="utf-8") as f:
            payments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing payment data.")
        return

    # Find all flight bookings for the user
    user_bookings = []
    for payment_id, payment in payments.items():
        if (payment['service_type'] == 'flight' and 
            payment['customer_name'] == user and 
            payment['status'] == 'completed'):
            
            # Extract booking details, handling cases where booking_details might not exist
            if 'booking_details' in payment:
                booking_details = payment['booking_details']
                user_bookings.append({
                    'payment_id': payment_id,
                    'booking_id': payment['booking_id'],
                    'voyage_number': booking_details['voyage_number'],
                    'departure': booking_details['departure'],
                    'arrival': booking_details['arrival'],
                    'date': booking_details['date'],
                    'time': booking_details['time'],
                    'seat_number': booking_details.get('seat_number', 'N/A')
                })
            else:
                # For older records without booking_details, extract info from booking_id
                # Format is typically: FLIGHT_voyage_number_username
                parts = payment['booking_id'].split('_')
                if len(parts) >= 3:
                    voyage_number = parts[1]
                    # Try to find flight details from flights.json
                    try:
                        with open("data/flights.json", "r", encoding="utf-8") as f:
                            flights = json.load(f)
                            # Find flight with matching voyage number
                            for flight in flights.values():
                                if flight['voyage_number'] == voyage_number:
                                    user_bookings.append({
                                        'payment_id': payment_id,
                                        'booking_id': payment['booking_id'],
                                        'voyage_number': voyage_number,
                                        'departure': flight['departure'],
                                        'arrival': flight['arrival'],
                                        'date': flight['date'],
                                        'time': flight['time'],
                                        'seat_number': 'N/A'  # Seat number not stored in old records
                                    })
                                    break
                    except (FileNotFoundError, json.JSONDecodeError):
                        print(f"Warning: Could not find flight details for booking {payment['booking_id']}")
                        continue

    if not user_bookings:
        print("You have no active flight bookings to cancel.")
        return

    # Display user's bookings
    print("\nYour Flight Bookings:")
    print("-" * 100)
    print(f"{'No.':<5} {'Voyage Number':<15} {'From':<15} {'To':<15} {'Date':<12} {'Time':<8} {'Seat':<8}")
    print("-" * 100)

    for idx, booking in enumerate(user_bookings, 1):
        print(f"{idx:<5} "
              f"{booking['voyage_number']:<15} "
              f"{booking['departure']:<15} "
              f"{booking['arrival']:<15} "
              f"{booking['date']:<12} "
              f"{booking['time']:<8} "
              f"{booking['seat_number']:<8}")
    print("-" * 100)

    # Get user's choice
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

    # Confirm cancellation
    confirm = input(f"\nAre you sure you want to cancel your flight from {selected_booking['departure']} to {selected_booking['arrival']} on {selected_booking['date']}? (Y/N): ")
    if confirm.lower() != 'y':
        print("Cancellation cancelled.")
        return

    # Load flights data to update seat availability
    try:
        with open("data/flights.json", "r", encoding="utf-8") as f:
            flights = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing flight data.")
        return

    # Find and update the flight's seat availability
    flight_updated = False
    for flight in flights.values():
        if flight['voyage_number'] == selected_booking['voyage_number']:
            flight['seat_available'] += 1
            flight_updated = True
            break

    if not flight_updated:
        print("Error: Flight not found in the system.")
        return

    # Save updated flights data
    with open("data/flights.json", "w", encoding="utf-8") as f:
        json.dump(flights, f, ensure_ascii=False, indent=2)

    # Update payment status
    payments[selected_booking['payment_id']]['status'] = 'cancelled'

    # Save updated payments data
    with open("data/payments.json", "w", encoding="utf-8") as f:
        json.dump(payments, f, ensure_ascii=False, indent=2)

    print("\nFlight booking cancelled successfully!")
    print(f"Booking ID: {selected_booking['booking_id']}")
    print(f"Voyage Number: {selected_booking['voyage_number']}")
    print(f"From: {selected_booking['departure']}")
    print(f"To: {selected_booking['arrival']}")
    print(f"Date: {selected_booking['date']}")
    print(f"Time: {selected_booking['time']}")
    print(f"Seat Number: {selected_booking['seat_number']}")


