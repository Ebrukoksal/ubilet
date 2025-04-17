from modules.user_transport import Transport

class Flight(Transport):
    def __init__(self):
        """
        Flight class inherits from Transport class to handle flight-specific functionality.
        The class is initialized with transport_type='flight' to load flight data and
        provide flight booking capabilities.
        """
        super().__init__('flight')

def user_flight_arrangement(user):
    """Arranges flight journey for the user by creating a flight instance and handling the booking process.

    Args:
        user: The user object containing user information for the booking.
    """
    flight = Flight()
    flight.arrangement(user)
