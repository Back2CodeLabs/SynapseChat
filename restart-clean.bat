@echo off
REM Script de redémarrage propre avec nettoyage

echo ========================================
echo Redemarrage propre du projet
echo ========================================
echo.

echo Etape 1/4 : Arret des conteneurs...
docker-compose down
echo [OK]
echo.

echo Etape 2/4 : Nettoyage Docker...
echo Cette operation peut prendre quelques secondes...
docker system prune -f
echo [OK]
echo.

echo Etape 3/4 : Reconstruction des images...
echo Cette operation peut prendre 5-10 minutes...
docker-compose build --no-cache
if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] Echec de la reconstruction
    echo.
    echo Suggestions :
    echo 1. Augmentez la RAM de Docker (Settings ^> Resources)
    echo 2. Verifiez votre connexion Internet
    echo 3. Consultez : PROBLEME_DOCKER_BUILD.md
    echo.
    pause
    exit /b 1
)
echo [OK]
echo.

echo Etape 4/4 : Demarrage des services...
docker-compose up -d
if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] Echec du demarrage
    echo Consultez les logs : docker-compose logs
    echo.
    pause
    exit /b 1
)
echo [OK]
echo.

echo ========================================
echo Redemarrage termine avec succes !
echo ========================================
echo.
echo Acces :
echo   Frontend  : http://localhost:3000
echo   Backend   : http://localhost:8000
echo   API Docs  : http://localhost:8000/docs
echo.
echo Logs : docker-compose logs -f
echo.
pause
