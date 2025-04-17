from modules.user_rentals import Rental

class Hotel(Rental):
    def __init__(self):
        """
        Hotel class inherits from Rental class to handle hotel-specific functionality.
        The class is initialized with rental_type='hotel' via the Rental parent class
        to load hotel data and provide hotel booking capabilities.
        """
        super().__init__('hotel')

# Function to be used in the main program
def user_hotel_arrangement(user):
    """Arranges hotel rental for the user by creating a Hotel instance and handling the booking process.

    Args:
        user: The user object containing user information for the booking.
    """
    hotel = Hotel()
    hotel.arrangement(user)