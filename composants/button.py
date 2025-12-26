from .base import PinIn, Pull
import threading
import time

class Button(PinIn):
    def __init__(self, pin: int, chip="gpiochip0", pull=Pull.NONE, debounce_time=0.03):
        super().__init__(pin, chip=chip, pull=pull)
        self.debounce_time = debounce_time
        self._last_state = self.is_pressed()
        self._running = True

        # Callbacks non bloquants
        self.when_pressed = None
        self.when_released = None
        self.when_clicked = None
        self.when_double_clicked = None
        self.when_held = None

        # Thread interne
        self._thread = threading.Thread(target=self._monitor, daemon=True)
        self._thread.start()

    # --- Méthode pour lire l'état actuel ---
    def is_pressed(self):
    """
    Retourne True si le bouton est pressé, False sinon.
    Gère correctement les pulls (UP / DOWN) et renvoie un bool.
    """
    val = self.read()  # lit la valeur physique de la GPIO
    # Si pull-up : bouton appuyé = 0 (low), relâché = 1 (high)
    if self.pull == Pull.UP:
        return val == 0
    # Si pull-down : bouton appuyé = 1 (high), relâché = 0 (low)
    elif self.pull == Pull.DOWN:
        return val == 1
    # Aucun pull : on renvoie simplement l'état tel quel
    else:
        return bool(val)


    # --- Méthodes non bloquantes ---
    def press(self):
        if self.when_pressed:
            self.when_pressed()

    def release(self):
        if self.when_released:
            self.when_released()

    def click(self):
        if self.when_clicked:
            self.when_clicked()

    def double_click(self):
        if self.when_double_clicked:
            self.when_double_clicked()

    def hold(self, duration=1):
        """Callback si le bouton est maintenu appuyé pendant 'duration' secondes"""
        if self.is_pressed():
            start = time.time()
            while self.is_pressed():
                if time.time() - start >= duration:
                    if self.when_held:
                        self.when_held()
                    break
                time.sleep(0.005)

    def stop(self):
        """Arrête le thread non bloquant"""
        self._running = False

    def close(self):
        """Arrête le thread et libère les GPIO"""
        self.stop()
        # release ou restore si nécessaire
        self.release()  # relâche le bouton avant fermeture
        super().close()  # utilise PinIn.close()

    # --- Méthodes bloquantes ---
    def wait_for_press(self):
        while not self.is_pressed():
            time.sleep(0.005)
        self.press()

    def wait_for_release(self):
        while self.is_pressed():
            time.sleep(0.005)
        self.release()

    def wait_for_click(self):
        self.wait_for_press()
        self.wait_for_release()
        self.click()

    # --- Méthodes internes ---
    def _monitor(self):
        """Thread interne pour détecter les événements non bloquants"""
        while self._running:
            state = self.is_pressed()
            if state != self._last_state:
                time.sleep(self.debounce_time)  # debounce
                state = self.is_pressed()
                if state != self._last_state:
                    if state:
                        self._on_press()
                    else:
                        self._on_release()
                    self._last_state = state
            time.sleep(0.005)

    def _on_press(self):
        self.press()
        # Ici on pourrait ajouter click/double_click/hold non bloquant

    def _on_release(self):
        self.release()
        # Ici on pourrait ajouter click/double_click non bloquant
if __name__ == "__main__":
    print("Ce module ne doit pas être exécuté directement.")   