from modules.transport import Transport

class Flight(Transport):
    def __init__(self):
        """
        Flight class inherits from Transport class to handle flight-specific functionality.
        The class is initialized with transport_type='flight' to load flight data and
        provide flight management capabilities.
        """
        super().__init__("flight")

def flight_arrangement(admin_username=None):
    """Arranges flight management for the admin by creating a Flight instance and handling the management process.

    Args:
        admin_username: The admin username for logging actions.
    """
    flight = Flight()
    flight.arrangement(admin_username)
