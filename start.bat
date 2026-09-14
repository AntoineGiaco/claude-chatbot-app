@echo off
REM Script de démarrage pour l'Agent IA Local (Windows)
REM Utilisation: Double-cliquez sur ce fichier

echo.
echo ========================================
echo   Agent IA Local avec Google Drive
echo ========================================
echo.

REM Vérifier Python
echo [1/5] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python n'est pas installe
    echo Telecharge depuis: https://python.org
    echo.
    pause
    exit /b 1
)
python --version
echo OK

REM Vérifier Ollama
echo.
echo [2/5] Verification d'Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Ollama n'est pas detecte
    echo Telecharge depuis: https://ollama.ai
    echo.
) else (
    ollama --version
    echo OK
)

REM Créer l'environnement virtuel
if not exist "venv" (
    echo.
    echo [3/5] Creation de l'environnement virtuel...
    python -m venv venv
    echo OK
) else (
    echo.
    echo [3/5] Environnement virtuel trouve
    echo OK
)

REM Activer l'environnement
echo.
echo [4/5] Activation de l'environnement...
call venv\Scripts\activate.bat
echo OK

REM Installer les dépendances
echo.
echo [5/5] Installation des dependances...
pip install -q -r requirements.txt
echo OK

REM Vérifier credentials.json
echo.
if not exist "credentials.json" (
    echo WARNING: credentials.json n'existe pas
    echo Telecharge depuis: https://console.cloud.google.com/
    echo.
)

REM Lancer le serveur
echo.
echo ========================================
echo   Demarrage du serveur Flask...
echo ========================================
echo.
echo URL: http://localhost:5000
echo Ouvrez index.html dans votre navigateur
echo.
echo Appuyez sur CTRL+C pour arreter
echo.

python app.py

pause
