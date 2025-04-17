from modules.user_transport import Transport

class Train(Transport):
    def __init__(self):
        """
        Train class inherits from Transport class to handle train-specific functionality.
        The class is initialized with transport_type='train' to load train data and
        provide train booking capabilities.
        """
        super().__init__('train')

# Function to be used in the main program
def user_train_arrangement(user):
    """Arranges train journey for the user by creating a Train instance and handling the booking process.

    Args:
        user: The user object containing user information for the booking.
    """
    train = Train()
    train.arrangement(user)
