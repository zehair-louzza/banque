"""
conftest.py : ajoute la racine du projet api_livres au sys.path
afin que `from src.main import app` fonctionne avec pytest.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
