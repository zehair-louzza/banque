#!/usr/bin/env bash
# ============================================================
#  Installation automatique du rendu (macOS / Linux)
#  Usage : bash setup.sh
#  Cree le venv, l'active et installe toutes les dependances.
# ============================================================
set -e

PY=python3
command -v "$PY" >/dev/null 2>&1 || PY=python

echo ""
echo "=== [1/3] Creation de l'environnement virtuel (.venv) ==="
if [ ! -d ".venv" ]; then
  "$PY" -m venv .venv
else
  echo "   .venv existe deja, on reutilise."
fi

echo ""
echo "=== [2/3] Activation du venv ==="
# shellcheck disable=SC1091
source .venv/bin/activate

echo ""
echo "=== [3/3] Installation des dependances ==="
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "============================================================"
echo " Installation terminee."
echo " Tests Partie 2 : (cd Partie_02/module_bancaire && pytest)"
echo " Tests Partie 3 : (cd Partie_03/api_livres && pytest)"
echo " Demarrer l'API : (cd Partie_03/api_livres && uvicorn src.main:app --reload)"
echo "============================================================"
