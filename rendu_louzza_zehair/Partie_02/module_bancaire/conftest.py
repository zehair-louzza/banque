"""
conftest.py : ajoute la racine du projet module_bancaire au sys.path
afin que `from src.compte import ...` fonctionne lors de l'exécution de pytest
depuis Partie_02/module_bancaire/.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
