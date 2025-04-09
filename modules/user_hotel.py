import json
from datetime import datetime
from modules.payment import process_payment
from utils import display_user_tickets

def user_hotel_arrangement(user):
    choice = False
    while not choice:
        choice = input("1 - Book a hotel \n"
                       "2 - Cancel a booked hotel \n"
                       "3 - View my tickets \n"
                       "4 - Go back \n")
        if choice == "1":
            user_hotel_search(user)
        elif choice == "2":
            user_hotel_cancel(user)
        elif choice == "3":
            display_user_tickets(user, "hotel")
        elif choice == "4":
            choice = True
        else:
            print("Invalid input! Please select an operation.")


def user_hotel_search(user):
    city = input("City: ")
    check_in_date = input("Check-in Date (DD/MM/YYYY): ")
    leaving_date = input("Leaving Date (DD/MM/YYYY): ")
    adults = int(input("Number of Adults: "))
    children = int(input("Number of Children: "))
    
    hotel_options = display_hotels_table(city) 
    
    if hotel_options:
        print("\nWould you like to book a hotel?")
        choice = input("Enter hotel number to book or 'N' to return to main menu: ")
        if choice.lower() != 'n':
            try:
                selected_index = int(choice)
                if 1 <= selected_index <= len(hotel_options):
                    selected_hotel = hotel_options[selected_index - 1]
                    user_hotel_booking(selected_hotel, user, check_in_date, leaving_date, adults, children)
                else:
                    print("Invalid number!")
            except ValueError:
                print("Invalid input! Please enter a valid number or 'N'.")


def display_hotels_table(city):
    try:
        with open("data/hotels.json", "r", encoding="utf-8") as f:
            hotels = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No hotels found.")
        return None

    if not hotels:
        print("No hotels found.")
        return None

    # Filter hotels based on user criteria
    matching_hotels = {
        id: hotel for id, hotel in hotels.items()
        if hotel['city'].lower() == city.lower()
    }

    if not matching_hotels:
        print(f"\nNo hotels found in {city}")
        return None

    # Table header
    print("\nAvailable Hotels:")
    print("-" * 120)
    print(f"{'No.':<5} {'Hotel ID':<15} {'Hotel Name':<15} {'City':<15} {'Rooms Available':<15} {'Adult Price/Day':<15} {'Child Price/Day':<15}")
    print("-" * 120)

    # Table rows with numbered listing
    hotel_options = list(matching_hotels.values())
    for idx, hotel in enumerate(hotel_options, 1):
        print(f"{idx:<5} "
              f"{hotel['hotel_id']:<15} "
              f"{hotel['hotel_name']:<15} "
              f"{hotel['city']:<15} "
              f"{hotel['rooms_available']:<15} "
              f"{hotel['adult_price']:<15} "
              f"{hotel['child_price']:<15}")
    print("-" * 120)
    print()
    
    return hotel_options

def user_hotel_booking(selected_hotel, user, check_in_date, leaving_date, adults, children):
    # Load the hotels data
    try:
        with open("data/hotels.json", "r", encoding="utf-8") as f:
            hotels = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing hotel data.")
        return

    # Find the hotel in the hotels data using hotel_id
    hotel_key = None
    for key, hotel in hotels.items():
        if hotel['hotel_id'] == selected_hotel['hotel_id']:
            hotel_key = key
            break

    if hotel_key is None:
        print("Hotel not found in the system.")
        return

    # Check if hotel is available
    if hotels[hotel_key]['rooms_available'] <= 0:
        print("Sorry, this hotel is not available for booking at the moment.")
        return

    # Calculate the number of days between check-in and check-out dates
    try:
        check_in_datetime = datetime.strptime(check_in_date, "%d/%m/%Y")
        check_out_datetime = datetime.strptime(leaving_date, "%d/%m/%Y")
        days = (check_out_datetime - check_in_datetime).days
        if days <= 0:
            print("Leaving date must be after check-in date.")
            return
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return

    # Calculate the total price
    adult_total = days * selected_hotel['adult_price'] * adults
    child_total = days * selected_hotel['child_price'] * children
    total_price = adult_total + child_total

    # Collect guest information
    guest_list = []
    
    # Collect adult guest information
    print("\nPlease enter information for adult guests:")
    for i in range(adults):
        print(f"\nAdult Guest #{i+1}:")
        guest_name = input("Name: ")
        guest_surname = input("Surname: ")
        guest_id = input("Identification Number: ")
        guest_list.append({
            "type": "adult",
            "name": guest_name,
            "surname": guest_surname,
            "id": guest_id
        })
    
    # Collect child guest information
    print("\nPlease enter information for child guests:")
    for i in range(children):
        print(f"\nChild Guest #{i+1}:")
        guest_name = input("Name: ")
        guest_surname = input("Surname: ")
        guest_id = input("Identification Number: ")
        guest_list.append({
            "type": "child",
            "name": guest_name,
            "surname": guest_surname,
            "id": guest_id
        })

    # Confirm booking with user
    print(f"\nHotel Details:")
    print(f"Hotel ID: {selected_hotel['hotel_id']}")
    print(f"Hotel Name: {selected_hotel['hotel_name']}")
    print(f"City: {selected_hotel['city']}")
    print(f"Check-in Date: {check_in_date}")
    print(f"Leaving Date: {leaving_date}")
    print(f"Number of Adults: {adults}")
    print(f"Number of Children: {children}")
    print(f"Price per adult per day: {selected_hotel['adult_price']}")
    print(f"Price per child per day: {selected_hotel['child_price']}")
    print(f"Number of days: {days}")
    print(f"Adult total: {adult_total}")
    print(f"Child total: {child_total}")
    print(f"Total price: {total_price}")
    
    print("\nGuest Information:")
    for i, guest in enumerate(guest_list, 1):
        print(f"\nGuest #{i}:")
        print(f"Type: {guest['type'].capitalize()}")
        print(f"Name: {guest['name']}")
        print(f"Surname: {guest['surname']}")
        print(f"ID: {guest['id']}")

    confirm = input("\nWould you like to proceed with the booking? (Y/N): ")
    if confirm.lower() != 'y':
        print("Booking cancelled.")
        return

    # Update available rooms
    hotels[hotel_key]['rooms_available'] -= 1

    # Save the updated hotels data
    with open("data/hotels.json", "w", encoding="utf-8") as f:
        json.dump(hotels, f, ensure_ascii=False, indent=2)

    # Generate booking ID
    booking_id = f"HOTEL_{selected_hotel['hotel_id']}_{user}"
    
    print("\nBooking successful! Your hotel has been booked.")
    print(f"Booking ID: {booking_id}")
    print(f"Remaining rooms available: {hotels[hotel_key]['rooms_available']}")
    
    # Process payment and store booking information
    process_payment(booking_id, total_price, "hotel", {
        "type": "hotel",
        "user": user,
        "hotel_id": selected_hotel['hotel_id'],
        "hotel_name": selected_hotel['hotel_name'],
        "city": selected_hotel['city'],
        "check_in_date": check_in_date,
        "leaving_date": leaving_date,
        "adults": adults,
        "children": children,
        "days": days,
        "adult_price_per_day": selected_hotel['adult_price'],
        "child_price_per_day": selected_hotel['child_price'],
        "adult_total": adult_total,
        "child_total": child_total,
        "total_price": total_price,
        "guests": guest_list
    })
    
    print("\nThank you for choosing our service!")


def user_hotel_cancel(user):
    # Load the payments data
    try:
        with open("data/payments.json", "r", encoding="utf-8") as f:
            payments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing payment data.")
        return

    # Find all hotel bookings for the user
    user_bookings = []
    for payment_id, payment in payments.items():
        if (payment['service_type'] == 'hotel' and 
            payment['customer_name'] == user and 
            payment['status'] == 'completed'):
            
            # Extract booking details, handling cases where booking_details might not exist
            if 'booking_details' in payment:
                booking_details = payment['booking_details']
                user_bookings.append({
                    'payment_id': payment_id,
                    'booking_id': payment['booking_id'],
                    'hotel_id': booking_details['hotel_id'],
                    'hotel_name': booking_details['hotel_name'],
                    'city': booking_details['city'],
                    'check_in_date': booking_details['check_in_date'],
                    'leaving_date': booking_details['leaving_date'],
                    'adults': booking_details['adults'],
                    'children': booking_details['children'],
                    'total_price': booking_details['total_price']
                })
            else:
                # For older records without booking_details, extract info from booking_id
                # Format is typically: HOTEL_hotel_id_username
                parts = payment['booking_id'].split('_')
                if len(parts) >= 3:
                    hotel_id = parts[1]
                    # Try to find hotel details from hotels.json
                    try:
                        with open("data/hotels.json", "r", encoding="utf-8") as f:
                            hotels = json.load(f)
                            # Find hotel with matching hotel_id
                            for hotel in hotels.values():
                                if hotel['hotel_id'] == hotel_id:
                                    user_bookings.append({
                                        'payment_id': payment_id,
                                        'booking_id': payment['booking_id'],
                                        'hotel_id': hotel_id,
                                        'hotel_name': hotel['hotel_name'],
                                        'city': hotel['city'],
                                        'check_in_date': 'N/A',
                                        'leaving_date': 'N/A',
                                        'adults': 'N/A',
                                        'children': 'N/A',
                                        'total_price': payment['amount']
                                    })
                                    break
                    except (FileNotFoundError, json.JSONDecodeError):
                        print(f"Warning: Could not find hotel details for booking {payment['booking_id']}")
                        continue

    if not user_bookings:
        print("You have no active hotel bookings to cancel.")
        return

    # Display user's bookings
    print("\nYour Hotel Bookings:")
    print("-" * 120)
    print(f"{'No.':<5} {'Hotel ID':<10} {'Hotel Name':<15} {'City':<15} {'Check-in':<12} {'Leaving':<12} {'Adults':<8} {'Children':<8} {'Price':<10}")
    print("-" * 120)

    for idx, booking in enumerate(user_bookings, 1):
        print(f"{idx:<5} "
              f"{booking['hotel_id']:<10} "
              f"{booking['hotel_name']:<15} "
              f"{booking['city']:<15} "
              f"{booking['check_in_date']:<12} "
              f"{booking['leaving_date']:<12} "
              f"{booking['adults']:<8} "
              f"{booking['children']:<8} "
              f"{booking['total_price']:<10}")
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
    confirm = input(f"\nAre you sure you want to cancel your hotel booking at {selected_booking['hotel_name']} in {selected_booking['city']}? (Y/N): ")
    if confirm.lower() != 'y':
        print("Cancellation cancelled.")
        return

    # Load hotels data to update room availability
    try:
        with open("data/hotels.json", "r", encoding="utf-8") as f:
            hotels = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing hotel data.")
        return

    # Find and update the hotel's room availability
    hotel_updated = False
    for hotel in hotels.values():
        if hotel['hotel_id'] == selected_booking['hotel_id']:
            hotel['rooms_available'] += 1
            hotel_updated = True
            break

    if not hotel_updated:
        print("Error: Hotel not found in the system.")
        return

    # Save updated hotels data
    with open("data/hotels.json", "w", encoding="utf-8") as f:
        json.dump(hotels, f, ensure_ascii=False, indent=2)

    # Update payment status
    payments[selected_booking['payment_id']]['status'] = 'cancelled'

    # Save updated payments data
    with open("data/payments.json", "w", encoding="utf-8") as f:
        json.dump(payments, f, ensure_ascii=False, indent=2)

    print("\nHotel booking cancelled successfully!")
    print(f"Booking ID: {selected_booking['booking_id']}")
    print(f"Hotel ID: {selected_booking['hotel_id']}")
    print(f"Hotel Name: {selected_booking['hotel_name']}")
    print(f"City: {selected_booking['city']}")
    print(f"Check-in Date: {selected_booking['check_in_date']}")
    print(f"Leaving Date: {selected_booking['leaving_date']}")
    print(f"Number of Adults: {selected_booking['adults']}")
    print(f"Number of Children: {selected_booking['children']}")
    print(f"Total Price: {selected_booking['total_price']}")


# car + hotel
# plane + bus + train
