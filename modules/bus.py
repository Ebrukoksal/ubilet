from modules.transport import Transport

class Bus(Transport):
    def __init__(self):
        """
        Bus class inherits from Transport class to handle bus-specific functionality.
        The class is initialized with transport_type='bus' to load bus data and
        provide bus management capabilities.
        """
        super().__init__("bus")

def bus_arrangement(admin_username=None):
    """Arranges bus management for the admin by creating a Bus instance and handling the management process.

    Args:
        admin_username: The admin username for logging actions.
    """
    bus = Bus()
    bus.arrangement(admin_username)
