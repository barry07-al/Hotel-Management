#!/bin/bash

# Se place à la racine du projet
cd "$(dirname "$0")"

# Ajoute src au PYTHONPATH
export PYTHONPATH=$(pwd)/src

# Lance les tests dans le dossier tests/
python3 -m unittest discover -s tests -p "test*.py"

