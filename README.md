# gpiodzero

**gpiodzero** est un projet open source conçu pour faciliter l'utilisation des GPIO sur Raspberry Pi 5, en utilisant la bibliothèque `libgpiod`.  
Il s’inspire de `gpiozero` et offre une API simple et moderne pour contrôler facilement LED, boutons, buzzers, capteurs et autres composants électroniques.

---

gpiodzero/
├── base/             # Gestion bas niveau des GPIO (libgpiod, pins, lignes, PWM)
├── composants/       # Composants haut niveau : LED, LEDRGB, Buzzer, Button, capteurs, afficheurs
├── tests/            # Tests unitaires pour garantir la stabilité de la bibliothèque
├── examples/         # Scripts d'exemples prêts à être exécutés
├── docs/             # Documentation complète du projet


## 🚀 Installation

Clonez le projet et installez-le avec `pip` :

```bash
git clone https://github.com/NSJ25/gpiodzero.git
cd gpiodzero
pip install .