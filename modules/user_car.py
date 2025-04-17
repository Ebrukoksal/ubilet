from modules.user_rentals import Rental

class Car(Rental):
    def __init__(self):
        """
        Car class inherits from Rental class to handle car-specific functionality.
        The class is initialized with rental_type='car' via the Rental parent class
        to load car data and provide car booking capabilities.
        """
        super().__init__('car')

# Function to be used in the main program
def user_car_arrangement(user):
    """Arranges car rental for the user by creating a Car instance and handling the booking process.

    Args:
        user: The user object containing user information for the booking.
    """
    car = Car()
    car.arrangement(user)

