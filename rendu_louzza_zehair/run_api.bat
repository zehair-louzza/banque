@echo off
REM ============================================================
REM  Demarre l'API livres (Windows)
REM  Prerequis : avoir lance setup.bat une fois.
REM  L'API sera disponible sur http://127.0.0.1:8000/docs
REM  Arret : Ctrl+C
REM ============================================================
setlocal

if not exist ".venv" (
    echo ERREUR : le venv n'existe pas. Lancez d'abord setup.bat
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

cd Partie_03\api_livres
echo.
echo === API livres : http://127.0.0.1:8000/docs  (Ctrl+C pour arreter) ===
echo.
uvicorn src.main:app --reload
