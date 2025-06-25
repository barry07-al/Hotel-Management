import os
import sys

# Ajoute le dossier "src" au chemin d'import
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Lance le point d'entrée principal
from src.infrastructure.cli import CLI

if __name__ == "__main__":
    main_class = CLI()
    main_class.run()
