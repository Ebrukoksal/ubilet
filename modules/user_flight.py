import json
import random
from modules.payment import process_payment

def user_flight_arrangement(user):
    choice = False
    while not choice:
        choice = input("1 - Search for a flight \n"
                       "2 - Cancel a flight \n")
        if choice == "1":
            user_flight_search(user)
        elif choice == "2":
            user_flight_cancel(user)
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
           flight['arrival'].lower() == arrival.lower() and
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
    pass
