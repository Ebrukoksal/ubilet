import json
import random
from modules.payment import process_payment
from utils import display_user_tickets

def user_bus_arrangement(user):
    choice = False
    while not choice:
        choice = input("1 - Search for a bus \n"
                       "2 - Cancel a bus \n"
                       "3 - View my tickets \n"
                       "4 - Go back \n")
        if choice == "1":
            user_bus_search(user)
        elif choice == "2":
            user_bus_cancel(user)
        elif choice == "3":
            display_user_tickets(user, "bus")
        elif choice == "4":
            choice = True
        else:
            print("Invalid input! Please select an operation.")


def display_buses_table(departure, arrival, date):
    try:
        with open("data/buses.json", "r", encoding="utf-8") as f:
            buses = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No buses found.")
        return None

    if not buses:
        print("No buses found.")
        return None

    # Filter flights based on user criteria
    matching_buses = {
        id: bus for id, bus in buses.items()
        if bus['departure'].lower() == departure.lower() and
           bus['arrival'].lower() == arrival.lower() or
           bus['date'] == date
    }

    if not matching_buses:
        print(f"\nNo buses found for the route from {departure} to {arrival} on {date}")
        return None

    # Table header
    print("\nAvailable Buses:")
    print("-" * 100)
    print(f"{'No.':<5} {'Voyage Number':<15} {'Company':<10} {'From':<15} {'To':<15} {'Date':<12} {'Time':<8} {'Price':<10}")
    print("-" * 100)

    # Table rows with numbered listing
    bus_options = list(matching_buses.values())
    for idx, bus in enumerate(bus_options, 1):
        print(f"{idx:<5} "
              f"{bus['voyage_number']:<15} "
              f"{bus['company']:<10} "
              f"{bus['departure']:<15} "
              f"{bus['arrival']:<15} "
              f"{bus['date']:<12} "
              f"{bus['time']:<8} "
              f"{bus['price']:<10}")
    print("-" * 100)
    print()
    
    return bus_options

def user_bus_search(user):
    departure = input("From : ")
    arrival = input("To : ")
    date = input("Date : ")
    bus_options = display_buses_table(departure, arrival, date)
    
    if bus_options:
        print("\nWould you like to book a bus?")
        choice = input("Enter bus number to book or 'N' to return to main menu: ")
        if choice.lower() != 'n':
            try:
                selected_index = int(choice)
                if 1 <= selected_index <= len(bus_options):
                    selected_bus = bus_options[selected_index - 1]
                    user_bus_booking(selected_bus, user)
                else:
                    print("Invalid bus number!")
            except ValueError:
                print("Invalid input! Please enter a valid number or 'N'.")


def user_bus_booking(selected_bus, user):
    # Load the buses data
    try:
        with open("data/buses.json", "r", encoding="utf-8") as f:
            buses = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing bus data.")
        return

    # Find the bus in the buses data using voyage number
    bus_key = None
    for key, bus in buses.items():
        if bus['voyage_number'] == selected_bus['voyage_number']:
            bus_key = key
            break

    if bus_key is None:
        print("Bus not found in the system.")
        return

    # Add seat_available field if it doesn't exist
    if 'seat_available' not in buses[bus_key]:
        buses[bus_key]['seat_available'] = 50  # Default number of seats
        # Save the updated buses data with seat_available field
        with open("data/buses.json", "w", encoding="utf-8") as f:
            json.dump(buses, f, ensure_ascii=False, indent=2)

    # Check seat availability
    if buses[bus_key]['seat_available'] <= 0:
        print("Sorry, this bus is fully booked. No seats available.")
        return

    # Assign a random seat number
    seat_number = random.randint(1, buses[bus_key]['seat_available'])

    # Confirm booking with user
    print(f"\nBus Details:")
    print(f"Voyage Number: {selected_bus['voyage_number']}")
    print(f"Company: {selected_bus['company']}")
    print(f"From: {selected_bus['departure']}")
    print(f"To: {selected_bus['arrival']}")
    print(f"Date: {selected_bus['date']}")
    print(f"Time: {selected_bus['time']}")
    print(f"Price: {selected_bus['price']}")
    print(f"Available Seats: {buses[bus_key]['seat_available']}")
    print(f"Your Seat Number: {seat_number}")

    confirm = input("\nWould you like to proceed with the booking? (Y/N): ")
    if confirm.lower() != 'y':
        print("Booking cancelled.")
        return

    # Update seat availability
    buses[bus_key]['seat_available'] -= 1

    # Save the updated buses data
    with open("data/buses.json", "w", encoding="utf-8") as f:
        json.dump(buses, f, ensure_ascii=False, indent=2)

    # Generate booking ID
    booking_id = f"BUS_{selected_bus['voyage_number']}_{user}"
    
    print("\nBooking successful! Your bus has been booked.")
    print(f"Booking ID: {booking_id}")
    print(f"Your Seat Number: {seat_number}")
    
    # Process payment and store booking information
    process_payment(booking_id, selected_bus['price'], "bus", {
        "type": "bus",
        "user": user,
        "voyage_number": selected_bus['voyage_number'],
        "departure": selected_bus['departure'],
        "arrival": selected_bus['arrival'],
        "date": selected_bus['date'],
        "time": selected_bus['time'],
        "seat_number": seat_number
    })
    
    print("\nThank you for choosing our service!")

def user_bus_cancel(user):
    # Load the payments data
    try:
        with open("data/payments.json", "r", encoding="utf-8") as f:
            payments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing payment data.")
        return

    # Find all bus bookings for the user
    user_bookings = []
    for payment_id, payment in payments.items():
        if (payment['service_type'] == 'bus' and 
            payment['customer_name'] == user and 
            payment['status'] == 'completed'):
            
            # Extract booking details, handling cases where booking_details might not exist
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
                # For older records without booking_details, extract info from booking_id
                # Format is typically: BUS_voyage_number_username
                parts = payment['booking_id'].split('_')
                if len(parts) >= 3:
                    voyage_number = parts[1]
                    # Try to find bus details from buses.json
                    try:
                        with open("data/buses.json", "r", encoding="utf-8") as f:
                            buses = json.load(f)
                            # Find bus with matching voyage number
                            for bus in buses.values():
                                if bus['voyage_number'] == voyage_number:
                                    user_bookings.append({
                                        'payment_id': payment_id,
                                        'booking_id': payment['booking_id'],
                                        'voyage_number': voyage_number,
                                        'company': bus['company'],
                                        'departure': bus['departure'],
                                        'arrival': bus['arrival'],
                                        'date': bus['date'],
                                        'time': bus['time'],
                                        'seat_number': 'N/A'  # Seat number not stored in old records
                                    })
                                    break
                    except (FileNotFoundError, json.JSONDecodeError):
                        print(f"Warning: Could not find bus details for booking {payment['booking_id']}")
                        continue

    if not user_bookings:
        print("You have no active bus bookings to cancel.")
        return

    # Display user's bookings
    print("\nYour Bus Bookings:")
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
    confirm = input(f"\nAre you sure you want to cancel your bus from {selected_booking['departure']} to {selected_booking['arrival']} on {selected_booking['date']}? (Y/N): ")
    if confirm.lower() != 'y':
        print("Cancellation cancelled.")
        return

    # Load buses data to update seat availability
    try:
        with open("data/buses.json", "r", encoding="utf-8") as f:
            buses = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing bus data.")
        return

    # Find and update the bus's seat availability
    bus_updated = False
    for bus in buses.values():
        if bus['voyage_number'] == selected_booking['voyage_number']:
            bus['seat_available'] += 1
            bus_updated = True
            break

    if not bus_updated:
        print("Error: Bus not found in the system.")
        return

    # Save updated buses data
    with open("data/buses.json", "w", encoding="utf-8") as f:
        json.dump(buses, f, ensure_ascii=False, indent=2)

    # Update payment status
    payments[selected_booking['payment_id']]['status'] = 'cancelled'

    # Save updated payments data
    with open("data/payments.json", "w", encoding="utf-8") as f:
        json.dump(payments, f, ensure_ascii=False, indent=2)

    print("\nBus booking cancelled successfully!")
    print(f"Booking ID: {selected_booking['booking_id']}")
    print(f"Voyage Number: {selected_booking['voyage_number']}")
    print(f"Company: {selected_booking['company']}")
    print(f"From: {selected_booking['departure']}")
    print(f"To: {selected_booking['arrival']}")
    print(f"Date: {selected_booking['date']}")
    print(f"Time: {selected_booking['time']}")
    print(f"Seat Number: {selected_booking['seat_number']}")



