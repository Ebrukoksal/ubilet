from modules.transport import Transport

class Train(Transport):
    def __init__(self):
        """
        Train class inherits from Transport class to handle train-specific functionality.
        The class is initialized with transport_type='train' to load train data and
        provide train management capabilities.
        """
        super().__init__("train")

def train_arrangement(admin_username=None):
    """Arranges train management for the admin by creating a Train instance and handling the management process.

    Args:
        admin_username: The admin username for logging actions.
    """
    train = Train()
    train.arrangement(admin_username)
