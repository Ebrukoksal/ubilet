from modules.rentals import Rental

class Hotel(Rental):
    """
    A class to manage hotel rentals, inheriting from the base Rental class.
    """
    def __init__(self):
        super().__init__(rental_type='hotel')

def hotel_arrangement(admin_username=None):
    """
    Function to handle hotel rental arrangements.
    
    Args:
        admin_username (str, optional): Username of the admin performing the action.
    """
    hotel = Hotel()
    hotel.arrangement(admin_username)
