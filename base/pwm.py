import threading
import time
from .base import PinOut
from .utils import is_gpiod_v2

class PWM(PinOut):
    """
    Classe PWM pour gérer les sorties en modulation de largeur d'impulsion.
    Hérite de PinOut. Compatible gpiod v1 et v2.
    
    Arguments:
        pin (int): Numéro de la broche GPIO.
        chip (str): Nom du chip GPIO (défaut "gpiochip0").
        frequency (int): Fréquence du PWM en Hz (défaut 1000).
    """

    def __init__(self, pin, chip="gpiochip0", frequency=1000):
        """
        Constructeur de la classe PWM.

        Arguments:
            pin (int): Numéro de la broche GPIO.
            chip (str): Nom du chip GPIO.
            frequency (int): Fréquence du PWM en Hz.
        """
        super().__init__(pin=pin, chip=chip, initial_value=0)
        self.__frequency = frequency
        self.__duty_value = 0
        self.__duty_max = 255  # valeur par défaut duty_cycle_8
        self.__running = False
        self.__thread = None

    @property
    def frequency(self):
        """
        Getter de la fréquence PWM
        
        Arguments:
            None
        
        Returns:
            int: Fréquence actuelle en Hz.
        """
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        """
        Setter de la fréquence PWM
        
        Arguments:
            value (int): Nouvelle fréquence en Hz.
        
        Returns:
            None
        """
        self.__frequency = value

    def duty_cycle_8(self, value=None):
        """
        Duty cycle 8 bits (0-255). Retourne la valeur actuelle si value=None.
        
        Arguments:
            value (int): Valeur du duty cycle (0-255).
        
        Returns:
            int: Valeur actuelle du duty cycle si value=None.
        """
        self.__duty_max = 255
        if value is None:
            return self.__duty_value
        self.__duty_value = max(0, min(value, self.__duty_max))

    def duty_cycle_10(self, value=None):
        """
        Duty cycle 10 bits (0-1023). Retourne la valeur actuelle si value=None.
        
        Arguments:
            value (int): Valeur du duty cycle (0-1023).
            
        Returns:
            int: Valeur actuelle du duty cycle si value=None.
        """
        self.__duty_max = 1023
        if value is None:
            return self.__duty_value
        self.__duty_value = max(0, min(value, self.__duty_max))

    def duty_cycle_12(self, value=None):
        """
        Duty cycle 12 bits (0-4095). Retourne la valeur actuelle si value=None.
        
        Arguments:
            value (int): Valeur du duty cycle (0-4095).

        Returns:
            int: Valeur actuelle du duty cycle si value=None.
        """
        self.__duty_max = 4095
        if value is None:
            return self.__duty_value
        self.__duty_value = max(0, min(value, self.__duty_max))

    def duty_cycle_16(self, value=None):
        """
        Duty cycle 16 bits (0-65535). Retourne la valeur actuelle si value=None.
        
        Arguments:
            value (int): Valeur du duty cycle (0-65535).

        Returns:
            int: Valeur actuelle du duty cycle si value=None.
        """
        self.__duty_max = 65535
        if value is None:
            return self.__duty_value
        self.__duty_value = max(0, min(value, self.__duty_max))

    def __pwm_thread(self):
        """Thread interne qui génère le PWM non bloquant."""
        period = 1.0 / self.__frequency
        while self.__running:
            on_time = period * (self.__duty_value / self.__duty_max)
            off_time = period - on_time
            if on_time > 0:
                super().write(1)
                time.sleep(on_time)
            if off_time > 0:
                super().write(0)
                time.sleep(off_time)

    def start(self):
        """
        Démarre le PWM en arrière-plan.
        
        Arguments:
            None
            
        Returns:
            None
        """
        if not self.__running:
            self.__running = True
            self.__thread = threading.Thread(target=self.__pwm_thread, daemon=True)
            self.__thread.start()

    def stop(self):
        """
        Arrête le PWM et éteint la broche.
        
        Arguments:
            None
        Returns:
            None
        """
        if self.__running:
            self.__running = False
            if self.__thread:
                self.__thread.join()
            super().write(0)

    def close(self):
        """
        Libère la broche GPIO et arrête le PWM.
        
        Arguments:
            None
            
        Returns:
            None
        """
        self.stop()
        super().close()
        
    def __str__(self):
        """
        Représentation en chaîne de caractères de l'objet PWM.
        
        Arguments:
            None
        
        Returns:
            str: Représentation textuelle de l'objet PWM.
        """
        return f"PWM(pin={self.pin}, frequency={self.__frequency})"
    
    def __repr__(self):
        """
        Représentation officielle de l'objet PWM.
        
        Arguments:
            None

        Returns:
            str: Représentation officielle de l'objet PWM.
        """
        return f"PWM(pin={self.pin}, frequency={self.__frequency}, duty_cycle={self.__duty_value}/{self.__duty_max})" 
    
     if __name__ == "__main__":
        print("Ce module ne doit pas être exécuté directement.")