from modules.user_transport import Transport

class Bus(Transport):
    def __init__(self):
        """
        Bus class inherits from Transport class to handle bus-specific functionality.
        The class is initialized with transport_type='bus' to load bus data and
        provide bus booking capabilities.
        """
        super().__init__('bus')

def user_bus_arrangement(user):
    """Arranges bus journey for the user by creating a bus instance and handling the booking process.

    Args:
        user: The user object containing user information for the booking.
    """
    bus = Bus()
    bus.arrangement(user)
