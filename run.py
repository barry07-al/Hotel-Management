import sys
import os

# Ajoute le dossier "src" au chemin d'import
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Lance le point d'entrée principal
from src.cli.main import cli

if __name__ == "__main__":
    cli()
