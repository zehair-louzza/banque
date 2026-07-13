@echo off
REM ============================================================
REM  Lance TOUS les tests des deux parties (Windows)
REM  Prerequis : avoir lance setup.bat une fois.
REM ============================================================
setlocal

if not exist ".venv" (
    echo ERREUR : le venv n'existe pas. Lancez d'abord setup.bat
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

echo.
echo === Tests Partie 2 : module bancaire ===
pushd Partie_02\module_bancaire
pytest
popd

echo.
echo === Tests Partie 3 : API livres ===
pushd Partie_03\api_livres
pytest
popd

echo.
pause
