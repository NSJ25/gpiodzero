import time
import threading
import random
from .base import PWM


class LEDRGB:
    """
    Classe LED RGB basée sur 3 sorties PWM.
    
    - Fréquence commune aux 3 LEDs
    - Duty cycle interne en 16 bits (non exposé)
    - Valeurs utilisateur en float (0.0 → 1.0)
    """

    def __init__(self, red_pin: int, green_pin: int, blue_pin: int, chip: str = "gpiochip0", frequency: int = 1000):
        """
        Initialise une LED RGB.

        Arguments:
            red_pin (int): GPIO pour la LED rouge
            green_pin (int): GPIO pour la LED verte
            blue_pin (int): GPIO pour la LED bleue
            chip (str): Nom du chip GPIO
            frequency (int): Fréquence PWM commune (Hz)
        """
        self._frequency = frequency

        # PWM internes (16 bits uniquement)
        self._red = PWM(red_pin, chip=chip, frequency=frequency)
        self._green = PWM(green_pin, chip=chip, frequency=frequency)
        self._blue = PWM(blue_pin, chip=chip, frequency=frequency)

        # Toujours en 16 bits
        self._red.duty_cycle_16(0)
        self._green.duty_cycle_16(0)
        self._blue.duty_cycle_16(0)

        # Couleur actuelle (float 0 → 1)
        self._color = (0.0, 0.0, 0.0)

        self._blinking = False
        self._blink_thread = None

    
    def frequency(self, value: int | None = None) -> int:
        """
        Getter / Setter de la fréquence PWM commune.

        - Sans paramètre → retourne la fréquence actuelle
        - Avec paramètre → modifie la fréquence des 3 LEDs

        Arguments:
            value (int | None): Nouvelle fréquence en Hz

        Returns:
            int: Fréquence actuelle
        """
        if value is None:
            return self._frequency

        if value <= 0:
            raise ValueError("La fréquence doit être > 0 Hz")

        self._frequency = value

        for pwm in (self._red, self._green, self._blue):
            pwm.frequency = value

        return self._frequency

    def color(self, r: float, g: float, b: float):
        """
        Définit la couleur de la LED RGB.

        Arguments:
            r (float): Rouge (0.0 → 1.0)
            g (float): Vert (0.0 → 1.0)
            b (float): Bleu (0.0 → 1.0)
        """
        r = max(0.0, min(1.0, r))
        g = max(0.0, min(1.0, g))
        b = max(0.0, min(1.0, b))

        self._color = (r, g, b)

        self._red.duty_cycle_16(int(r * 65535))
        self._green.duty_cycle_16(int(g * 65535))
        self._blue.duty_cycle_16(int(b * 65535))

        self._red.start()
        self._green.start()
        self._blue.start()

    def color_percent(self, r: float, g: float, b: float):
        """
        Définit la couleur en pourcentage.

        Arguments:
            r (float): Rouge (0 → 100)
            g (float): Vert (0 → 100)
            b (float): Bleu (0 → 100)
        """
        self.color(r / 100.0, g / 100.0, b / 100.0)

    
    def off(self):
        """
        Éteint complètement la LED RGB.
        """
        self._blinking = False
        self.color(0.0, 0.0, 0.0)

   

    def blink(self, count: int, interval: float = 0.5):
        """
        Clignote avec la couleur actuelle (non bloquant).

        Arguments:
            count (int): Nombre de clignotements
            interval (float): Temps ON / OFF
        """
        if self._blinking:
            return

        def _blink():
            self._blinking = True
            for _ in range(count):
                if not self._blinking:
                    break
                self.color(*self._color)
                time.sleep(interval)
                self.off()
                time.sleep(interval)
            self._blinking = False

        self._blink_thread = threading.Thread(target=_blink, daemon=True)
        self._blink_thread.start()

    def blink_times(self, seconds: float, interval: float = 0.5):
        """
        Clignote pendant une durée donnée (non bloquant).

        Arguments:
            seconds (float): Durée totale
            interval (float): Temps ON / OFF
            
        Returns:
            None
        """
        if self._blinking:
            return

        def _blink_times():
            self._blinking = True
            end_time = time.time() + seconds
            while self._blinking and time.time() < end_time:
                self.color(*self._color)
                time.sleep(interval)
                self.off()
                time.sleep(interval)
            self._blinking = False

        self._blink_thread = threading.Thread(target=_blink_times, daemon=True)
        self._blink_thread.start()

    

    def close(self):
        """
        Libère toutes les ressources GPIO.
        
        """
        self._blinking = False
        self._red.close()
        self._green.close()
        self._blue.close()

   
    def __str__(self):
        r, g, b = self._color
        return f"LEDRGB(R={r:.2f}, G={g:.2f}, B={b:.2f}, freq={self._frequency}Hz)"

    def __repr__(self):
        """
        R
        """
        return (
            f"LEDRGB(red_pin={self._red.pin}, "
            f"green_pin={self._green.pin}, "
            f"blue_pin={self._blue.pin}, "
            f"frequency={self._frequency})"
        )


if __name__ == "__main__":
    print("Ce module ne doit pas être exécuté directement.")
