@echo off
REM ============================================================
REM  Installation automatique du rendu (Windows)
REM  Double-cliquez sur ce fichier OU lancez-le : .\setup.bat
REM  Il cree le venv, l'active et installe toutes les dependances.
REM ============================================================
setlocal

echo.
echo === [1/3] Creation de l'environnement virtuel (.venv) ===
if not exist ".venv" (
    python -m venv .venv
    if errorlevel 1 (
        echo ERREUR : impossible de creer le venv. Verifiez que Python est installe ^(python --version^).
        pause
        exit /b 1
    )
) else (
    echo    .venv existe deja, on reutilise.
)

echo.
echo === [2/3] Activation du venv ===
call .venv\Scripts\activate.bat

echo.
echo === [3/3] Installation des dependances ===
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERREUR : l'installation des dependances a echoue.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  Installation terminee avec succes.
echo  Pour lancer les tests       : run_tests.bat
echo  Pour demarrer l'API livres  : run_api.bat
echo ============================================================
echo.
pause
