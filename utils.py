import hashlib

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
                date = date.strptime(value, "%d/%m/%Y")
                return date.strftime("%d/%m/%Y")
            except ValueError:
                print("Please enter a valid date in the format DD/MM/YYYY.")
                continue
        return value


# def get_bus_voyage_number(company, departure, arrival, date, time):
#     # Get first letters of company, departure, arrival
#     voyage_number = company[0].upper() + departure[0].upper() + arrival[0].upper()
    
#     # Remove "/" from date and add it
#     voyage_number += date.replace("/", "")
    
#     # Remove ":" from time and add it
#     voyage_number += time.replace(":", "")
    
#     return voyage_number

# def get_train_voyage_number(train_type, departure, arrival, date, time):
#     # Get first letters of train type, departure, arrival
#     voyage_number = train_type[0].upper() + departure[0].upper() + arrival[0].upper()
    
#     # Remove "/" from date and add it
#     voyage_number += date.replace("/", "")
    
#     # Remove ":" from time and add it
#     voyage_number += time.replace(":", "")
    
#     return voyage_number

# def get_car_voyage_number(company, departure, arrival, date, time):
#     # Get first letters of company, departure, arrival
#     voyage_number = company[0].upper() + departure[0].upper() + arrival[0].upper()
    
#     # Remove "/" from date and add it
#     voyage_number += date.replace("/", "")
    
#     # Remove ":" from time and add it
#     voyage_number += time.replace(":", "")
    
#     return voyage_number
