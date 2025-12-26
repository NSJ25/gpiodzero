import gpiod

def is_gpiod_v2():
    """
    Vérifie si la version 2 de la bibliothèque gpiod est utilisée.
    
    Arguments:
        Aucun.
    
    Returns:
        bool: True si gpiod version 2 est utilisé, False sinon.
    """
    return hasattr(gpiod, "LineSettings")

if __name__ == "__main__":
    print("Ce module ne doit pas être exécuté directement.")