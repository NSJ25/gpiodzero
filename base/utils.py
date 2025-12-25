import gpiod

def is_gpiod_v2():
    """
    Vérifie si la version 2 de la bibliothèque gpiod est utilisée.
    Returns:
        bool: True si gpiod version 2 est utilisé, False sinon.
    """
    return hasattr(gpiod, "LineSettings")
