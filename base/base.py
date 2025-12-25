import gpiod
from enum import Enum
from .utils import is_gpiod_v2

class Pull(Enum):
    """
    Classe énumérée pour les résistances de tirage (pull-up, pull-down, none).
    
    Arguments:
        UP (int): Résistance de tirage vers le haut (pull-up).
        DOWN (int): Résistance de tirage vers le bas (pull-down).
        NONE (int): Aucune résistance de tirage.
    
    Returns:
        Pull: Une instance de la classe Pull représentant le type de résistance de tirage.
    """
    UP = 1
    DOWN = 2
    NONE = 3

class PinIn:
    """
    Classe pour gérer une broche GPIO en entrée.
    Code compatible avec gpiod version 1 et 2.
    
    Arguments:
        pin (int): Numéro de la broche GPIO.
        chip (str): Nom du chip GPIO (par défaut "gpiochip0").
        pull (Pull): Type de résistance de tirage (Pull.UP, Pull.DOWN, Pull.NONE).
    """
    def __init__(self, pin, chip="gpiochip0", pull=Pull.NONE):
        """
        Constructeur de la classe PinIn.
        Arguments:
            pin (int): Numéro de la broche GPIO.
            chip (str): Nom du chip GPIO (par défaut "gpiochip0").
            pull (Pull): Type de résistance de tirage (Pull.UP, Pull.DOWN, Pull.NONE).
        """
        self.pin = pin
        self.chip_name = chip
        self.pull = pull

        if is_gpiod_v2():
            if pull == Pull.UP:
                bias = gpiod.LineBias.PULL_UP
            elif pull == Pull.DOWN:
                bias = gpiod.LineBias.PULL_DOWN
            else:
                bias = gpiod.LineBias.DISABLED

            self.chip = gpiod.Chip(self.chip_name)
            self.request = self.chip.request_lines(
                consumer="gpiodzero",
                config={self.pin: gpiod.LineSettings(
                    direction=gpiod.LineDirection.INPUT,
                    bias=bias
                )}
            )
        else:
            self.chip = gpiod.Chip(self.chip_name)
            self.line = self.chip.get_line(self.pin)
            self.line.request(
                consumer="gpiodzero",
                type=gpiod.LINE_REQ_DIR_IN
            )

    def read(self) -> int:
        """
        Lit la valeur de la broche GPIO.
        
        Arguments:
            None
            
        Returns:
            int: Valeur lue sur la broche GPIO (0 ou 1).
        """
        if is_gpiod_v2():
            return self.request.get_value(self.pin)
        return self.line.get_value()

    def close(self):
        """
        Libère la broche GPIO.
        
        Arguments:
            None
            
        Returns:
            None
        """
        if is_gpiod_v2():
            self.request.release()
        else:
            self.line.release()

    def __str__(self):
        """
        Représentation en chaîne de la broche GPIO.
        
        Arguments:
            None
        
        Returns:
            str: Chaîne représentant l'état de la broche GPIO.
            
        """
        return f"Pin {self.pin} = {self.read()}"

    def __repr__(self):
        """
        Représentation en chaîne de la broche GPIO. 
        
        Arguments:
            None

        Returns:
            str: Chaîne représentant l'état de la broche GPIO.
            
        """
        return f"PinIn(chip='{self.chip_name}', pin={self.pin}, pull={self.pull})"

# ----------Fin de la classe PinIn et de la classe PinOut----------

class PinOut:
    """
    Classe pour gérer une broche GPIO en sortie.
    Code compatible avec gpiod version 1 et 2.
    
    Arguments:
        pin (int): Numéro de la broche GPIO.
        chip (str): Nom du chip GPIO (par défaut "gpiochip0").
        __state (int): Valeur initiale de la broche (0 ou 1).
    """
    def __init__(self, pin, chip="gpiochip0", initial_value=0):
        """
        Constructeur de la classe PinOut.
        
        Arguments:
            pin (int): Numéro de la broche GPIO.
            chip (str): Nom du chip GPIO (par défaut "gpiochip0").
            initial_value (int): Valeur initiale de la broche (0 ou 1).
        """
        self.pin = pin
        self.chip_name = chip
        self.__state = 1 if initial_value else 0

        # Configuration de la broche en sortie selon la version de gpiod
        if is_gpiod_v2():
            self.chip = gpiod.Chip(self.chip_name)
            self.request = self.chip.request_lines(
                consumer="gpiodzero",
                config={self.pin: gpiod.LineSettings(
                    direction=gpiod.LineDirection.OUTPUT,
                    output_value=self.__state
                )}
            )
        else:
            self.chip = gpiod.Chip(self.chip_name)
            self.line = self.chip.get_line(self.pin)
            self.line.request(
                consumer="gpiodzero",
                type=gpiod.LINE_REQ_DIR_OUT,
                default_vals=[self.__state]
            )
    
    def write(self, value: int):
        """
        Écrit une valeur sur la broche GPIO.

        Arguments:
            value (int): Valeur à écrire sur la broche GPIO (0 ou 1).

        Returns:
            None
        """
        value = 1 if value else 0
        self.__state = value
        if is_gpiod_v2():
            self.request.set_value(self.pin, value)
        else:
            self.line.set_value(value)
    
    @property
    def state(self):
        return self.__state

    
    def close(self):
        """
        Libère la broche GPIO.y
        
        Arguments:
            None
            
        Returns:
            None
        """
        if is_gpiod_v2():
            self.request.release()
        else:
            self.line.release()

    def __str__(self):
        """
        Représentation en chaîne de la broche GPIO.
        
        Arguments:
            None
        
        Returns:
            str: Chaîne représentant l'état de la broche GPIO.
            
        """
        return f"Pin {self.pin} = {self.__state}"

    def __repr__(self):
        """
        Représentation en chaîne de la broche GPIO.
        
        Arguments:
            None
        
        Returns:
            str: Chaîne représentant l'état de la broche GPIO.
            
        """
        return f"PinOut(chip='{self.chip_name}', pin={self.pin}, value={self.__state})"

if __name__ == "__main__":
    print("Ce module ne doit pas être exécuté directement.")    
