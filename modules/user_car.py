import json
import random
from datetime import datetime
from modules.payment import process_payment
from utils import display_user_tickets

def user_car_arrangement(user):
    choice = False
    while not choice:
        choice = input("1 - Rent a car \n"
                       "2 - Cancel a rented car \n"
                       "3 - View my tickets \n"
                       "4 - Go back \n")
        if choice == "1":
            user_car_search(user)
        elif choice == "2":
            user_car_cancel(user)
        elif choice == "3":
            display_user_tickets(user, "car")
        elif choice == "4":
            choice = True
        else:
            print("Invalid input! Please select an operation.")

def user_car_search(user):
    brand = input("Brand : ")   
    car_options = display_cars_table(brand)
    
    if car_options:
        print("\nWould you like to rent a car?")
        choice = input("Enter car number to rent or 'N' to return to main menu: ")
        if choice.lower() != 'n':
            try:
                selected_index = int(choice)
                if 1 <= selected_index <= len(car_options):
                    selected_car = car_options[selected_index - 1]
                    user_car_booking(selected_car, user)
                else:
                    print("Invalid number!")
            except ValueError:
                print("Invalid input! Please enter a valid number or 'N'.")

def display_cars_table(brand):
    try:
        with open("data/cars.json", "r", encoding="utf-8") as f:
            cars = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No cars found.")
        return None

    if not cars:
        print("No cars found.")
        return None

    # Filter cars based on user criteria
    matching_cars = {
        id: car for id, car in cars.items()
        if car['brand'].lower() == brand.lower()
    }

    if not matching_cars:
        print(f"\nNo {brand} cars found")
        return None

    # Table header
    print("\nAvailable Cars:")
    print("-" * 100)
    print(f"{'No.':<5} {'Car ID':<15} {'Brand':<10} {'Price/Day':<15} {'Available':<12} {'Car Plate':<10}")
    print("-" * 100)

    # Table rows with numbered listing
    car_options = list(matching_cars.values())
    for idx, car in enumerate(car_options, 1):
        print(f"{idx:<5} "
              f"{car['car_id']:<15} "
              f"{car['brand']:<10} "
              f"{car['price']:<15} "
              f"{car['cars_available']:<12} "
              f"{car['car_plate']:<10}")
    print("-" * 100)
    print()
    
    return car_options

def user_car_booking(selected_car, user):
    # Load the cars data
    try:
        with open("data/cars.json", "r", encoding="utf-8") as f:
            cars = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing car data.")
        return

    # Find the car in the cars data using car_id
    car_key = None
    for key, car in cars.items():
        if car['car_id'] == selected_car['car_id']:
            car_key = key
            break

    if car_key is None:
        print("Car not found in the system.")
        return

    # Check if car is available
    if cars[car_key]['cars_available'] <= 0:
        print("Sorry, this car is not available for booking at the moment.")
        return

    # Get rental and return dates from user
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
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return

    # Calculate the total fee
    total_fee = days * selected_car['price']

    # Confirm booking with user
    print(f"\nCar Details:")
    print(f"Car ID: {selected_car['car_id']}")
    print(f"Brand: {selected_car['brand']}")
    print(f"Car Plate: {selected_car['car_plate']}")
    print(f"Available: {cars[car_key]['cars_available']}")
    print(f"Rental Date: {rental_date}")
    print(f"Return Date: {return_date}")
    print(f"Price per day: {selected_car['price']}")
    print(f"Number of days: {days}")
    print(f"Total fee: {total_fee}")

    confirm = input("\nWould you like to proceed with the booking? (Y/N): ")
    if confirm.lower() != 'y':
        print("Booking cancelled.")
        return

    # Update available cars
    cars[car_key]['cars_available'] -= 1

    # Save the updated cars data
    with open("data/cars.json", "w", encoding="utf-8") as f:
        json.dump(cars, f, ensure_ascii=False, indent=2)

    # Generate booking ID
    booking_id = f"CAR_{selected_car['car_id']}_{user}"
    
    print("\nBooking successful! Your car has been booked.")
    print(f"Booking ID: {booking_id}")
    print(f"Remaining cars available: {cars[car_key]['cars_available']}")
    
    # Process payment and store booking information
    process_payment(booking_id, total_fee, "car", {
        "type": "car",
        "user": user,
        "car_id": selected_car['car_id'],
        "brand": selected_car['brand'],
        "car_plate": selected_car['car_plate'],
        "rental_date": rental_date,
        "return_date": return_date,
        "days": days,
        "price_per_day": selected_car['price'],
        "total_fee": total_fee
    })
    
    print("\nThank you for choosing our service!")

def user_car_cancel(user):
    # Load the payments data
    try:
        with open("data/payments.json", "r", encoding="utf-8") as f:
            payments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing payment data.")
        return

    # Find all car bookings for the user
    user_bookings = []
    for payment_id, payment in payments.items():
        if (payment['service_type'] == 'car' and 
            payment['customer_name'] == user and 
            payment['status'] == 'completed'):
            
            # Extract booking details, handling cases where booking_details might not exist
            if 'booking_details' in payment:
                booking_details = payment['booking_details']
                user_bookings.append({
                    'payment_id': payment_id,
                    'booking_id': payment['booking_id'],
                    'car_id': booking_details['car_id'],
                    'brand': booking_details['brand'],
                    'car_plate': booking_details['car_plate'],
                    'rental_date': booking_details['rental_date'],
                    'return_date': booking_details['return_date'],
                    'days': booking_details.get('days', 'N/A'),
                    'price_per_day': booking_details.get('price_per_day', 'N/A'),
                    'total_fee': booking_details.get('total_fee', payment['amount'])
                })
            else:
                # For older records without booking_details, extract info from booking_id
                # Format is typically: CAR_car_id_username
                parts = payment['booking_id'].split('_')
                if len(parts) >= 3:
                    car_id = parts[1]
                    # Try to find car details from cars.json
                    try:
                        with open("data/cars.json", "r", encoding="utf-8") as f:
                            cars = json.load(f)
                            # Find car with matching car_id
                            for car in cars.values():
                                if car['car_id'] == car_id:
                                    user_bookings.append({
                                        'payment_id': payment_id,
                                        'booking_id': payment['booking_id'],
                                        'car_id': car_id,
                                        'brand': car['brand'],
                                        'car_plate': car['car_plate'],
                                        'rental_date': 'N/A',
                                        'return_date': 'N/A',
                                        'days': 'N/A',
                                        'price_per_day': car['price'],
                                        'total_fee': payment['amount']
                                    })
                                    break
                    except (FileNotFoundError, json.JSONDecodeError):
                        print(f"Warning: Could not find car details for booking {payment['booking_id']}")
                        continue

    if not user_bookings:
        print("You have no active car rental bookings to cancel.")
        return

    # Display user's bookings
    print("\nYour Car Rental Bookings:")
    print("-" * 120)
    print(f"{'No.':<5} {'Car ID':<15} {'Brand':<10} {'Plate':<10} {'Rental Date':<12} {'Return Date':<12} {'Days':<8} {'Price/Day':<10} {'Total':<10}")
    print("-" * 120)

    for idx, booking in enumerate(user_bookings, 1):
        print(f"{idx:<5} "
              f"{booking['car_id']:<15} "
              f"{booking['brand']:<10} "
              f"{booking['car_plate']:<10} "
              f"{booking['rental_date']:<12} "
              f"{booking['return_date']:<12} "
              f"{booking['days']:<8} "
              f"{booking['price_per_day']:<10} "
              f"{booking['total_fee']:<10}")
    print("-" * 120)

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
    confirm = input(f"\nAre you sure you want to cancel your car rental for {selected_booking['brand']} (Plate: {selected_booking['car_plate']})? (Y/N): ")
    if confirm.lower() != 'y':
        print("Cancellation cancelled.")
        return

    # Load cars data to update availability
    try:
        with open("data/cars.json", "r", encoding="utf-8") as f:
            cars = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing car data.")
        return

    # Find and update the car's availability
    car_updated = False
    for car in cars.values():
        if car['car_id'] == selected_booking['car_id']:
            car['cars_available'] += 1
            car_updated = True
            break

    if not car_updated:
        print("Error: Car not found in the system.")
        return

    # Save updated cars data
    with open("data/cars.json", "w", encoding="utf-8") as f:
        json.dump(cars, f, ensure_ascii=False, indent=2)

    # Update payment status
    payments[selected_booking['payment_id']]['status'] = 'cancelled'

    # Save updated payments data
    with open("data/payments.json", "w", encoding="utf-8") as f:
        json.dump(payments, f, ensure_ascii=False, indent=2)

    print("\nCar rental booking cancelled successfully!")
    print(f"Booking ID: {selected_booking['booking_id']}")
    print(f"Car ID: {selected_booking['car_id']}")
    print(f"Brand: {selected_booking['brand']}")
    print(f"Car Plate: {selected_booking['car_plate']}")
    print(f"Rental Date: {selected_booking['rental_date']}")
    print(f"Return Date: {selected_booking['return_date']}")
    print(f"Number of Days: {selected_booking['days']}")
    print(f"Price per Day: {selected_booking['price_per_day']}")
    print(f"Total Fee: {selected_booking['total_fee']}")


