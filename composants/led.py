from .base import PinOut

class LED(PinOut):
    """Class representing an LED component."""

    def __init__(self, pin: int):
        """Initialize the LED with the specified pin."""
        super().__init__(pin)

    