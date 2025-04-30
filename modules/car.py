from modules.rentals import Rental


class Car(Rental):
    """
    A class to manage car rentals, inheriting from the base Rental class.
    """
    def __init__(self):
        super().__init__(rental_type='car')

def car_arrangement(admin_username=None):
    """
    Function to handle car rental arrangements.
    
    Args:
        admin_username (str, optional): Username of the admin performing the action.
    """
    car = Car()
    car.arrangement(admin_username)

