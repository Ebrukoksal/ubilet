import hashlib
import json
from datetime import datetime

def get_hash(*args):
    combined_str = ""
    for arg in args:
        combined_str += str(arg)
    return hashlib.sha256(combined_str.encode()).hexdigest()

def get_hash_with_kwargs(**kwargs):
    combined_str = ""
    for key, value in kwargs.items():
        combined_str += str(value)
    return hashlib.sha256(combined_str.encode()).hexdigest()

def get_voyage_number(**kwargs):
    voyage_number = ""
    for key, value in kwargs.items():
        voyage_number += str(value)[0]
    return voyage_number

def get_valid_input(prompt, is_price=False, is_date=False):
    while True:
        value = input(prompt).strip()
        if not value:
            print("This field cannot be empty. Please try again.")
            continue
        if is_price:
            try:
                price = int(value)
                if price < 0:
                    print("Price cannot be negative. Please try again.")
                    continue
                return str(price)
            except ValueError:
                print("Please enter a valid number for price.")
                continue
        if is_date:
            try:
                date = datetime.strptime(value, "%d/%m/%Y")
                return date.strftime("%d/%m/%Y")
            except ValueError:
                print("Please enter a valid date in the format DD/MM/YYYY.")
                continue
        return value

def display_user_tickets(username, service_type=None):
    """
    Display all tickets and services a user has paid for.
    
    Args:
        username (str): The username of the user whose tickets to display
        service_type (str, optional): If provided, only display tickets for this service type
    """
    try:
        with open("data/payments.json", "r", encoding="utf-8") as f:
            payments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error accessing payment data.")
        return

    # Find all payments for the user
    user_payments = []
    for payment_id, payment in payments.items():
        if payment['customer_name'] == username:
            # If service_type is specified, only include payments of that type
            if service_type and payment['service_type'] != service_type:
                continue
            user_payments.append({
                'payment_id': payment_id,
                'booking_id': payment['booking_id'],
                'service_type': payment['service_type'],
                'amount': payment['amount'],
                'payment_date': payment['payment_date'],
                'status': payment['status'],
                'booking_details': payment.get('booking_details', {})
            })

    if not user_payments:
        if service_type:
            print(f"No {service_type} tickets found for user: {username}")
        else:
            print(f"No tickets or services found for user: {username}")
        return

    # Sort payments by date (newest first)
    user_payments.sort(key=lambda x: x['payment_date'], reverse=True)

    # Display user's tickets and services
    if service_type:
        print(f"\n{service_type.upper()} Tickets for {username}:")
    else:
        print(f"\nTickets and Services for {username}:")
    print("-" * 120)
    
    # Group payments by service type
    service_types = {}
    for payment in user_payments:
        service_type = payment['service_type']
        if service_type not in service_types:
            service_types[service_type] = []
        service_types[service_type].append(payment)
    
    # Display each service type separately
    for service_type, payments in service_types.items():
        print(f"\n{service_type.upper()} BOOKINGS:")
        print("-" * 120)
        
        if service_type == 'flight':
            print(f"{'No.':<5} {'Booking ID':<25} {'From':<15} {'To':<15} {'Date':<12} {'Time':<8} {'Seat':<8} {'Price':<10} {'Status':<10}")
            print("-" * 120)
            
            for idx, payment in enumerate(payments, 1):
                details = payment['booking_details']
                print(f"{idx:<5} "
                      f"{payment['booking_id']:<25} "
                      f"{details.get('departure', 'N/A'):<15} "
                      f"{details.get('arrival', 'N/A'):<15} "
                      f"{details.get('date', 'N/A'):<12} "
                      f"{details.get('time', 'N/A'):<8} "
                      f"{details.get('seat_number', 'N/A'):<8} "
                      f"{payment['amount']:<10} "
                      f"{payment['status']:<10}")
            print("-" * 120)
        
        elif service_type == 'hotel':
            print(f"{'No.':<5} {'Booking ID':<25} {'Hotel':<15} {'City':<15} {'Check-in':<12} {'Leaving':<12} {'Adults':<8} {'Children':<8} {'Price':<10} {'Status':<10}")
            print("-" * 120)
            
            for idx, payment in enumerate(payments, 1):
                details = payment['booking_details']
                print(f"{idx:<5} "
                      f"{payment['booking_id']:<25} "
                      f"{details.get('hotel_name', 'N/A'):<15} "
                      f"{details.get('city', 'N/A'):<15} "
                      f"{details.get('check_in_date', 'N/A'):<12} "
                      f"{details.get('leaving_date', 'N/A'):<12} "
                      f"{details.get('adults', 'N/A'):<8} "
                      f"{details.get('children', 'N/A'):<8} "
                      f"{payment['amount']:<10} "
                      f"{payment['status']:<10}")
            print("-" * 120)
        
        elif service_type == 'car':
            print(f"{'No.':<5} {'Booking ID':<25} {'Brand':<10} {'Plate':<10} {'Rental Date':<12} {'Return Date':<12} {'Days':<8} {'Price':<10} {'Status':<10}")
            print("-" * 120)
            
            for idx, payment in enumerate(payments, 1):
                details = payment['booking_details']
                print(f"{idx:<5} "
                      f"{payment['booking_id']:<25} "
                      f"{details.get('brand', 'N/A'):<10} "
                      f"{details.get('car_plate', 'N/A'):<10} "
                      f"{details.get('rental_date', 'N/A'):<12} "
                      f"{details.get('return_date', 'N/A'):<12} "
                      f"{details.get('days', 'N/A'):<8} "
                      f"{payment['amount']:<10} "
                      f"{payment['status']:<10}")
            print("-" * 120)
        
        else:
            # Generic display for other service types
            print(f"{'No.':<5} {'Booking ID':<25} {'Service Type':<15} {'Amount':<10} {'Date':<20} {'Status':<10}")
            print("-" * 120)
            
            for idx, payment in enumerate(payments, 1):
                print(f"{idx:<5} "
                      f"{payment['booking_id']:<25} "
                      f"{payment['service_type']:<15} "
                      f"{payment['amount']:<10} "
                      f"{payment['payment_date']:<20} "
                      f"{payment['status']:<10}")
            print("-" * 120)
    
    # Display summary
    total_payments = len(user_payments)
    active_payments = sum(1 for p in user_payments if p['status'] == 'completed')
    cancelled_payments = sum(1 for p in user_payments if p['status'] == 'cancelled')
    
    print(f"\nSummary:")
    print(f"Total bookings: {total_payments}")
    print(f"Active bookings: {active_payments}")
    print(f"Cancelled bookings: {cancelled_payments}")

