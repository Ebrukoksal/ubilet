import json
from datetime import datetime

def process_payment(booking_id, amount, service_type, booking_details): 

    print("\n=== Payment Information ===")
    print(f"Booking ID: {booking_id}")
    print(f"Amount to Pay: {amount} TL")
    print("\nPlease enter your payment information:")
    
    name = input("Name: ")
    surname = input("Surname: ")
    id_number = input("Identification Number: ")
    card_number = input("Credit Card Number: ")
    exp_date = input("Card Expiration Date (MM/YY): ")
    cvv = input("CVV: ")
    
    try:
        with open("data/payments.json", "r", encoding="utf-8") as f:
            payments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        payments = {}
    
    payment_id = f"PAY_{datetime.now().strftime('%Y%m%d%H%M%S')}_{booking_id}"
    
    payments[payment_id] = {
        "booking_id": booking_id,
        "service_type": service_type,
        "amount": amount,
        "payment_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "customer_name": name,
        "customer_surname": surname,
        "id_number": id_number,
        "card_number": card_number[-4:], 
        "exp_date": exp_date,
        "status": "completed",
        "booking_details": booking_details  
    }
    
    with open("data/payments.json", "w", encoding="utf-8") as f:
        json.dump(payments, f, ensure_ascii=False, indent=2)
    
    print("\nPayment processed successfully!")
    print(f"Payment ID: {payment_id}")
    print("Thank you for your payment!")
    
    return payment_id
