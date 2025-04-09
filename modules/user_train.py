import json
import random
from modules.payment import process_payment
from utils import display_user_tickets

def user_train_arrangement(user):
    choice = False
    while not choice:
        choice = input("1 - Search for a train \n"
                       "2 - Cancel a train \n"
                       "3 - View my tickets \n"
                       "4 - Go back \n")
        if choice == "1":
            user_train_search(user)
        elif choice == "2":
            user_train_cancel(user)
        elif choice == "3":
            display_user_tickets(user, "train")
        elif choice == "4":
            choice = True
        else:
            print("Invalid input! Please select an operation.")


def user_train_search(user):
    departure = input("From : ")
    arrival = input("To : ")
    date = input("Date : ")
    train_options = display_trains_table(departure, arrival, date)
    
    if train_options:
        print("\nWould you like to book a train?")
        choice = input("Enter train number to book or 'N' to return to main menu: ")
        if choice.lower() != 'n':
            try:
                selected_index = int(choice)
                if 1 <= selected_index <= len(train_options):
                    selected_train = train_options[selected_index - 1]
                    user_train_booking(selected_train, user)
                else:
                    print("Invalid train number!")
            except ValueError:
                print("Invalid input! Please enter a valid number or 'N'.")

def display_trains_table(departure, arrival, date):
    try:
        with open("data/trains.json", "r", encoding="utf-8") as f:
            trains = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No trains found.")
        return None

    if not trains:
        print("No trains found.")
        return None

    # Filter trains based on user criteria
    matching_trains = {
        id: train for id, train in trains.items()
        if train['departure'].lower() == departure.lower() and
           train['arrival'].lower() == arrival.lower() or
           train['date'] == date
    }

    if not matching_trains:
        print(f"\nNo trains found for the route from {departure} to {arrival} on {date}")
        return None

    # Table header
    print("\nAvailable Trains:")
    print("-" * 100)
    print(f"{'No.':<5} {'Voyage Number':<15} {'Company':<10} {'From':<15} {'To':<15} {'Date':<12} {'Time':<8} {'Price':<10}")
    print("-" * 100)

    # Table rows with numbered listing
    train_options = list(matching_trains.values())
    for idx, train in enumerate(train_options, 1):
        print(f"{idx:<5} "
              f"{train['voyage_number']:<15} "
              f"{train['company']:<10} "
              f"{train['departure']:<15} "
              f"{train['arrival']:<15} "
              f"{train['date']:<12} "
              f"{train['time']:<8} "
              f"{train['price']:<10} ")
    print("-" * 100)
    print()
    
    return train_options

def user_train_booking(selected_train, user):
    # Load the trains data
    try:
        with open("data/trains.json", "r", encoding="utf-8") as f:
            trains = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing train data.")
        return

    # Find the train in the trains data using voyage number
    train_key = None
    for key, train in trains.items():
        if train['voyage_number'] == selected_train['voyage_number']:
            train_key = key
            break

    if train_key is None:
        print("Train not found in the system.")
        return

    # Add seat_available field if it doesn't exist
    if 'seat_available' not in trains[train_key]:
        trains[train_key]['seat_available'] = 50  # Default number of seats
        # Save the updated trains data with seat_available field
        with open("data/trains.json", "w", encoding="utf-8") as f:
            json.dump(trains, f, ensure_ascii=False, indent=2)

    # Check seat availability
    if trains[train_key]['seat_available'] <= 0:
        print("Sorry, this train is fully booked. No seats available.")
        return

    # Assign a random seat number
    seat_number = random.randint(1, trains[train_key]['seat_available'])

    # Confirm booking with user
    print(f"\nTrain Details:")
    print(f"Voyage Number: {selected_train['voyage_number']}")
    print(f"Company: {selected_train['company']}")
    print(f"From: {selected_train['departure']}")
    print(f"To: {selected_train['arrival']}")
    print(f"Date: {selected_train['date']}")
    print(f"Time: {selected_train['time']}")
    print(f"Price: {selected_train['price']}")
    print(f"Available Seats: {trains[train_key]['seat_available']}")
    print(f"Your Seat Number: {seat_number}")

    confirm = input("\nWould you like to proceed with the booking? (Y/N): ")
    if confirm.lower() != 'y':
        print("Booking cancelled.")
        return

    # Update seat availability
    trains[train_key]['seat_available'] -= 1

    # Save the updated trains data
    with open("data/trains.json", "w", encoding="utf-8") as f:
        json.dump(trains, f, ensure_ascii=False, indent=2)

    # Generate booking ID
    booking_id = f"TRAIN_{selected_train['voyage_number']}_{user}"
    
    print("\nBooking successful! Your train has been booked.")
    print(f"Booking ID: {booking_id}")
    print(f"Your Seat Number: {seat_number}")
    
    # Process payment and store booking information
    process_payment(booking_id, selected_train['price'], "train", {
        "type": "train",
        "user": user,
        "voyage_number": selected_train['voyage_number'],
        "company": selected_train['company'],
        "departure": selected_train['departure'],
        "arrival": selected_train['arrival'],
        "date": selected_train['date'],
        "time": selected_train['time'],
        "seat_number": seat_number
    })
    
    print("\nThank you for choosing our service!")


def user_train_cancel(user):
    # Load the payments data
    try:
        with open("data/payments.json", "r", encoding="utf-8") as f:
            payments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing payment data.")
        return

    # Find all train bookings for the user
    user_bookings = []
    for payment_id, payment in payments.items():
        if (payment['service_type'] == 'train' and 
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
                # Format is typically: TRAIN_voyage_number_username
                parts = payment['booking_id'].split('_')
                if len(parts) >= 3:
                    voyage_number = parts[1]
                    # Try to find train details from trains.json
                    try:
                        with open("data/trains.json", "r", encoding="utf-8") as f:
                            trains = json.load(f)
                            # Find train with matching voyage number
                            for train in trains.values():
                                if train['voyage_number'] == voyage_number:
                                    user_bookings.append({
                                        'payment_id': payment_id,
                                        'booking_id': payment['booking_id'],
                                        'voyage_number': voyage_number,
                                        'company': train['company'],
                                        'departure': train['departure'],
                                        'arrival': train['arrival'],
                                        'date': train['date'],
                                        'time': train['time'],
                                        'seat_number': 'N/A'  # Seat number not stored in old records
                                    })
                                    break
                    except (FileNotFoundError, json.JSONDecodeError):
                        print(f"Warning: Could not find train details for booking {payment['booking_id']}")
                        continue

    if not user_bookings:
        print("You have no active train bookings to cancel.")
        return

    # Display user's bookings
    print("\nYour Train Bookings:")
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
    confirm = input(f"\nAre you sure you want to cancel your train from {selected_booking['departure']} to {selected_booking['arrival']} on {selected_booking['date']}? (Y/N): ")
    if confirm.lower() != 'y':
        print("Cancellation cancelled.")
        return

    # Load trains data to update seat availability
    try:
        with open("data/trains.json", "r", encoding="utf-8") as f:
            trains = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing train data.")
        return

    # Find and update the train's seat availability
    train_updated = False
    for train in trains.values():
        if train['voyage_number'] == selected_booking['voyage_number']:
            train['seat_available'] += 1
            train_updated = True
            break

    if not train_updated:
        print("Error: Train not found in the system.")
        return

    # Save updated trains data
    with open("data/trains.json", "w", encoding="utf-8") as f:
        json.dump(trains, f, ensure_ascii=False, indent=2)

    # Update payment status
    payments[selected_booking['payment_id']]['status'] = 'cancelled'

    # Save updated payments data
    with open("data/payments.json", "w", encoding="utf-8") as f:
        json.dump(payments, f, ensure_ascii=False, indent=2)

    print("\nTrain booking cancelled successfully!")
    print(f"Booking ID: {selected_booking['booking_id']}")
    print(f"Voyage Number: {selected_booking['voyage_number']}")
    print(f"Company: {selected_booking['company']}")
    print(f"From: {selected_booking['departure']}")
    print(f"To: {selected_booking['arrival']}")
    print(f"Date: {selected_booking['date']}")
    print(f"Time: {selected_booking['time']}")
    print(f"Seat Number: {selected_booking['seat_number']}")



