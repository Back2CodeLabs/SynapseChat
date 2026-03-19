@echo off
REM Script de démarrage pour Windows

echo ========================================
echo Demarrage de Synapse Chat
echo ========================================
echo.

REM Vérifier si Docker est en cours d'exécution
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Docker n'est pas demarre !
    echo.
    echo Veuillez demarrer Docker Desktop et reessayer.
    echo.
    pause
    exit /b 1
)

echo [OK] Docker est en cours d'execution
echo.

REM Vérifier si les fichiers .env existent
if not exist backend\.env (
    echo [ATTENTION] Le fichier backend\.env n'existe pas !
    echo.
    echo Lancement de la configuration...
    call setup-windows.bat
)

echo Demarrage des services Docker...
echo.
echo Services qui seront demarres :
echo - PostgreSQL (base de donnees)
echo - Redis (cache)
echo - Backend API (FastAPI)
echo - Frontend (React)
echo.
echo NOTE: Ollama est sur votre VM (localhost:11434)
echo       Il ne sera PAS demarre par Docker
echo.

REM Démarrer sans le profil Ollama (car il est distant)
docker-compose up -d

if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] Echec du demarrage !
    echo Consultez les logs avec : docker-compose logs
    pause
    exit /b 1
)

echo.
echo ========================================
echo Services demarres avec succes !
echo ========================================
echo.
echo Acces a l'application :
echo   Frontend  : http://localhost:3000
echo   Backend   : http://localhost:8000
echo   API Docs  : http://localhost:8000/docs
echo   Health    : http://localhost:8000/api/health
echo.
echo Ollama distant : http://localhost:11434
echo.
echo Commandes utiles :
echo   Voir les logs       : docker-compose logs -f
echo   Arreter             : docker-compose down
echo   Redemarrer          : docker-compose restart
echo.
echo Appuyez sur une touche pour ouvrir le frontend...
pause >nul

start http://localhost:3000

echo.
echo Pour voir les logs en temps reel :
echo   docker-compose logs -f
echo.
pause
