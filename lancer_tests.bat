@echo off
REM Script de lancement rapide du projet bancaire

echo.
echo ========================================
echo  SYSTEME BANCAIRE ROBUSTE
echo ========================================
echo.

cd /d "%~dp0"

REM Tester si pytest est installé
python -m pip show pytest >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installation de pytest...
    python -m pip install pytest
)

echo.
echo [1] Lancer les tests unitaires...
echo ========================================
python -m pytest test/test_compte_bancaire.py -v --tb=short
echo.

echo [2] Voir la demo de regression...
echo ========================================
echo (Voir fichier test_regression_demo.py ou RAPPORT_REGRESSION.md)
echo.

echo.
echo ========================================
echo  FICHIERS IMPORTANTS :
echo  - README.md : Documentation complète
echo  - NOTE_LIVRAISON.txt : Résumé de livraison
echo  - RAPPORT_REGRESSION.md : Analyse de régression
echo  - src/ : Code métier
echo  - test/ : Tests unitaires
echo ========================================
echo.

pause
