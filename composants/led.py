from .base import PinOut
import time
import threading

class LED(PinOut):
    """Class representing an LED component."""

    def __init__(self, pin: int, chip="gpiochip0"):
        """
        Initialize the LED with the specified pin.
        """
        super().__init__(pin, chip="gpiochip0")
        self.__blink_thread = None
        self.__blinking = False
    
    def on(self):
        """
        Allume la LED.

        Arguments:
            None
            
        Returns:
            None
        """
        super().write(1)
        
    def off(self):
        """
        Éteint la LED.
        
        Arguments:
            None
            
        Returns:
            None
        """
        self.__blinking = False
        super().write(0)
        
    def toggle(self):
        """
        Bascule l'état de la LED.
        
        Arguments:
            None
            
        Returns:
            None
        """
        self.write(0 if self.state else 1)
    
    def blink(self, count: int, interval: float = 0.5):
        """
        Clignote un nombre défini de fois (non bloquant).

        Arguments:
            count (int): nombre de clignotements
            interval (float): temps ON/OFF
        
        Returns:
            None
        """
        if self.__blinking:
            return

        def _blink():
            """Fonction interne pour clignoter."""
            self.__blinking = True
            for _ in range(count):
                if not self.__blinking:
                    break
                self.write(1)
                time.sleep(interval)
                self.write(0)
                time.sleep(interval)
            self.__blinking = False

        self.__blink_thread = threading.Thread(target=_blink, daemon=True)
        self.__blink_thread.start()

  
    def blink_times(self, seconds: float, interval: float = 0.5):
        """
        Clignote pendant une durée donnée (non bloquant).

        Arguments:
            seconds (float): durée totale en secondes
            interval (float): temps ON/OFF
            
        Returns:
            None
        """
        if self.__blinking:
            return

        def _blink_times():
            """Fonction interne pour clignoter pendant une durée."""
            self.__blinking = True
            end_time = time.time() + seconds
            while self.__blinking and time.time() < end_time:
                self.write(1)
                time.sleep(interval)
                self.write(0)
                time.sleep(interval)
            self.__blinking = False

        self.__blink_thread = threading.Thread(target=_blink_times, daemon=True)
        self.__blink_thread.start()    
    
    def close(self):
        """
        Libère la broche GPIO et éteint la LED.
        
        Arguments:
            None
            
        Returns:
            None
        """
        self.off()
        super().close()
        
    def __str__(self):
        """
        Représentation en chaîne de l'état de la LED.
        
        Arguments:
            None
        
        Returns:
            str: Chaîne représentant l'état de la LED.
            
        """
        return f"LED on pin {self.pin} is {'ON' if self.state else 'OFF'}"
    
    def __repr__(self):
        """
        Représentation en chaîne de la LED.
        
        Arguments:
            None
        
        Returns:
            str: Chaîne représentant la LED.
            
        """
        return f"LED(pin={self.pin}, chip='{self.chip_name}', state={'ON' if self.state else 'OFF'})"
        
    
if __name__ == "__main__":
    print("Ce module ne doit pas être exécuté directement.")
        