@echo off
REM Script pour démarrer avec docker-compose simplifié (sans build)

echo ========================================
echo Demarrage VERSION SIMPLIFIEE
echo (sans build Docker personnalise)
echo ========================================
echo.

echo Cette version utilise :
echo - Images officielles Python et Node
echo - Installation des dependances au demarrage
echo - Plus lent au premier demarrage mais plus fiable
echo.

REM Vérifier si Docker est en cours d'exécution
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Docker n'est pas demarre !
    pause
    exit /b 1
)

echo [OK] Docker detecte
echo.

REM Vérifier les fichiers .env
if not exist backend\.env (
    echo Configuration des fichiers .env...
    call setup-windows.bat
)

echo Arret des conteneurs existants...
docker-compose down
echo.

echo Demarrage avec docker-compose-simple.yml...
echo.
echo ATTENTION: Premier demarrage peut prendre 5-10 minutes
echo (installation des dependances Python et Node)
echo.

docker-compose -f docker-compose-simple.yml up -d

if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] Echec du demarrage
    echo.
    echo Verifiez les logs :
    echo   docker-compose -f docker-compose-simple.yml logs
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Services demarres !
echo ========================================
echo.
echo IMPORTANT: Attendez 2-3 minutes que les dependances s'installent
echo.
echo Pour voir la progression :
echo   docker-compose -f docker-compose-simple.yml logs -f
echo.
echo Une fois pret, accedez a :
echo   Frontend  : http://localhost:3000
echo   Backend   : http://localhost:8000
echo.
pause
